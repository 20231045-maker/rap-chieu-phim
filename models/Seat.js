const { query, get, run } = require('../database/db');

class Seat {
    static async getByRoomId(roomId) {
        return await query(`
            SELECT * FROM seats
            WHERE room_id = ?
            ORDER BY seat_row ASC, seat_number ASC
        `, [roomId]);
    }

    static async findById(id) {
        return await get('SELECT * FROM seats WHERE id = ?', [id]);
    }

    static async updateType(id, seat_type, price_multiplier) {
        return await run(`
            UPDATE seats SET seat_type = ?, price_multiplier = ? WHERE id = ?
        `, [seat_type, price_multiplier, id]);
    }

    static async updateStatus(id, status) {
        return await run('UPDATE seats SET status = ? WHERE id = ?', [status, id]);
    }

    // Lấy toàn bộ ghế của suất chiếu kèm trạng thái thực tế:
    // available (trống), booked (đã bán), locked (đang bị người khác giữ), selected (đang được chính mình giữ)
    static async getSeatsWithStatusForShowtime(showtimeId, currentSessionId = '') {
        const showtime = await get('SELECT room_id, base_price FROM showtimes WHERE id = ?', [showtimeId]);
        if (!showtime) return [];

        const now = new Date().toISOString().replace('T', ' ').substring(0, 19);

        // Lấy danh sách ghế của phòng
        const seats = await query(`
            SELECT s.*,
                -- Kiểm tra vé đã thanh toán
                (SELECT t.id FROM tickets t 
                 JOIN bookings b ON t.booking_id = b.id
                 WHERE t.showtime_id = ? AND t.seat_id = s.id AND b.booking_status != 'cancelled') as ticket_id,
                -- Kiểm tra ghế đang bị khóa tạm thời
                (SELECT sl.session_id FROM seat_locks sl 
                 WHERE sl.showtime_id = ? AND sl.seat_id = s.id AND sl.expires_at > ?) as lock_session
            FROM seats s
            WHERE s.room_id = ?
            ORDER BY s.seat_row ASC, s.seat_number ASC
        `, [showtimeId, showtimeId, now, showtime.room_id]);

        return seats.map(seat => {
            let seatStatus = 'available';
            if (seat.status === 'maintenance') {
                seatStatus = 'maintenance';
            } else if (seat.ticket_id) {
                seatStatus = 'booked';
            } else if (seat.lock_session) {
                if (seat.lock_session === currentSessionId) {
                    seatStatus = 'selected';
                } else {
                    seatStatus = 'locked';
                }
            }

            const calculatedPrice = Math.round(Number(showtime.base_price) * Number(seat.price_multiplier));

            return {
                ...seat,
                current_status: seatStatus,
                calculated_price: calculatedPrice
            };
        });
    }
}

module.exports = Seat;
