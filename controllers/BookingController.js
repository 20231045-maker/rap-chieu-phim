const Showtime = require('../models/Showtime');
const Seat = require('../models/Seat');
const Combo = require('../models/Combo');
const SeatLock = require('../models/SeatLock');
const Booking = require('../models/Booking');
const Ticket = require('../models/Ticket');

class BookingController {
    // 1. Sơ đồ chọn ghế ngồi trực quan theo phòng
    static async selectSeats(req, res) {
        try {
            const showtimeId = req.params.showtimeId;
            const showtime = await Showtime.findById(showtimeId);

            if (!showtime) {
                return res.status(404).render('client/404', {
                    title: 'Không Tìm Thấy Suất Chiếu',
                    message: 'Suất chiếu này không tồn tại hoặc đã bị hủy.'
                });
            }

            // Lấy danh sách ghế cùng trạng thái (available, booked, locked, selected)
            const seats = await Seat.getSeatsWithStatusForShowtime(showtimeId, req.sessionID);

            // Nhóm các ghế theo từng hàng (A, B, C, ...)
            const seatsByRow = {};
            seats.forEach(s => {
                if (!seatsByRow[s.seat_row]) {
                    seatsByRow[s.seat_row] = [];
                }
                seatsByRow[s.seat_row].push(s);
            });

            const breadcrumbs = [
                { label: 'Phim', url: '/movies' },
                { label: showtime.movie_title, url: `/movies/${showtime.movie_id}` },
                { label: 'Chọn Ghế' }
            ];

            res.render('client/select-seats', {
                title: `Chọn Ghế - ${showtime.movie_title}`,
                showtime,
                seatsByRow,
                rows: Object.keys(seatsByRow),
                sessionId: req.sessionID,
                breadcrumbs
            });
        } catch (err) {
            console.error('Lỗi chọn ghế:', err);
            res.status(500).render('client/404', {
                title: '500 - Lỗi',
                message: 'Không thể tải sơ đồ phòng chiếu: ' + err.message
            });
        }
    }

    // 2. API Khóa giữ ghế tạm thời (5 phút) để tránh Race condition
    static async apiLockSeats(req, res) {
        try {
            const { showtimeId, seatIds } = req.body;

            if (!showtimeId || !seatIds || !Array.isArray(seatIds) || seatIds.length === 0) {
                return res.status(400).json({
                    success: false,
                    message: 'Vui lòng chọn ít nhất 1 ghế!'
                });
            }

            if (seatIds.length > 8) {
                return res.status(400).json({
                    success: false,
                    message: 'Mỗi lần đặt vé chỉ được chọn tối đa 8 ghế để tránh chiếm dụng chỗ!'
                });
            }

            const result = await SeatLock.lockSeats({
                showtimeId: Number(showtimeId),
                seatIds: seatIds.map(Number),
                sessionId: req.sessionID,
                userId: req.session.user ? req.session.user.id : null,
                minutes: 5
            });

            if (!result.success) {
                return res.status(409).json(result); // 409 Conflict
            }

            // Lưu danh sách ghế đã chọn vào session để chuyển tiếp các bước sau
            req.session.bookingData = {
                showtimeId: Number(showtimeId),
                seatIds: seatIds.map(Number),
                lockExpiresAt: result.expiresAt
            };

            return req.session.save((err) => {
                if (err) console.error('Session save error:', err);
                return res.json({
                    success: true,
                    message: 'Đã giữ ghế tạm thời trong 5 phút!',
                    expiresAt: result.expiresAt
                });
            });
        } catch (err) {
            console.error('Lỗi khóa ghế:', err);
            return res.status(500).json({ success: false, message: 'Lỗi khóa ghế: ' + err.message });
        }
    }

