const User = require('../models/User');

function isSafeRedirect(url) {
    if (!url || typeof url !== 'string') return false;
    return url.startsWith('/') && !url.startsWith('//') && !url.includes('\\');
}

class AuthController {
    static showLogin(req, res) {
        if (req.session.user) {
            return res.redirect('/');
        }
        res.render('auth/login', {
            title: 'Đăng Nhập - Hệ Thống Đặt Vé Xem Phim',
            error: req.query.error || null,
            success: req.query.success || null,
            returnTo: req.query.redirect || req.session.returnTo || ''
        });
    }

    static async processLogin(req, res) {
        const { email, password, returnTo } = req.body;

        if (!email || !password) {
            return res.render('auth/login', {
                title: 'Đăng Nhập',
                error: 'Vui lòng nhập đầy đủ Email và Mật khẩu!',
                success: null,
                returnTo
            });
        }

        try {
            const user = await User.findByEmail(email.trim().toLowerCase());
            if (!user) {
                return res.render('auth/login', {
                    title: 'Đăng Nhập',
                    error: 'Email hoặc mật khẩu không chính xác!',
                    success: null,
                    returnTo
                });
            }

            if (user.status === 'locked') {
                return res.render('auth/login', {
                    title: 'Đăng Nhập',
                    error: 'Tài khoản của bạn đã bị khóa! Vui lòng liên hệ quản trị viên.',
                    success: null,
                    returnTo
                });
            }

            const isValid = User.verifyPassword(password, user.password_hash);
            if (!isValid) {
                return res.render('auth/login', {
                    title: 'Đăng Nhập',
                    error: 'Email hoặc mật khẩu không chính xác!',
                    success: null,
                    returnTo
                });
            }

            // Lưu thông tin vào session
            req.session.user = {
                id: user.id,
                role_id: user.role_id,
                role_name: user.role_name,
                role_display: user.role_display,
                full_name: user.full_name,
                email: user.email,
                phone: user.phone,
                avatar: user.avatar
            };

            // Điều hướng an toàn (Chống Open Redirect Attack)
            if (isSafeRedirect(returnTo)) {
                delete req.session.returnTo;
                return res.redirect(returnTo);
            }

            if (user.role_name === 'admin') {
                return res.redirect('/admin/users');
            } else if (user.role_name === 'manager') {
                return res.redirect('/manager/dashboard');
            } else if (user.role_name === 'staff') {
                return res.redirect('/staff/pos');
            } else {
                return res.redirect('/');
            }
        } catch (err) {
            console.error('Lỗi khi đăng nhập:', err);
            return res.render('auth/login', {
                title: 'Đăng Nhập',
                error: 'Có lỗi xảy ra trong quá trình đăng nhập. Vui lòng thử lại!',
                success: null,
                returnTo
            });
        }
    }

    static showRegister(req, res) {
        if (req.session.user) {
            return res.redirect('/');
        }
        res.render('auth/register', {
            title: 'Đăng Ký Tài Khoản Khách Hàng',
            error: req.query.error || null,
            formData: {},
            returnTo: req.query.redirect || req.session.returnTo || ''
        });
    }

