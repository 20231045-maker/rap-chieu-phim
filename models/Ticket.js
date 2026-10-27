const { query, get, run } = require('../database/db');

class Ticket {
    static async findByCode(ticketCode) {
        return await get(`
            SELECT t.*, 
                   s.seat_code, s.seat_row, s.seat_number, s.seat_type,
                   st.start_time, st.end_time,
                   m.title as movie_title, m.poster_url, m.age_rating, m.duration,
                   r.room_name, r.screen_type,
                   b.booking_code, b.customer_name, b.customer_phone, b.payment_status,
                   u.full_name as staff_name
            FROM tickets t
            JOIN seats s ON t.seat_id = s.id
            JOIN showtimes st ON t.showtime_id = st.id
            JOIN movies m ON st.movie_id = m.id
            JOIN rooms r ON st.room_id = r.id
            JOIN bookings b ON t.booking_id = b.id
            LEFT JOIN users u ON t.checked_in_by = u.id
            WHERE t.ticket_code = ?
        `, [ticketCode]);
    }

    static async checkIn(ticketCode, staffId) {
        const ticket = await this.findByCode(ticketCode);
        if (!ticket) {
            return {
                success: false,
                status: 'not_found',
                message: 'Không tìm thấy vé trong hệ thống! Vui lòng kiểm tra lại mã vé.'
            };
        }

        if (ticket.status === 'checked_in') {
            return {
                success: false,
                status: 'already_used',
                message: `CẢNH BÁO: Vé đã được sử dụng vào lúc ${ticket.checked_in_at || 'trước đó'} bởi nhân viên ${ticket.staff_name || 'quầy'}!`,
                ticket
            };
        }

        if (ticket.status === 'cancelled') {
            return {
                success: false,
                status: 'cancelled',
                message: 'Vé này đã bị hủy!',
                ticket
            };
        }

        const now = new Date().toISOString().replace('T', ' ').substring(0, 19);
        await run(`
            UPDATE tickets
            SET status = 'checked_in', checked_in_at = ?, checked_in_by = ?
            WHERE ticket_code = ?
        `, [now, staffId, ticketCode]);

        const updatedTicket = await this.findByCode(ticketCode);
        return {
            success: true,
            status: 'success',
            message: 'Soát vé THÀNH CÔNG! Cho phép khách vào phòng chiếu.',
            ticket: updatedTicket
        };
    }

    static async getTodayScanned(staffId = null) {
        let sql = `
            SELECT t.*, 
                   s.seat_code,
                   m.title as movie_title,
                   r.room_name,
                   st.start_time,
                   u.full_name as staff_name
            FROM tickets t
            JOIN seats s ON t.seat_id = s.id
            JOIN showtimes st ON t.showtime_id = st.id
            JOIN movies m ON st.movie_id = m.id
            JOIN rooms r ON st.room_id = r.id
            LEFT JOIN users u ON t.checked_in_by = u.id
            WHERE t.status = 'checked_in' AND DATE(t.checked_in_at) = CURDATE()
        `;
        const params = [];
        if (staffId) {
            sql += ' AND t.checked_in_by = ?';
            params.push(staffId);
        }
        sql += ' ORDER BY t.checked_in_at DESC LIMIT 50';
        return await query(sql, params);
    }
}

module.exports = Ticket;
