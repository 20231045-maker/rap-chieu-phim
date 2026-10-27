-- ====================================================================
-- HỆ THỐNG ĐẶT VÉ VÀ QUẢN LÝ SUẤT CHIẾU RẠP CHIẾU PHIM
-- ĐỒ ÁN CHUYÊN NGÀNH CÔNG NGHỆ PHẦN MỀM - NHÓM 10
-- Sinh viên thực hiện:
--   1. Nguyễn Mạnh Quyết (MSV: 20231053)
--   2. Hà Thái Bảo      (MSV: 20231045)
-- SƠ ĐỒ CƠ SỞ DỮ LIỆU CHUẨN HÓA 3NF (DDL SCRIPT)
-- ====================================================================

-- 1. BẢNG VAI TRÒ (ROLES) - Phân quyền RBAC
CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,             -- 'admin', 'manager', 'staff', 'client'
    display_name TEXT NOT NULL,            -- Tên hiển thị tiếng Việt
    description TEXT
);

-- 2. BẢNG NGƯỜI DÙNG (USERS)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_id INTEGER NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    password_hash TEXT NOT NULL,
    avatar TEXT DEFAULT '/images/default-avatar.png',
    status TEXT DEFAULT 'active' CHECK(status IN ('active', 'locked')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE RESTRICT
);

-- 3. BẢNG PHIM (MOVIES)
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    original_title TEXT,
    genre TEXT NOT NULL,                   -- Thể loại (Hành động, Phiêu lưu, Hoạt hình,...)
    duration INTEGER NOT NULL,             -- Thời lượng tính theo phút (VD: 125)
    release_date DATE NOT NULL,
    end_date DATE,
    age_rating TEXT DEFAULT 'P' CHECK(age_rating IN ('P', 'K', 'T13', 'T16', 'T18')),
    director TEXT,
    cast TEXT,
    description TEXT,
    poster_url TEXT,
    banner_url TEXT,
    trailer_url TEXT,                      -- Link trailer Youtube
    language TEXT DEFAULT 'Phụ đề Tiếng Việt',
    status TEXT DEFAULT 'now_showing' CHECK(status IN ('now_showing', 'coming_soon', 'ended')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 4. BẢNG PHÒNG CHIẾU (ROOMS)
CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_name TEXT NOT NULL,               -- VD: 'Phòng Chiếu 01 (IMAX)', 'Phòng Chiếu 02'
    screen_type TEXT DEFAULT '2D' CHECK(screen_type IN ('2D', '3D', 'IMAX', '4DX')),
    total_rows INTEGER DEFAULT 7,          -- Hàng A -> G
    seats_per_row INTEGER DEFAULT 12,      -- 1 -> 12
    total_seats INTEGER DEFAULT 84,
    status TEXT DEFAULT 'active' CHECK(status IN ('active', 'maintenance'))
);

-- 5. BẢNG GHẾ NGỒI (SEATS)
CREATE TABLE IF NOT EXISTS seats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER NOT NULL,
    seat_row TEXT NOT NULL,                -- 'A', 'B', 'C', 'D', 'E', 'F', 'G'
    seat_number INTEGER NOT NULL,          -- 1 .. 12
    seat_code TEXT NOT NULL,               -- 'A1', 'B5', 'G11'
    seat_type TEXT DEFAULT 'regular' CHECK(seat_type IN ('regular', 'vip', 'sweetbox')),
    price_multiplier REAL DEFAULT 1.0,     -- Ghế thường: 1.0, VIP: 1.25, Sweetbox: 2.2
    status TEXT DEFAULT 'active' CHECK(status IN ('active', 'maintenance')),
    FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE,
    UNIQUE(room_id, seat_row, seat_number)
);

-- 6. BẢNG SUẤT CHIẾU (SHOWTIMES)
CREATE TABLE IF NOT EXISTS showtimes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    start_time DATETIME NOT NULL,          -- 'YYYY-MM-DD HH:MM:SS'
    end_time DATETIME NOT NULL,            -- start_time + duration + buffer_minutes
    buffer_minutes INTEGER DEFAULT 15,     -- Thời gian dọn dẹp và chuẩn bị phòng chiếu
    base_price INTEGER DEFAULT 80000,      -- Giá vé cơ bản (VND)
    status TEXT DEFAULT 'scheduled' CHECK(status IN ('scheduled', 'cancelled', 'completed')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE RESTRICT,
    FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE RESTRICT
);

-- 7. BẢNG COMBO BẮP NƯỚC (COMBOS)
CREATE TABLE IF NOT EXISTS combos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL,
    image_url TEXT,
    status TEXT DEFAULT 'active' CHECK(status IN ('active', 'inactive'))
);

