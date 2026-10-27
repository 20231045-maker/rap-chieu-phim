# Script tạo các file PlantUML cho báo cáo BTL DACN CNPM
# Tuân thủ nghiêm ngặt:
# 1. skinparam monochrome true (không dùng màu)
# 2. skinparam linetype ortho (nét thẳng, không nét cong)
# 3. skinparam shadowing false (không đổ bóng)
# 4. dpi 300 (hình vẽ to, sắc nét)
# 5. Kiểm tra chính tả tiếng Việt chuẩn xác
import os
import subprocess

puml_dir = os.path.join('report_assets', 'plantuml')
os.makedirs(puml_dir, exist_ok=True)

files = {}

# 1. Activity Diagram: Dat ve & Chon ghe
files['activity_dat_ve.puml'] = """@startuml
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName "Arial"
skinparam defaultFontSize 12
skinparam linetype ortho
skinparam roundCorner 0
skinparam dpi 300

title BIỂU ĐỒ HOẠT ĐỘNG: QUY TRÌNH ĐẶT VÉ VÀ CHỌN GHẾ (KHÁCH HÀNG)

start

:Khách hàng truy cập hệ thống và chọn phim muốn xem;
:Hệ thống hiển thị danh sách cụm rạp, ngày chiếu và các suất chiếu;
:Khách hàng chọn cụm rạp và khung giờ suất chiếu phù hợp;
:Hệ thống truy vấn CSDL và kết xuất sơ đồ ghế theo phòng chiếu;
:Khách hàng chọn vị trí ghế ngồi (Thường, VIP hoặc Sweetbox);

:Gửi yêu cầu kiểm tra và khóa giữ ghế tạm thời;
if (Ghế đã bị người khác giữ hoặc đã bán?) then (Có xung đột)
  :Thông báo ghế không còn trống, yêu cầu chọn ghế khác;
  detach
else (Còn trống)
  :Hệ thống thiết lập khóa giữ ghế (SeatLock) trong 5 phút;
endif

:Khách hàng chọn combo bắp nước đi kèm (nếu có);
:Hệ thống hiển thị hóa đơn tạm tính và đồng hồ đếm ngược 5 phút;
:Khách hàng nhập thông tin liên hệ và chọn phương thức thanh toán;

if (Thực hiện thanh toán thành công trong 5 phút?) then (Thành công)
  :Hệ thống tạo đơn đặt vé (Booking) và các vé chi tiết (Ticket);
  :Hệ thống sinh mã QR Code bảo mật cho từng vé;
  :Gửi xác nhận đặt vé và vé điện tử kèm mã QR tới Khách hàng;
  :Xóa bản ghi khóa tạm thời trong bảng SeatLock;
  stop
else (Quá 5 phút hoặc Thất bại)
  :Hệ thống tự động hủy giữ chỗ và nhả ghế về trạng thái trống;
  :Thông báo giao dịch thất bại hoặc hết hạn phiên đặt vé;
  stop
endif

@enduml
"""

# 2. Activity Diagram: Lap lich suat chieu (Manager)
files['activity_lap_suat_chieu.puml'] = """@startuml
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName "Arial"
skinparam defaultFontSize 12
skinparam linetype ortho
skinparam roundCorner 0
skinparam dpi 300

title BIỂU ĐỒ HOẠT ĐỘNG: QUY TRÌNH LẬP LỊCH SUẤT CHIẾU (MANAGER)

start

:Quản lý đăng nhập vào phân hệ Manager;
:Chọn chức năng Quản lý suất chiếu;
:Chọn thêm mới suất chiếu;
:Chọn phim chiếu, phòng chiếu, ngày chiếu và giờ bắt đầu (T_start);
:Hệ thống lấy thời lượng phim (duration) và thời gian đệm vệ sinh (buffer);
:Hệ thống tính toán thời gian kết thúc (T_end = T_start + duration + buffer);

:Hệ thống gọi module ConflictDetector để kiểm tra xung đột lịch;
if (Tồn tại suất chiếu khác trong cùng phòng giao thoa khoảng [T_start, T_end]?) then (Xung đột lịch)
  :Hiển thị cảnh báo xung đột suất chiếu kèm thông tin chi tiết suất trùng;
  :Khóa nút xác nhận lưu suất chiếu;
  :Quản lý điều chỉnh lại giờ chiếu hoặc đổi phòng chiếu;
  detach
else (Hợp lệ, không trùng)
  :Hiển thị trạng thái phòng hợp lệ (sẵn sàng xếp lịch);
  :Quản lý thiết lập giá vé cơ bản và ấn Lưu suất chiếu;
  :Hệ thống lưu bản ghi mới vào bảng Showtimes;
  :Cập nhật lịch chiếu lên hệ thống bán vé toàn rạp;
  stop
endif

@enduml
"""

