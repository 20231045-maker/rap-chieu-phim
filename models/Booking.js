const { query, get, run } = require('../database/db');
const QRCode = require('qrcode');

class Booking {
    static async createBooking({
        userId = null,
        customerName,
        customerEmail,
        customerPhone,
        showtimeId,
        seats, // Array of { id, price, seat_code }
        combos = [], // Array of { id, quantity, price }
        paymentMethod = 'vnpay',
        bookingType = 'online',
        createdBy = null,
        sessionId = null
    }) {
        // Tính tổng tiền vé
        const seatTotal = seats.reduce((sum, s) => sum + Number(s.price), 0);
        // Tính tổng tiền combo
        const comboTotal = combos.reduce((sum, c) => sum + (Number(c.price) * Number(c.quantity)), 0);
        const totalAmount = seatTotal + comboTotal;

        // Sinh mã booking duy nhất
        const datePrefix = new Date().toISOString().slice(0, 10).replace(/-/g, '');
        const randomSuffix = Math.random().toString(36).substring(2, 8).toUpperCase();
        const bookingCode = `BKG-${datePrefix}-${randomSuffix}`;

        // Bắt đầu chèn đơn đặt vé
        const bookingRes = await run(`
            INSERT INTO bookings (
                booking_code, user_id, customer_name, customer_email, customer_phone,
                showtime_id, total_amount, payment_method, payment_status, booking_status,
                booking_type, created_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'paid', 'confirmed', ?, ?)
        `, [
            bookingCode, userId, customerName, customerEmail, customerPhone,
            showtimeId, totalAmount, paymentMethod, bookingType, createdBy
        ]);
        const bookingId = bookingRes.lastInsertRowid;

        const createdTickets = [];

        for (let i = 0; i < seats.length; i++) {
            const seat = seats[i];
            const tktSuffix = Math.random().toString(36).substring(2, 6).toUpperCase();
            const ticketCode = `TKT-${datePrefix}-${seat.seat_code}-${tktSuffix}`;
            
            // Dữ liệu mã hóa trong QR Code
            const qrPayload = JSON.stringify({
                code: ticketCode,
                bkg: bookingCode,
                seat: seat.seat_code,
                st: showtimeId
            });

            // Sinh ảnh QR base64 data URL
            const qrDataUrl = await QRCode.toDataURL(qrPayload, {
                errorCorrectionLevel: 'H',
                margin: 2,
                width: 250
            });

            await run(`
                INSERT INTO tickets (ticket_code, booking_id, showtime_id, seat_id, price, qr_data, status)
                VALUES (?, ?, ?, ?, ?, ?, 'unused')
            `, [ticketCode, bookingId, showtimeId, seat.id, seat.price, qrDataUrl]);

            createdTickets.push({
                ticket_code: ticketCode,
                seat_code: seat.seat_code,
                price: seat.price,
                qr_data: qrDataUrl
            });
        }

        // Chèn combo nếu có
        if (combos && combos.length > 0) {
            for (const c of combos) {
                if (c.quantity > 0) {
                    const lineTotal = c.quantity * c.price;
                    await run(`
                        INSERT INTO booking_combos (booking_id, combo_id, quantity, unit_price, total_price)
                        VALUES (?, ?, ?, ?, ?)
                    `, [bookingId, c.id, c.quantity, c.price, lineTotal]);
                }
            }
        }

        // Xóa khóa ghế tạm thời của session
        if (sessionId) {
            await run('DELETE FROM seat_locks WHERE showtime_id = ? AND session_id = ?', [showtimeId, sessionId]);
        }

        return {
            bookingId,
            bookingCode,
            totalAmount,
            tickets: createdTickets
        };
    }

