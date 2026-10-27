const express = require('express');
const router = express.Router();
const ManagerController = require('../controllers/ManagerController');
const { requireRole } = require('../middlewares/authMiddleware');
const upload = require('../middlewares/uploadMiddleware');

// Chỉ Quản lý (manager) hoặc Quản trị viên (admin) mới được vào
router.use(requireRole(['manager', 'admin']));

// Dashboard
router.get('/', (req, res) => res.redirect('/manager/dashboard'));
router.get('/dashboard', ManagerController.dashboard);

// Quản lý Phim
router.get('/movies', ManagerController.movies);
router.get('/movies/create', ManagerController.createMovieForm);
router.post('/movies/create', upload.single('poster_file'), ManagerController.storeMovie);
router.get('/movies/edit/:id', ManagerController.editMovieForm);
router.post('/movies/edit/:id', upload.single('poster_file'), ManagerController.updateMovie);
router.post('/movies/delete/:id', ManagerController.deleteMovie);

// Quản lý Phòng & Sơ đồ ghế
router.get('/rooms', ManagerController.rooms);
router.post('/rooms/create', ManagerController.createRoom);
router.get('/rooms/:id', ManagerController.roomDetail);
router.post('/api/update-seat', ManagerController.updateSeat);

// Quản lý Suất chiếu & Thuật toán chống xung đột
router.get('/showtimes', ManagerController.showtimes);
router.get('/showtimes/create', ManagerController.createShowtimeForm);
router.post('/showtimes/create', ManagerController.storeShowtime);
router.get('/api/check-conflict', ManagerController.apiCheckConflict);
router.post('/showtimes/cancel/:id', ManagerController.cancelShowtime);
router.post('/showtimes/delete/:id', ManagerController.deleteShowtime);

// Quản lý Combo bắp nước
router.get('/combos', ManagerController.combos);
router.post('/combos/create', ManagerController.storeCombo);
router.post('/combos/edit/:id', ManagerController.updateCombo);
router.post('/combos/delete/:id', ManagerController.deleteCombo);

// Báo cáo doanh thu & tỷ lệ lấp đầy
router.get('/reports', ManagerController.reports);

module.exports = router;