-- 8. BẢNG ĐƠN ĐẶT VÉ (BOOKINGS)
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_code TEXT UNIQUE NOT NULL,     -- VD: 'BKG-20261013-ABC123'
    user_id INTEGER,                       -- NULL nếu khách mua tại quầy không tài khoản
    customer_name TEXT,
    customer_email TEXT,
    customer_phone TEXT,
    showtime_id INTEGER NOT NULL,
    total_amount INTEGER NOT NULL,
    discount_amount INTEGER DEFAULT 0,
    payment_method TEXT DEFAULT 'vnpay' CHECK(payment_method IN ('vnpay', 'momo', 'card', 'cash')),
    payment_status TEXT DEFAULT 'paid' CHECK(payment_status IN ('pending', 'paid', 'failed', 'refunded')),
    booking_status TEXT DEFAULT 'confirmed' CHECK(booking_status IN ('pending', 'confirmed', 'cancelled')),
    booking_type TEXT DEFAULT 'online' CHECK(booking_type IN ('online', 'pos')),
    created_by INTEGER,                    -- ID nhân viên nếu bán tại POS
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (showtime_id) REFERENCES showtimes(id) ON DELETE RESTRICT,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
);

-- 9. BẢNG VÉ XEM PHIM CHI TIẾT (TICKETS)
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_code TEXT UNIQUE NOT NULL,      -- VD: 'TKT-20261013-XYZ789'
    booking_id INTEGER NOT NULL,
    showtime_id INTEGER NOT NULL,
    seat_id INTEGER NOT NULL,
    price INTEGER NOT NULL,
    qr_data TEXT NOT NULL,                 -- Dữ liệu mã hóa trong QR Code
    status TEXT DEFAULT 'unused' CHECK(status IN ('unused', 'checked_in', 'expired', 'cancelled')),
    checked_in_at DATETIME,
    checked_in_by INTEGER,                 -- Nhân viên thực hiện soát vé
    FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE,
    FOREIGN KEY (showtime_id) REFERENCES showtimes(id) ON DELETE RESTRICT,
    FOREIGN KEY (seat_id) REFERENCES seats(id) ON DELETE RESTRICT,
    FOREIGN KEY (checked_in_by) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE(showtime_id, seat_id)          -- Ràng buộc không thể bán 2 vé cho 1 ghế trong cùng suất chiếu
);

-- 10. BẢNG CHI TIẾT COMBO BẮP NƯỚC THEO ĐƠN (BOOKING_COMBOS)
CREATE TABLE IF NOT EXISTS booking_combos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER NOT NULL,
    combo_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price INTEGER NOT NULL,
    total_price INTEGER NOT NULL,
    FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE,
    FOREIGN KEY (combo_id) REFERENCES combos(id) ON DELETE RESTRICT
);

-- 11. BẢNG KHÓA GIỮ GHẾ TẠM THỜI (SEAT_LOCKS) - Chống Race Condition
CREATE TABLE IF NOT EXISTS seat_locks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    showtime_id INTEGER NOT NULL,
    seat_id INTEGER NOT NULL,
    session_id TEXT NOT NULL,
    user_id INTEGER,
    locked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME NOT NULL,
    FOREIGN KEY (showtime_id) REFERENCES showtimes(id) ON DELETE CASCADE,
    FOREIGN KEY (seat_id) REFERENCES seats(id) ON DELETE CASCADE,
    UNIQUE(showtime_id, seat_id)
);

-- 12. BẢNG CÀU ĐẶT HỆ THỐNG (SYSTEM_SETTINGS)
CREATE TABLE IF NOT EXISTS system_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    description TEXT
);

-- TẠO CÁC CHỈ MỤC (INDEXES) TỐI ƯU HIỆU NĂNG TRUY VẤN
CREATE INDEX IF NOT EXISTS idx_showtimes_room_time ON showtimes(room_id, start_time, end_time);
CREATE INDEX IF NOT EXISTS idx_showtimes_movie_time ON showtimes(movie_id, start_time);
CREATE INDEX IF NOT EXISTS idx_tickets_booking ON tickets(booking_id);
CREATE INDEX IF NOT EXISTS idx_tickets_showtime_seat ON tickets(showtime_id, seat_id);
CREATE INDEX IF NOT EXISTS idx_tickets_code ON tickets(ticket_code);
CREATE INDEX IF NOT EXISTS idx_seat_locks_expiry ON seat_locks(expires_at);
