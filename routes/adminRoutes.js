const express = require('express');
const router = express.Router();
const AdminController = require('../controllers/AdminController');
const { requireRole } = require('../middlewares/authMiddleware');

// Chỉ Quản trị viên (admin) mới được vào
router.use(requireRole(['admin']));

// Quản lý người dùng & Phân quyền RBAC
router.get('/', (req, res) => res.redirect('/admin/users'));
router.get('/users', AdminController.users);
router.get('/users/create', AdminController.createUserForm);
router.post('/users/create', AdminController.storeUser);
router.get('/users/edit/:id', AdminController.editUserForm);
router.post('/users/edit/:id', AdminController.updateUser);
router.post('/users/toggle-status/:id', AdminController.toggleStatus);
router.post('/users/delete/:id', AdminController.deleteUser);

// Cấu hình hệ thống & Audit logs
router.get('/settings', AdminController.settings);
router.post('/settings', AdminController.updateSettings);
router.get('/audit-logs', AdminController.auditLogs);

module.exports = router;