    static async findById(id) {
        return await get(`
            SELECT b.*, 
                   st.start_time, st.end_time, st.room_id,
                   m.title as movie_title, m.poster_url, m.duration, m.age_rating,
                   r.room_name, r.screen_type,
                   c.name as cinema_name, c.address as cinema_address, c.city as cinema_city,
                   u.full_name as user_name
            FROM bookings b
            JOIN showtimes st ON b.showtime_id = st.id
            JOIN movies m ON st.movie_id = m.id
            JOIN rooms r ON st.room_id = r.id
            LEFT JOIN cinemas c ON r.cinema_id = c.id
            LEFT JOIN users u ON b.user_id = u.id
            WHERE b.id = ?
        `, [id]);
    }

    static async findByCode(code) {
        return await get(`
            SELECT b.*, 
                   st.start_time, st.end_time, st.room_id,
                   m.title as movie_title, m.poster_url, m.duration, m.age_rating,
                   r.room_name, r.screen_type,
                   c.name as cinema_name, c.address as cinema_address, c.city as cinema_city,
                   u.full_name as user_name
            FROM bookings b
            JOIN showtimes st ON b.showtime_id = st.id
            JOIN movies m ON st.movie_id = m.id
            JOIN rooms r ON st.room_id = r.id
            LEFT JOIN cinemas c ON r.cinema_id = c.id
            LEFT JOIN users u ON b.user_id = u.id
            WHERE b.booking_code = ?
        `, [code]);
    }

    static async getByUserId(userId) {
        return await query(`
            SELECT b.*, 
                   st.start_time, st.end_time,
                   m.title as movie_title, m.poster_url,
                   r.room_name,
                   (SELECT COUNT(*) FROM tickets WHERE booking_id = b.id) as ticket_count
            FROM bookings b
            JOIN showtimes st ON b.showtime_id = st.id
            JOIN movies m ON st.movie_id = m.id
            JOIN rooms r ON st.room_id = r.id
            WHERE b.user_id = ?
            ORDER BY b.created_at DESC
        `, [userId]);
    }

    static async getTicketsByBookingId(bookingId) {
        return await query(`
            SELECT t.*, s.seat_row, s.seat_number, s.seat_code, s.seat_type
            FROM tickets t
            JOIN seats s ON t.seat_id = s.id
            WHERE t.booking_id = ?
            ORDER BY s.seat_row ASC, s.seat_number ASC
        `, [bookingId]);
    }

    static async getCombosByBookingId(bookingId) {
        return await query(`
            SELECT bc.*, c.name as combo_name, c.image_url
            FROM booking_combos bc
            JOIN combos c ON bc.combo_id = c.id
            WHERE bc.booking_id = ?
        `, [bookingId]);
    }

    static async getAll() {
        return await query(`
            SELECT b.*, 
                   m.title as movie_title,
                   r.room_name,
                   st.start_time,
                   (SELECT COUNT(*) FROM tickets WHERE booking_id = b.id) as ticket_count
            FROM bookings b
            JOIN showtimes st ON b.showtime_id = st.id
            JOIN movies m ON st.movie_id = m.id
            JOIN rooms r ON st.room_id = r.id
            ORDER BY b.created_at DESC
        `);
    }

