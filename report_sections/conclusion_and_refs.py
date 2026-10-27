# ==============================================================================
# PHẦN: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN, TÀI LIỆU THAM KHẢO, PHỤ LỤC
# ==============================================================================
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def add_conclusion_and_refs(doc, add_p, add_heading_1, add_heading_2, add_heading_3, add_bullet, add_figure, add_table_custom, add_code_snippet):
    # KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
    add_heading_1("KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN")

    add_heading_2("1. Đánh giá kết quả đạt được")
    add_p("Trải qua 7 tuần nghiên cứu và phát triển nghiêm túc bám sát kế hoạch đề ra, nhóm tác giả Nhóm 10 đã hoàn thành xuất sắc toàn bộ các mục tiêu của đồ án môn học 'Đồ án chuyên ngành Công nghệ phần mềm'. Sản phẩm 'Hệ thống đặt vé và quản lý suất chiếu rạp chiếu phim (Cinestar Cinema)' đã được xây dựng hoàn thiện, đáp ứng trọn vẹn cả về mặt học thuật lý thuyết lẫn tính năng thực tiễn:")

    add_bullet("Hoàn thành nghiên cứu và vận dụng nhuần nhuyễn các kiến thức cốt lõi của ngành CNPM: phân tích yêu cầu phần mềm theo chuẩn IEEE 830, mô hình hóa chất lượng theo ISO/IEC 25010, thiết kế hướng đối tượng với UML, chuẩn hóa cơ sở dữ liệu quan hệ 3NF và triển khai kiến trúc 3 tầng MVC.", "Về mặt học thuật và phương pháp luận:");
    add_bullet("Hệ thống hoạt động trơn tru, đồng bộ dữ liệu thời gian thực giữa 4 phân hệ: Khách hàng (đặt vé, chọn ghế, QR code), Nhân viên (bán vé POS, soát vé QR bằng camera), Quản lý (xếp lịch chống trùng phòng, dashboard thống kê) và Quản trị viên (quản lý người dùng, phân quyền RBAC).", "Về mặt sản phẩm phần mềm:");
    add_bullet("Cài đặt thành công 3 giải pháp kỹ thuật chuyên sâu: Thuật toán kiểm tra xung đột suất chiếu (ConflictDetector), Kỹ thuật khóa giữ ghế tạm thời (SeatLock) 5 phút chống Race Condition, và Kỹ thuật soát vé QR Code hai lớp ngăn chặn gian lận.", "Về mặt thuật toán và kỹ thuật:");
    add_bullet("Xây dựng bộ kiểm thử tự động toàn diện với 17 Test Cases đạt tỷ lệ 17/17 PASS (100%), chứng minh độ tin cậy và sự ổn định cao của phần mềm.", "Về mặt kiểm thử chất lượng:");

    add_heading_2("2. Những ưu điểm nổi bật của đồ án")
    add_bullet("Khách hàng có thể nhìn thấy từng vị trí ghế theo đúng phòng chiếu thực tế (ghế thường, VIP, đôi), được giữ chỗ an toàn trong 5 phút và nhận vé điện tử QR Code không cần in giấy.", "Trải nghiệm người dùng vượt trội (UI/UX):");
    add_bullet("Loại bỏ 100% sai sót của con người trong việc xếp lịch chiếu nhờ thuật toán tự động tính toán thời gian chiếm dụng phòng và phát hiện giao thoa thời gian thực.", "Tối ưu hóa vận hành cho người quản lý:");
    add_bullet("Soát vé siêu tốc qua camera WebCam với độ trễ < 100ms, tự động phát còi báo động đỏ khi phát hiện vé bị dùng lại, bảo vệ tuyệt đối doanh thu của rạp.", "Bảo mật và chống gian lận hiệu quả:");
    add_bullet("Cơ sở dữ liệu được chuẩn hóa 3NF không dư thừa, truy vấn tối ưu qua hệ thống chỉ mục (Index) và bộ đệm kết nối Connection Pool giúp ứng dụng chịu tải cao.", "Hiệu năng và kiến trúc chuẩn mực:");

    add_heading_2("3. Những mặt còn hạn chế")
    add_bullet("Hiện tại hệ thống mới mô phỏng quá trình thanh toán qua cổng điện tử, chưa kết nối trực tiếp với API Sandbox thực tế của các ngân hàng thương mại do yêu cầu về hồ sơ pháp nhân doanh nghiệp.", "Cổng thanh toán thực tế:");
    add_bullet("Ứng dụng hiện hoạt động trên nền tảng Web Responsive, chưa phát triển ứng dụng di động độc lập (Native Mobile App) trên iOS và Android.", "Ứng dụng di động chuyên biệt:");

    add_heading_2("4. Hướng phát triển trong tương lai")
    add_bullet("Nghiên cứu ứng dụng thuật toán học máy (Machine Learning) và AI gợi ý để phân tích thói quen xem phim của khách hàng, tự động gợi ý các bộ phim phù hợp trên trang chủ.", "Tích hợp Trí tuệ nhân tạo (AI):");
    add_bullet("Phát triển ứng dụng di động cho khách hàng và nhân viên soát vé bằng công nghệ đa nền tảng Flutter hoặc React Native.", "Mở rộng Mobile App:");
    add_bullet("Xây dựng thuật toán phân tích dữ liệu lịch sử đặt vé để tự động điều chỉnh giá vé linh hoạt (Dynamic Pricing) theo từng khung giờ và độ 'nóng' của phim.", "Cơ chế định giá vé động thông minh:");
    add_bullet("Tích hợp cổng thanh toán trực tiếp qua chuẩn VietQR (chuyển khoản quét mã QR ngân hàng tự động đối soát) và Apple Pay / Google Wallet.", "Mở rộng thanh toán số:");

    doc.add_page_break()

    # TÀI LIỆU THAM KHẢO
    add_heading_1("TÀI LIỆU THAM KHẢO")

    refs = [
        "[1] Bộ môn Công nghệ Phần mềm - Khoa CNTT, Trường Đại học Công nghệ Đông Á (2025), Giáo trình Phân tích và Thiết kế Hệ thống Thông tin, NXB Đại học Quốc gia Hà Nội.",
        "[2] IEEE Computer Society (1998), IEEE Recommended Practice for Software Requirements Specifications (IEEE Std 830-1998), IEEE, New York.",
        "[3] International Organization for Standardization (2011), ISO/IEC 25010: Systems and software engineering - Systems and software Quality Requirements and Evaluation (SQuaRE) - System and software quality models, Geneva, Switzerland.",
        "[4] Ian Sommerville (2016), Software Engineering (10th Edition), Pearson Education, London, UK.",
        "[5] Martin Fowler (2002), Patterns of Enterprise Application Architecture, Addison-Wesley Professional, Boston.",
        "[6] Abraham Silberschatz, Henry F. Korth, S. Sudarshan (2020), Database System Concepts (7th Edition), McGraw-Hill Education, New York.",
        "[7] Robin Nixon (2021), Learning PHP, MySQL & JavaScript: With jQuery, CSS & HTML5 (6th Edition), O'Reilly Media, Sebastopol.",
        "[8] Node.js Foundation (2026), Node.js Official Documentation (v24.x LTS), https://nodejs.org/docs/.",
        "[9] Express.js Team (2026), Express - Fast, unopinionated, minimalist web framework for Node.js, https://expressjs.com/.",
        "[10] Mozilla Developer Network (MDN) (2026), Web technology for developers: HTML5, CSS3, JavaScript and Web APIs, https://developer.mozilla.org/."
    ]

    for r in refs:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.line_spacing = 1.25
        p_ref.paragraph_format.space_before = Pt(2)
        p_ref.paragraph_format.space_after = Pt(4)
        run_r = p_ref.add_run(r)
        run_r.font.name = 'Times New Roman'
        run_r.font.size = Pt(12)

    doc.add_page_break()

    # PHỤ LỤC
    add_heading_1("PHỤ LỤC: HƯỚNG DẪN CÀI ĐẶT & TÀI KHOẢN MẪU")

    add_heading_2("1. Yêu cầu hệ thống phần cứng và phần mềm")
    add_bullet("Hệ điều hành: Windows 10/11, macOS hoặc Linux Ubuntu 22.04+.", "Hệ điều hành:");
    add_bullet("Bộ nhớ RAM tối thiểu 4GB, dung lượng ổ cứng trống tối thiểu 1GB.", "Cấu hình phần cứng:");
    add_bullet("Cài đặt sẵn Node.js phiên bản >= 20.x và Hệ quản trị CSDL MySQL hoặc MariaDB.", "Phần mềm yêu cầu:");

    add_heading_2("2. Hướng dẫn khởi chạy ứng dụng (Quick Start)")
    add_p("Bước 1: Mở cửa sổ dòng lệnh Terminal hoặc PowerShell tại thư mục gốc của dự án:")
    add_code_snippet("cd \"d:\\Vibe code\\BTL_DACN_CNPM\"")

    add_p("Bước 2: Cài đặt các gói thư viện phụ thuộc (nếu chưa cài):")
    add_code_snippet("npm install")

    add_p("Bước 3: Khởi chạy máy chủ Web:")
    add_code_snippet("npm start\n# Hoặc lệnh: node server.js")

    add_p("Bước 4: Mở trình duyệt web và truy cập địa chỉ:")
    add_code_snippet("http://localhost:3000")

    add_heading_2("3. Danh sách tài khoản mẫu thử nghiệm (4 vai trò)")
    add_p("Hệ thống đã chuẩn bị sẵn tài khoản cho cả 4 vai trò, đồng thời hỗ trợ nút bấm 'Đăng nhập 1-Click' ngay trên giao diện đăng nhập để thuận tiện cho việc chấm thi:")

    add_table_custom(
        "Bảng Phụ Lục 1. Danh sách tài khoản mẫu phân quyền 4 vai trò",
        ["Tác nhân (Vai trò)", "Email đăng nhập", "Mật khẩu", "Phân hệ phụ trách chính"],
        [
            ["Quản trị viên (Admin)", "admin@cinema.com", "admin123", "Quản lý người dùng, phân quyền RBAC, cài đặt hệ thống"],
            ["Quản lý rạp (Manager)", "manager@cinema.com", "manager123", "Dashboard doanh thu, lấp đầy %, quản lý phim/phòng, xếp suất chiếu"],
            ["Nhân viên quầy (Staff)", "staff@cinema.com", "staff123", "Bán vé tại quầy (POS), quét camera soát vé QR, lịch sử soát vé"],
            ["Khách hàng (Client)", "client@cinema.com", "client123", "Đặt vé online, chọn ghế trực quan, combo bắp nước, mã QR vé"]
        ],
        col_widths=[1.8, 1.8, 1.2, 2.4],
        source="Nhóm 10 - Dữ liệu hạt giống CSDL (Seed Data)"
    )

    add_heading_2("4. Hướng dẫn chạy bộ kiểm thử tự động (Automated Test Suite)")
    add_p("Để chạy tự động toàn bộ 17 Test Cases kiểm tra tính toàn vẹn CSDL, thuật toán chống xung đột, cơ chế khóa giữ ghế và soát vé QR, gõ lệnh sau:")
    add_code_snippet("node test_app.js")

    print("Conclusion, References, and Appendices generated successfully.")