# 3. Activity Diagram: Soat ve tai quay (Staff)
files['activity_soat_ve.puml'] = """@startuml
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName "Arial"
skinparam defaultFontSize 12
skinparam linetype ortho
skinparam roundCorner 0
skinparam dpi 300

title BIỂU ĐỒ HOẠT ĐỘNG: QUY TRÌNH SOÁT VÉ TẠI QUẦY (STAFF)

start

:Nhân viên đăng nhập vào phân hệ Soát vé;
:Bật camera thiết bị quét mã hoặc kết nối súng quét mã vạch;
:Khách hàng xuất trình vé điện tử có mã QR trên điện thoại hoặc vé in;
:Hệ thống tiếp nhận chuỗi ký tự mã vé từ mã QR;

:Hệ thống truy vấn bảng Tickets theo mã vé;
if (Mã vé có tồn tại trong hệ thống?) then (Không tìm thấy)
  :Báo lỗi "Vé không hợp lệ hoặc vé giả mạo!";
  :Từ chối cho khách hàng vào phòng chiếu;
  stop
else (Tìm thấy vé)
  if (Trạng thái vé là gì?) then (checked_in - Đã soát trước đó)
    :Phát cảnh báo gian lận "VÉ ĐÃ ĐƯỢC SỬ DỤNG VÀO LÚC...";
    :Hiển thị thông tin nhân viên đã soát vé trước đó;
    :Từ chối cho vào phòng chiếu và xử lý gian lận;
    stop
  else (unused - Chưa sử dụng)
    :Kiểm tra thông tin suất chiếu, phòng chiếu và giờ chiếu hiện tại;
    :Cập nhật trạng thái vé thành "checked_in";
    :Ghi nhận thời gian soát vé và ID nhân viên soát vé;
    :Thông báo "Soát vé thành công - Mời khách vào phòng chiếu";
    stop
  endif
endif

@enduml
"""

