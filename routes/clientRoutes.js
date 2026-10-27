const express = require('express');
const router = express.Router();
const HomeController = require('../controllers/HomeController');
const MovieController = require('../controllers/MovieController');
const BookingController = require('../controllers/BookingController');
const AuthController = require('../controllers/AuthController');
const { requireLogin } = require('../middlewares/authMiddleware');

// Trang chủ & Thông tin chung
router.get('/', HomeController.index);
router.get('/movies', HomeController.showMovies);
router.get('/movies/:id', MovieController.detail);
router.get('/pricing', HomeController.pricing);
router.get('/about', HomeController.about);

// Quy trình đặt vé xem phim (Bắt buộc phải đăng nhập hoặc đăng ký tài khoản thành viên)
router.get('/booking/seats/:showtimeId', requireLogin, BookingController.selectSeats);
router.post('/booking/api/lock-seats', requireLogin, BookingController.apiLockSeats);
router.get('/booking/combos/:showtimeId', requireLogin, BookingController.selectCombos);
router.post('/booking/save-combos/:showtimeId', requireLogin, BookingController.saveCombosAndProceed);
router.get('/booking/checkout/:showtimeId', requireLogin, BookingController.checkout);
router.post('/booking/process-payment', requireLogin, BookingController.processPayment);
router.get('/booking/success/:bookingCode', BookingController.ticketSuccess);

// Lịch sử vé & hồ sơ
router.get('/my-tickets', requireLogin, BookingController.myTickets);
router.get('/profile', requireLogin, AuthController.showProfile);
router.post('/profile', requireLogin, AuthController.updateProfile);
router.post('/change-password', requireLogin, AuthController.changePassword);

module.exports = router;
