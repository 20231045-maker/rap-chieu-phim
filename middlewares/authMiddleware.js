/**
 * Phân quyền truy cập dựa trên vai trò (Role-Based Access Control - RBAC)
 * Các vai trò: 'admin', 'manager', 'staff', 'client'
 */

function formatTime(val) {
    if (!val) return '';
    if (val instanceof Date) {
        const h = String(val.getHours()).padStart(2, '0');
        const m = String(val.getMinutes()).padStart(2, '0');
        return `${h}:${m}`;
    }
    const str = String(val);
    if (str.includes(' ')) {
        const parts = str.split(' ');
        if (parts[1]) return parts[1].substring(0, 5);
    }
    if (str.includes('T')) {
        const timePart = str.split('T')[1];
        return timePart.substring(0, 5);
    }
    return str.substring(0, 5);
}

function formatDate(val) {
    if (!val) return '';
    if (val instanceof Date) {
        const d = String(val.getDate()).padStart(2, '0');
        const m = String(val.getMonth() + 1).padStart(2, '0');
        const y = val.getFullYear();
        return `${d}/${m}/${y}`;
    }
    const str = String(val);
    const datePart = str.split(' ')[0].split('T')[0];
    const parts = datePart.split('-');
    if (parts.length === 3) return `${parts[2]}/${parts[1]}/${parts[0]}`;
    return str;
}

function formatDateTime(val) {
    if (!val) return '';
    return `${formatTime(val)} ${formatDate(val)}`;
}

function formatPrice(val) {
    return Number(val || 0).toLocaleString('vi-VN') + ' đ';
}

const { query } = require('../database/db');

let cachedCinemas = null;
async function getCinemasMap() {
    if (!cachedCinemas) {
        try {
            const list = await query('SELECT * FROM cinemas');
            cachedCinemas = {};
            list.forEach(c => {
                cachedCinemas[c.id] = c;
            });
        } catch (e) {
            cachedCinemas = {};
        }
    }
    return cachedCinemas;
}

async function checkAuth(req, res, next) {
    res.locals.currentUser = req.session.user || null;
    res.locals.currentPath = req.path;
    res.locals.formatTime = formatTime;
    res.locals.formatDate = formatDate;
    res.locals.formatDateTime = formatDateTime;
    res.locals.formatPrice = formatPrice;

    const cinemaId = req.cookies.selectedCinemaId || null;
    res.locals.selectedCinemaId = cinemaId;
    if (cinemaId) {
        const map = await getCinemasMap();
        res.locals.selectedCinema = map[cinemaId] || null;
    } else {
        res.locals.selectedCinema = null;
    }
    next();
}

function requireLogin(req, res, next) {
    if (!req.session.user) {
        if (req.headers['content-type']?.includes('application/json') || req.xhr) {
            return res.status(401).json({
                success: false,
                requireLogin: true,
                message: 'Vui lòng đăng nhập hoặc đăng ký tài khoản thành viên để đặt vé xem phim!'
            });
        }
        req.session.returnTo = req.originalUrl;
        return res.redirect('/auth/login?redirect=' + encodeURIComponent(req.originalUrl) + '&error=' + encodeURIComponent('Vui lòng đăng nhập hoặc đăng ký tài khoản thành viên để đặt vé xem phim!'));
    }
    next();
}

function requireRole(roles = []) {
    return (req, res, next) => {
        if (!req.session.user) {
            req.session.returnTo = req.originalUrl;
            return res.redirect('/auth/login?error=' + encodeURIComponent('Vui lòng đăng nhập trước!'));
        }

        const userRole = req.session.user.role_name;
        // Quản trị viên (admin) luôn có quyền truy cập tất cả
        if (userRole === 'admin') {
            return next();
        }

        if (Array.isArray(roles) ? roles.includes(userRole) : roles === userRole) {
            return next();
        }

        return res.status(403).render('auth/forbidden', {
            title: '403 - Không Có Quyền Truy Cập',
            message: 'Tài khoản của bạn không có quyền truy cập khu vực này!'
        });
    };
}

module.exports = {
    checkAuth,
    requireLogin,
    requireRole
};
