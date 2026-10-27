# HỆ THỐNG ĐẶT VÉ VÀ QUẢN LÝ SUẤT CHIẾU RẠP CHIẾU PHIM (CINESTAR CINEMA)

> **HỌC PHẦN: ĐỒ ÁN CHUYÊN NGÀNH CÔNG NGHỆ PHẦN MỀM (CNPM)**  
> **Lớp tín chỉ:** Đồ án chuyên ngành CNPM-1-1-26(N05)  
> **Lớp hành chính:** DCCNTT.14.3  
> **Nhóm thực hiện:** Nhóm 10  
> **Thành viên thực hiện:**  
> 1. **Nguyễn Mạnh Quyết** - MSV: **20231053** *(Phụ trách: Phân hệ Quản lý & Quản trị viên, CSDL, Thuật toán chống xung đột)*  
> 2. **Hà Thái Bảo** - MSV: **20231045** *(Phụ trách: Phân hệ Khách hàng & Nhân viên quầy, UI/UX, Sơ đồ ghế động & Soát vé QR)*  

---

## 📌 1. TỔNG QUAN HỆ THỐNG
Dự án được xây dựng theo chuẩn kiến trúc **MVC (Model - View - Controller)** hoàn chỉnh, đáp ứng đầy đủ yêu cầu theo kế hoạch 7 tuần của Đề cương Đồ án chuyên ngành CNPM:
- **Phân quyền người dùng RBAC (Role-Based Access Control)** chặt chẽ với 4 tác nhân:
  1. **Khách hàng (Client)**: Tra cứu phim, lịch chiếu, sơ đồ ghế động, combo bắp nước, thanh toán đếm ngược 5 phút, vé điện tử QR Code.
  2. **Nhân viên (Staff)**: Bán vé tại quầy (POS Counter), Soát vé QR Code (qua Camera WebCam hoặc máy quét mã vạch), cảnh báo gian lận vé đã qua sử dụng.
  3. **Quản lý (Manager)**: Dashboard thống kê doanh thu, **tỷ lệ lấp đầy rạp (Occupancy Rate %)**, biểu đồ Chart.js, quản lý phim, quản lý phòng & cấu hình sơ đồ ghế, lập lịch suất chiếu tích hợp **Thuật toán kiểm tra xung đột suất chiếu**.
  4. **Quản trị viên (Admin)**: Quản lý người dùng, phân quyền vai trò, cài đặt hệ thống rạp (thời gian đệm vệ sinh, thời gian giữ ghế), nhật ký giao dịch toàn hệ thống.

---

## 🛠 2. CÔNG NGHỆ SỬ DỤNG
- **Backend:** Node.js (v24+), Express Framework, Session & Cookie Parser, BCrypt password hashing.
- **Database:** SQLite chuẩn hóa 3NF (sử dụng module native `node:sqlite` cực kỳ ổn định, không cần cài đặt SQL Server/MySQL cồng kềnh, tự động khởi tạo khi chạy). Kèm theo 2 file `database/schema.sql` (DDL) và `database/seed.sql` (DML) phục vụ nộp báo cáo.
- **Frontend:** EJS Template Engine, Bootstrap 5, FontAwesome 6, Chart.js, HTML5-QRCode Scanner.
- **Mã QR:** Thư viện `qrcode` sinh mã QR SVG/PNG độ phân giải cao cho từng vé điện tử.

---

## 🚀 3. HƯỚNG DẪN CÀI ĐẶT & KHỞI CHẠY (QUICK START)

### Bước 1: Khởi chạy ứng dụng
Mở terminal trong thư mục dự án và gõ:
```bash
npm start
```
*(Hoặc `node server.js`)*