    // Thống kê tổng hợp cho Dashboard của Manager
    static async getDashboardStats() {
        // Tổng doanh thu & tổng vé bán
        const totalStats = await get(`
            SELECT 
                COALESCE(SUM(total_amount), 0) as total_revenue,
                COUNT(id) as total_bookings
            FROM bookings
            WHERE payment_status = 'paid' AND booking_status != 'cancelled'
        `);

        // Doanh thu hôm nay
        const todayStats = await get(`
            SELECT 
                COALESCE(SUM(total_amount), 0) as today_revenue,
                COUNT(id) as today_bookings
            FROM bookings
            WHERE payment_status = 'paid' AND booking_status != 'cancelled'
              AND DATE(created_at) = CURDATE()
        `);

        // Tổng số vé bán được
        const ticketsSold = await get(`
            SELECT COUNT(t.id) as count
            FROM tickets t
            JOIN bookings b ON t.booking_id = b.id
            WHERE b.payment_status = 'paid' AND b.booking_status != 'cancelled'
        `);

        // Tỷ lệ lấp đầy rạp (%) = (Tổng vé đã bán / Tổng ghế khả dụng của các suất chiếu đang/đã mở) * 100
        const occupancyData = await get(`
            SELECT 
                (SELECT COUNT(*) FROM tickets t JOIN bookings b ON t.booking_id = b.id WHERE b.booking_status != 'cancelled') as sold_tickets,
                (SELECT COALESCE(SUM(r.total_seats), 1) FROM showtimes st JOIN rooms r ON st.room_id = r.id WHERE st.status != 'cancelled') as capacity
        `);
        
        const soldCount = occupancyData ? Number(occupancyData.sold_tickets || 0) : 0;
        const capCount = occupancyData ? Number(occupancyData.capacity || 1) : 1;
        const occupancyRate = capCount > 0 ? Math.min(100, Math.round((soldCount / capCount) * 1000) / 10) : 0;

        // Doanh thu theo 7 ngày gần nhất (cho Chart.js)
        const days = [];
        for (let i = 6; i >= 0; i--) {
            const d = new Date();
            d.setDate(d.getDate() - i);
            const pad = (n) => String(n).padStart(2, '0');
            days.push(`${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`);
        }

        const rows = await query(`
            SELECT DATE_FORMAT(created_at, '%Y-%m-%d') as date_str,
                   COALESCE(SUM(total_amount), 0) as revenue,
                   COUNT(id) as booking_count
            FROM bookings
            WHERE payment_status = 'paid' AND booking_status != 'cancelled'
              AND created_at >= DATE_SUB(CURDATE(), INTERVAL 6 DAY)
            GROUP BY DATE_FORMAT(created_at, '%Y-%m-%d')
        `);

        const rowMap = new Map();
        rows.forEach(r => rowMap.set(r.date_str, r));

        const revenueByDays = days.map(d => ({
            date_str: d,
            revenue: Number(rowMap.get(d)?.revenue || 0),
            booking_count: Number(rowMap.get(d)?.booking_count || 0)
        }));

        // Top 5 phim có doanh thu cao nhất
        const topMovies = await query(`
            SELECT 
                m.title,
                COALESCE(SUM(b.total_amount), 0) as movie_revenue,
                COUNT(t.id) as tickets_sold
            FROM movies m
            LEFT JOIN showtimes st ON m.id = st.movie_id
            LEFT JOIN bookings b ON st.id = b.showtime_id AND b.payment_status = 'paid' AND b.booking_status != 'cancelled'
            LEFT JOIN tickets t ON b.id = t.booking_id
            GROUP BY m.id, m.title
            ORDER BY movie_revenue DESC
            LIMIT 5
        `);

        // Thống kê theo loại vé (regular, vip, sweetbox)
        const seatTypeStats = await query(`
            SELECT 
                s.seat_type,
                COUNT(t.id) as count
            FROM tickets t
            JOIN seats s ON t.seat_id = s.id
            JOIN bookings b ON t.booking_id = b.id
            WHERE b.booking_status != 'cancelled'
            GROUP BY s.seat_type
        `);

        return {
            totalRevenue: totalStats ? Number(totalStats.total_revenue) : 0,
            todayRevenue: todayStats ? Number(todayStats.today_revenue) : 0,
            totalBookings: totalStats ? Number(totalStats.total_bookings) : 0,
            ticketsSold: ticketsSold ? Number(ticketsSold.count) : 0,
            occupancyRate,
            revenueByDays,
            topMovies: topMovies.map(m => ({ ...m, movie_revenue: Number(m.movie_revenue), tickets_sold: Number(m.tickets_sold) })),
            seatTypeStats
        };
    }
}

module.exports = Booking;
