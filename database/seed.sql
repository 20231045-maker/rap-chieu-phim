-- ====================================================================
-- HỆ THỐNG ĐẶT VÉ VÀ QUẢN LÝ SUẤT CHIẾU RẠP CHIẾU PHIM
-- ĐỒ ÁN CHUYÊN NGÀNH CÔNG NGHỆ PHẦN MỀM - NHÓM 10
-- Sinh viên: Nguyễn Mạnh Quyết (20231053) & Hà Thái Bảo (20231045)
-- SCRIPT NẠP DỮ LIỆU MẪU (DML SEED DATA)
-- ====================================================================

-- 1. VAI TRÒ
INSERT OR IGNORE INTO roles (id, name, display_name, description) VALUES
(1, 'admin', 'Quản trị viên', 'Quản trị toàn bộ người dùng, quyền hạn và hệ thống'),
(2, 'manager', 'Quản lý rạp', 'Quản lý danh mục phim, phòng chiếu, suất chiếu và báo cáo doanh thu'),
(3, 'staff', 'Nhân viên rạp', 'Bán vé tại quầy (POS) và thực hiện soát vé QR Code'),
(4, 'client', 'Khách hàng', 'Đặt vé trực tuyến, chọn ghế, chọn combo và thanh toán');

-- 2. CÀI ĐẶT HỆ THỐNG
INSERT OR REPLACE INTO system_settings (key, value, description) VALUES
('cinema_name', 'CINESTAR CINEMA COMPLEX', 'Tên chuỗi rạp chiếu phim'),
('address', 'Tầng 5, Trung tâm Thương mại Vincom Plaza, Hà Nội', 'Địa chỉ rạp'),
('hotline', '1900 6868', 'Hotline hỗ trợ'),
('buffer_time', '15', 'Thời gian chuẩn bị phòng chiếu giữa 2 suất (phút)'),
('seat_lock_time', '5', 'Thời gian giữ ghế tạm thời khi thanh toán (phút)');

-- 3. COMBO BẮP NƯỚC
INSERT OR IGNORE INTO combos (id, name, description, price, image_url, status) VALUES
(1, 'Combo Solo', '1 Bắp rang bơ thơm giòn (Lớn) + 1 Coca-Cola mát lạnh (Lớn)', 75000, 'https://images.unsplash.com/photo-1578849278619-e73505e9610f?w=400&auto=format&fit=crop&q=60', 'active'),
(2, 'Combo Couple', '1 Bắp rang bơ phô mai (Lớn) + 2 Nước ngọt tự chọn (Lớn)', 99000, 'https://images.unsplash.com/photo-1585647347483-22b66260dfff?w=400&auto=format&fit=crop&q=60', 'active'),
(3, 'Combo Family Party', '2 Bắp rang bơ vị Caramel/Phô mai + 4 Nước ngọt + 1 Khoai tây chiên giòn', 179000, 'https://images.unsplash.com/photo-1505686994434-e3cc5abf1330?w=400&auto=format&fit=crop&q=60', 'active'),
(4, 'Sweetbox Romance', '1 Bắp phô mai đặc biệt + 2 Trà đào túi lọc cam sả + 1 Socola cao cấp', 129000, 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400&auto=format&fit=crop&q=60', 'active');