# 4. Sequence Diagram: Dat ve & Thanh toan (Khach hang)
files['sequence_dat_ve.puml'] = """@startuml
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName "Arial"
skinparam defaultFontSize 12
skinparam linetype ortho
skinparam roundCorner 0
skinparam dpi 300

title BIỂU ĐỒ TUẦN TỰ: QUY TRÌNH ĐẶT VÉ VÀ THANH TOÁN (KHÁCH HÀNG)

actor "Khách hàng" as Client
boundary "Giao diện Chọn ghế" as UI_Seat
boundary "Giao diện Thanh toán" as UI_Checkout
control "BookingController" as Ctrl
entity "SeatLock" as ModelLock
entity "Booking" as ModelBooking
entity "Ticket" as ModelTicket
database "Cơ sở dữ liệu" as DB

Client -> UI_Seat: 1. Chọn ghế [D07, D08] và bấm Tiếp tục
activate UI_Seat

UI_Seat -> Ctrl: 2. POST /booking/lock-seats (showtime_id, seat_ids)
activate Ctrl

Ctrl -> ModelLock: 3. lockSeats(showtime_id, seat_ids, sessionId, 5 min)
activate ModelLock

ModelLock -> DB: 4. Kiểm tra vé đã bán (Tickets) và ghế đang khóa (SeatLocks)
activate DB
DB --> ModelLock: Kết quả kiểm tra
deactivate DB

alt Ghế đã bị giữ hoặc đã bán
    ModelLock --> Ctrl: {success: false, message: "Ghế đang bận"}
    Ctrl --> UI_Seat: Trả về lỗi xung đột ghế
    UI_Seat --> Client: Hiển thị cảnh báo ghế đã được đặt
else Ghế còn trống hợp lệ
    ModelLock -> DB: 5. INSERT INTO seat_locks (expires_at = now + 5m)
    activate DB
    DB --> ModelLock: Thành công
    deactivate DB
    ModelLock --> Ctrl: {success: true, expiresAt}
    deactivate ModelLock
    Ctrl --> UI_Seat: Phản hồi khóa ghế thành công (200 OK)
    deactivate Ctrl
    UI_Seat -> UI_Checkout: 6. Chuyển hướng sang màn hình thanh toán
    deactivate UI_Seat
    activate UI_Checkout
    UI_Checkout --> Client: Hiển thị đếm ngược 5:00 và form thanh toán
end

Client -> UI_Checkout: 7. Chọn phương thức thanh toán và ấn Xác nhận thanh toán
UI_Checkout -> Ctrl: 8. POST /booking/checkout (thông tin khách, booking data)
activate Ctrl

Ctrl -> ModelLock: 9. checkValidLock(sessionId, showtime_id)
activate ModelLock
ModelLock -> DB: Truy vấn seat_locks (expires_at > NOW())
activate DB
DB --> ModelLock: Khóa còn hiệu lực
deactivate DB
ModelLock --> Ctrl: Hợp lệ
deactivate ModelLock

Ctrl -> ModelBooking: 10. createBooking(user_id, showtime_id, amount,...)
activate ModelBooking
ModelBooking -> DB: INSERT INTO bookings
activate DB
DB --> ModelBooking: booking_id mới
deactivate DB
ModelBooking --> Ctrl: booking_id
deactivate ModelBooking

Ctrl -> ModelTicket: 11. createTickets(booking_id, seats, qr_data)
activate ModelTicket
ModelTicket -> DB: INSERT INTO tickets (status='unused', qr_data)
activate DB
DB --> ModelTicket: tickets created
deactivate DB
ModelTicket --> Ctrl: Danh sách vé điện tử
deactivate ModelTicket

Ctrl -> ModelLock: 12. releaseSession(sessionId)
activate ModelLock
ModelLock -> DB: DELETE FROM seat_locks
activate DB
DB --> ModelLock: Đã giải phóng khóa
deactivate DB
ModelLock --> Ctrl: OK
deactivate ModelLock

Ctrl --> UI_Checkout: 13. Phản hồi đặt vé thành công (booking_code, QR codes)
deactivate Ctrl
UI_Checkout --> Client: 14. Hiển thị vé điện tử kèm mã QR Code
deactivate UI_Checkout

@enduml
"""

# 5. Sequence Diagram: Lap suat chieu moi & Chong xung dot (Manager)
files['sequence_lap_suat_chieu.puml'] = """@startuml
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName "Arial"
skinparam defaultFontSize 12
skinparam linetype ortho
skinparam roundCorner 0
skinparam dpi 300

title BIỂU ĐỒ TUẦN TỰ: LẬP SUẤT CHIẾU VÀ KIỂM TRA XUNG ĐỘT (MANAGER)

actor "Quản lý (Manager)" as Mgr
boundary "Giao diện Xếp lịch" as UI_Showtime
control "ManagerController" as Ctrl
participant "ConflictDetector" as ServiceConflict
entity "Showtime" as ModelShowtime
database "Cơ sở dữ liệu" as DB

Mgr -> UI_Showtime: 1. Chọn Phim, Phòng chiếu, Ngày và Giờ bắt đầu
activate UI_Showtime

UI_Showtime -> Ctrl: 2. AJAX GET /manager/showtimes/check-conflict
activate Ctrl

Ctrl -> ServiceConflict: 3. checkConflict(roomId, startTime, duration, buffer)
activate ServiceConflict

ServiceConflict -> DB: 4. SELECT * FROM showtimes WHERE room_id = ? AND date = ?
activate DB
DB --> ServiceConflict: Danh sách suất chiếu hiện có trong phòng
deactivate DB

ServiceConflict -> ServiceConflict: 5. Tính T_end = T_start + duration + buffer\\nKiểm tra: T_new_start < T_old_end AND T_new_end > T_old_start

alt Phát hiện xung đột lịch chiếu
    ServiceConflict --> Ctrl: {hasConflict: true, conflictInfo, message}
    Ctrl --> UI_Showtime: Phản hồi xung đột (cảnh báo đỏ)
    UI_Showtime --> Mgr: Hiển thị thông báo trùng lịch, khóa nút Lưu
else Không có xung đột (Khung giờ an toàn)
    ServiceConflict --> Ctrl: {hasConflict: false, message: "Phòng trống"}
    deactivate ServiceConflict
    Ctrl --> UI_Showtime: Phản hồi hợp lệ (thông báo xanh)
    deactivate Ctrl
    UI_Showtime --> Mgr: Kích hoạt nút Lưu suất chiếu
end

Mgr -> UI_Showtime: 6. Nhập giá vé cơ bản và ấn "Lưu suất chiếu"
UI_Showtime -> Ctrl: 7. POST /manager/showtimes/create (dữ liệu suất chiếu)
activate Ctrl

Ctrl -> ServiceConflict: 8. Xác thực lại lần cuối (checkConflict)
activate ServiceConflict
ServiceConflict --> Ctrl: Xác nhận an toàn
deactivate ServiceConflict

Ctrl -> ModelShowtime: 9. createShowtime(movieId, roomId, start, end, basePrice)
activate ModelShowtime

ModelShowtime -> DB: 10. INSERT INTO showtimes (movie_id, room_id, start_time, end_time,...)
activate DB
DB --> ModelShowtime: showtime_id mới
deactivate DB

ModelShowtime --> Ctrl: Kết quả thêm mới thành công
deactivate ModelShowtime

Ctrl --> UI_Showtime: 11. Chuyển hướng về danh sách suất chiếu kèm thông báo thành công
deactivate Ctrl
UI_Showtime --> Mgr: 12. Hiển thị thông báo thêm suất chiếu thành công trên giao diện
deactivate UI_Showtime

@enduml
"""

