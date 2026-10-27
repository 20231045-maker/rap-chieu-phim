const Movie = require('../models/Movie');
const Showtime = require('../models/Showtime');
const Seat = require('../models/Seat');
const Combo = require('../models/Combo');
const Booking = require('../models/Booking');
const Ticket = require('../models/Ticket');
const { query } = require('../database/db');

class StaffController {
    // 1. Giao diện bán vé tại quầy (POS Counter)
    static async pos(req, res) {
        try {
            const todayStr = new Date().toISOString().split('T')[0];
            const movies = await Movie.getNowShowing();
            const combos = await Combo.getAllActive();
            const cinemas = await query('SELECT * FROM cinemas WHERE status = "active" ORDER BY id ASC');

            // Xác định rạp đang bán vé: query param > cookie > user cinema_id > mặc định 1
            let selectedCinemaId = req.query.cinema_id || req.cookies.selectedCinemaId;
            if (!selectedCinemaId && req.session.user && req.session.user.cinema_id) {
                selectedCinemaId = req.session.user.cinema_id;
            }
            if (!selectedCinemaId) {
                selectedCinemaId = 1;
            }
            selectedCinemaId = Number(selectedCinemaId);

            const currentCinema = cinemas.find(c => Number(c.id) === selectedCinemaId) || cinemas[0];

            // Lấy tất cả các suất chiếu hôm nay của rạp này (hoặc fallback nếu chưa có)
            let showtimes = await query(`
                SELECT st.*, m.title as movie_title, m.poster_url, m.duration,
                       r.room_name, r.screen_type, r.cinema_id,
                       c.name as cinema_name, c.city as cinema_city, c.address as cinema_address
                FROM showtimes st
                JOIN movies m ON st.movie_id = m.id
                JOIN rooms r ON st.room_id = r.id
                JOIN cinemas c ON r.cinema_id = c.id
                WHERE DATE(st.start_time) = DATE(?) AND st.status = 'scheduled' AND r.cinema_id = ?
                ORDER BY st.start_time ASC
            `, [todayStr, selectedCinemaId]);

            if (showtimes.length === 0) {
                showtimes = await query(`
                    SELECT st.*, m.title as movie_title, m.poster_url, m.duration,
                           r.room_name, r.screen_type, r.cinema_id,
                           c.name as cinema_name, c.city as cinema_city, c.address as cinema_address
                    FROM showtimes st
                    JOIN movies m ON st.movie_id = m.id
                    JOIN rooms r ON st.room_id = r.id
                    JOIN cinemas c ON r.cinema_id = c.id
                    WHERE DATE(st.start_time) = DATE(?) AND st.status = 'scheduled'
                    ORDER BY st.start_time ASC
                `, [todayStr]);
            }

            res.render('staff/pos', {
                title: 'Hệ Thống Bán Vé Tại Quầy (POS Counter)',
                movies,
                showtimes,
                combos,
                cinemas,
                selectedCinemaId,
                currentCinema,
                todayStr,
                staffUser: req.session.user
            });
        } catch (err) {
            console.error('Lỗi POS:', err);
            res.redirect('/');
        }
    }

    // API lấy sơ đồ ghế cho POS
    static async apiPosSeats(req, res) {
        try {
            const showtimeId = req.params.showtimeId;
            const seats = await Seat.getSeatsWithStatusForShowtime(showtimeId, req.sessionID);
            
            const seatsByRow = {};
            seats.forEach(s => {
                if (!seatsByRow[s.seat_row]) {
                    seatsByRow[s.seat_row] = [];
                }
                seatsByRow[s.seat_row].push(s);
            });

            res.json({
                success: true,
                seatsByRow
            });
        } catch (err) {
            res.status(500).json({ success: false, message: err.message });
        }
    }

