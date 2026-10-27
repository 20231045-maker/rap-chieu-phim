require('dotenv').config();
const express = require('express');
const path = require('path');
const session = require('express-session');
const cookieParser = require('cookie-parser');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');

// Khởi tạo CSDL & kết nối
require('./database/db');

// Import Middlewares
const { checkAuth } = require('./middlewares/authMiddleware');

// Import Routes
const authRoutes = require('./routes/authRoutes');
const clientRoutes = require('./routes/clientRoutes');
const staffRoutes = require('./routes/staffRoutes');
const managerRoutes = require('./routes/managerRoutes');
const adminRoutes = require('./routes/adminRoutes');

const app = express();
const PORT = process.env.PORT || 3000;
const isProd = process.env.NODE_ENV === 'production';

// Tắt header công nghệ Express (Chống footprinting)
app.disable('x-powered-by');

// Cấu hình HTTP Security Headers với Helmet
app.use(helmet({
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            scriptSrc: ["'self'", "'unsafe-inline'", "'unsafe-eval'", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com", "https://unpkg.com"],
            scriptSrcAttr: ["'unsafe-inline'"],
            styleSrc: ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com", "https://fonts.googleapis.com"],
            fontSrc: ["'self'", "https://cdnjs.cloudflare.com", "https://fonts.gstatic.com"],
            imgSrc: ["'self'", "data:", "blob:", "https:", "http:"],
            childSrc: ["'self'", "https://www.youtube.com", "https://youtube.com", "https://*.youtube.com", "https://www.youtube-nocookie.com", "https://*.youtube-nocookie.com"],
            frameSrc: ["'self'", "https://www.youtube.com", "https://youtube.com", "https://*.youtube.com", "https://www.youtube-nocookie.com", "https://*.youtube-nocookie.com"],
            connectSrc: ["'self'"],
            upgradeInsecureRequests: null
        }
    },
    referrerPolicy: { policy: "strict-origin-when-cross-origin" },
    crossOriginEmbedderPolicy: false,
    crossOriginOpenerPolicy: false,
    crossOriginResourcePolicy: false,
    strictTransportSecurity: false
}));

// Cấu hình View Engine (EJS)
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Cấu hình Static Files & Uploads (Thiết lập X-Content-Type-Options nosniff chống MIME sniffing)
app.use(express.static(path.join(__dirname, 'public'), {
    etag: false,
    maxAge: 0,
    setHeaders: (res) => {
        res.set('Cache-Control', 'no-store, no-cache, must-revalidate, private');
    }
}));
app.use('/uploads', express.static(path.join(__dirname, 'uploads'), {
    etag: false,
    maxAge: 0,
    setHeaders: (res) => {
        res.set('X-Content-Type-Options', 'nosniff');
        res.set('Cache-Control', 'no-store, no-cache, must-revalidate, private');
    }
}));

// Cấu hình Body Parser & Cookie Parser
app.use(express.urlencoded({ extended: true, limit: '2mb' }));
app.use(express.json({ limit: '2mb' }));
app.use(cookieParser());

// Cấu hình Session bảo mật
app.use(session({
    name: 'cinestar_sid', // Đổi tên cookie session mặc định tránh nhận diện công nghệ
    secret: process.env.SESSION_SECRET || 'cinestar_secret_key_cnpm_nhom10_2026',
    resave: false,
    saveUninitialized: false, // Tránh tạo session rác không cần thiết
    cookie: {
        httpOnly: true, // Ngăn chặn mã JavaScript phía client đánh cắp cookie (chống XSS Cookie Theft)
        secure: isProd, // Bật cờ Secure khi chạy HTTPS trên production
        sameSite: 'lax', // Ngăn chặn các cuộc tấn công Cross-Site Request Forgery (CSRF)
        maxAge: 24 * 60 * 60 * 1000 // 24 giờ
    }
}));