    static async processRegister(req, res) {
        const { full_name, email, phone, password, confirm_password, returnTo } = req.body;

        if (!full_name || !email || !password) {
            return res.render('auth/register', {
                title: 'Đăng Ký Tài Khoản',
                error: 'Vui lòng điền đầy đủ các thông tin bắt buộc!',
                formData: req.body,
                returnTo: returnTo || ''
            });
        }

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email.trim())) {
            return res.render('auth/register', {
                title: 'Đăng Ký Tài Khoản',
                error: 'Địa chỉ Email không đúng định dạng hợp lệ!',
                formData: req.body,
                returnTo: returnTo || ''
            });
        }

        if (phone && phone.trim()) {
            const phoneRegex = /^[0-9+() -]{8,20}$/;
            if (!phoneRegex.test(phone.trim())) {
                return res.render('auth/register', {
                    title: 'Đăng Ký Tài Khoản',
                    error: 'Số điện thoại không đúng định dạng hợp lệ!',
                    formData: req.body,
                    returnTo: returnTo || ''
                });
            }
        }

        if (password !== confirm_password) {
            return res.render('auth/register', {
                title: 'Đăng Ký Tài Khoản',
                error: 'Mật khẩu xác nhận không khớp!',
                formData: req.body,
                returnTo: returnTo || ''
            });
        }

        if (password.length < 6) {
            return res.render('auth/register', {
                title: 'Đăng Ký Tài Khoản',
                error: 'Mật khẩu phải chứa ít nhất 6 ký tự!',
                formData: req.body,
                returnTo: returnTo || ''
            });
        }

        try {
            const existingUser = await User.findByEmail(email.trim().toLowerCase());
            if (existingUser) {
                return res.render('auth/register', {
                    title: 'Đăng Ký Tài Khoản',
                    error: 'Email này đã được sử dụng trên hệ thống!',
                    formData: req.body,
                    returnTo: returnTo || ''
                });
            }

            // Role ID 4 là Khách hàng (client)
            const userId = await User.create({
                role_id: 4,
                full_name: full_name.trim(),
                email: email.trim().toLowerCase(),
                phone: phone ? phone.trim() : '',
                password
            });

            // Tự động đăng nhập
            const newUser = await User.findById(userId);
            req.session.user = {
                id: newUser.id,
                role_id: newUser.role_id,
                role_name: newUser.role_name,
                role_display: newUser.role_display,
                full_name: newUser.full_name,
                email: newUser.email,
                phone: newUser.phone,
                avatar: newUser.avatar
            };

            // Nếu đang trong luồng mua vé, điều hướng an toàn (Chống Open Redirect)
            if (isSafeRedirect(returnTo)) {
                delete req.session.returnTo;
                return res.redirect(returnTo);
            }

            return res.redirect('/?welcome=1');
        } catch (err) {
            console.error('Lỗi khi đăng ký:', err);
            return res.render('auth/register', {
                title: 'Đăng Ký Tài Khoản',
                error: 'Có lỗi xảy ra khi tạo tài khoản. Vui lòng thử lại!',
                formData: req.body,
                returnTo: returnTo || ''
            });
        }
    }

    static logout(req, res) {
        req.session.destroy(() => {
            res.redirect('/');
        });
    }

    static async showProfile(req, res) {
        try {
            const user = await User.findById(req.session.user.id);
            res.render('client/profile', {
                title: 'Hồ Sơ Cá Nhân',
                user,
                error: null,
                success: req.query.success || null
            });
        } catch (err) {
            console.error('Lỗi xem hồ sơ:', err);
            res.redirect('/');
        }
    }

    static async updateProfile(req, res) {
        try {
            const { full_name, phone } = req.body;
            const userId = req.session.user.id;

            await User.updateProfile(userId, { full_name, phone });
            
            // Cập nhật lại session
            req.session.user.full_name = full_name;
            req.session.user.phone = phone;

            res.redirect('/profile?success=' + encodeURIComponent('Cập nhật thông tin thành công!'));
        } catch (err) {
            console.error('Lỗi cập nhật hồ sơ:', err);
            res.redirect('/profile');
        }
    }

    static async changePassword(req, res) {
        try {
            const { current_password, new_password, confirm_password } = req.body;
            const userId = req.session.user.id;
            const user = await User.findById(userId);

            if (!User.verifyPassword(current_password, user.password_hash)) {
                return res.render('client/profile', {
                    title: 'Hồ Sơ Cá Nhân',
                    user,
                    error: 'Mật khẩu hiện tại không chính xác!',
                    success: null
                });
            }

            if (new_password !== confirm_password) {
                return res.render('client/profile', {
                    title: 'Hồ Sơ Cá Nhân',
                    user,
                    error: 'Mật khẩu mới và xác nhận mật khẩu không khớp!',
                    success: null
                });
            }

            if (new_password.length < 6) {
                return res.render('client/profile', {
                    title: 'Hồ Sơ Cá Nhân',
                    user,
                    error: 'Mật khẩu mới phải có tối thiểu 6 ký tự!',
                    success: null
                });
            }

            await User.changePassword(userId, new_password);
            res.redirect('/profile?success=' + encodeURIComponent('Đổi mật khẩu thành công!'));
        } catch (err) {
            console.error('Lỗi đổi mật khẩu:', err);
            res.redirect('/profile');
        }
    }
}

module.exports = AuthController;