    // Xử lý hoàn tất đơn hàng POS tại quầy
    static async posCheckout(req, res) {
        const {
            showtime_id,
            seat_ids,
            combos,
            customer_name,
            customer_phone,
            payment_method
        } = req.body;

        try {
            const parsedSeatIds = JSON.parse(seat_ids);
            const parsedCombos = combos ? JSON.parse(combos) : [];

            const allSeats = await Seat.getSeatsWithStatusForShowtime(showtime_id, req.sessionID);
            const selectedSeats = allSeats
                .filter(s => parsedSeatIds.includes(s.id))
                .map(s => ({
                    id: s.id,
                    seat_code: s.seat_code,
                    price: s.calculated_price
                }));

            const comboList = [];
            for (const c of parsedCombos) {
                if (c.quantity > 0) {
                    const comboObj = await Combo.findById(c.id);
                    if (comboObj) {
                        comboList.push({
                            id: comboObj.id,
                            quantity: c.quantity,
                            price: comboObj.price
                        });
                    }
                }
            }

            const result = await Booking.createBooking({
                userId: null,
                customerName: customer_name || 'Khách vãng lai (Quầy)',
                customerEmail: 'pos@cinema.com',
                customerPhone: customer_phone || '',
                showtimeId: Number(showtime_id),
                seats: selectedSeats,
                combos: comboList,
                paymentMethod: payment_method || 'cash',
                bookingType: 'pos',
                createdBy: req.session.user.id,
                sessionId: req.sessionID
            });

            res.json({
                success: true,
                message: 'Xuất vé tại quầy thành công!',
                bookingCode: result.bookingCode
            });
        } catch (err) {
            console.error('Lỗi POS checkout:', err);
            res.status(500).json({
                success: false,
                message: 'Lỗi khi tạo vé tại quầy: ' + err.message
            });
        }
    }

    // 2. Giao diện Soát vé QR tại quầy (Staff Ticket Scanner & Verification)
    static async scanTicket(req, res) {
        try {
            const prefillCode = req.query.code || '';
            const recentScans = await Ticket.getTodayScanned();

            res.render('staff/scan-ticket', {
                title: 'Soát Vé QR Code Tại Cửa Phòng Chiếu',
                prefillCode,
                recentScans
            });
        } catch (err) {
            console.error('Lỗi scan ticket view:', err);
            res.redirect('/');
        }
    }

    // API Kiểm tra thông tin vé khi quét mã QR
    static async apiCheckTicket(req, res) {
        try {
            let code = req.query.code || req.body.code;
            if (!code) {
                return res.status(400).json({ success: false, message: 'Vui lòng cung cấp mã vé!' });
            }

            code = code.trim();

            // Nếu mã quét là JSON (từ QR), trích xuất ticket_code
            if (code.startsWith('{')) {
                try {
                    const parsed = JSON.parse(code);
                    code = parsed.code || code;
                } catch (e) {
                    // Giữ nguyên chuỗi
                }
            }

            const ticket = await Ticket.findByCode(code);
            if (!ticket) {
                return res.status(404).json({
                    success: false,
                    status: 'not_found',
                    message: `Không tìm thấy mã vé "${code}" trên hệ thống!`
                });
            }

            res.json({
                success: true,
                ticket
            });
        } catch (err) {
            res.status(500).json({ success: false, message: err.message });
        }
    }

    // API Xác nhận soát vé (Check-in)
    static async apiConfirmCheckIn(req, res) {
        try {
            let { code } = req.body;
            if (!code) {
                return res.status(400).json({ success: false, message: 'Vui lòng cung cấp mã vé!' });
            }

            code = code.trim();
            if (code.startsWith('{')) {
                try {
                    const parsed = JSON.parse(code);
                    code = parsed.code || code;
                } catch (e) {}
            }

            const staffId = req.session.user.id;
            const result = await Ticket.checkIn(code, staffId);

            res.json(result);
        } catch (err) {
            res.status(500).json({ success: false, message: err.message });
        }
    }

    // 3. Lịch sử soát vé hôm nay
    static async history(req, res) {
        try {
            const scannedTickets = await Ticket.getTodayScanned();
            res.render('staff/history', {
                title: 'Lịch Sử Soát Vé Hôm Nay',
                scannedTickets
            });
        } catch (err) {
            console.error('Lỗi history:', err);
            res.redirect('/staff/scan');
        }
    }
}

module.exports = StaffController;