### Bước 2: Truy cập trình duyệt
Mở trình duyệt web và truy cập:
👉 **[http://localhost:3000](http://localhost:3000)**

---

## 🔑 4. TÀI KHOẢN MẪU ĐĂNG NHẬP (4 VAI TRÒ)
Hệ thống đã chuẩn bị sẵn tài khoản cho cả 4 vai trò (có nút bấm Đăng Nhập 1-Click trên giao diện đăng nhập):

| Tác nhân (Vai trò) | Email đăng nhập | Mật khẩu | Chức năng chính |
| :--- | :--- | :--- | :--- |
| **Quản trị viên (Admin)** | `admin@cinema.com` | `admin123` | Quản lý tài khoản, phân quyền RBAC, cấu hình rạp, nhật ký giao dịch |
| **Quản lý rạp (Manager)** | `manager@cinema.com` | `manager123` | Dashboard doanh thu, tỷ lệ lấp đầy %, duyệt phim, phòng & ghế, xếp lịch chống xung đột |
| **Nhân viên (Staff)** | `staff@cinema.com` | `staff123` | Bán vé tại quầy (POS), Soát vé QR camera & súng quét, lịch sử soát vé |
| **Khách hàng (Client)** | `client@cinema.com` | `client123` | Đặt vé, chọn ghế trực quan, chọn combo, nhận vé điện tử QR Code |

---

## 💡 5. THUẬT TOÁN & KỸ THUẬT NỔI BẬT

### 5.1. Thuật toán kiểm tra xung đột suất chiếu (Showtime Conflict Detection Algorithm)
- **File mã nguồn:** `services/conflictDetector.js`
- **Nguyên lý:**
  Khoảng thời gian suất chiếu mới $[T_{new\_start}, T_{new\_end}]$ (trong đó $T_{new\_end} = T_{new\_start} + \text{Thời lượng phim} + \text{Thời gian đệm dọn phòng}$).
  Giao thoa với suất chiếu đã có $[T_{old\_start}, T_{old\_end}]$ trong cùng phòng chiếu khi và chỉ khi:
  $$\mathbf{T_{new\_start} < T_{old\_end} \quad \text{VÀ} \quad T_{new\_end} > T_{old\_start}}$$
- **Giao diện:** Khi Manager chọn Phim, Phòng và Giờ bắt đầu, hệ thống tự động gọi AJAX kiểm tra thời gian thực:
  - Nếu trùng: Hiển thị cảnh báo màu ĐỎ và khóa nút Lưu.
  - Nếu không trùng: Hiển thị thông báo màu XANH và cho phép lưu.

### 5.2. Kỹ thuật khóa giữ ghế tạm thời (Temporary Seat Lock Mechanism)
- **File mã nguồn:** `models/SeatLock.js`
- **Nguyên lý:** Tránh tranh chấp đồng thời (Race Condition) khi nhiều khách cùng chọn 1 ghế. Khi khách bấm tiếp tục thanh toán, ghế được khóa tạm thời trong 5 phút. Nếu hết 5 phút mà chưa thanh toán, hệ thống tự động nhả ghế để khách khác có thể đặt.

### 5.3. Vé điện tử QR Code & Chống gian lận khi soát vé
- **File mã nguồn:** `models/Ticket.js`, `controllers/StaffController.js`
- Mỗi vé sinh một mã QR duy nhất mã hóa thông tin đơn hàng và mã vé.
- Nhân viên soát vé quét QR:
  - Lần 1: Thành công, đổi trạng thái vé sang `checked_in`, lưu nhân viên và thời gian soát.
  - Lần 2 (quét lại): Báo động ĐỎ "VÉ ĐÃ ĐƯỢC SỬ DỤNG VÀO LÚC ...! CẢNH BÁO GIAN LẬN!"

---

## 🧪 6. CHẠY KIỂM THỬ TỰ ĐỘNG (AUTOMATED TEST SUITE)
Chạy bộ kiểm thử để kiểm tra toàn bộ 16 test cases:
```bash
node test_app.js
```
Kết quả kiểm thử bao gồm:
- Kiểm tra tính toàn vẹn CSDL chuẩn 3NF
- Kiểm tra thuật toán chống xung đột lịch chiếu
- Kiểm tra cơ chế khóa giữ ghế 5 phút
- Kiểm tra soát vé QR và ngăn chặn gian lận
- Kiểm tra công thức tính tỷ lệ lấp đầy rạp (%)

---

## 📁 7. CẤU TRÚC THƯ MỤC CHUẨN MVC
```
BTL_DACN_CNPM/
├── database/
│   ├── db.js                 # Kết nối SQLite native và helper truy vấn
│   ├── schema.sql            # Script DDL 3NF CSDL phục vụ báo cáo
│   ├── seed.sql              # Script DML nạp dữ liệu mẫu
│   ├── seed.js               # Runner nạp CSDL tự động
│   └── cinema.sqlite         # Database file
├── models/                   # Models tầng dữ liệu
│   ├── User.js, Movie.js, Room.js, Seat.js, Showtime.js,
│   ├── Booking.js, Ticket.js, Combo.js, SeatLock.js
├── services/                 # Tầng nghiệp vụ & thuật toán
│   └── conflictDetector.js   # Thuật toán chống xung đột suất chiếu
├── middlewares/              # Phân quyền RBAC & upload ảnh
│   ├── authMiddleware.js, uploadMiddleware.js
├── controllers/              # Bộ điều hướng theo mô hình MVC
│   ├── HomeController.js, MovieController.js, BookingController.js,
│   ├── AuthController.js, StaffController.js, ManagerController.js, AdminController.js
├── routes/                   # Định tuyến URL theo phân hệ
│   ├── clientRoutes.js, authRoutes.js, staffRoutes.js,
│   ├── managerRoutes.js, adminRoutes.js
├── views/                    # Tầng giao diện EJS
│   ├── layouts/ (header, footer, admin-header, admin-footer)
│   ├── client/ (home, movies, movie-detail, select-seats, select-combos, checkout, ticket-success, my-tickets, profile, pricing, about, 404)
│   ├── auth/ (login, register, forbidden)
│   ├── staff/ (pos, scan-ticket, history)
│   ├── manager/ (dashboard, movies, movie-form, rooms, room-detail, showtimes, showtime-create, combos, reports)
│   └── admin/ (users, user-form, settings, audit-logs)
├── public/                   # CSS, JS, Ảnh tĩnh
│   ├── css/ (style.css, admin.css)
├── server.js                 # Điểm khởi chạy ứng dụng Express
├── test_app.js               # Bộ kiểm thử tự động
└── README.md                 # Tài liệu hướng dẫn
```