// Giới hạn tần suất request (Rate Limiting) cho các thao tác đăng nhập & đăng ký
const authLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 phút
    max: 100, // Tối đa 100 lượt thao tác trong 15 phút
    skip: (req) => req.method === 'GET', // Chỉ áp dụng giới hạn cho request POST gửi biểu mẫu
    standardHeaders: true,
    legacyHeaders: false,
    message: 'Bạn đã thực hiện quá nhiều yêu cầu xác thực. Vui lòng thử lại sau 15 phút để bảo đảm an toàn!'
});
app.use('/auth/login', authLimiter);
app.use('/auth/register', authLimiter);

// Chống CSRF cơ bản: Kiểm tra Host và Origin cho các request thay đổi trạng thái (POST/PUT/DELETE)
app.use((req, res, next) => {
    if (['POST', 'PUT', 'DELETE'].includes(req.method)) {
        const origin = req.headers['origin'];
        const host = req.headers['host'];
        if (origin && host) {
            try {
                const originHost = new URL(origin).host;
                if (originHost !== host && originHost.replace('localhost', '127.0.0.1') !== host.replace('localhost', '127.0.0.1')) {
                    return res.status(403).send('Yêu cầu bị từ chối do vi phạm quy tắc bảo mật nguồn gốc (Cross-Origin Request Blocked).');
                }
            } catch (e) {
                // Bỏ qua lỗi URL parse
            }
        }
    }
    next();
});

// Global Authentication Middleware
app.use(checkAuth);

// Đăng ký các Routes theo phân hệ
app.use('/auth', authRoutes);
app.use('/staff', staffRoutes);
app.use('/manager', managerRoutes);
app.use('/admin', adminRoutes);
app.use('/', clientRoutes);

// Xử lý trang 404 Not Found
app.use((req, res) => {
    res.status(404).render('client/404', {
        title: '404 - Không Tìm Thấy Trang',
        message: 'Trang bạn đang yêu cầu không tồn tại hoặc đã bị gỡ bỏ.'
    });
});

// Xử lý lỗi toàn cục 500 (Không lộ thông tin nhạy cảm của server khi ở môi trường production)
app.use((err, req, res, next) => {
    console.error('SERVER ERROR:', err);
    res.status(500).render('client/404', {
        title: '500 - Lỗi Máy Chủ Nội Bộ',
        message: isProd 
            ? 'Hệ thống đang gặp sự cố tạm thời. Vui lòng thử lại sau ít phút!'
            : 'Có lỗi xảy ra trong quá trình xử lý: ' + err.message
    });
});

// Khởi động Web Server
app.listen(PORT, () => {
    console.log('====================================================================');
    console.log('🎬 CINESTAR CINEMA - HỆ THỐNG ĐẶT VÉ VÀ QUẢN LÝ SUẤT CHIẾU');
    console.log('📚 ĐỒ ÁN CHUYÊN NGÀNH CÔNG NGHỆ PHẦN MỀM - NHÓM 10');
    console.log('👤 Sinh viên thực hiện:');
    console.log('   1. Nguyễn Mạnh Quyết (MSV: 20231053) - Phân hệ Manager & Admin');
    console.log('   2. Hà Thái Bảo      (MSV: 20231045) - Phân hệ Client & Staff');
    console.log('--------------------------------------------------------------------');
    console.log(`🚀 Web Application đang chạy tại: http://localhost:${PORT}`);
    console.log(`🛡️  Bảo mật: Helmet Enabled | Rate Limiting Enabled | Strict Session`);
    console.log('--------------------------------------------------------------------');
    console.log('🔑 TÀI KHOẢN MẪU ĐĂNG NHẬP (4 VAI TRÒ):');
    console.log('   - Quản trị viên (Admin)   : admin@cinema.com   / pass: admin123');
    console.log('   - Quản lý rạp (Manager)   : manager@cinema.com / pass: manager123');
    console.log('   - Nhân viên quầy (Staff)  : staff@cinema.com   / pass: staff123');
    console.log('   - Khách hàng (Client)     : client@cinema.com  / pass: client123');
    console.log('====================================================================');
});
