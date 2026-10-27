# ==============================================================================
# CHƯƠNG II. TỔNG HỢP, PHÂN TÍCH VÀ ĐÁNH GIÁ THỰC TẾ
# Biên soạn và chuẩn hóa toàn diện theo cấu trúc file tham khảo:
# 2.1. Tổng hợp và thu thập dữ liệu
#      2.1.1. Mục tiêu khảo sát
#      2.1.2. Phương pháp khảo sát và thu thập dữ liệu
#      2.1.3. Nội dung khảo sát (Kèm Bảng tổng hợp nội dung khảo sát)
#      2.1.4. Kết quả khảo sát (Kèm Bảng tổng hợp kết quả phân tích khảo sát)
# 2.2. Phân tích dữ liệu
#      2.2.1. Người dùng (Khách vãng lai, Khách hàng, Nhân viên, Quản trị viên/Quản lý rạp + Bảng ma trận RBAC)
#      2.2.2. Yêu cầu chức năng (Đặc tả chi tiết từng chức năng nghiệp vụ)
#      2.2.3. Yêu cầu phi chức năng (12 tiêu chí chất lượng + Bảng chuẩn ISO/IEC 25010)
# ==============================================================================
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def add_chapter_2(doc, add_p, add_heading_1, add_heading_2, add_heading_3, add_bullet, add_figure, add_table_custom):
    add_heading_1("CHƯƠNG II. TỔNG HỢP, PHÂN TÍCH VÀ ĐÁNH GIÁ THỰC TẾ")

    # =========================================================================
    # 2.1. TỔNG HỢP VÀ THU THẬP DỮ LIỆU
    # =========================================================================
    add_heading_2("2.1. Tổng hợp và thu thập dữ liệu")

    add_p("Trong bối cảnh công nghệ thông tin và chuyển đổi số ngày càng phát triển mạnh mẽ, việc ứng dụng các nền tảng trực tuyến vào hoạt động kinh doanh dịch vụ giải trí đã trở thành một xu hướng tất yếu. Đặc biệt, trong ngành công nghiệp điện ảnh và chiếu phim thương mại, nhu cầu tra cứu thông tin phim, xem lịch chiếu theo thời gian thực, lựa chọn vị trí ghế ngồi trực quan và mua vé trực tuyến của khán giả ngày càng tăng cao.")

    add_p("Tuy nhiên, quá trình vận hành và quản lý tại nhiều cụm rạp chiếu phim truyền thống vẫn còn tồn tại những hạn chế đáng kể: khán giả phải trực tiếp đến rạp để xếp hàng mua vé giấy, khó hình dung góc nhìn thực tế từ ghế tới màn hình chiếu, hoặc mất nhiều thời gian chờ đợi vào các khung giờ cao điểm cuối tuần. Về phía rạp chiếu phim, công tác quản lý danh mục phim, kiểm soát phòng chiếu, xếp lịch suất chiếu thủ công (dễ gây xung đột trùng giờ), quản lý bán vé quầy, soát vé và tổng hợp báo cáo doanh thu đòi hỏi nhiều nhân lực và tiềm ẩn nguy cơ sai sót nếu chưa được hỗ trợ bằng hệ thống phần mềm chuyên nghiệp.")

    add_p("Xuất phát từ thực tế đó, nhóm thực hiện khảo sát hiện trạng và thu thập thông tin chuyên sâu nhằm xác định chính xác nhu cầu của người sử dụng (khán giả, nhân viên, quản lý, quản trị viên), tìm hiểu các quy trình nghiệp vụ rạp chiếu phim thực tế và làm cơ sở vững chắc để xây dựng 'Hệ thống đặt vé và quản lý suất chiếu rạp chiếu phim (Cinestar Cinema)' có tính ứng dụng thực tiễn cao.")

    # -------------------------------------------------------------------------
    # 2.1.1. Mục tiêu khảo sát
    # -------------------------------------------------------------------------
    add_heading_3("2.1.1. Mục tiêu khảo sát")
    add_p("Mục tiêu của quá trình khảo sát là tìm hiểu thực trạng hoạt động bán vé và quản lý vận hành tại các cụm rạp chiếu phim thương mại hiện đại (như Cinestar, CGV, Lotte Cinema, Beta Cinemas), đồng thời xác định rõ nhu cầu của khán giả, nhân viên bán vé/soát vé và người quản lý rạp đối với một hệ thống ứng dụng Web tích hợp. Thông qua quá trình khảo sát, nhóm tập trung vào 4 mục tiêu chính sau:")

    add_bullet("Khảo sát nhằm xác định những nhu cầu thường gặp của người xem phim khi tìm kiếm thông tin và mua vé xem phim: tra cứu phim đang chiếu và sắp chiếu, xem trailer và tóm tắt nội dung, lọc theo cụm rạp gần nhất, xem lịch chiếu theo ngày, tương tác trực quan với sơ đồ ghế ngồi của phòng chiếu, đặt combo bắp nước, áp dụng mã ưu đãi, thực hiện thanh toán trực tuyến an toàn và nhận vé điện tử kèm mã QR Code bảo mật để vào phòng chiếu không cần vé giấy.", "Thứ nhất, tìm hiểu nhu cầu của khách hàng (khán giả):");
    add_bullet("Khảo sát quy trình quản lý danh mục phim chiếu rạp, thông số kỹ thuật phòng chiếu (2D, 3D, IMAX Laser, Dolby Atmos), cấu hình ma trận ghế ngồi (ghế thường, VIP, đôi sweetbox) và chính sách giá vé linh hoạt. Đặc biệt, tìm hiểu quy trình lập lịch suất chiếu, tính toán thời gian chiếm dụng phòng (thời lượng phim cộng thời gian đệm vệ sinh), quy trình bán vé tại quầy (POS), quy trình soát vé vào phòng và nhu cầu thống kê doanh thu, tỷ lệ lấp đầy rạp theo thời gian thực.", "Thứ hai, tìm hiểu quy trình quản lý và vận hành của rạp chiếu phim:");
    add_bullet("Xác định rõ những khó khăn mà khách hàng và ban quản lý rạp thường gặp phải trong mô hình vận hành cũ: tình trạng quá tải và ùn tắc tại quầy vé vào giờ cao điểm, nguy cơ mua trùng ghế do tranh chấp đồng thời (race condition), sai sót con người khi xếp lịch chiếu dẫn đến xung đột phòng chiếu, rủi ro gian lận quay vòng vé giấy do khâu soát vé thủ công, và sự chậm trễ trong việc tổng hợp số liệu doanh thu phục vụ ra quyết định kinh doanh.", "Thứ ba, xác định những hạn chế và bất cập trong quá trình vận hành thực tế:");
    add_bullet("Từ các thông tin thu thập được, nhóm xác định cụ thể các module chức năng cần thiết cho hệ thống: quản lý tài khoản và phân quyền vai trò RBAC, tra cứu phim và lịch chiếu, sơ đồ chọn ghế động kèm cơ chế khóa ghế 5 phút, đặt bắp nước, thanh toán trực tuyến, vé điện tử QR Code, bán vé tại quầy POS, quét mã QR soát vé tích hợp camera, thuật toán tự động ngăn chặn xung đột suất chiếu (Conflict Detector), Dashboard thống kê doanh thu và tỷ lệ lấp đầy rạp (Chart.js), cấu hình tham số hệ thống và nhật ký kiểm toán (Audit Logs).", "Thứ tư, xác định các yêu cầu đối với hệ thống phần mềm mới:");

    # -------------------------------------------------------------------------
    # 2.1.2. Phương pháp khảo sát và thu thập dữ liệu
    # -------------------------------------------------------------------------
    add_heading_3("2.1.2. Phương pháp khảo sát và thu thập dữ liệu")
    add_p("Để thu thập thông tin toàn diện phục vụ quá trình phân tích và xây dựng hệ thống Cinestar Cinema, nhóm sử dụng kết hợp nhiều phương pháp nghiên cứu khoa học, bao gồm: phân tích mã nguồn và kiến trúc hệ thống, nghiên cứu cơ sở dữ liệu quan hệ, phân tích giao diện và quy trình nghiệp vụ, khảo sát người dùng thực tế và tổng hợp dữ liệu.")

    add_p("a) Phương pháp phân tích mã nguồn và kiến trúc", bold=True, space_before=4, space_after=2)
    add_p("Phân tích mã nguồn và kiến trúc là phương pháp giúp nhóm nghiên cứu cách tổ chức các thành phần kỹ thuật của một ứng dụng Web MVC hiện đại:")
    add_bullet("Xem xét cách cấu hình Express Framework, cách thiết lập các tuyến đường (Routing) phân tầng: tuyến đường công khai của khách hàng (clientRoutes.js), tuyến đường xác thực (authRoutes.js), tuyến đường nghiệp vụ nhân viên (staffRoutes.js), tuyến đường điều hành của quản lý (managerRoutes.js) và tuyến đường quản trị tối cao (adminRoutes.js).", "Hệ thống định tuyến (Routing):");
    add_bullet("Tìm hiểu cách Controller tiếp nhận HTTP Request, gọi các Service độc lập (conflictDetector.js) và Model nghiệp vụ, sau đó kết xuất View qua EJS Template Engine hoặc phản hồi dữ liệu JSON qua AJAX.", "Cấu trúc Controller và Service:");
    add_bullet("Nghiên cứu cơ chế xác thực dựa trên Session và Cookie, Middleware kiểm tra quyền truy cập RBAC (authMiddleware.js), và giải thuật băm mật khẩu một chiều BCrypt với độ trễ tính toán an toàn.", "Kiểm soát xác thực và bảo mật:");

    add_p("b) Phương pháp nghiên cứu cơ sở dữ liệu", bold=True, space_before=4, space_after=2)
    add_p("Cơ sở dữ liệu là nền tảng cốt lõi quản lý toàn bộ thực thể và quan hệ nghiệp vụ của hệ thống rạp chiếu phim. Nhóm tiến hành phân tích cấu trúc CSDL quan hệ chuẩn hóa 3NF bao gồm 12 bảng dữ liệu then chốt:")
    add_bullet("roles (vai trò RBAC), users (tài khoản người dùng), movies (100 bộ phim điện ảnh phong phú), cinemas (10 cụm rạp Cinestar tại Hà Nội và TP.HCM), rooms (22 phòng chiếu 2D, 3D, IMAX Laser), seats (1.584 ghế ngồi phân bổ theo ma trận A-H, 1-14).", "Nhóm danh mục rạp:");
    add_bullet("showtimes (224 suất chiếu có buffer_minutes=15), combos (bắp nước F&B), bookings & booking_combos (đơn đặt vé), tickets (vé điện tử QR Code), seat_locks (khóa ghế tạm thời 5 phút) và system_settings (cấu hình vận hành rạp).", "Nhóm nghiệp vụ vé:");

    add_p("c) Phương pháp phân tích giao diện và quy trình nghiệp vụ", bold=True, space_before=4, space_after=2)
    add_p("Phương pháp này nhằm tìm hiểu cách người dùng tương tác với hệ thống và trình tự các bước thực hiện thao tác:")
    add_bullet("Truy cập trang chủ, tra cứu phim, chọn cụm rạp và suất chiếu, tương tác với sơ đồ ghế động, chọn combo, thanh toán với đồng hồ đếm ngược 5:00 và nhận vé điện tử kèm mã QR bảo mật.", "Khu vực Khách hàng:");
    add_bullet("Chọn suất, chọn ghế và in vé vật lý siêu tốc tại quầy POS; thao tác bật camera quét mã QR soát vé tại cửa phòng chiếu và xử lý cảnh báo vé gian lận.", "Khu vực Nhân viên quầy:");
    add_bullet("Dashboard trực quan hóa doanh thu theo 7 ngày gần nhất (Chart.js), theo dõi tỷ lệ lấp đầy rạp (%); quản lý phim, phòng, ghế; form lập lịch suất chiếu tích hợp thuật toán kiểm tra xung đột thời gian thực.", "Khu vực Quản lý rạp (Manager):");
    add_bullet("Quản lý người dùng toàn hệ thống, gán vai trò RBAC, cấu hình thời gian đệm dọn phòng và giám sát nhật ký kiểm toán giao dịch (Audit Logs).", "Khu vực Quản trị viên (Admin):");

    add_p("d) Phương pháp khảo sát người dùng", bold=True, space_before=4, space_after=2)
    add_p("Nhóm đã tiến hành khảo sát thực tế kết hợp hai hình thức: Bảng câu hỏi trực tuyến qua Google Forms (thu hút 250 lượt phản hồi từ khán giả trẻ, sinh viên và người đi làm tại Hà Nội và TP.HCM) và Phỏng vấn trực tiếp nhân viên thu ngân, nhân viên soát vé và quản lý cụm rạp Cinestar. Nội dung khảo sát hướng tới việc làm rõ: thói quen mua vé xem phim, mức độ ưu tiên giữa đặt online so với mua tại quầy, tầm quan trọng của việc tự chọn vị trí ghế trên sơ đồ trực quan, nhu cầu thanh toán nhanh qua mã QR/ví điện tử, những khó khăn thường gặp khi xếp lịch chiếu của quản lý rạp và nguy cơ thất thoát doanh thu trong khâu soát vé thủ công.")

    # -------------------------------------------------------------------------
    # 2.1.3. Nội dung khảo sát
    # -------------------------------------------------------------------------
    add_heading_3("2.1.3. Nội dung khảo sát")
    add_p("Nội dung khảo sát được cấu trúc thành các nhóm vấn đề chuyên biệt nhằm đánh giá toàn diện nhu cầu của khách hàng và yêu cầu vận hành của rạp chiếu phim:")

    add_p("Nhóm 1: Khảo sát về nhu cầu tra cứu và đặt vé xem phim", bold=True, italic=True, space_before=3, space_after=1)
    add_bullet("Khán giả thường mua vé trực tuyến qua website hay đến quầy rạp? (Câu hỏi 1). Khán giả có thường xuyên xem video trailer, đọc tóm tắt nội dung và kiểm tra độ tuổi trước khi đặt vé không? (Câu hỏi 2).", "Thói quen tìm kiếm:");
    add_bullet("Khán giả có nhu cầu lọc suất chiếu theo cụm rạp gần nhất và theo ngày cụ thể không? (Câu hỏi 3). Sơ đồ ghế trực quan và vé điện tử QR Code có ảnh hưởng lớn tới quyết định đặt vé không? (Câu hỏi 4 & 5).", "Tiện ích chọn vé:");

    add_p("Nhóm 2: Khảo sát về thông tin chi tiết phim và phòng chiếu", bold=True, italic=True, space_before=3, space_after=1)
    add_bullet("Tên phim (tiếng Việt và tên gốc), thể loại, thời lượng phút; phân loại độ tuổi theo quy định Bộ Văn hóa, Thể thao và Du lịch (P, K, T13, T16, T18); đạo diễn, diễn viên, video trailer YouTube; định dạng phòng chiếu (2D, 3D, IMAX Laser, Dolby Atmos) và giá vé.", "Dữ liệu bắt buộc:");

    add_p("Nhóm 3: Khảo sát về quy trình chọn ghế, combo bắp nước và thanh toán", bold=True, italic=True, space_before=3, space_after=1)
    add_bullet("Sơ đồ ma trận ghế rõ ràng: ghế trống, ghế đã bán [X], ghế đang chọn [V]; cơ chế khóa giữ ghế tạm thời (5 phút) bảo vệ quyền giữ chỗ; chọn thêm combo bắp nước F&B (Solo, Couple, Family); thanh toán ví điện tử (VNPay, MoMo), thẻ ngân hàng hoặc tiền mặt.", "Quy trình đặt mua:");

    add_p("Nhóm 4: Khảo sát về nhu cầu quản lý vận hành của rạp chiếu phim", bold=True, italic=True, space_before=3, space_after=1)
    add_bullet("Thêm, sửa thông tin phim, tải poster; cấu hình ma trận ghế phòng chiếu, bật/tắt bảo trì ghế; lập lịch suất chiếu tự động tính giờ kết thúc (+15 phút dọn phòng); thuật toán tự động ngăn chặn xung đột lịch chiếu; Dashboard doanh thu và tỷ lệ lấp đầy rạp (%).", "Nghiệp vụ quản lý:");

    add_p("Nhóm 5: Khảo sát về nghiệp vụ soát vé và phòng chống gian lận tại rạp", bold=True, italic=True, space_before=3, space_after=1)
    add_bullet("Quét mã QR vé qua camera thiết bị trong < 100ms; tự động đổi trạng thái sang 'checked_in'; lập tức phát còi báo động màu đỏ khi vé bị quét lại lần 2 để ngăn chặn hành vi quay vòng vé vào cửa.", "Nghiệp vụ soát vé:");

    # Bảng 2.1
    add_table_custom(
        "Bảng 2.1. Bảng tổng hợp nội dung khảo sát hệ thống rạp chiếu phim",
        ["STT", "Nội dung khảo sát", "Mục đích"],
        [
            ["1", "Nhu cầu tra cứu và đặt vé xem phim trực tuyến", "Xác định nhu cầu sử dụng website của khán giả hiện đại"],
            ["2", "Tìm kiếm, lọc phim theo rạp và suất chiếu", "Xây dựng chức năng tìm kiếm, bộ lọc theo ngày và cụm rạp"],
            ["3", "Thông tin chi tiết phim và trailer", "Xác định các trường dữ liệu đa phương tiện cần hiển thị"],
            ["4", "Sơ đồ ma trận ghế ngồi và khóa giữ ghế", "Thiết kế giao diện chọn ghế trực quan và giải thuật khóa 5 phút"],
            ["5", "Combo bắp nước và quy trình thanh toán", "Xây dựng chu trình bán hàng F&B và cổng thanh toán an toàn"],
            ["6", "Vé điện tử và sinh mã QR Code bảo mật", "Thay thế vé giấy truyền thống, hỗ trợ vé số không chạm"],
            ["7", "Bán vé trực tiếp tại quầy (POS)", "Xây dựng giao diện thao tác nhanh cho nhân viên quầy vé"],
            ["8", "Soát vé QR bằng camera và chống vé lậu", "Tự động hóa kiểm soát vào phòng chiếu và cảnh báo gian lận"],
            ["9", "Quản lý danh mục phim, phòng chiếu và ghế", "Xây dựng các chức năng quản trị danh mục rạp"],
            ["10", "Lập lịch suất chiếu và chống trùng giờ", "Cài đặt thuật toán kiểm tra xung đột lịch chiếu tự động"],
            ["11", "Thống kê doanh thu và tỷ lệ lấp đầy rạp (%)", "Cung cấp Dashboard trực quan hỗ trợ quản lý ra quyết định"],
            ["12", "Phân quyền vai trò RBAC và bảo mật", "Xác định các yêu cầu phi chức năng và kiểm soát truy cập"]
        ],
        col_widths=[0.6, 2.8, 2.9],
        align_cols=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT],
        source="Nhóm 10 - Tổng hợp nội dung phiếu khảo sát thực tế"
    )

    # -------------------------------------------------------------------------
    # 2.1.4. Kết quả khảo sát
    # -------------------------------------------------------------------------
    add_heading_3("2.1.4. Kết quả khảo sát")
    add_p("Sau khi tổng hợp dữ liệu từ phiếu khảo sát trực tuyến và các buổi làm việc thực tế, nhóm đã rút ra những kết luận quan trọng làm nền tảng xây dựng hệ thống:")

    add_bullet("84.8% khán giả ưu tiên đặt vé trực tuyến nếu hệ thống có sơ đồ chọn ghế rõ ràng và hỗ trợ vé điện tử QR Code; 92% khán giả đánh giá tính năng đếm ngược giữ ghế trong 5 phút là vô cùng cần thiết để an tâm hoàn tất thanh toán; 76% khán giả sẵn sàng đặt thêm combo bắp nước nếu được tích hợp tiện lợi ngay trên đơn vé.", "Về phía Khách hàng (khán giả):");
    add_bullet("Nhân viên quầy mong muốn giao diện bán vé POS tối giản thao tác, hỗ trợ xuất vé trong dưới 30 giây. Nhân viên soát vé đánh giá rất cao tính năng quét mã QR tự động qua camera và cơ chế cảnh báo gian lận khi vé bị quét lại, giúp loại bỏ 100% tình trạng gian lận quay vòng vé.", "Về phía Nhân viên rạp (Staff):");
    add_bullet("Quản lý rạp nhấn mạnh sự cần thiết của thuật toán tự động phát hiện xung đột lịch chiếu, bởi việc xếp lịch thủ công trên Excel trước đây rất dễ gây trùng phòng chiếu. Quản lý cũng cần Dashboard trực quan hóa doanh thu và tỷ lệ lấp đầy rạp (%) để kịp thời điều chỉnh giá vé và phân bổ suất chiếu cho các phim ăn khách.", "Về phía Quản lý (Manager) & Quản trị viên (Admin):");
    add_bullet("Hệ thống phải phân quyền chặt chẽ theo mô hình RBAC; giao diện chuẩn Responsive hiển thị mượt mà trên cả máy tính và smartphone; tốc độ tải trang < 1.5 giây; thời gian xử lý API < 200ms; và cơ sở dữ liệu phải đạt chuẩn 3NF đảm bảo không bao giờ xảy ra lỗi bán trùng ghế (Double Booking).", "Về mặt chất lượng hệ thống:");

    # Bảng 2.2
    add_table_custom(
        "Bảng 2.2. Bảng tổng hợp kết quả phân tích khảo sát",
        ["Nhóm đối tượng", "Nhu cầu xác định qua khảo sát", "Giải pháp phần mềm đề xuất"],
        [
            ["Khách vãng lai", "Tìm hiểu thông tin phim, xem lịch chiếu rạp", "Trang chủ, danh mục phim đang chiếu/sắp chiếu, xem trailer, bảng giá vé"],
            ["Khách hàng", "Chọn ghế trực quan, không bị mất chỗ, thanh toán nhanh", "Sơ đồ ghế động theo phòng, khóa ghế tạm 5 phút, combo F&B, vé QR Code"],
            ["Nhân viên quầy", "Bán vé nhanh cho khách trực tiếp tại rạp", "Giao diện POS bán vé quầy, chọn suất/ghế nhanh, in hóa đơn vé"],
            ["Nhân viên soát vé", "Kiểm soát khách vào phòng chiếu, chống vé giả", "Module quét mã QR tích hợp camera, tự động báo động đỏ khi vé đã sử dụng"],
            ["Quản lý rạp", "Xếp lịch chiếu không bị trùng, theo dõi doanh thu", "Thuật toán kiểm tra xung đột suất chiếu, Dashboard Chart.js, tỷ lệ lấp đầy %"],
            ["Quản trị viên", "Quản lý người dùng toàn hệ thống, cấu hình tham số", "Phân quyền vai trò RBAC, khóa/mở tài khoản, cài đặt thời gian đệm rạp, Audit Logs"]
        ],
        col_widths=[1.5, 2.5, 2.3],
        align_cols=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT],
        source="Nhóm 10 - Phân tích kết quả khảo sát thực tế"
    )

    # =========================================================================
    # 2.2. PHÂN TÍCH DỮ LIỆU
    # =========================================================================
    add_heading_2("2.2. Phân tích dữ liệu")

    add_p("Sau khi xác định được các nhóm dữ liệu và nghiệp vụ cần quản lý, nhóm tiến hành phân tích mối quan hệ giữa người dùng, dữ liệu và các luồng xử lý của hệ thống nhằm trả lời ba câu hỏi cốt lõi: Những đối tượng tác nhân nào tham gia tương tác với hệ thống? Mỗi đối tượng tác nhân được phép thực hiện những chức năng và quyền hạn cụ thể nào? Và hệ thống cần đáp ứng những tiêu chuẩn chất lượng kỹ thuật về hiệu năng, bảo mật, độ tin cậy và khả năng mở rộng như thế nào?")

    # -------------------------------------------------------------------------
    # 2.2.1. Người dùng (Tác nhân hệ thống)
    # -------------------------------------------------------------------------
    add_heading_3("2.2.1. Người dùng (Tác nhân hệ thống)")
    add_p("Dựa vào chức năng thực tế của hệ thống rạp chiếu phim, người dùng được phân định rõ ràng thành 4 nhóm đối tượng tác nhân:")

    add_p("a) Khách vãng lai (Guest)", bold=True, space_before=4, space_after=2)
    add_p("Khách vãng lai là người truy cập website nhưng chưa thực hiện đăng nhập tài khoản. Đối tượng này chủ yếu có nhu cầu tìm hiểu thông tin phim và tham khảo giá vé trước khi quyết định đặt vé:")
    add_bullet("Truy cập trang chủ hệ thống Cinestar Cinema; xem danh sách phim đang chiếu và phim sắp chiếu; xem banner phim bom tấn nổi bật; tìm kiếm phim theo từ khóa tiêu đề.", "Khám phá phim:");
    add_bullet("Lọc phim theo thể loại, cụm rạp hoặc ngày chiếu; sắp xếp danh sách theo thời lượng hoặc ngày khởi chiếu; xem chi tiết phim (đạo diễn, diễn viên, cốt truyện, phân loại độ tuổi P/K/T13/T16/T18); xem trailer YouTube; xem lịch chiếu tại 10 cụm rạp và bảng giá vé; thực hiện đăng ký tài khoản mới hoặc đăng nhập.", "Tra cứu và tương tác:");
    add_p("Khách vãng lai chưa có quyền chọn ghế giữ chỗ và không được truy cập vào bất kỳ khu vực quản trị nào của hệ thống.", italic=True, space_after=3)

    add_p("b) Khách hàng thành viên (Client)", bold=True, space_before=4, space_after=2)
    add_p("Khách hàng thành viên là người đã đăng nhập tài khoản khách hàng trên hệ thống để thực hiện trọn vẹn quy trình đặt vé và thanh toán trực tuyến. Ngoài toàn bộ quyền của khách vãng lai, khách hàng có thể:")
    add_bullet("Lựa chọn cụm rạp, ngày chiếu và khung giờ suất chiếu; truy cập sơ đồ ma trận ghế ngồi trực quan của phòng chiếu; chọn vị trí ghế theo nhu cầu (Regular, VIP, Sweetbox); kích hoạt cơ chế khóa giữ ghế 5 phút.", "Đặt vé & Chọn ghế:");
    add_bullet("Chọn thêm gói combo bắp nước F&B (Solo, Couple, Family); nhập mã ưu đãi; kiểm tra hóa đơn tạm tính và theo dõi đồng hồ đếm ngược 5:00; chọn thanh toán trực tuyến (VNPay, MoMo, Thẻ ngân hàng); nhận vé điện tử tức thì kèm mã QR Code bảo mật; quản lý 'Vé của tôi' và đổi mật khẩu.", "Thanh toán & Vé điện tử:");

    add_p("c) Nhân viên quầy và nhân viên soát vé (Staff)", bold=True, space_before=4, space_after=2)
    add_p("Nhân viên là người trực tiếp vận hành hoạt động hàng ngày tại cụm rạp. Sau khi đăng nhập tài khoản có vai trò 'staff', nhân viên được chuyển hướng vào phân hệ nghiệp vụ:")
    add_bullet("Truy cập phân hệ Bán vé quầy (POS Counter): chọn phim, chọn suất chiếu, chọn ghế trên sơ đồ và combo F&B theo yêu cầu khách mua trực tiếp; thu tiền mặt hoặc quẹt thẻ, in vé vật lý và xuất hóa đơn quầy trong < 30 giây.", "Bán vé quầy POS:");
    add_bullet("Truy cập phân hệ Soát vé QR (Ticket Scanner) qua camera: quét mã QR trên vé khách hàng; hệ thống tự động xác thực trong CSDL, chuyển trạng thái vé sang 'checked_in', lưu thời gian soát và mã nhân viên; lập tức cảnh báo còi báo động màu đỏ nếu phát hiện vé đã qua sử dụng; xem lịch sử đối soát vé theo ca.", "Soát vé QR & Chống gian lận:");

    add_p("d) Quản trị viên và Quản lý rạp (Admin & Manager)", bold=True, space_before=4, space_after=2)
    add_p("Quản lý rạp (Manager) và Quản trị viên hệ thống (Admin) là nhóm người dùng nắm giữ quyền hạn điều hành và giám sát toàn diện:")
    add_bullet("Quản lý danh mục 100 bộ phim (thêm, sửa, đổi trạng thái phim); quản lý 22 phòng chiếu và ma trận ghế ngồi (bật/tắt bảo trì ghế hỏng); lập lịch suất chiếu mới tích hợp thuật toán kiểm tra xung đột thời gian thực; quản lý bảng giá vé và combo F&B; theo dõi Dashboard phân tích doanh thu 7 ngày gần nhất và tỷ lệ lấp đầy rạp (%).", "Quyền hạn Quản lý rạp (Manager):");
    add_bullet("Là vai trò tối cao: quản lý toàn bộ tài khoản người dùng (thêm, sửa, khóa/mở khóa tài khoản); phân quyền vai trò RBAC (Admin, Manager, Staff, Client); cấu hình tham số rạp (thời gian đệm dọn phòng, thời gian khóa ghế); giám sát nhật ký kiểm toán giao dịch (Audit Logs) và sao lưu dữ liệu.", "Quyền hạn Quản trị viên (Admin):");

    # Bảng 2.3: Ma trận phân quyền RBAC
    add_table_custom(
        "Bảng 2.3. Ma trận phân quyền RBAC giữa các nhóm người dùng trong hệ thống",
        ["Mã phân hệ / Quyền hạn", "Guest", "Client", "Staff", "Manager", "Admin"],
        [
            ["Xem trang chủ, danh sách phim, trailer, giá vé", "Có", "Có", "Có", "Có", "Có"],
            ["Chọn ghế trực quan & Đặt vé Online (khóa 5p)", "Không", "Có", "Không", "Không", "Không"],
            ["Xem 'Vé của tôi', lưu trữ mã QR cá nhân", "Không", "Có", "Không", "Không", "Không"],
            ["Bán vé tại quầy (POS Counter) & in vé", "Không", "Không", "Có", "Có", "Có"],
            ["Quét mã QR soát vé qua camera & báo gian lận", "Không", "Không", "Có", "Có", "Có"],
            ["Xem lịch sử đối soát vé theo ca trực", "Không", "Không", "Có", "Có", "Có"],
            ["Quản lý danh mục phim & Phòng chiếu/ghế", "Không", "Không", "Không", "Có", "Có"],
            ["Lập lịch suất chiếu mới (chống trùng phòng/giờ)", "Không", "Không", "Không", "Có", "Có"],
            ["Dashboard doanh thu, tỷ lệ lấp đầy rạp %", "Không", "Không", "Không", "Có", "Có"],
            ["Quản lý người dùng & Phân quyền vai trò RBAC", "Không", "Không", "Không", "Không", "Có"],
            ["Cài đặt tham số hệ thống rạp & Audit Logs", "Không", "Không", "Không", "Không", "Có"]
        ],
        col_widths=[2.5, 0.7, 0.7, 0.7, 0.8, 0.8],
        align_cols=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER],
        source="Nhóm 10 - Ma trận phân quyền kiểm soát truy cập RBAC"
    )

    # -------------------------------------------------------------------------
    # 2.2.2. Yêu cầu chức năng
    # -------------------------------------------------------------------------
    add_heading_3("2.2.2. Yêu cầu chức năng")
    add_p("Yêu cầu chức năng mô tả chi tiết các quy trình nghiệp vụ và tác vụ xử lý mà hệ thống bắt buộc phải thực thi để đáp ứng nhu cầu của từng nhóm người dùng. Nhóm đã tiến hành đặc tả chi tiết từng chức năng nghiệp vụ cốt lõi:")

    add_p("Chức năng 1: Đăng ký tài khoản", bold=True, space_before=4, space_after=1)
    add_bullet("Người dùng nhập Họ tên, Email, Số điện thoại và Mật khẩu. Hệ thống kiểm tra định dạng email và tính duy nhất trong bảng users; mật khẩu được băm một chiều an toàn bằng BCrypt (salt rounds = 10). Nếu hợp lệ, tài khoản mới được tạo với role_id = 4 ('client') và trạng thái active. Nếu trùng email, hệ thống thông báo lỗi yêu cầu đổi email khác.", "Nghiệp vụ:");

    add_p("Chức năng 2: Đăng nhập và Phân quyền", bold=True, space_before=4, space_after=1)
    add_bullet("Người dùng nhập Email và Mật khẩu. Hệ thống truy vấn CSDL, so khớp mật khẩu bằng bcrypt.compare() và kiểm tra trạng thái active. Nếu thành công, khởi tạo Session lưu user_id, role_name và điều hướng chính xác: Admin -> /admin/users, Manager -> /manager/dashboard, Staff -> /staff/scan-ticket, Client -> /. Cung cấp tiện ích Đăng nhập 1-Click với 4 tài khoản mẫu để phục vụ chấm điểm đồ án.", "Nghiệp vụ:");

    add_p("Chức năng 3: Hiển thị danh mục phim", bold=True, space_before=4, space_after=1)
    add_bullet("Trang chủ hiển thị danh sách 100 bộ phim phân tách thành 2 nhóm rõ ràng: Phim đang chiếu (now_showing) hiển thị poster sắc nét, thời lượng, thể loại, độ tuổi và nút 'MUA VÉ'; Phim sắp chiếu (coming_soon) hiển thị ngày khởi chiếu dự kiến; Banner bom tấn nổi bật hiển thị ở đầu trang chủ tạo điểm nhấn thị giác.", "Nghiệp vụ:");

    add_p("Chức năng 4: Tìm kiếm, Lọc và Sắp xếp phim", bold=True, space_before=4, space_after=1)
    add_bullet("Tìm kiếm phim theo từ khóa SQL LIKE %keyword% trên cả tiêu đề tiếng Việt và tiêu đề gốc; lọc phim linh hoạt theo Thể loại, Cụm rạp (Hà Nội, TP.HCM), hoặc Ngày chiếu; hỗ trợ sắp xếp theo Thời lượng tăng/giảm dần hoặc theo Ngày khởi chiếu mới nhất.", "Nghiệp vụ:");

    add_p("Chức năng 5: Xem chi tiết phim và Trailer", bold=True, space_before=4, space_after=1)
    add_bullet("Kết xuất trang chi tiết đầy đủ gồm: Tên phim, poster, banner màn ảnh rộng, thời lượng phút, thể loại, đạo diễn, diễn viên, cốt truyện, phân loại độ tuổi P/K/T13/T16/T18; video trailer chính thức nhúng trực tiếp từ YouTube; bảng lịch chiếu phân bổ theo cụm rạp và các khung giờ chiếu trong ngày.", "Nghiệp vụ:");

    add_p("Chức năng 6: Xem lịch chiếu theo cụm rạp", bold=True, space_before=4, space_after=1)
    add_bullet("Khách hàng chọn cụm rạp Cinestar mong muốn (trong số 10 cụm rạp) và chọn ngày xem phim. Hệ thống truy vấn bảng showtimes kết hợp movies và rooms, nhóm suất chiếu theo định dạng phòng (2D, 3D, IMAX) và giờ chiếu (ví dụ: 18:45) để khách nhấp chọn chuyển sang màn hình chọn ghế.", "Nghiệp vụ:");

    add_p("Chức năng 7: Sơ đồ chọn ghế ngồi trực quan", bold=True, space_before=4, space_after=1)
    add_bullet("Kết xuất sơ đồ ma trận phòng chiếu: Màn hình (Screen) ở phía trên cùng kèm đường cung định hướng thị giác; ma trận 8 hàng (A-H) x 14 cột (1-14); phân biệt rõ ghế Regular (hệ số 1.0, 75k), ghế VIP ở giữa (hệ số 1.25, 90k), ghế Sweetbox ở hàng cuối (hệ số 2.2, 180k); ghế đã bán hiển thị [X] xám (vô hiệu hóa); ghế đang chọn hiển thị [V]; thanh tóm tắt thời gian thực tính tổng tiền tạm tính.", "Nghiệp vụ:");

    add_p("Chức năng 8: Khóa giữ ghế tạm thời (Temporary Seat Lock)", bold=True, space_before=4, space_after=1)
    add_bullet("Khi khách bấm 'TIẾP TỤC >>', gửi yêu cầu kèm Session ID tới API /booking/lock-seats. Hệ thống kiểm tra tính sẵn sàng trong CSDL và ghi bản ghi vào seat_locks với expires_at = NOW() + 5 phút, ngăn chặn triệt để hiện tượng tranh chấp ghế đồng thời (Race Condition). Trên giao diện hiển thị đồng hồ đếm ngược 5:00; nếu quá 5 phút chưa thanh toán thì khóa tự động giải phóng.", "Nghiệp vụ:");

    add_p("Chức năng 9: Chọn combo bắp nước (F&B)", bold=True, space_before=4, space_after=1)
    add_bullet("Cho phép chọn các gói combo bắp nước F&B (Combo Solo, Combo Couple, Combo Family); hỗ trợ nút tăng/giảm số lượng từng phần; hệ thống tự động nhân đơn giá và cộng dồn vào tổng tiền đơn hàng.", "Nghiệp vụ:");

    add_p("Chức năng 10: Đặt vé và Thanh toán trực tuyến", bold=True, space_before=4, space_after=1)
    add_bullet("Khách hàng xác nhận thông tin đơn hàng; chọn phương thức thanh toán (VNPay, MoMo, Thẻ quốc tế Visa/Mastercard, Thẻ ATM nội địa). Hệ thống thực thi Database Transaction: tạo đơn bookings, tạo các bản ghi vé tickets, xóa khóa trong seat_locks và đổi trạng thái thanh toán sang paid đảm bảo tính toàn vẹn ACID tuyệt đối.", "Nghiệp vụ:");

    add_p("Chức năng 11: Vé điện tử và Mã QR Code", bold=True, space_before=4, space_after=1)
    add_bullet("Sau khi thanh toán thành công, hệ thống sinh mã vé duy nhất định dạng TKT-[YYYYMMDD]-[MÃ_GHẾ] (ví dụ: TKT-20261013-D05); thư viện qrcode mã hóa dữ liệu vé thành hình ảnh QR Code bảo mật; khách hàng có thể lưu vé về điện thoại hoặc xem lại trong mục 'Vé của tôi' để xuất trình khi vào rạp.", "Nghiệp vụ:");

    add_p("Chức năng 12: Bán vé tại quầy (POS Counter)", bold=True, space_before=4, space_after=1)
    add_bullet("Giao diện POS tối ưu thao tác nhanh cho nhân viên: chọn phim, chọn suất, chọn ghế và combo bắp nước; nhập thông tin khách, chọn thanh toán 'Tiền mặt' hoặc 'Quẹt thẻ', in vé vật lý và xuất hóa đơn quầy trong dưới 30 giây.", "Nghiệp vụ:");

    add_p("Chức năng 13: Quét mã QR Soát vé qua Camera", bold=True, space_before=4, space_after=1)
    add_bullet("Nhân viên mở phân hệ /staff/scan-ticket trên điện thoại hoặc laptop; thư viện HTML5-QRCode Scanner tự động truy cập camera, nhận diện và trích xuất mã vé trong < 100ms; gửi chuỗi mã tới API /staff/tickets/checkin để xác thực CSDL.", "Nghiệp vụ:");

    add_p("Chức năng 14: Kiểm tra vé hợp lệ và Cảnh báo gian lận", bold=True, space_before=4, space_after=1)
    add_bullet("Vé hợp lệ chưa dùng (unused): Cập nhật trạng thái 'checked_in', lưu checked_in_at và ID nhân viên; hiển thị thông báo XANH 'SOÁT VÉ THÀNH CÔNG'. Vé đã dùng (checked_in): Phát còi báo động màu ĐỎ 'CẢNH BÁO GIAN LẬN: Vé đã sử dụng vào lúc... bởi nhân viên...!', ngăn chặn tuyệt đối quay vòng vé. Vé không tồn tại: Báo lỗi 'Vé giả mạo'.", "Nghiệp vụ:");

    add_p("Chức năng 15: Lập lịch suất chiếu và Thuật toán chống xung đột", bold=True, space_before=4, space_after=1)
    add_bullet("Quản lý chọn Phim, Phòng chiếu, Ngày chiếu và Giờ bắt đầu; hệ thống tự tính giờ kết thúc (end_time = start_time + duration + 15 phút dọn phòng). Module conflictDetector.js kiểm tra giao thoa khoảng thời gian theo công thức T_new_start < T_old_end VÀ T_new_end > T_old_start; nếu trùng lịch: khóa nút Lưu và hiển thị cảnh báo ĐỎ chi tiết tên phim và giờ suất bị trùng; nếu an toàn: báo XANH cho phép lưu.", "Nghiệp vụ:");

    add_p("Chức năng 16: Dashboard thống kê doanh thu và Tỷ lệ lấp đầy rạp", bold=True, space_before=4, space_after=1)
    add_bullet("Hiển thị 4 thẻ KPI hàng đầu: Tổng doanh thu, Số vé đã bán, Tỷ lệ lấp đầy rạp (%) và Số suất chiếu hoạt động; biểu đồ cột Chart.js trực quan hóa doanh thu 7 ngày gần nhất; công thức tính tỷ lệ lấp đầy: Occupancy Rate (%) = (Vé bán / Tổng ghế khả dụng) * 100; bảng xếp hạng top các bộ phim ăn khách nhất.", "Nghiệp vụ:");

    add_p("Chức năng 17: Quản lý người dùng và Phân quyền RBAC", bold=True, space_before=4, space_after=1)
    add_bullet("Quản trị viên có toàn quyền xem danh sách người dùng, tìm kiếm theo tên/email, tạo tài khoản mới, chỉnh sửa thông tin, đổi vai trò (Admin, Manager, Staff, Client), và khóa/mở khóa tài khoản vi phạm.", "Nghiệp vụ:");

    add_p("Chức năng 18: Cấu hình hệ thống rạp và Nhật ký kiểm toán (Audit Logs)", bold=True, space_before=4, space_after=1)
    add_bullet("Cấu hình thời gian đệm dọn phòng (buffer_minutes, mặc định 15 phút) và thời gian khóa ghế (lock_minutes, mặc định 5 phút); tự động ghi nhận nhật ký toàn bộ giao dịch đặt vé, lượt đăng nhập và thao tác quản trị phục vụ thanh tra bảo mật.", "Nghiệp vụ:");

    # -------------------------------------------------------------------------
    # 2.2.3. Yêu cầu phi chức năng
    # -------------------------------------------------------------------------
    add_heading_3("2.2.3. Yêu cầu phi chức năng")
    add_p("Yêu cầu phi chức năng mô tả các tiêu chí về chất lượng vận hành của hệ thống. Website không chỉ cần thực hiện đúng chức năng nghiệp vụ mà còn phải đảm bảo tính dễ sử dụng, hiệu năng cao, an toàn bảo mật, toàn vẹn dữ liệu và độ tin cậy tuyệt đối:")

    add_p("1. Yêu cầu về giao diện người dùng (UI):", bold=True, space_before=3, space_after=1)
    add_bullet("Giao diện thiết kế hiện đại, tông màu rạp chiếu phim chuyên nghiệp; bố trí khoa học thanh tìm kiếm, danh mục phim, nút Mua vé, sơ đồ ghế, giỏ bắp nước; menu quản trị chia tách rõ ràng giúp thao tác thuận tiện.", "Tiêu chuẩn:");

    add_p("2. Yêu cầu về tính dễ sử dụng (Usability):", bold=True, space_before=3, space_after=1)
    add_bullet("Khán giả không cần kiến thức kỹ thuật vẫn hoàn tất đặt vé trong dưới 3 phút; quy trình chuẩn: Chọn phim -> Suất chiếu -> Ghế ngồi -> Combo -> Thanh toán -> Nhận vé QR; thông báo trạng thái rõ ràng (thành công xanh, lỗi đỏ).", "Tiêu chuẩn:");

    add_p("3. Yêu cầu về hiệu năng (Performance):", bold=True, space_before=3, space_after=1)
    add_bullet("Thời gian tải trang ban đầu < 1.5 giây; thời gian phản hồi API xung đột lịch và API khóa ghế < 200ms; tốc độ nhận diện QR qua camera < 100ms; tối ưu CSDL bằng chỉ mục (Indexes) và Connection Pool (tối đa 15 kết nối), đáp ứng >= 500 người truy cập đồng thời.", "Tiêu chuẩn:");

    add_p("4. Yêu cầu về an toàn và bảo mật (Security):", bold=True, space_before=3, space_after=1)
    add_bullet("Phân quyền đa lớp qua Middleware RBAC; mật khẩu băm một chiều BCrypt (salt rounds = 10); tuân thủ OWASP Top 10: chống SQL Injection bằng truy vấn có tham số, chống XSS bằng cơ chế mã hóa ký tự EJS, chống CSRF qua Session token; mã QR vé mã hóa chuỗi nhận diện duy nhất.", "Tiêu chuẩn:");

    add_p("5. Yêu cầu về tính chính xác (Accuracy):", bold=True, space_before=3, space_after=1)
    add_bullet("Giá vé tính toán chính xác tuyệt đối: Giá cơ bản suất chiếu nhân hệ số hạng ghế (Regular 1.0, VIP 1.25, Sweetbox 2.2) cộng combo F&B; thuật toán kiểm tra xung đột tính toán chính xác thời gian chiếm dụng phòng theo phút, không bỏ sót giao thoa lịch.", "Tiêu chuẩn:");

    add_p("6. Yêu cầu về tính toàn vẹn dữ liệu (Data Integrity):", bold=True, space_before=3, space_after=1)
    add_bullet("Toàn vẹn ghế ngồi tuyệt đối: Ràng buộc duy nhất UNIQUE(showtime_id, seat_id) ngăn chặn 100% bán trùng ghế (No Double Booking); giao dịch thanh toán và tạo vé bao bọc trong Database Transactions đảm bảo thuộc tính ACID (tự động Rollback nếu lỗi).", "Tiêu chuẩn:");

    add_p("7. Yêu cầu về tính ổn định và sẵn sàng (Reliability & Availability):", bold=True, space_before=3, space_after=1)
    add_bullet("Độ sẵn sàng cao: >= 99.9% thời gian hoạt động; bắt lỗi tập trung (Error Handling Middleware) không làm sập ứng dụng; khóa ghế tự động giải phóng khi hết hạn 5 phút tránh treo ghế vĩnh viễn.", "Tiêu chuẩn:");

    add_p("8. Yêu cầu về khả năng tương thích (Compatibility):", bold=True, space_before=3, space_after=1)
    add_bullet("Chuẩn Responsive Web Design, tương thích hoàn hảo Chrome, Edge, Firefox, Safari; hiển thị tối ưu trên nhiều độ phân giải: Desktop (1920x1080), Laptop, Tablet (768px) đến Smartphone (375px).", "Tiêu chuẩn:");

    add_p("9. Yêu cầu về khả năng mở rộng (Scalability):", bold=True, space_before=3, space_after=1)
    add_bullet("Kiến trúc MVC module hóa cao cho phép dễ dàng tích hợp thêm: Cổng thanh toán VietQR/Apple Pay, Tích điểm thành viên, Native Mobile App (React Native/Flutter), và Chatbot AI tư vấn phim bằng Gemini API.", "Tiêu chuẩn:");

    add_p("10. Yêu cầu về khả năng bảo trì (Maintainability):", bold=True, space_before=3, space_after=1)
    add_bullet("Tuân thủ Clean Code, chia tách Router, Controller, Service, Model và View; đặt tên biến/hàm/bảng nhất quán bằng tiếng Anh (camelCase, snake_case); chú thích mã nguồn đầy đủ, giúp lập trình viên mới tiếp cận trong dưới 2 ngày.", "Tiêu chuẩn:");

    add_p("11. Yêu cầu về sao lưu và phục hồi dữ liệu (Backup & Recovery):", bold=True, space_before=3, space_after=1)
    add_bullet("Hỗ trợ xuất script DDL và DML sao lưu định kỳ CSDL cinema_db; khôi phục nguyên trạng hệ thống nhanh chóng khi có sự cố phần cứng hoặc phần mềm.", "Tiêu chuẩn:");

    add_p("12. Yêu cầu về độ tin cậy và phòng chống gian lận soát vé:", bold=True, space_before=3, space_after=1)
    add_bullet("Thông tin phim, lịch chiếu và trạng thái ghế đồng bộ thời gian thực 100% với CSDL máy chủ; kiểm soát vé 2 lớp tại cửa phòng chiếu ngăn chặn triệt để hành vi chụp ảnh màn hình vé quay vòng vào rạp.", "Tiêu chuẩn:");

    # Bảng 2.4: Bảng ISO/IEC 25010
    add_table_custom(
        "Bảng 2.4. Bảng đặc tả yêu cầu phi chức năng theo chuẩn quốc tế ISO/IEC 25010",
        ["Đặc tính ISO/IEC 25010", "Yêu cầu chất lượng kỹ thuật chi tiết", "Chỉ số đo lường mục tiêu (Target KPI)"],
        [
            ["1. Functional Suitability\n(Tính phù hợp chức năng)", 
             "Hệ thống đáp ứng đầy đủ và chính xác 100% các yêu cầu nghiệp vụ đặt vé, chống xung đột lịch, khóa ghế và soát vé không sai sót dữ liệu.", 
             "- Độ bao phủ tính năng: 100%\n- Tỷ lệ lỗi logic nghiệp vụ: 0%"],
            ["2. Performance Efficiency\n(Hiệu năng hoạt động)", 
             "Thời gian phản hồi trang web và API nhanh chóng; tối ưu hóa truy vấn CSDL bằng chỉ mục (Indexes); sử dụng Connection Pool quản lý kết nối.", 
             "- Tải trang ban đầu: < 1.5 giây\n- API kiểm tra xung đột / khóa ghế: < 200 ms\n- Hỗ trợ tối thiểu 500 người truy cập đồng thời"],
            ["3. Compatibility\n(Khả năng tương thích)", 
             "Giao diện chuẩn Responsive Web Design, hiển thị hoàn hảo trên các độ phân giải màn hình từ Desktop (1920x1080), Tablet đến Smartphone (375x667).", 
             "- Tương thích 100% các trình duyệt: Chrome, Edge, Firefox, Safari\n- Không vỡ layout trên thiết bị di động"],
            ["4. Usability\n(Tính khả dụng & UI/UX)", 
             "Thiết kế giao diện theo chuẩn công thái học; sơ đồ ghế phân biệt rõ ràng trạng thái (Trống, Đang chọn, Đã bán); quy trình đặt vé nhanh gọn.", 
             "- Thời gian hoàn tất 1 đơn đặt vé: < 3 phút\n- Điểm đánh giá trải nghiệm người dùng: >= 8.5/10"],
            ["5. Reliability\n(Độ tin cậy & Toàn vẹn)", 
             "Toàn vẹn dữ liệu ghế ngồi tuyệt đối. Không bao giờ xảy ra hiện tượng 2 khách hàng mua trùng một ghế (No double booking); tự động khôi phục khi lỗi.", 
             "- Tính sẵn sàng (Availability): >= 99.9%\n- Tỷ lệ lỗi tranh chấp ghế: 0% tuyệt đối"],
            ["6. Security\n(An toàn & Bảo mật)", 
             "Mật khẩu băm một chiều BCrypt với độ trễ tính toán 10 rounds; cơ chế phân quyền RBAC đa lớp qua Middleware; bảo mật mã QR vé tránh làm giả.", 
             "- Đạt chuẩn OWASP Top 10 về phòng chống SQL Injection, XSS, CSRF\n- Thời gian sống phiên đăng nhập: 24 giờ"],
            ["7. Maintainability\n(Khả năng bảo trì)", 
             "Mã nguồn tuân thủ nghiêm ngặt mô hình MVC; chia tách rõ Router, Controller, Service, Model; tài liệu hóa chú thích code đầy đủ.", 
             "- Thời gian làm quen và bảo trì mã nguồn cho lập trình viên mới: < 2 ngày\n- Cấu trúc thư mục chuẩn mực"],
            ["8. Portability\n(Tính khả chuyển)", 
             "Ứng dụng có khả năng đóng gói chạy trên nhiều môi trường hệ điều hành khác nhau mà không cần sửa đổi mã nguồn.", 
             "- Chạy thông suốt trên Windows 10/11, Ubuntu Linux, macOS\n- Hỗ trợ cả cơ sở dữ liệu MySQL và SQLite"]
        ],
        col_widths=[1.8, 2.7, 1.8],
        align_cols=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT],
        source="Nhóm 10 - Chuẩn chất lượng phần mềm ISO/IEC 25010"
    )

    doc.add_page_break()
    print("Chapter 2 updated successfully based on reference file.")
