const express = require('express');
const router = express.Router();
const StaffController = require('../controllers/StaffController');
const { requireRole } = require('../middlewares/authMiddleware');

// Chỉ nhân viên (staff), quản lý (manager) hoặc quản trị viên (admin) mới được truy cập
router.use(requireRole(['staff', 'manager', 'admin']));

// POS Bán vé quầy
router.get('/', (req, res) => res.redirect('/staff/pos'));
router.get('/pos', StaffController.pos);
router.get('/api/pos-seats/:showtimeId', StaffController.apiPosSeats);
router.post('/api/pos-checkout', StaffController.posCheckout);

// Soát vé QR
router.get('/scan', StaffController.scanTicket);
router.get('/api/check-ticket', StaffController.apiCheckTicket);
router.post('/api/check-ticket', StaffController.apiCheckTicket);
router.post('/api/confirm-checkin', StaffController.apiConfirmCheckIn);

// Lịch sử soát vé
router.get('/history', StaffController.history);

module.exports = router;