    // 3. Chọn Combo bắp nước
    static async selectCombos(req, res) {
        try {
            const showtimeId = req.params.showtimeId;
            const showtime = await Showtime.findById(showtimeId);
            const bookingData = req.session.bookingData;

            if (!showtime || !bookingData || Number(bookingData.showtimeId) !== Number(showtimeId)) {
                return res.redirect(`/booking/seats/${showtimeId}`);
            }

            // Lấy chi tiết các ghế đã chọn
            const allSeats = await Seat.getSeatsWithStatusForShowtime(showtimeId, req.sessionID);
            const selectedSeats = allSeats.filter(s => bookingData.seatIds.includes(s.id));
            const combos = await Combo.getAllActive();

            res.render('client/select-combos', {
                title: `Chọn Bắp Nước - ${showtime.movie_title}`,
                showtime,
                selectedSeats,
                combos
            });
        } catch (err) {
            console.error('Lỗi chọn combo:', err);
            res.redirect(`/booking/seats/${req.params.showtimeId}`);
        }
    }

    // Lưu combo vào session và chuyển sang thanh toán
    static saveCombosAndProceed(req, res) {
        const showtimeId = req.params.showtimeId;
        const combos = req.body.combos ? JSON.parse(req.body.combos) : [];

        if (req.session.bookingData) {
            req.session.bookingData.combos = combos;
        }

        res.redirect(`/booking/checkout/${showtimeId}`);
    }

    // 4. Trang Thanh toán vé & Đếm ngược 5 phút
    static async checkout(req, res) {
        try {
            const showtimeId = req.params.showtimeId;
            const showtime = await Showtime.findById(showtimeId);
            const bookingData = req.session.bookingData;

            if (!showtime || !bookingData || Number(bookingData.showtimeId) !== Number(showtimeId)) {
                return res.redirect(`/booking/seats/${showtimeId}`);
            }

            // Kiểm tra xem ghế đã bị hết hạn giữ chỗ chưa
            const now = new Date();
            const lockExpiry = new Date(bookingData.lockExpiresAt);
            if (now > lockExpiry) {
                delete req.session.bookingData;
                return res.redirect(`/booking/seats/${showtimeId}?error=` + encodeURIComponent('Thời gian giữ ghế (5 phút) đã hết! Vui lòng chọn lại ghế.'));
            }

            const remainingSeconds = Math.max(0, Math.floor((lockExpiry.getTime() - now.getTime()) / 1000));

            // Lấy thông tin chi tiết các ghế
            const allSeats = await Seat.getSeatsWithStatusForShowtime(showtimeId, req.sessionID);
            const selectedSeats = allSeats.filter(s => bookingData.seatIds.includes(s.id));
            const seatTotal = selectedSeats.reduce((sum, s) => sum + s.calculated_price, 0);

            // Lấy thông tin combo
            const selectedCombos = [];
            let comboTotal = 0;
            if (bookingData.combos && Array.isArray(bookingData.combos)) {
                for (const c of bookingData.combos) {
                    if (c.quantity > 0) {
                        const comboObj = await Combo.findById(c.id);
                        if (comboObj) {
                            const total = comboObj.price * c.quantity;
                            comboTotal += total;
                            selectedCombos.push({
                                id: comboObj.id,
                                name: comboObj.name,
                                price: comboObj.price,
                                quantity: c.quantity,
                                total
                            });
                        }
                    }
                }
            }

            const grandTotal = seatTotal + comboTotal;

            const breadcrumbs = [
                { label: 'Phim', url: '/movies' },
                { label: showtime.movie_title, url: `/movies/${showtime.movie_id}` },
                { label: 'Thanh Toán Vé' }
            ];

            res.render('client/checkout', {
                title: `Thanh Toán Vé - ${showtime.movie_title}`,
                showtime,
                selectedSeats,
                seatTotal,
                selectedCombos,
                comboTotal,
                grandTotal,
                remainingSeconds,
                currentUser: req.session.user || null,
                breadcrumbs
            });
        } catch (err) {
            console.error('Lỗi checkout:', err);
            res.redirect(`/booking/seats/${req.params.showtimeId}`);
        }
    }

