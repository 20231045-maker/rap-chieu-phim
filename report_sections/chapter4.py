# ==============================================================================
# CHƯƠNG IV. PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG
# ==============================================================================
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def add_chapter_4(doc, add_p, add_heading_1, add_heading_2, add_heading_3, add_bullet, add_figure, add_table_custom, add_code_snippet):
    add_heading_1("CHƯƠNG IV. PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG")

    # 4.1. PHÂN TÍCH HỆ THỐNG
    add_heading_2("4.1. Phân tích hệ thống")

    add_heading_3("4.1.1. Xác định Use Case cho các tác nhân")
    add_p("Dựa trên quá trình phân tích 20 yêu cầu chức năng (FR01 - FR20) và 4 nhóm tác nhân ở Chương II, nhóm nghiên cứu đã mô hình hóa hành vi hệ thống thành các Ca sử dụng (Use Cases). Hệ thống bao gồm 4 nhóm ca sử dụng tương ứng với 4 tác nhân:")
    add_bullet("UC01 (Đăng nhập / Đăng ký), UC02 (Tra cứu phim), UC03 (Xem lịch chiếu & phòng), UC04 (Chọn ghế ngồi & Khóa 5p), UC05 (Chọn combo bắp nước), UC06 (Thanh toán trực tuyến), UC07 (Xem vé điện tử & Mã QR), UC08 (Quản lý lịch sử vé).", "Nhóm Ca sử dụng của Khách hàng (Client):");
    add_bullet("UC09 (Bán vé tại quầy POS), UC10 (In vé & Hóa đơn quầy), UC11 (Quét mã QR soát vé), UC12 (Xác thực vé & Cảnh báo gian lận), UC13 (Xem lịch sử soát vé của ca trực).", "Nhóm Ca sử dụng của Nhân viên quầy (Staff):");
    add_bullet("UC14 (Quản lý danh mục phim), UC15 (Quản lý phòng chiếu & Ma trận ghế), UC16 (Lập lịch suất chiếu mới), UC17 (Kiểm tra xung đột suất chiếu), UC18 (Quản lý bảng giá vé & Combo F&B), UC19 (Dashboard thống kê doanh thu & Tỷ lệ lấp đầy rạp %).", "Nhóm Ca sử dụng của Quản lý rạp (Manager):");
    add_bullet("UC20 (Quản lý tài khoản người dùng), UC21 (Phân quyền vai trò RBAC), UC22 (Cấu hình tham số vận hành rạp), UC23 (Giám sát nhật ký kiểm toán Audit Logs).", "Nhóm Ca sử dụng của Quản trị viên (Admin):");

    add_heading_3("4.1.2. Mô tả Use Case chi tiết (Use Case Specifications)")
    add_p("Nhằm cung cấp góc nhìn tường minh về luồng xử lý và tương tác giữa người dùng với hệ thống, nhóm tiến hành lập bảng đặc tả chi tiết cho 8 Use Case nghiệp vụ quan trọng nhất:")

    # UC01
    add_table_custom(
        "Bảng 4.1. Đặc tả Use Case UC01: Đăng ký / Đăng nhập tài khoản",
        ["Mục thông tin", "Nội dung đặc tả Use Case"],
        [
            ["Tên Use Case", "UC01: Đăng ký / Đăng nhập tài khoản"],
            ["Tác nhân chính", "Khách hàng (Client), Nhân viên (Staff), Quản lý (Manager), Quản trị viên (Admin)"],
            ["Mục đích", "Xác thực danh tính người dùng và cấp phiên làm việc tương ứng với vai trò trong hệ thống."],
            ["Tiền điều kiện", "Người dùng đã truy cập vào hệ thống website."],
            ["Hậu điều kiện", "Người dùng được cấp phiên đăng nhập an toàn, hệ thống lưu session và chuyển hướng đúng trang."],
            ["Luồng sự kiện chính (Basic Flow)", 
             "1. Người dùng bấm vào nút 'Đăng nhập' trên thanh điều hướng.\n"
             "2. Hệ thống hiển thị form nhập Email và Mật khẩu.\n"
             "3. Người dùng nhập thông tin và bấm 'Đăng nhập'.\n"
             "4. Hệ thống kiểm tra email trong CSDL, băm mật khẩu và đối soát qua hàm bcrypt.compare().\n"
             "5. Hệ thống khởi tạo Session lưu user_id và role_name.\n"
             "6. Hệ thống điều hướng: Admin -> /admin/users, Manager -> /manager/dashboard, Staff -> /staff/scan-ticket, Client -> /."],
            ["Luồng sự kiện thay thế (Alternative Flow)", 
             "4a. Nếu email không tồn tại hoặc mật khẩu sai, hệ thống báo lỗi 'Email hoặc mật khẩu không chính xác' và giữ lại form nhập."],
            ["Luồng ngoại lệ (Exception Flow)", 
             "4b. Nếu tài khoản có trạng thái 'locked' (bị khóa), hệ thống từ chối đăng nhập và thông báo 'Tài khoản của bạn đã bị khóa bởi Quản trị viên'."]
        ],
        col_widths=[1.8, 4.5],
        source="Nhóm 10 - Tài liệu đặc tả Use Case chi tiết"
    )

    # UC02
    add_table_custom(
        "Bảng 4.2. Đặc tả Use Case UC02: Đặt vé trực tuyến & Chọn ghế ngồi",
        ["Mục thông tin", "Nội dung đặc tả Use Case"],
        [
            ["Tên Use Case", "UC02: Đặt vé trực tuyến & Chọn ghế ngồi"],
            ["Tác nhân chính", "Khách hàng (Client)"],
            ["Mục đích", "Cho phép khách hàng lựa chọn vị trí ghế ngồi trực quan và giữ chỗ trong 5 phút."],
            ["Tiền điều kiện", "Khách hàng đã chọn một suất chiếu cụ thể của một bộ phim."],
            ["Hậu điều kiện", "Ghế được chuyển sang trạng thái tạm khóa trong bảng SeatLock, tạo hóa đơn tạm."],
            ["Luồng sự kiện chính (Basic Flow)", 
             "1. Khách hàng bấm chọn suất chiếu mong muốn.\n"
             "2. Hệ thống tải sơ đồ ma trận ghế của phòng chiếu tương ứng (hiển thị rõ ghế thường, VIP, đôi).\n"
             "3. Khách hàng click chọn vị trí ghế mong muốn (ví dụ: D07, D08).\n"
             "4. Khách hàng bấm nút 'TIẾP TỤC >>'.\n"
             "5. Hệ thống kiểm tra tình trạng ghế; gọi hàm SeatLock.lockSeats() cấp khóa trong 5 phút.\n"
             "6. Hệ thống chuyển hướng sang bước chọn combo bắp nước và trang thanh toán kèm đồng hồ đếm ngược 5:00."],
            ["Luồng sự kiện thay thế (Alternative Flow)", 
             "5a. Nếu ghế đã bị khách hàng khác đặt mua hoặc đang bị giữ chỗ, hệ thống đổi màu ghế sang xám/đỏ và báo lỗi 'Ghế đã có người chọn, vui lòng chọn ghế khác'."],
            ["Luồng ngoại lệ (Exception Flow)", 
             "6a. Nếu hết thời gian 5 phút mà khách hàng chưa hoàn tất thanh toán, hệ thống tự động xóa bản ghi trong bảng SeatLock và thông báo hết hạn phiên giữ ghế."]
        ],
        col_widths=[1.8, 4.5],
        source="Nhóm 10 - Tài liệu đặc tả Use Case chi tiết"
    )

    # UC03
    add_table_custom(
        "Bảng 4.3. Đặc tả Use Case UC03: Bán vé trực tiếp tại quầy POS",
        ["Mục thông tin", "Nội dung đặc tả Use Case"],
        [
            ["Tên Use Case", "UC03: Bán vé trực tiếp tại quầy POS"],
            ["Tác nhân chính", "Nhân viên quầy (Staff)"],
            ["Mục đích", "Giúp nhân viên phục vụ khách mua vé tại rạp nhanh chóng, thu tiền và in vé."],
            ["Tiền điều kiện", "Nhân viên đã đăng nhập tài khoản có vai trò 'staff'."],
            ["Hậu điều kiện", "Đơn hàng và vé được tạo trong CSDL với booking_type='pos', in vé thành công."],
            ["Luồng sự kiện chính (Basic Flow)", 
             "1. Nhân viên mở giao diện Bán vé POS (/staff/pos).\n"
             "2. Chọn phim và suất chiếu theo yêu cầu của khách hàng.\n"
             "3. Chọn vị trí ghế ngồi và số lượng combo bắp nước (nếu có).\n"
             "4. Nhập họ tên, số điện thoại khách hàng (không bắt buộc) và chọn phương thức 'Tiền mặt' hoặc 'Quẹt thẻ'.\n"
             "5. Bấm 'Xác nhận bán vé & Xuất hóa đơn'.\n"
             "6. Hệ thống lưu Booking, sinh các bản ghi Ticket, cập nhật doanh thu và mở lệnh in vé."]
        ],
        col_widths=[1.8, 4.5],
        source="Nhóm 10 - Tài liệu đặc tả Use Case chi tiết"
    )

    # UC04
    add_table_custom(
        "Bảng 4.4. Đặc tả Use Case UC04: Quét mã QR Soát vé & Báo gian lận",
        ["Mục thông tin", "Nội dung đặc tả Use Case"],
        [
            ["Tên Use Case", "UC04: Quét mã QR Soát vé & Báo gian lận"],
            ["Tác nhân chính", "Nhân viên quầy (Staff)"],
            ["Mục đích", "Kiểm soát ra vào phòng chiếu bằng mã QR và ngăn chặn hành vi sử dụng vé lậu."],
            ["Tiền điều kiện", "Nhân viên đăng nhập vào phân hệ Soát vé (/staff/scan-ticket) và kích hoạt camera."],
            ["Hậu điều kiện", "Vé hợp lệ được đổi trạng thái sang 'checked_in', lưu thời gian và ID nhân viên."],
            ["Luồng sự kiện chính (Basic Flow)", 
             "1. Khách hàng đưa mã QR vé xem phim trước camera hoặc súng quét.\n"
             "2. Module HTML5-QRCode tự động nhận diện và trích xuất chuỗi mã vé.\n"
             "3. Hệ thống gửi mã vé tới API /staff/tickets/checkin.\n"
             "4. Hệ thống kiểm tra bảng tickets: Vé tồn tại và trạng thái là 'unused'.\n"
             "5. Cập nhật trạng thái vé thành 'checked_in', lưu checked_in_at=NOW() và checked_in_by=staff_id.\n"
             "6. Hiển thị thông báo XANH: 'SOÁT VÉ THÀNH CÔNG! Ghế: D07, Phim: Dune'."],
            ["Luồng sự kiện thay thế (Alternative Flow)", 
             "4a. Nếu mã vé không tồn tại, hiển thị cảnh báo: 'VÉ KHÔNG HỢP LỆ HOẶC VÉ GIẢ MẠO!'."],
            ["Luồng ngoại lệ (Exception Flow)", 
             "4b. Nếu vé có trạng thái 'checked_in' (đã dùng), hệ thống lập tức phát còi báo động ĐỎ: 'CẢNH BÁO GIAN LẬN: Vé đã được sử dụng vào lúc... bởi nhân viên...!'."]
        ],
        col_widths=[1.8, 4.5],
        source="Nhóm 10 - Tài liệu đặc tả Use Case chi tiết"
    )

    # UC05
    add_table_custom(
        "Bảng 4.5. Đặc tả Use Case UC05: Lập lịch suất chiếu chống trùng giờ",
        ["Mục thông tin", "Nội dung đặc tả Use Case"],
        [
            ["Tên Use Case", "UC05: Lập lịch suất chiếu chống trùng giờ"],
            ["Tác nhân chính", "Quản lý rạp (Manager)"],
            ["Mục đích", "Tạo suất chiếu mới cho phim trong phòng chiếu mà không bị xung đột giờ với các suất khác."],
            ["Tiền điều kiện", "Quản lý đăng nhập vào phân hệ /manager/showtimes/create."],
            ["Hậu điều kiện", "Suất chiếu mới được ghi nhận an toàn vào CSDL và đồng bộ lên lịch bán vé."],
            ["Luồng sự kiện chính (Basic Flow)", 
             "1. Quản lý chọn Phim chiếu, Phòng chiếu, Ngày chiếu và Giờ bắt đầu (start_time).\n"
             "2. Hệ thống tự động tính thời gian kết thúc: end_time = start_time + duration + 15p dọn phòng.\n"
             "3. Hệ thống gọi AJAX tới ConflictDetector để kiểm tra xung đột thời gian thực.\n"
             "4. Không phát hiện xung đột: Hiển thị thông báo xanh 'Phòng chiếu trống, khung giờ an toàn'.\n"
             "5. Quản lý nhập giá vé cơ bản (base_price) và ấn 'Lưu suất chiếu'.\n"
             "6. Hệ thống thêm bản ghi vào bảng showtimes và chuyển hướng về danh sách suất chiếu."],
            ["Luồng sự kiện thay thế (Alternative Flow)", 
             "4a. Nếu có giao thoa thời gian với suất chiếu khác trong cùng phòng: Hệ thống khóa nút Lưu và hiển thị cảnh báo đỏ chi tiết: '⚠️ XUNG ĐỘT! Phòng đã có lịch chiếu phim [Tên phim] từ [Giờ bắt đầu] đến [Giờ kết thúc]'."],
            ["Luồng ngoại lệ (Exception Flow)", 
             "1a. Nếu thời gian bắt đầu được chọn trong quá khứ, hệ thống báo lỗi không cho phép."]
        ],
        col_widths=[1.8, 4.5],
        source="Nhóm 10 - Tài liệu đặc tả Use Case chi tiết"
    )

    # UC06, UC07, UC08 tóm tắt
    add_table_custom(
        "Bảng 4.6. Đặc tả Use Case UC06: Quản lý danh mục phim chiếu rạp",
        ["Mục thông tin", "Nội dung đặc tả Use Case"],
        [
            ["Tên Use Case", "UC06: Quản lý danh mục phim chiếu rạp"],
            ["Tác nhân chính", "Quản lý rạp (Manager)"],
            ["Mục đích", "Thêm phim mới, cập nhật thông tin phim, tải lên poster và quản lý trạng thái phát hành."],
            ["Tiền điều kiện", "Người dùng đăng nhập với quyền Manager hoặc Admin."],
            ["Luồng chính", "1. Quản lý truy cập /manager/movies.\n2. Bấm 'Thêm phim mới'.\n3. Nhập tiêu đề, thể loại, thời lượng, phân loại tuổi, đạo diễn, tóm tắt, link trailer YouTube và upload ảnh poster.\n4. Chọn trạng thái: Đang chiếu (now_showing) hoặc Sắp chiếu (coming_soon).\n5. Bấm Lưu: Dữ liệu được ghi vào bảng movies."]
        ],
        col_widths=[1.8, 4.5],
        source="Nhóm 10 - Tài liệu đặc tả Use Case chi tiết"
    )

    add_table_custom(
        "Bảng 4.7. Đặc tả Use Case UC07: Quản lý phòng chiếu & Cấu hình ghế",
        ["Mục thông tin", "Nội dung đặc tả Use Case"],
        [
            ["Tên Use Case", "UC07: Quản lý phòng chiếu & Cấu hình ghế"],
            ["Tác nhân chính", "Quản lý rạp (Manager)"],
            ["Mục đích", "Quản lý thông số kỹ thuật phòng chiếu và trạng thái hoạt động của từng vị trí ghế."],
            ["Tiền điều kiện", "Người dùng đăng nhập với quyền Manager."],
            ["Luồng chính", "1. Quản lý truy cập /manager/rooms.\n2. Chọn một phòng để xem chi tiết sơ đồ ma trận ghế.\n3. Nhấp chọn vị trí ghế bị hỏng hoặc cần bảo trì để đổi trạng thái sang 'maintenance'.\n4. Ghế bảo trì sẽ tự động bị vô hiệu hóa trên giao diện đặt vé của khách hàng."]
        ],
        col_widths=[1.8, 4.5],
        source="Nhóm 10 - Tài liệu đặc tả Use Case chi tiết"
    )

    add_table_custom(
        "Bảng 4.8. Đặc tả Use Case UC08: Thống kê doanh thu & Tỷ lệ lấp đầy",
        ["Mục thông tin", "Nội dung đặc tả Use Case"],
        [
            ["Tên Use Case", "UC08: Thống kê doanh thu & Tỷ lệ lấp đầy rạp"],
            ["Tác nhân chính", "Quản lý rạp (Manager)"],
            ["Mục đích", "Theo dõi sức khỏe tài chính và hiệu quả sử dụng ghế ngồi của rạp theo thời gian thực."],
            ["Tiền điều kiện", "Quản lý đăng nhập vào phân hệ /manager/dashboard."],
            ["Luồng chính", "1. Hệ thống truy vấn tổng doanh thu từ bảng bookings (payment_status='paid').\n2. Tính toán Tỷ lệ lấp đầy rạp: Occupancy Rate (%) = (Tổng vé đã bán / Tổng ghế khả dụng của các suất) * 100.\n3. Trực quan hóa dữ liệu qua biểu đồ Chart.js doanh thu 7 ngày gần nhất.\n4. Bảng thống kê top 5 phim có doanh thu và tỷ lệ lấp đầy cao nhất."]
        ],
        col_widths=[1.8, 4.5],
        source="Nhóm 10 - Tài liệu đặc tả Use Case chi tiết"
    )

    # 4.1.3. BIỂU ĐỒ PHÂN CẤP CHỨC NĂNG (FDD)
    add_heading_3("4.1.3. Biểu đồ phân cấp chức năng (FDD - Functional Decomposition Diagram)")
    add_p("Biểu đồ phân cấp chức năng (FDD) mô tả cấu trúc phân rã có thứ bậc của toàn bộ hệ thống từ mục tiêu cấp cao nhất xuống các chức năng cụ thể của từng phân hệ. Toàn bộ biểu đồ được thiết kế trên Draw.io với các đường nét vuông góc, thẳng tắp, không nét cong và không màu sắc theo đúng quy chuẩn học thuật:")

    add_figure("report_assets/images/drawio_fdd.png", 
               "Hình 4.1. Biểu đồ phân cấp chức năng hệ thống (FDD - Draw.io)",
               source="Nhóm 10 - Thiết kế bằng Draw.io", width_inches=6.2)

    # 4.1.4. BIỂU ĐỒ USE CASE
    add_heading_3("4.1.4. Biểu đồ Use Case (Tổng quát & Phân rã 4 tác nhân)")
    add_p("Bộ biểu đồ Use Case thể hiện ranh giới hệ thống, các tác nhân bên ngoài và các ca sử dụng tương ứng. Dưới đây là biểu đồ tổng quát và 4 biểu đồ phân rã chi tiết cho từng tác nhân:")

    add_figure("report_assets/images/drawio_usecase_tong_quat.png",
               "Hình 4.2. Biểu đồ Use Case tổng quát hệ thống rạp chiếu phim (Draw.io)",
               source="Nhóm 10 - Thiết kế bằng Draw.io", width_inches=6.2)

    add_figure("report_assets/images/drawio_usecase_khach_hang.png",
               "Hình 4.3. Biểu đồ Use Case phân rã phân hệ Khách hàng (Draw.io)",
               source="Nhóm 10 - Thiết kế bằng Draw.io", width_inches=6.0)

    add_figure("report_assets/images/drawio_usecase_nhan_vien.png",
               "Hình 4.4. Biểu đồ Use Case phân rã phân hệ Nhân viên quầy (Draw.io)",
               source="Nhóm 10 - Thiết kế bằng Draw.io", width_inches=6.0)

    add_figure("report_assets/images/drawio_usecase_quan_ly.png",
               "Hình 4.5. Biểu đồ Use Case phân rã phân hệ Quản lý rạp (Draw.io)",
               source="Nhóm 10 - Thiết kế bằng Draw.io", width_inches=6.0)

    add_figure("report_assets/images/drawio_usecase_quan_tri.png",
               "Hình 4.6. Biểu đồ Use Case phân rã phân hệ Quản trị viên (Draw.io)",
               source="Nhóm 10 - Thiết kế bằng Draw.io", width_inches=6.0)

    # 4.1.5. BIỂU ĐỒ HOẠT ĐỘNG (ACTIVITY DIAGRAMS)
    add_heading_3("4.1.5. Biểu đồ hoạt động (Activity Diagrams)")
    add_p("Biểu đồ hoạt động mô tả luồng công việc logic, các điểm rẽ nhánh điều kiện và sự phối hợp giữa người dùng và hệ thống. Bộ biểu đồ được vẽ bằng PlantUML chuẩn monochrome, nét thẳng:")

    add_figure("report_assets/images/activity_dat_ve.png",
               "Hình 4.7. Biểu đồ hoạt động: Quy trình Đặt vé và chọn ghế của Khách hàng (PlantUML)",
               source="Nhóm 10 - Thiết kế bằng PlantUML", width_inches=5.8)

    add_figure("report_assets/images/activity_lap_suat_chieu.png",
               "Hình 4.8. Biểu đồ hoạt động: Quy trình Lập lịch suất chiếu của Manager (PlantUML)",
               source="Nhóm 10 - Thiết kế bằng PlantUML", width_inches=5.8)

    add_figure("report_assets/images/activity_soat_ve.png",
               "Hình 4.9. Biểu đồ hoạt động: Quy trình Soát vé tại quầy của Staff (PlantUML)",
               source="Nhóm 10 - Thiết kế bằng PlantUML", width_inches=5.8)

    # 4.2. THIẾT KẾ HỆ THỐNG THEO MÔ HÌNH MVC
    add_heading_2("4.2. Thiết kế hệ thống theo mô hình MVC")

    add_heading_3("4.2.1. Thiết kế hướng đối tượng và kiến trúc phân tầng MVC")
    add_p("Hệ thống được thiết kế hướng đối tượng phân tầng theo chuẩn MVC. Tầng Model ánh xạ CSDL và quy tắc nghiệp vụ; Tầng Controller tiếp nhận yêu cầu và điều hướng; Tầng Service giải quyết các bài toán tính toán độc lập:")

    add_figure("report_assets/images/class_diagram_model.png",
               "Hình 4.10. Biểu đồ lớp (Class Diagram) theo MVC: Nhóm Model và Thực thể CSDL (PlantUML)",
               source="Nhóm 10 - Thiết kế bằng PlantUML", width_inches=6.2)

    add_figure("report_assets/images/class_diagram_controller.png",
               "Hình 4.11. Biểu đồ lớp (Class Diagram) theo MVC: Nhóm Controller và Service (PlantUML)",
               source="Nhóm 10 - Thiết kế bằng PlantUML", width_inches=6.0)

    add_p("Biểu đồ tuần tự (Sequence Diagrams) thể hiện sự trao đổi thông điệp theo thời gian giữa các đối tượng trong kiến trúc MVC:")

    add_figure("report_assets/images/sequence_dat_ve.png",
               "Hình 4.12. Biểu đồ tuần tự: Quy trình Đặt vé và Thanh toán của Khách hàng (PlantUML)",
               source="Nhóm 10 - Thiết kế bằng PlantUML", width_inches=6.2)

    add_figure("report_assets/images/sequence_lap_suat_chieu.png",
               "Hình 4.13. Biểu đồ tuần tự: Quy trình Lập suất chiếu mới & Chống xung đột (PlantUML)",
               source="Nhóm 10 - Thiết kế bằng PlantUML", width_inches=6.2)

    add_figure("report_assets/images/sequence_soat_ve.png",
               "Hình 4.14. Biểu đồ tuần tự: Quy trình Soát vé QR & Cảnh báo gian lận của Staff (PlantUML)",
               source="Nhóm 10 - Thiết kế bằng PlantUML", width_inches=6.2)

    add_p("Biểu đồ chuyển trạng thái (State Machine Diagrams) mô tả vòng đời của hai đối tượng có biến đổi trạng thái phức tạp nhất trong hệ thống: Ghế ngồi (Seat) và Vé xem phim (Ticket):")

    add_figure("report_assets/images/state_ghe_ngoi.png",
               "Hình 4.15. Biểu đồ chuyển trạng thái của Ghế ngồi (Seat State Machine - PlantUML)",
               source="Nhóm 10 - Thiết kế bằng PlantUML", width_inches=5.5)

    add_figure("report_assets/images/state_ve_xem_phim.png",
               "Hình 4.16. Biểu đồ chuyển trạng thái của Vé xem phim (Ticket State Machine - PlantUML)",
               source="Nhóm 10 - Thiết kế bằng PlantUML", width_inches=5.5)

    # 4.2.2. THIẾT KẾ CƠ SỞ DỮ LIỆU
    add_heading_3("4.2.2. Thiết kế cơ sở dữ liệu chuẩn hóa 3NF có phân quyền RBAC")
    add_p("Cơ sở dữ liệu của hệ thống được chuẩn hóa triệt để đạt Dạng chuẩn 3 (Third Normal Form - 3NF). Toàn bộ các bảng không tồn tại phụ thuộc hàm bộ phận vào khóa chính và không tồn tại phụ thuộc bắc cầu qua thuộc tính không khóa. CSDL gồm 12 bảng liên kết chặt chẽ:")

    add_figure("report_assets/images/drawio_erd_database.png",
               "Hình 4.17. Sơ đồ quan hệ thực thể (ERD) chuẩn hóa 3NF có phân quyền RBAC (Draw.io)",
               source="Nhóm 10 - Thiết kế bằng Draw.io", width_inches=6.2)

    add_p("Từ điển dữ liệu (Data Dictionary) chi tiết cấu trúc của 12 bảng trong cơ sở dữ liệu:")

    # Table 4.9: roles
    add_table_custom(
        "Bảng 4.9. Cấu trúc bảng CSDL Roles (Vai trò người dùng)",
        ["Tên cột", "Kiểu dữ liệu", "Khóa", "Ràng buộc", "Mô tả ý nghĩa nghiệp vụ"],
        [
            ["id", "INTEGER", "PK", "AUTOINCREMENT", "Mã định danh duy nhất của vai trò"],
            ["name", "VARCHAR(50)", "", "UNIQUE, NOT NULL", "Tên định danh vai trò ('admin', 'manager', 'staff', 'client')"],
            ["display_name", "VARCHAR(100)", "", "NOT NULL", "Tên hiển thị tiếng Việt ('Quản trị viên', 'Khách hàng')"],
            ["description", "TEXT", "", "NULL", "Mô tả quyền hạn của vai trò"]
        ],
        col_widths=[1.2, 1.2, 0.6, 1.5, 1.8],
        source="Nhóm 10 - Từ điển dữ liệu CSDL"
    )

    # Table 4.10: users
    add_table_custom(
        "Bảng 4.10. Cấu trúc bảng CSDL Users (Tài khoản người dùng)",
        ["Tên cột", "Kiểu dữ liệu", "Khóa", "Ràng buộc", "Mô tả ý nghĩa nghiệp vụ"],
        [
            ["id", "INTEGER", "PK", "AUTOINCREMENT", "Mã định danh duy nhất của người dùng"],
            ["role_id", "INTEGER", "FK", "NOT NULL, -> roles(id)", "Vai trò của người dùng trong hệ thống"],
            ["full_name", "VARCHAR(150)", "", "NOT NULL", "Họ và tên đầy đủ của người dùng"],
            ["email", "VARCHAR(150)", "", "UNIQUE, NOT NULL", "Email đăng nhập (duy nhất trên toàn hệ thống)"],
            ["phone", "VARCHAR(20)", "", "NULL", "Số điện thoại liên hệ"],
            ["password_hash", "VARCHAR(255)", "", "NOT NULL", "Chuỗi mật khẩu băm bảo mật bằng giải thuật BCrypt"],
            ["avatar", "VARCHAR(255)", "", "DEFAULT '/images/default.png'", "Đường dẫn ảnh đại diện"],
            ["status", "VARCHAR(20)", "", "CHECK IN ('active','locked')", "Trạng thái hoạt động của tài khoản"],
            ["created_at", "DATETIME", "", "DEFAULT CURRENT_TIMESTAMP", "Thời điểm đăng ký tài khoản"]
        ],
        col_widths=[1.2, 1.2, 0.6, 1.5, 1.8],
        source="Nhóm 10 - Từ điển dữ liệu CSDL"
    )

    # Table 4.11: movies
    add_table_custom(
        "Bảng 4.11. Cấu trúc bảng CSDL Movies (Thông tin phim chiếu)",
        ["Tên cột", "Kiểu dữ liệu", "Khóa", "Ràng buộc", "Mô tả ý nghĩa nghiệp vụ"],
        [
            ["id", "INTEGER", "PK", "AUTOINCREMENT", "Mã định danh duy nhất của bộ phim"],
            ["title", "VARCHAR(255)", "", "NOT NULL", "Tiêu đề tiếng Việt của phim"],
            ["original_title", "VARCHAR(255)", "", "NULL", "Tiêu đề gốc tiếng Anh của phim"],
            ["genre", "VARCHAR(150)", "", "NOT NULL", "Thể loại phim (Hành động, Hoạt hình, Tâm lý...)"],
            ["duration", "INTEGER", "", "NOT NULL", "Thời lượng phim tính bằng phút (ví dụ: 125, 166)"],
            ["release_date", "DATE", "", "NOT NULL", "Ngày bắt đầu khởi chiếu"],
            ["end_date", "DATE", "", "NULL", "Ngày dự kiến kết thúc chiếu"],
            ["age_rating", "VARCHAR(10)", "", "CHECK ('P','K','T13','T16','T18')", "Phân loại độ tuổi khán giả theo quy định Bộ VHTTDL"],
            ["director", "VARCHAR(150)", "", "NULL", "Đạo diễn bộ phim"],
            ["cast", "TEXT", "", "NULL", "Dàn diễn viên chính tham gia đóng phim"],
            ["description", "TEXT", "", "NULL", "Tóm tắt cốt truyện phim"],
            ["poster_url", "VARCHAR(255)", "", "NULL", "Đường dẫn ảnh poster độ phân giải cao"],
            ["banner_url", "VARCHAR(255)", "", "NULL", "Đường dẫn ảnh banner màn ảnh rộng"],
            ["trailer_url", "VARCHAR(255)", "", "NULL", "Đường dẫn video trailer YouTube chính thức"],
            ["status", "VARCHAR(20)", "", "CHECK ('now_showing','coming_soon')", "Trạng thái phim đang chiếu hoặc sắp chiếu"]
        ],
        col_widths=[1.2, 1.2, 0.6, 1.5, 1.8],
        source="Nhóm 10 - Từ điển dữ liệu CSDL"
    )

    # Table 4.12: rooms
    add_table_custom(
        "Bảng 4.12. Cấu trúc bảng CSDL Rooms (Phòng chiếu phim)",
        ["Tên cột", "Kiểu dữ liệu", "Khóa", "Ràng buộc", "Mô tả ý nghĩa nghiệp vụ"],
        [
            ["id", "INTEGER", "PK", "AUTOINCREMENT", "Mã định danh phòng chiếu"],
            ["room_name", "VARCHAR(100)", "", "NOT NULL", "Tên phòng chiếu (ví dụ: CINEMA 03 (2D Atmos))"],
            ["screen_type", "VARCHAR(20)", "", "CHECK ('2D','3D','IMAX','4DX')", "Định dạng công nghệ màn hình và âm thanh"],
            ["total_rows", "INTEGER", "", "DEFAULT 7", "Số hàng ghế của phòng (A đến G hoặc H)"],
            ["seats_per_row", "INTEGER", "", "DEFAULT 12", "Số lượng ghế trên mỗi hàng (1 đến 14)"],
            ["total_seats", "INTEGER", "", "NOT NULL", "Tổng số ghế ngồi có trong phòng chiếu"],
            ["status", "VARCHAR(20)", "", "CHECK ('active','maintenance')", "Trạng thái phòng chiếu sẵn sàng hoặc đang bảo trì"]
        ],
        col_widths=[1.2, 1.2, 0.6, 1.5, 1.8],
        source="Nhóm 10 - Từ điển dữ liệu CSDL"
    )

    # Table 4.13: seats
    add_table_custom(
        "Bảng 4.13. Cấu trúc bảng CSDL Seats (Ghế ngồi trong phòng)",
        ["Tên cột", "Kiểu dữ liệu", "Khóa", "Ràng buộc", "Mô tả ý nghĩa nghiệp vụ"],
        [
            ["id", "INTEGER", "PK", "AUTOINCREMENT", "Mã định danh vị trí ghế"],
            ["room_id", "INTEGER", "FK", "NOT NULL, -> rooms(id)", "Thuộc về phòng chiếu nào"],
            ["seat_row", "VARCHAR(5)", "", "NOT NULL", "Ký tự hàng ghế ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')"],
            ["seat_number", "INTEGER", "", "NOT NULL", "Số thứ tự ghế trong hàng (1 đến 14)"],
            ["seat_code", "VARCHAR(10)", "", "NOT NULL", "Mã ghế hiển thị ('A1', 'D07', 'D08', 'H12')"],
            ["seat_type", "VARCHAR(20)", "", "CHECK ('regular','vip','sweetbox')", "Hạng ghế: thường, VIP (ở giữa), hoặc đôi Sweetbox"],
            ["price_multiplier", "REAL", "", "DEFAULT 1.0", "Hệ số nhân giá vé (Thường: 1.0, VIP: 1.25, Sweetbox: 2.2)"],
            ["status", "VARCHAR(20)", "", "CHECK ('active','maintenance')", "Ghế đang hoạt động hoặc bảo trì hư hỏng"]
        ],
        col_widths=[1.2, 1.2, 0.6, 1.5, 1.8],
        source="Nhóm 10 - Từ điển dữ liệu CSDL"
    )

    # Table 4.14: showtimes
    add_table_custom(
        "Bảng 4.14. Cấu trúc bảng CSDL Showtimes (Lịch suất chiếu)",
        ["Tên cột", "Kiểu dữ liệu", "Khóa", "Ràng buộc", "Mô tả ý nghĩa nghiệp vụ"],
        [
            ["id", "INTEGER", "PK", "AUTOINCREMENT", "Mã định danh suất chiếu"],
            ["movie_id", "INTEGER", "FK", "NOT NULL, -> movies(id)", "Bộ phim được chiếu trong suất này"],
            ["room_id", "INTEGER", "FK", "NOT NULL, -> rooms(id)", "Phòng chiếu diễn ra suất phim"],
            ["start_time", "DATETIME", "", "NOT NULL", "Thời điểm bắt đầu chiếu ('YYYY-MM-DD HH:MM:SS')"],
            ["end_time", "DATETIME", "", "NOT NULL", "Thời điểm kết thúc (đã gồm 15 phút dọn dẹp)"],
            ["buffer_minutes", "INTEGER", "", "DEFAULT 15", "Thời gian đệm vệ sinh chuẩn bị phòng chiếu"],
            ["base_price", "INTEGER", "", "DEFAULT 80000", "Giá vé cơ bản của suất chiếu (VND)"],
            ["status", "VARCHAR(20)", "", "CHECK ('scheduled','cancelled')", "Trạng thái suất chiếu đã lên lịch hoặc đã hủy"]
        ],
        col_widths=[1.2, 1.2, 0.6, 1.5, 1.8],
        source="Nhóm 10 - Từ điển dữ liệu CSDL"
    )

    # Table 4.15: combos
    add_table_custom(
        "Bảng 4.15. Cấu trúc bảng CSDL Combos (Combo bắp nước)",
        ["Tên cột", "Kiểu dữ liệu", "Khóa", "Ràng buộc", "Mô tả ý nghĩa nghiệp vụ"],
        [
            ["id", "INTEGER", "PK", "AUTOINCREMENT", "Mã định danh gói combo F&B"],
            ["name", "VARCHAR(150)", "", "NOT NULL", "Tên gói combo (ví dụ: Combo Couple, Combo Bắp Ngọt)"],
            ["description", "TEXT", "", "NULL", "Mô tả thành phần (1 Bắp phô mai + 2 Nước ngọt lớn)"],
            ["price", "INTEGER", "", "NOT NULL", "Đơn giá gói combo (VND)"],
            ["image_url", "VARCHAR(255)", "", "NULL", "Ảnh minh họa combo bắp nước"],
            ["status", "VARCHAR(20)", "", "CHECK ('active','inactive')", "Trạng thái đang kinh doanh hoặc tạm ngừng"]
        ],
        col_widths=[1.2, 1.2, 0.6, 1.5, 1.8],
        source="Nhóm 10 - Từ điển dữ liệu CSDL"
    )

    # Table 4.16: bookings
    add_table_custom(
        "Bảng 4.16. Cấu trúc bảng CSDL Bookings (Đơn đặt vé)",
        ["Tên cột", "Kiểu dữ liệu", "Khóa", "Ràng buộc", "Mô tả ý nghĩa nghiệp vụ"],
        [
            ["id", "INTEGER", "PK", "AUTOINCREMENT", "Mã định danh đơn hàng"],
            ["booking_code", "VARCHAR(50)", "", "UNIQUE, NOT NULL", "Mã đơn hàng duy nhất (ví dụ: BKG-20261013-ABC123)"],
            ["user_id", "INTEGER", "FK", "NULL, -> users(id)", "ID tài khoản đặt vé (NULL nếu mua tại quầy không tài khoản)"],
            ["customer_name", "VARCHAR(150)", "", "NULL", "Họ tên khách hàng mua vé"],
            ["customer_email", "VARCHAR(150)", "", "NULL", "Email nhận vé điện tử"],
            ["customer_phone", "VARCHAR(20)", "", "NULL", "Số điện thoại liên hệ"],
            ["showtime_id", "INTEGER", "FK", "NOT NULL, -> showtimes(id)", "Suất chiếu được đặt vé"],
            ["total_amount", "INTEGER", "", "NOT NULL", "Tổng số tiền thanh toán của đơn hàng (VND)"],
            ["payment_method", "VARCHAR(20)", "", "CHECK ('vnpay','momo','cash')", "Phương thức: VNPay, MoMo, Thẻ hoặc Tiền mặt"],
            ["payment_status", "VARCHAR(20)", "", "CHECK ('paid','pending','failed')", "Trạng thái thanh toán (đã trả, chờ xử lý, thất bại)"],
            ["booking_type", "VARCHAR(10)", "", "CHECK ('online','pos')", "Kênh đặt vé: Khách đặt qua web ('online') hoặc bán tại quầy ('pos')"],
            ["created_by", "INTEGER", "FK", "NULL, -> users(id)", "ID nhân viên bán vé nếu thực hiện tại quầy POS"],
            ["created_at", "DATETIME", "", "DEFAULT CURRENT_TIMESTAMP", "Thời điểm khởi tạo đơn hàng"]
        ],
        col_widths=[1.2, 1.2, 0.6, 1.5, 1.8],
        source="Nhóm 10 - Từ điển dữ liệu CSDL"
    )

    # Table 4.17: tickets
    add_table_custom(
        "Bảng 4.17. Cấu trúc bảng CSDL Tickets (Chi tiết vé điện tử)",
        ["Tên cột", "Kiểu dữ liệu", "Khóa", "Ràng buộc", "Mô tả ý nghĩa nghiệp vụ"],
        [
            ["id", "INTEGER", "PK", "AUTOINCREMENT", "Mã định danh vé xem phim"],
            ["ticket_code", "VARCHAR(50)", "", "UNIQUE, NOT NULL", "Mã vé duy nhất (ví dụ: TKT-20261013-D05)"],
            ["booking_id", "INTEGER", "FK", "NOT NULL, -> bookings(id)", "Thuộc về đơn đặt vé nào"],
            ["showtime_id", "INTEGER", "FK", "NOT NULL, -> showtimes(id)", "Suất chiếu của vé"],
            ["seat_id", "INTEGER", "FK", "NOT NULL, -> seats(id)", "Vị trí ghế ngồi tương ứng của vé"],
            ["price", "INTEGER", "", "NOT NULL", "Giá bán thực tế của vé sau khi nhân hệ số hạng ghế"],
            ["qr_data", "TEXT", "", "NOT NULL", "Dữ liệu chuỗi ký tự bảo mật được mã hóa trong QR Code"],
            ["status", "VARCHAR(20)", "", "CHECK ('unused','checked_in')", "Trạng thái: chưa dùng ('unused') hoặc đã soát ('checked_in')"],
            ["checked_in_at", "DATETIME", "", "NULL", "Thời điểm nhân viên quét QR soát vé vào phòng"],
            ["checked_in_by", "INTEGER", "FK", "NULL, -> users(id)", "ID của nhân viên trực tiếp thực hiện soát vé"]
        ],
        col_widths=[1.2, 1.2, 0.6, 1.5, 1.8],
        source="Nhóm 10 - Từ điển dữ liệu CSDL"
    )

    # Table 4.18: booking_combos
    add_table_custom(
        "Bảng 4.18. Cấu trúc bảng CSDL Booking_Combos (Chi tiết combo theo đơn)",
        ["Tên cột", "Kiểu dữ liệu", "Khóa", "Ràng buộc", "Mô tả ý nghĩa nghiệp vụ"],
        [
            ["id", "INTEGER", "PK", "AUTOINCREMENT", "Mã định danh chi tiết combo"],
            ["booking_id", "INTEGER", "FK", "NOT NULL, -> bookings(id)", "Mã đơn hàng liên kết"],
            ["combo_id", "INTEGER", "FK", "NOT NULL, -> combos(id)", "Gói combo bắp nước được chọn"],
            ["quantity", "INTEGER", "", "NOT NULL", "Số lượng phần combo khách hàng đặt mua"],
            ["unit_price", "INTEGER", "", "NOT NULL", "Đơn giá combo tại thời điểm đặt (VND)"],
            ["total_price", "INTEGER", "", "NOT NULL", "Thành tiền (quantity * unit_price)"]
        ],
        col_widths=[1.2, 1.2, 0.6, 1.5, 1.8],
        source="Nhóm 10 - Từ điển dữ liệu CSDL"
    )

    # Table 4.19: seat_locks
    add_table_custom(
        "Bảng 4.19. Cấu trúc bảng CSDL Seat_Locks (Khóa giữ ghế tạm thời)",
        ["Tên cột", "Kiểu dữ liệu", "Khóa", "Ràng buộc", "Mô tả ý nghĩa nghiệp vụ"],
        [
            ["id", "INTEGER", "PK", "AUTOINCREMENT", "Mã định danh khóa ghế"],
            ["showtime_id", "INTEGER", "FK", "NOT NULL, -> showtimes(id)", "Suất chiếu xảy ra việc giữ ghế"],
            ["seat_id", "INTEGER", "FK", "NOT NULL, -> seats(id)", "Vị trí ghế ngồi bị khóa"],
            ["session_id", "VARCHAR(100)", "", "NOT NULL", "Mã phiên làm việc (Session ID) của khách đang giữ ghế"],
            ["user_id", "INTEGER", "FK", "NULL, -> users(id)", "ID tài khoản khách hàng (nếu đã đăng nhập)"],
            ["locked_at", "DATETIME", "", "DEFAULT CURRENT_TIMESTAMP", "Thời điểm thiết lập khóa"],
            ["expires_at", "DATETIME", "", "NOT NULL", "Thời điểm hết hạn khóa (đúng 5 phút sau khi locked_at)"]
        ],
        col_widths=[1.2, 1.2, 0.6, 1.5, 1.8],
        source="Nhóm 10 - Từ điển dữ liệu CSDL"
    )

    # Table 4.20: system_settings
    add_table_custom(
        "Bảng 4.20. Cấu trúc bảng CSDL System_Settings (Cấu hình rạp)",
        ["Tên cột", "Kiểu dữ liệu", "Khóa", "Ràng buộc", "Mô tả ý nghĩa nghiệp vụ"],
        [
            ["key", "VARCHAR(50)", "PK", "NOT NULL", "Tên tham số cấu hình ('buffer_minutes', 'lock_minutes')"],
            ["value", "TEXT", "", "NOT NULL", "Giá trị tham số (ví dụ: '15', '5')"],
            ["description", "TEXT", "", "NULL", "Mô tả mục đích sử dụng của tham số rạp"]
        ],
        col_widths=[1.2, 1.2, 0.6, 1.5, 1.8],
        source="Nhóm 10 - Từ điển dữ liệu CSDL"
    )

    add_p("Kịch bản DDL SQL tạo bảng và ràng buộc toàn vẹn của CSDL (`database/schema.sql`):", italic=True)
    add_code_snippet("""-- Script DDL tạo cấu trúc CSDL chuẩn hóa 3NF - CINEMA STAR
CREATE TABLE IF NOT EXISTS roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    description TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role_id INT NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(20),
    password_hash VARCHAR(255) NOT NULL,
    avatar VARCHAR(255) DEFAULT '/images/default-avatar.png',
    status ENUM('active', 'locked') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticket_code VARCHAR(50) UNIQUE NOT NULL,
    booking_id INT NOT NULL,
    showtime_id INT NOT NULL,
    seat_id INT NOT NULL,
    price INT NOT NULL,
    qr_data TEXT NOT NULL,
    status ENUM('unused', 'checked_in', 'expired', 'cancelled') DEFAULT 'unused',
    checked_in_at TIMESTAMP NULL,
    checked_in_by INT NULL,
    FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE,
    FOREIGN KEY (showtime_id) REFERENCES showtimes(id) ON DELETE RESTRICT,
    FOREIGN KEY (seat_id) REFERENCES seats(id) ON DELETE RESTRICT,
    FOREIGN KEY (checked_in_by) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE(showtime_id, seat_id) -- Ràng buộc không thể bán 2 vé cho 1 ghế trong cùng suất chiếu
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Các chỉ mục tối ưu hiệu năng truy vấn
CREATE INDEX idx_showtimes_room_time ON showtimes(room_id, start_time, end_time);
CREATE INDEX idx_tickets_showtime_seat ON tickets(showtime_id, seat_id);
CREATE INDEX idx_seat_locks_expiry ON seat_locks(expires_at);""")

    # 4.2.3. THIẾT KẾ GIAO DIỆN NGƯỜI DÙNG (WIREFRAMES PHÁC THẢO)
    add_heading_3("4.2.3. Thiết kế giao diện người dùng (Wireframes phác thảo)")
    add_p("Giao diện người dùng được thiết kế dựa trên nguyên lý thiết kế công thái học (Ergonomics) và trải nghiệm người dùng hiện đại. Toàn bộ các bản phác thảo (Wireframes) được thực hiện với phong cách kỹ thuật đen trắng, sắc nét, mô tả chân thực cấu trúc các vùng chức năng của hệ thống:")

    add_heading_3("4.2.3.1. Thiết kế phác thảo Màn hình Sơ đồ chọn ghế xem phim (Seat Selection Wireframe)")
    add_p("Đây là màn hình cốt lõi nhất trong trải nghiệm đặt vé của khách hàng. Bản phác thảo được thiết kế tái hiện chuẩn xác 100% theo mẫu đặc tả kỹ thuật, bao gồm đầy đủ các khối chức năng nghiệp vụ:")
    add_bullet("Hiển thị địa chỉ truy cập chuẩn: `https://cinemabooking.vn/chon-ghe` kèm các nút điều hướng chuẩn trình duyệt.", "1. Khung cửa sổ trình duyệt (Browser Header):");
    add_bullet("Logo thương hiệu 'CINEMA STAR' nằm bên trái; hệ thống menu điều hướng chính: 'Trang chủ', 'Phim đang chiếu', 'Lịch chiếu rạp', 'Khuyến mãi', 'Giá vé' và nút 'Đăng nhập / Đăng ký'.", "2. Thanh điều hướng đầu trang (Navigation Bar):");
    add_bullet("Khung thông tin tóm tắt nằm nổi bật: 'Phim: DUNE | Phòng chiếu: CINEMA 03 (2D Atmos) | Suất: 18:45', giúp khách hàng luôn nắm rõ ngữ cảnh suất chiếu mình đang đặt vé.", "3. Thẻ thông tin suất chiếu (Showtime Context Card):");
    add_bullet("Vị trí màn chiếu được đặt ở phía trên, kèm theo đường cong thị giác hình cánh cung mô phỏng góc nhìn thực tế của khán giả hướng về màn chiếu (Screen Viewing Arc).", "4. Vùng Màn hình chiếu (Screen):");
    add_bullet("Được bố trí theo ma trận 8 hàng ghế (ký hiệu từ A đến H ở cả hai bên mép trái và phải) và 14 cột ghế mỗi hàng. Các vị trí ghế được phân loại trực quan: Ô ghế trống (ghế có thể chọn), Ô ghế có chữ [X] (ghế đã bán cho khách khác), và Ô ghế màu xám có chữ [V] (vị trí ghế đang được chọn, cụ thể là D07 và D08).", "5. Sơ đồ ma trận ghế ngồi (Seat Grid):");
    add_bullet("Giải thích rõ ràng quy ước màu sắc và ký hiệu: Ghế thường (75k), [ ] Ghế VIP (90k), [--] Sweetbox (180k), [X] Đã bán, [V] Đang chọn.", "6. Bảng chú thích loại ghế (Seat Legend):");
    add_bullet("Hiển thị thông tin tóm tắt thời gian thực: 'Ghế chọn: D07, D08 (VIP) | Tạm tính: 180.000 VNĐ | Giữ ghế: 04:32' kèm theo nút hành động nổi bật 'TIẾP TỤC >>' để chuyển sang bước thanh toán.", "7. Thanh tổng kết đơn hàng & Đồng hồ đếm ngược (Order Summary Bar):");

    add_figure("report_assets/images/wireframe_chon_ghe.png",
               "Hình 4.18. Thiết kế giao diện phác thảo: Màn hình Sơ đồ chọn ghế xem phim (Wireframe)",
               source="Nhóm 10 - Thiết kế phác thảo giao diện chuẩn xác", width_inches=6.2)

    add_heading_3("4.2.3.2. Thiết kế phác thảo Màn hình Trang chủ (Home Page Wireframe)")
    add_p("Màn hình trang chủ đón tiếp khách hàng với Banner nổi bật giới thiệu phim bom tấn đang chiếu rạp (Dune: Part Two), lời kêu gọi hành động 'ĐẶT VÉ NGAY' và lưới các thẻ phim (Movie Cards) đang chiếu kèm nút 'MUA VÉ' nhanh:")

    add_figure("report_assets/images/wireframe_trang_chu.png",
               "Hình 4.19. Thiết kế giao diện phác thảo: Màn hình Trang chủ khách hàng (Wireframe)",
               source="Nhóm 10 - Thiết kế phác thảo giao diện", width_inches=6.2)

    add_heading_3("4.2.3.3. Thiết kế phác thảo Màn hình Lập suất chiếu chống xung đột (Manager Showtimes)")
    add_p("Giao diện lập lịch suất chiếu của Quản lý rạp tích hợp form chọn Phim, Phòng chiếu, Ngày chiếu, Giờ bắt đầu, Thời gian đệm vệ sinh (15 phút) và Hộp thông báo trạng thái kiểm tra xung đột thời gian thực:")

    add_figure("report_assets/images/wireframe_lap_suat_chieu.png",
               "Hình 4.20. Thiết kế giao diện phác thảo: Màn hình Lập suất chiếu chống xung đột (Wireframe)",
               source="Nhóm 10 - Thiết kế phác thảo giao diện", width_inches=6.2)

    add_heading_3("4.2.3.4. Thiết kế phác thảo Màn hình Soát vé QR & Bán vé quầy POS (Staff Portal)")
    add_p("Giao diện của Nhân viên quầy vé chia làm hai phân vùng: Bên trái là vùng camera quét mã QR thời gian thực và ô nhập mã vé thủ công; Bên phải là bảng kết quả soát vé hiển thị thông báo hợp lệ màu xanh hoặc cảnh báo gian lận màu đỏ:")

    add_figure("report_assets/images/wireframe_soat_ve_pos.png",
               "Hình 4.21. Thiết kế giao diện phác thảo: Màn hình Soát vé QR và Bán vé quầy POS (Wireframe)",
               source="Nhóm 10 - Thiết kế phác thảo giao diện", width_inches=6.2)

    add_heading_3("4.2.3.5. Thiết kế phác thảo Màn hình Dashboard quản lý doanh thu (Manager Analytics)")
    add_p("Dashboard thống kê của Quản lý rạp gồm 4 khối chỉ số KPI hàng đầu (Doanh thu hôm nay, Vé đã bán, Tỷ lệ lấp đầy rạp 78.4%, Số suất chiếu) kết hợp biểu đồ cột doanh thu 7 ngày và biểu đồ thanh tỷ lệ lấp đầy theo phim:")

    add_figure("report_assets/images/wireframe_dashboard_manager.png",
               "Hình 4.22. Thiết kế giao diện phác thảo: Màn hình Dashboard quản lý doanh thu (Wireframe)",
               source="Nhóm 10 - Thiết kế phác thảo giao diện", width_inches=6.2)

    doc.add_page_break()
    print("Chapter 4 generated successfully.")
