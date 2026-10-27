-- ====================================================================
-- HỆ THỐNG ĐẶT VÉ VÀ QUẢN LÝ SUẤT CHIẾU RẠP CHIẾU PHIM (CINESTAR / BETACINEMAS / CGV)
-- ĐỒ ÁN CHUYÊN NGÀNH CÔNG NGHỆ PHẦN MỀM - NHÓM 10
-- Sinh viên: Nguyễn Mạnh Quyết (20231053) & Hà Thái Bảo (20231045)
-- CƠ SỞ DỮ LIỆU MYSQL CHUẨN HÓA 3NF (DDL SCRIPT)
-- ====================================================================

CREATE DATABASE IF NOT EXISTS cinema_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE cinema_db;

-- 1. BẢNG VAI TRÒ (ROLES)
CREATE TABLE IF NOT EXISTS roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    description TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. BẢNG NGƯỜI DÙNG (USERS)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role_id INT NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(30),
    password_hash VARCHAR(255) NOT NULL,
    avatar VARCHAR(255) DEFAULT '/images/default-avatar.png',
    status ENUM('active', 'locked') DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. BẢNG PHIM (MOVIES)
CREATE TABLE IF NOT EXISTS movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    original_title VARCHAR(255),
    genre VARCHAR(255) NOT NULL,
    duration INT NOT NULL,
    release_date DATE NOT NULL,
    end_date DATE,
    age_rating ENUM('P', 'K', 'T13', 'T16', 'T18') DEFAULT 'P',
    director VARCHAR(255),
    cast TEXT,
    description TEXT,
    poster_url TEXT,
    banner_url TEXT,
    trailer_url TEXT,
    language VARCHAR(100) DEFAULT 'Phụ đề Tiếng Việt',
    status ENUM('now_showing', 'coming_soon', 'ended') DEFAULT 'now_showing',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. BẢNG PHÒNG CHIẾU (ROOMS)
CREATE TABLE IF NOT EXISTS rooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_name VARCHAR(100) NOT NULL,
    screen_type ENUM('2D', '3D', 'IMAX', '4DX') DEFAULT '2D',
    total_rows INT DEFAULT 7,
    seats_per_row INT DEFAULT 12,
    total_seats INT DEFAULT 84,
    status ENUM('active', 'maintenance') DEFAULT 'active'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. BẢNG GHẾ NGỒI (SEATS)
CREATE TABLE IF NOT EXISTS seats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_id INT NOT NULL,
    seat_row VARCHAR(10) NOT NULL,
    seat_number INT NOT NULL,
    seat_code VARCHAR(20) NOT NULL,
    seat_type ENUM('regular', 'vip', 'sweetbox') DEFAULT 'regular',
    price_multiplier DECIMAL(4, 2) DEFAULT 1.00,
    status ENUM('active', 'maintenance') DEFAULT 'active',
    FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE,
    UNIQUE KEY uk_room_seat (room_id, seat_row, seat_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. BẢNG SUẤT CHIẾU (SHOWTIMES)
CREATE TABLE IF NOT EXISTS showtimes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT NOT NULL,
    room_id INT NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    buffer_minutes INT DEFAULT 15,
    base_price INT DEFAULT 80000,
    status ENUM('scheduled', 'cancelled', 'completed') DEFAULT 'scheduled',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE RESTRICT,
    FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. BẢNG COMBO BẮP NƯỚC (COMBOS)
CREATE TABLE IF NOT EXISTS combos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    price INT NOT NULL,
    image_url TEXT,
    status ENUM('active', 'inactive') DEFAULT 'active'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 8. BẢNG ĐƠN ĐẶT VÉ (BOOKINGS)
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_code VARCHAR(100) UNIQUE NOT NULL,
    user_id INT,
    customer_name VARCHAR(150),
    customer_email VARCHAR(150),
    customer_phone VARCHAR(30),
    showtime_id INT NOT NULL,
    total_amount INT NOT NULL,
    discount_amount INT DEFAULT 0,
    payment_method VARCHAR(50) DEFAULT 'mbbank_qr',
    payment_status ENUM('pending', 'paid', 'failed', 'refunded') DEFAULT 'paid',
    booking_status ENUM('pending', 'confirmed', 'cancelled') DEFAULT 'confirmed',
    booking_type ENUM('online', 'pos') DEFAULT 'online',
    created_by INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (showtime_id) REFERENCES showtimes(id) ON DELETE RESTRICT,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 9. BẢNG VÉ XEM PHIM CHI TIẾT (TICKETS)
CREATE TABLE IF NOT EXISTS tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticket_code VARCHAR(100) UNIQUE NOT NULL,
    booking_id INT NOT NULL,
    showtime_id INT NOT NULL,
    seat_id INT NOT NULL,
    price INT NOT NULL,
    qr_data LONGTEXT NOT NULL,
    status ENUM('unused', 'checked_in', 'expired', 'cancelled') DEFAULT 'unused',
    checked_in_at DATETIME,
    checked_in_by INT,
    FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE,
    FOREIGN KEY (showtime_id) REFERENCES showtimes(id) ON DELETE RESTRICT,
    FOREIGN KEY (seat_id) REFERENCES seats(id) ON DELETE RESTRICT,
    FOREIGN KEY (checked_in_by) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE KEY uk_showtime_seat (showtime_id, seat_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 10. BẢNG CHI TIẾT COMBO BẮP NƯỚC THEO ĐƠN (BOOKING_COMBOS)
CREATE TABLE IF NOT EXISTS booking_combos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    combo_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price INT NOT NULL,
    total_price INT NOT NULL,
    FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE,
    FOREIGN KEY (combo_id) REFERENCES combos(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 11. BẢNG KHÓA GIỮ GHẾ TẠM THỜI (SEAT_LOCKS) - Chống Race Condition
CREATE TABLE IF NOT EXISTS seat_locks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    showtime_id INT NOT NULL,
    seat_id INT NOT NULL,
    session_id VARCHAR(100) NOT NULL,
    user_id INT,
    locked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME NOT NULL,
    FOREIGN KEY (showtime_id) REFERENCES showtimes(id) ON DELETE CASCADE,
    FOREIGN KEY (seat_id) REFERENCES seats(id) ON DELETE CASCADE,
    UNIQUE KEY uk_showtime_lock (showtime_id, seat_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 12. BẢNG CÀI ĐẶT HỆ THỐNG (SYSTEM_SETTINGS)
CREATE TABLE IF NOT EXISTS system_settings (
    `key` VARCHAR(100) PRIMARY KEY,
    value TEXT NOT NULL,
    description TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- TẠO CHỈ MỤC TỐI ƯU HIỆU NĂNG TRUY VẤN
CREATE INDEX idx_showtimes_room_time ON showtimes(room_id, start_time, end_time);
CREATE INDEX idx_showtimes_movie_time ON showtimes(movie_id, start_time);
CREATE INDEX idx_tickets_booking ON tickets(booking_id);
CREATE INDEX idx_tickets_showtime_seat ON tickets(showtime_id, seat_id);
CREATE INDEX idx_tickets_code ON tickets(ticket_code);
CREATE INDEX idx_seat_locks_expiry ON seat_locks(expires_at);