    // 5. Xử lý Thanh toán vé
    static async processPayment(req, res) {
        const {
            showtime_id,
            customer_name,
            customer_email,
            customer_phone,
            payment_method
        } = req.body;

        const bookingData = req.session.bookingData;
        if (!bookingData || Number(bookingData.showtimeId) !== Number(showtime_id)) {
            return res.redirect('/');
        }

        // Kiểm tra hết hạn giữ ghế
        const now = new Date();
        if (now > new Date(bookingData.lockExpiresAt)) {
            delete req.session.bookingData;
            return res.redirect(`/booking/seats/${showtime_id}?error=` + encodeURIComponent('Thời gian giữ chỗ đã hết! Vui lòng đặt lại.'));
        }

        // Chuẩn bị dữ liệu ghế
        const allSeats = await Seat.getSeatsWithStatusForShowtime(showtime_id, req.sessionID);
        const selectedSeats = allSeats
            .filter(s => bookingData.seatIds.includes(s.id))
            .map(s => ({
                id: s.id,
                seat_code: s.seat_code,
                price: s.calculated_price
            }));

        // Chuẩn bị dữ liệu combo
        const comboList = [];
        if (bookingData.combos && Array.isArray(bookingData.combos)) {
            for (const c of bookingData.combos) {
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
        }

        try {
            const result = await Booking.createBooking({
                userId: req.session.user ? req.session.user.id : null,
                customerName: customer_name || (req.session.user ? req.session.user.full_name : 'Khách hàng'),
                customerEmail: customer_email || (req.session.user ? req.session.user.email : 'guest@cinema.com'),
                customerPhone: customer_phone || (req.session.user ? req.session.user.phone : ''),
                showtimeId: Number(showtime_id),
                seats: selectedSeats,
                combos: comboList,
                paymentMethod: payment_method || 'mbbank_qr',
                bookingType: 'online',
                sessionId: req.sessionID
            });

            // Xóa session đặt vé tạm
            delete req.session.bookingData;

            return res.redirect(`/booking/success/${result.bookingCode}`);
        } catch (err) {
            console.error('Lỗi khi thanh toán booking:', err);
            return res.redirect(`/booking/checkout/${showtime_id}?error=` + encodeURIComponent('Có lỗi xảy ra trong quá trình thanh toán! Vui lòng thử lại.'));
        }
    }

    // 6. Vé điện tử & Hiển thị mã QR Code
    static async ticketSuccess(req, res) {
        try {
            const bookingCode = req.params.bookingCode;
            const booking = await Booking.findByCode(bookingCode);

            if (!booking) {
                return res.status(404).render('client/404', {
                    title: 'Không Tìm Thấy Vé',
                    message: 'Không tìm thấy thông tin đơn đặt vé!'
                });
            }

            const tickets = await Booking.getTicketsByBookingId(booking.id);
            const combos = await Booking.getCombosByBookingId(booking.id);

            res.render('client/ticket-success', {
                title: `Vé Điện Tử - Mã Đơn ${booking.booking_code}`,
                booking,
                tickets,
                combos
            });
        } catch (err) {
            console.error('Lỗi vé điện tử:', err);
            res.status(500).render('client/404', {
                title: '500 - Lỗi',
                message: 'Không thể xem vé: ' + err.message
            });
        }
    }

    // 7. Lịch sử đặt vé cá nhân của khách hàng
    static async myTickets(req, res) {
        try {
            const userId = req.session.user.id;
            const bookings = await Booking.getByUserId(userId);

            res.render('client/my-tickets', {
                title: 'Lịch Sử Đặt Vé Của Tôi',
                bookings,
                breadcrumbs: [
                    { label: 'Tài Khoản' },
                    { label: 'Vé Đã Mua' }
                ]
            });
        } catch (err) {
            console.error('Lỗi lịch sử vé:', err);
            res.redirect('/');
        }
    }
}

module.exports = BookingController;