# 6. Sequence Diagram: Soat ve QR & Canh bao gian lan (Staff)
files['sequence_soat_ve.puml'] = """@startuml
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName "Arial"
skinparam defaultFontSize 12
skinparam linetype ortho
skinparam roundCorner 0
skinparam dpi 300

title BIỂU ĐỒ TUẦN TỰ: SOÁT VÉ QR VÀ CẢNH BÁO GIAN LẬN (STAFF)

actor "Nhân viên soát vé" as Staff
boundary "Giao diện Soát vé QR" as UI_Scan
control "StaffController" as Ctrl
entity "Ticket" as ModelTicket
database "Cơ sở dữ liệu" as DB

Staff -> UI_Scan: 1. Hướng camera quét mã QR trên vé khách hàng
activate UI_Scan

UI_Scan -> Ctrl: 2. POST /staff/tickets/checkin (ticketCode: "TKT-20261013-D05")
activate Ctrl

Ctrl -> ModelTicket: 3. checkIn(ticketCode, staffUserId)
activate ModelTicket

ModelTicket -> DB: 4. SELECT * FROM tickets WHERE ticket_code = ?
activate DB
DB --> ModelTicket: Bản ghi vé tìm thấy
deactivate DB

alt Trường hợp 1: Mã vé không tồn tại trong hệ thống
    ModelTicket --> Ctrl: {success: false, status: 'not_found', message: 'Vé không hợp lệ'}
    Ctrl --> UI_Scan: Phản hồi mã lỗi vé giả mạo
    UI_Scan --> Staff: Báo động ĐỎ: "VÉ KHÔNG HỢP LỆ HOẶC VÉ GIẢ MẠO!"
else Trường hợp 2: Vé đã qua sử dụng (status == 'checked_in')
    ModelTicket --> Ctrl: {success: false, status: 'already_used', checkedInAt, staffName}
    Ctrl --> UI_Scan: Phản hồi cảnh báo gian lận
    UI_Scan --> Staff: CẢNH BÁO ĐỎ: "VÉ ĐÃ QUA SỬ DỤNG VÀO LÚC... BỞI NHÂN VIÊN...!"
else Trường hợp 3: Vé hợp lệ chưa sử dụng (status == 'unused')
    ModelTicket -> DB: 5. UPDATE tickets SET status = 'checked_in', checked_in_at = NOW(), checked_in_by = staffUserId WHERE ticket_code = ?
    activate DB
    DB --> ModelTicket: Cập nhật thành công (affectedRows = 1)
    deactivate DB
    ModelTicket --> Ctrl: {success: true, ticketInfo: {movie, room, seat, showtime}}
    deactivate ModelTicket
    Ctrl --> UI_Scan: Phản hồi soát vé thành công
    deactivate Ctrl
    UI_Scan --> Staff: THÔNG BÁO XANH: "SOÁT VÉ THÀNH CÔNG! Ghế: D05, Phim: Dune"
    deactivate UI_Scan
end

@enduml
"""

