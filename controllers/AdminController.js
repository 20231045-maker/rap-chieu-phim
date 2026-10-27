const User = require('../models/User');
const Booking = require('../models/Booking');
const { query, run } = require('../database/db');

class AdminController {
    // 1. Quản lý Tài khoản & Phân quyền RBAC
    static async users(req, res) {
        try {
            const users = await User.getAll();
            const roles = await User.getAllRoles();

            res.render('admin/users', {
                title: 'Quản Lý Tài Khoản & Phân Quyền (RBAC)',
                users,
                roles,
                error: req.query.error || null,
                success: req.query.success || null
            });
        } catch (err) {
            console.error('Lỗi admin users:', err);
            res.redirect('/');
        }
    }

    static async createUserForm(req, res) {
        try {
            const roles = await User.getAllRoles();
            res.render('admin/user-form', {
                title: 'Tạo Tài Khoản Mới',
                roles,
                user: null,
                isEdit: false
            });
        } catch (err) {
            console.error('Lỗi createUserForm:', err);
            res.redirect('/admin/users');
        }
    }

    static async storeUser(req, res) {
        try {
            const { full_name, email, phone, role_id, password, status } = req.body;
            await User.create({
                full_name,
                email: email.trim().toLowerCase(),
                phone,
                role_id: Number(role_id),
                password,
                status: status || 'active'
            });
            res.redirect('/admin/users?success=' + encodeURIComponent('Tạo tài khoản người dùng thành công!'));
        } catch (err) {
            console.error('Lỗi tạo user:', err);
            res.redirect('/admin/users?error=' + encodeURIComponent('Lỗi tạo tài khoản (có thể email đã trùng)!'));
        }
    }

    static async editUserForm(req, res) {
        try {
            const user = await User.findById(req.params.id);
            const roles = await User.getAllRoles();
            if (!user) {
                return res.redirect('/admin/users?error=' + encodeURIComponent('Không tìm thấy tài khoản!'));
            }
            res.render('admin/user-form', {
                title: `Sửa Quyền & Thông Tin - ${user.full_name}`,
                roles,
                user,
                isEdit: true
            });
        } catch (err) {
            console.error('Lỗi editUserForm:', err);
            res.redirect('/admin/users');
        }
    }

    static async updateUser(req, res) {
        try {
            const { full_name, phone, role_id, status, password } = req.body;
            await User.update(req.params.id, {
                full_name,
                phone,
                role_id: Number(role_id),
                status,
                password
            });
            res.redirect('/admin/users?success=' + encodeURIComponent('Cập nhật tài khoản thành công!'));
        } catch (err) {
            res.redirect('/admin/users?error=' + encodeURIComponent('Lỗi cập nhật: ' + err.message));
        }
    }

    static async toggleStatus(req, res) {
        try {
            if (req.session.user && Number(req.params.id) === Number(req.session.user.id)) {
                return res.redirect('/admin/users?error=' + encodeURIComponent('Không thể tự khóa tài khoản quản trị đang đăng nhập!'));
            }
            const user = await User.findById(req.params.id);
            if (user) {
                const newStatus = user.status === 'active' ? 'locked' : 'active';
                await run('UPDATE users SET status = ? WHERE id = ?', [newStatus, user.id]);
            }
            res.redirect('/admin/users?success=' + encodeURIComponent('Đã đổi trạng thái tài khoản!'));
        } catch (err) {
            res.redirect('/admin/users');
        }
    }

    static async deleteUser(req, res) {
        try {
            if (req.session.user && Number(req.params.id) === Number(req.session.user.id)) {
                return res.redirect('/admin/users?error=' + encodeURIComponent('Không thể tự xóa tài khoản quản trị đang đăng nhập!'));
            }
            await User.delete(req.params.id);
            res.redirect('/admin/users?success=' + encodeURIComponent('Đã xóa tài khoản!'));
        } catch (err) {
            res.redirect('/admin/users?error=' + encodeURIComponent('Không thể xóa tài khoản đã có phát sinh giao dịch đặt vé!'));
        }
    }

    // 2. Cài đặt hệ thống
    static async settings(req, res) {
        try {
            const settingsList = await query('SELECT * FROM system_settings');
            const settings = {};
            settingsList.forEach(s => {
                settings[s.key] = s.value;
            });

            res.render('admin/settings', {
                title: 'Cài Đặt Cấu Hình Hệ Thống',
                settings,
                success: req.query.success || null
            });
        } catch (err) {
            console.error('Lỗi settings:', err);
            res.redirect('/');
        }
    }

    static async updateSettings(req, res) {
        try {
            const { cinema_name, address, hotline, buffer_time, seat_lock_time } = req.body;

            await run('REPLACE INTO system_settings (`key`, value) VALUES (?, ?)', ['cinema_name', cinema_name || '']);
            await run('REPLACE INTO system_settings (`key`, value) VALUES (?, ?)', ['address', address || '']);
            await run('REPLACE INTO system_settings (`key`, value) VALUES (?, ?)', ['hotline', hotline || '']);
            await run('REPLACE INTO system_settings (`key`, value) VALUES (?, ?)', ['buffer_time', buffer_time || '15']);
            await run('REPLACE INTO system_settings (`key`, value) VALUES (?, ?)', ['seat_lock_time', seat_lock_time || '5']);

            res.redirect('/admin/settings?success=' + encodeURIComponent('Lưu cấu hình hệ thống thành công!'));
        } catch (err) {
            res.redirect('/admin/settings?error=' + encodeURIComponent(err.message));
        }
    }

    // 3. Nhật ký giao dịch
    static async auditLogs(req, res) {
        try {
            const bookings = await Booking.getAll();
            res.render('admin/audit-logs', {
                title: 'Nhật Ký Giao Dịch & Đơn Vé Toàn Hệ Thống',
                bookings
            });
        } catch (err) {
            console.error('Lỗi auditLogs:', err);
            res.redirect('/');
        }
    }
}

module.exports = AdminController;
