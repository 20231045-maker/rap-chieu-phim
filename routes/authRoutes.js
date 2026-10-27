const express = require('express');
const router = express.Router();
const AuthController = require('../controllers/AuthController');
const { requireLogin } = require('../middlewares/authMiddleware');

router.get('/login', AuthController.showLogin);
router.post('/login', AuthController.processLogin);
router.get('/register', AuthController.showRegister);
router.post('/register', AuthController.processRegister);
router.get('/logout', AuthController.logout);

// Profile
router.get('/profile', requireLogin, AuthController.showProfile);
router.post('/profile', requireLogin, AuthController.updateProfile);
router.post('/change-password', requireLogin, AuthController.changePassword);

module.exports = router;