# 7. Class Diagram MVC: Model & CSDL
files['class_diagram_model.puml'] = """@startuml
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName "Arial"
skinparam defaultFontSize 11
skinparam linetype ortho
skinparam roundCorner 0
skinparam dpi 300
skinparam classAttributeIconSize 0

title BIỂU ĐỒ LỚP KIẾN TRÚC MVC - PHÂN HỆ MODEL & THỰC THỂ CSDL

class Role {
  + id: Integer
  + name: String
  + display_name: String
  + description: String
  + getAll(): List<Role>
  + getById(id): Role
}

class User {
  + id: Integer
  + role_id: Integer
  + full_name: String
  + email: String
  + phone: String
  + password_hash: String
  + status: String
  + created_at: DateTime
  + findByEmail(email): User
  + create(userData): Integer
  + update(id, userData): Boolean
  + checkPassword(plain, hash): Boolean
}

class Movie {
  + id: Integer
  + title: String
  + original_title: String
  + genre: String
  + duration: Integer
  + release_date: Date
  + age_rating: String
  + director: String
  + status: String
  + getNowShowing(): List<Movie>
  + getComingSoon(): List<Movie>
  + getById(id): Movie
  + create(movieData): Integer
  + update(id, movieData): Boolean
}

class Room {
  + id: Integer
  + room_name: String
  + screen_type: String
  + total_rows: Integer
  + seats_per_row: Integer
  + total_seats: Integer
  + status: String
  + getAll(): List<Room>
  + getById(id): Room
  + getSeats(roomId): List<Seat>
}

class Seat {
  + id: Integer
  + room_id: Integer
  + seat_row: String
  + seat_number: Integer
  + seat_code: String
  + seat_type: String
  + price_multiplier: Float
  + status: String
  + getByRoom(roomId): List<Seat>
  + updateType(seatId, type): Boolean
}

class Showtime {
  + id: Integer
  + movie_id: Integer
  + room_id: Integer
  + start_time: DateTime
  + end_time: DateTime
  + buffer_minutes: Integer
  + base_price: Integer
  + status: String
  + getByDate(date): List<Showtime>
  + getDetail(id): Showtime
  + create(showtimeData): Integer
}

class SeatLock {
  + id: Integer
  + showtime_id: Integer
  + seat_id: Integer
  + session_id: String
  + user_id: Integer
  + expires_at: DateTime
  + lockSeats(showtimeId, seatIds, sessionId, minutes): Result
  + isSeatAvailable(showtimeId, seatId): Boolean
  + releaseSession(showtimeId, sessionId): Boolean
  + cleanExpiredLocks(): Integer
}

class Booking {
  + id: Integer
  + booking_code: String
  + user_id: Integer
  + showtime_id: Integer
  + total_amount: Integer
  + payment_method: String
  + payment_status: String
  + booking_status: String
  + booking_type: String
  + create(bookingData): Integer
  + getById(id): Booking
  + getDashboardStats(): Object
}

class Ticket {
  + id: Integer
  + ticket_code: String
  + booking_id: Integer
  + showtime_id: Integer
  + seat_id: Integer
  + price: Integer
  + qr_data: String
  + status: String
  + checked_in_at: DateTime
  + checked_in_by: Integer
  + createTickets(bookingId, tickets): Boolean
  + checkIn(ticketCode, staffId): Result
  + getByBooking(bookingId): List<Ticket>
}

class Combo {
  + id: Integer
  + name: String
  + description: String
  + price: Integer
  + status: String
  + getAllActive(): List<Combo>
}

Role "1" -- "0..*" User : has
User "1" -- "0..*" Booking : places
Movie "1" -- "0..*" Showtime : schedules
Room "1" -- "0..*" Showtime : hosts
Room "1" -- "1..*" Seat : contains
Showtime "1" -- "0..*" Booking : reserves
Showtime "1" -- "0..*" SeatLock : locks
Showtime "1" -- "0..*" Ticket : issues
Seat "1" -- "0..*" SeatLock : targets
Seat "1" -- "0..*" Ticket : assigns
Booking "1" -- "1..*" Ticket : includes
Booking "0..*" -- "0..*" Combo : orders

@enduml
"""

# 8. Class Diagram MVC: Controller & Service
files['class_diagram_controller.puml'] = """@startuml
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName "Arial"
skinparam defaultFontSize 11
skinparam linetype ortho
skinparam roundCorner 0
skinparam dpi 300
skinparam classAttributeIconSize 0

title BIỂU ĐỒ LỚP KIẾN TRÚC MVC - PHÂN HỆ CONTROLLER & SERVICE

class HomeController {
  + index(req, res): void
  + pricing(req, res): void
  + about(req, res): void
}

class MovieController {
  + listMovies(req, res): void
  + movieDetail(req, res): void
}

class BookingController {
  + selectSeats(req, res): void
  + lockSeats(req, res): JSON
  + selectCombos(req, res): void
  + checkout(req, res): void
  + processPayment(req, res): void
  + ticketSuccess(req, res): void
  + myTickets(req, res): void
}

class StaffController {
  + posDashboard(req, res): void
  + posSelectSeats(req, res): void
  + posCheckout(req, res): void
  + scanTicketPage(req, res): void
  + checkInTicket(req, res): JSON
  + checkInHistory(req, res): void
}

class ManagerController {
  + dashboard(req, res): void
  + listMovies(req, res): void
  + createMovie(req, res): void
  + listRooms(req, res): void
  + roomDetail(req, res): void
  + listShowtimes(req, res): void
  + checkShowtimeConflict(req, res): JSON
  + createShowtime(req, res): void
  + revenueReports(req, res): void
}

class AdminController {
  + listUsers(req, res): void
  + createUser(req, res): void
  + updateUserRole(req, res): void
  + systemSettings(req, res): void
  + auditLogs(req, res): void
}

class ConflictDetector <<Service>> {
  + {static} checkConflict(params): Object
  + {static} isOverlapping(s1, e1, s2, e2): Boolean
}

HomeController ..> MovieController
BookingController ..> ConflictDetector : checks
ManagerController ..> ConflictDetector : invokes
StaffController ..> BookingController

@enduml
"""

# 9. State Diagram: Trang thai Ghe ngoi
files['state_ghe_ngoi.puml'] = """@startuml
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName "Arial"
skinparam defaultFontSize 12
skinparam linetype ortho
skinparam roundCorner 0
skinparam dpi 300

title BIỂU ĐỒ CHUYỂN TRẠNG THÁI CỦA GHẾ NGỒI (SEAT STATE MACHINE)

[*] --> TRONG : Khởi tạo suất chiếu mới

TRONG --> TAM_GIU : Khách hàng bấm chọn ghế\\n(Tạo SeatLock 5 phút)

TAM_GIU --> TRONG : Khách bấm bỏ chọn ghế\\nhoặc hết 5 phút chưa thanh toán

TAM_GIU --> DA_DAT : Thanh toán thành công trong 5 phút\\n(Tạo Ticket & Booking)

DA_DAT --> HOAN_TAT : Suất chiếu kết thúc

HOAN_TAT --> [*]

@enduml
"""

# 10. State Diagram: Trang thai Ve xem phim
files['state_ve_xem_phim.puml'] = """@startuml
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName "Arial"
skinparam defaultFontSize 12
skinparam linetype ortho
skinparam roundCorner 0
skinparam dpi 300

title BIỂU ĐỒ CHUYỂN TRẠNG THÁI CỦA VÉ XEM PHIM (TICKET STATE MACHINE)

[*] --> UNUSED : Thanh toán thành công (Tạo vé & cấp QR Code)

UNUSED --> CHECKED_IN : Nhân viên quét QR soát vé hợp lệ tại cửa phòng chiếu

UNUSED --> EXPIRED : Quá giờ chiếu phim mà khách không tới soát vé

UNUSED --> CANCELLED : Hủy đơn đặt vé / hoàn tiền theo chính sách rạp

CHECKED_IN --> [*] : Suất chiếu hoàn tất
EXPIRED --> [*]
CANCELLED --> [*]

@enduml
"""

for fname, code in files.items():
    filepath = os.path.join(puml_dir, fname)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(code)
    print(f"Created: {filepath}")

print("All PlantUML files successfully created!")
