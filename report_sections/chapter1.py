# ==============================================================================
# CHƯƠNG I. TỔNG QUAN VỀ ĐỀ TÀI
# ==============================================================================
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def add_chapter_1(doc, add_p, add_heading_1, add_heading_2, add_heading_3, add_bullet, add_figure, add_table_custom):
    add_heading_1("CHƯƠNG I. TỔNG QUAN VỀ ĐỀ TÀI")

    # 1.1. ĐẶT VẤN ĐỀ
    add_heading_2("1.1. Đặt vấn đề")

    add_p("Trong bối cảnh nền kinh tế số và sự phát triển vượt bậc của công nghệ thông tin, ngành công nghiệp điện ảnh và giải trí tại Việt Nam đang chứng kiến sự tăng trưởng vượt bậc về quy mô lẫn chất lượng dịch vụ. Các chuỗi cụm rạp hiện đại như Cinestar, CGV, Lotte Cinema, Beta Cinemas ngày càng mở rộng mạng lưới, phục vụ hàng chục nghìn lượt khán giả mỗi ngày. Tuy nhiên, đi cùng với sự mở rộng đó là bài toán nan giải trong công tác quản lý và vận hành.")

    add_p("Khảo sát thực tế tại nhiều cụm rạp cho thấy, phương thức quản lý bán vé truyền thống và bán vé bán tự động còn tồn tại rất nhiều bất cập và hạn chế nghiêm trọng:")

    add_bullet("Khán giả phải trực tiếp đến rạp để xếp hàng mua vé, đặc biệt vào các dịp cuối tuần, ngày lễ hoặc các suất chiếu phim 'bom tấn'. Tình trạng quá tải tại sảnh chờ không chỉ gây mệt mỏi, khó chịu cho khách hàng mà còn làm gia tăng áp lực cực lớn lên đội ngũ nhân viên quầy vé.", "Tình trạng ùn tắc và xếp hàng cục bộ:");
    add_bullet("Khách hàng khi mua vé tại quầy chỉ được nhân viên chỉ định ghế qua màn hình xoay hoặc mô tả bằng miệng, thiếu tính chủ động và khó hình dung được góc nhìn thực tế tới màn chiếu, dẫn đến những trải nghiệm không hài lòng sau khi vào phòng xem phim.", "Thiếu tính trực quan trong lựa chọn vị trí ghế ngồi:");
    add_bullet("Việc quản lý lịch chiếu tại nhiều cụm rạp vẫn dựa vào bảng tính Excel thủ công hoặc ghi chép sổ sách của người quản lý rạp (Manager). Quá trình này rất dễ xảy ra sai sót con người (Human Error), điển hình là sự cố xếp trùng giờ chiếu trong cùng một phòng chiếu, không tính toán đủ thời gian dọn dẹp vệ sinh phòng (cleaning buffer time) dẫn đến tình trạng phim trước chưa tan mà khán giả suất sau đã vào phòng.", "Xung đột lịch chiếu và sai sót xếp lịch thủ công:");
    add_bullet("Vé giấy truyền thống dễ bị rách nát, thất lạc, phai mực in nhiệt và đặc biệt là nguy cơ bị quay vòng (một vé sử dụng cho nhiều người vào cửa) do khâu soát vé thủ công chỉ nhìn bằng mắt thường hoặc xé góc vé mà không lưu trữ nhật ký đối soát trên hệ thống số hóa.", "Nguy cơ gian lận và thất thoát doanh thu từ vé giấy:");
    add_bullet("Người quản trị và quản lý rạp không thể nắm bắt được doanh thu bán vé, số lượng ghế trống và tỷ lệ lấp đầy rạp (Occupancy Rate %) theo thời gian thực. Các báo cáo tài chính phải chờ tổng hợp cuối ngày hoặc cuối tháng, làm chậm trễ các quyết định điều chỉnh giá vé hay tăng/giảm suất chiếu cho từng bộ phim.", "Thiếu hụt dữ liệu thống kê báo cáo thời gian thực:");

    add_p("Trước những thách thức cấp bách nêu trên, việc nghiên cứu, phân tích và xây dựng một 'Hệ thống đặt vé và quản lý suất chiếu rạp chiếu phim (Cinestar Cinema)' hoàn chỉnh trên nền tảng Web Application theo mô hình kiến trúc MVC (Model - View - Controller) chuẩn mực là một đòi hỏi tất yếu và mang tính ứng dụng thực tiễn vô cùng sâu sắc. Hệ thống không chỉ giải phóng người xem khỏi việc xếp hàng, mang lại trải nghiệm chọn ghế tương tác thời gian thực mà còn cung cấp bộ công cụ quản trị thông minh, tự động hóa phát hiện xung đột lịch chiếu, khóa giữ ghế chống tranh chấp đồng thời và kiểm soát vé điện tử QR Code bảo mật tuyệt đối.")

    # 1.2. YÊU CẦU NGHIỆP VỤ
    add_heading_2("1.2. Yêu cầu nghiệp vụ")

    add_p("Hệ thống quản lý rạp chiếu phim là một hệ thống thông tin tích hợp đa phân hệ, phục vụ đồng thời 4 nhóm đối tượng tác nhân với các quy trình nghiệp vụ gắn kết chặt chẽ. Qua quá trình khảo sát thực tế và phân tích quy trình vận hành cụm rạp, nhóm nghiên cứu đã tổng hợp các khối nghiệp vụ then chốt sau:")

    add_heading_3("1.2.1. Nghiệp vụ Bán vé và Đặt chỗ đa kênh (Omni-channel Ticketing)")
    add_p("Hệ thống phải hỗ trợ song song hai kênh bán vé đồng bộ dữ liệu thời gian thực:")
    add_bullet("Khách hàng truy cập website qua máy tính hoặc điện thoại thông minh để xem trailer, đọc tóm tắt nội dung, lựa chọn cụm rạp, suất chiếu, chọn vị trí ghế ngồi trực quan trên sơ đồ ma trận phòng chiếu, đặt combo bắp nước và thanh toán qua cổng thanh toán điện tử hoặc thẻ ngân hàng. Hệ thống cấp vé điện tử kèm mã QR Code bảo mật gửi về tài khoản.", "Kênh trực tuyến (Online Booking):");
    add_bullet("Dành cho nhân viên quầy vé (Staff POS) phục vụ khách hàng vãng lai mua vé trực tiếp tại rạp. Giao diện POS tối ưu thao tác nhanh, cho phép nhân viên chọn phim, chọn suất, bấm ghế, thu tiền mặt hoặc quẹt thẻ, in vé vật lý và xuất hóa đơn trong thời gian dưới 30 giây.", "Kênh tại quầy (POS Counter):");

    add_heading_3("1.2.2. Nghiệp vụ Quản lý Phòng chiếu và Phân loại Cấu hình Ghế")
    add_p("Mỗi cụm rạp sở hữu nhiều phòng chiếu với các định dạng công nghệ khác nhau (2D Standard, 3D Digital, IMAX Laser, Dolby Atmos). Nghiệp vụ yêu cầu:")
    add_bullet("Quản lý danh sách phòng chiếu: tên phòng, định dạng màn hình, số hàng ghế, số ghế mỗi hàng và tổng sức chứa.", "Quản lý phòng chiếu:");
    add_bullet("Mỗi vị trí ghế trong phòng được định danh theo tọa độ (Hàng chữ cái A-H, Số thứ tự 1-14). Ghế được phân loại thành 3 hạng với hệ số giá khác nhau: Ghế Thường (Regular - hệ số 1.0), Ghế VIP (nằm ở trung tâm phòng chiếu, góc nhìn tối ưu - hệ số 1.25) và Ghế Đôi Sweetbox (dành cho cặp đôi ở hàng cuối - hệ số 2.2). Hệ thống phải cho phép quản lý bật/tắt trạng thái bảo trì cho từng ghế.", "Cấu hình phân loại ghế:");

    add_heading_3("1.2.3. Nghiệp vụ Lên lịch Suất chiếu và Tối ưu hóa Vận hành")
    add_p("Đây là nghiệp vụ trung tâm và phức tạp nhất của người Quản lý rạp (Manager):")
    add_bullet("Người quản lý chọn phim, chọn phòng chiếu, ngày chiếu và giờ bắt đầu (Start Time).", "Lập lịch chiếu:");
    add_bullet("Hệ thống phải tự động tính toán thời gian kết thúc của suất chiếu dựa trên thời lượng phim cộng thêm thời gian đệm vệ sinh phòng chiếu (Cleaning Buffer, mặc định 15 phút).", "Tính toán thời gian chiếm dụng phòng:");
    add_bullet("Hệ thống bắt buộc phải kiểm tra tự động xem khung giờ dự kiến có bị giao thoa, đè lấn lên bất kỳ suất chiếu nào đã xếp trước đó trong cùng một phòng hay không. Nếu có xung đột, hệ thống phải ngăn chặn hành vi lưu và đưa ra cảnh báo chi tiết.", "Ngăn chặn xung đột lịch chiếu:");

    add_heading_3("1.2.4. Nghiệp vụ Soát vé Điện tử và Chống gian lận (Fraud Prevention)")
    add_bullet("Khách hàng khi đến cửa phòng chiếu xuất trình vé điện tử có mã QR trên màn hình smartphone hoặc vé in.", "Kiểm soát ra vào:");
    add_bullet("Nhân viên soát vé sử dụng thiết bị camera hoặc máy quét chuyên dụng để quét mã QR. Hệ thống giải mã chuỗi định danh, truy vấn CSDL để xác thực tính hợp lệ của vé.", "Quét mã QR tự động:");
    add_bullet("Nếu vé chưa sử dụng (unused), hệ thống cập nhật trạng thái thành 'checked_in', lưu thời gian soát và ID nhân viên soát. Nếu vé này bị quét lại lần thứ hai, hệ thống phải phát còi báo động màu đỏ: 'CẢNH BÁO GIAN LẬN: Vé đã được sử dụng vào lúc... bởi nhân viên...!', ngăn chặn triệt để hành vi quay vòng vé vào rạp.", "Cảnh báo gian lận hai lớp:");

    add_heading_3("1.2.5. Nghiệp vụ Quản lý Bảng giá vé và Combo Bắp nước")
    add_bullet("Giá vé được cấu thành từ: Giá cơ bản của suất chiếu (Base Price) nhân với Hệ số loại ghế (Regular 1.0, VIP 1.25, Sweetbox 2.2), kèm theo các phụ thu định dạng phòng (IMAX, 3D).", "Định giá vé động:");
    add_bullet("Quản lý danh mục các gói combo bắp nước (Bắp ngọt, Bắp phô mai, Nước ngọt, Combo Couple, Combo Family). Cho phép khách hàng thêm combo trực tiếp vào đơn hàng đặt vé.", "Kinh doanh bắp nước (F&B):");

    add_heading_3("1.2.6. Nghiệp vụ Phân quyền Bảo mật (RBAC) và Báo cáo Thống kê")
    add_bullet("Phân quyền chặt chẽ theo mô hình RBAC với 4 vai trò: Khách hàng (Client), Nhân viên quầy (Staff), Quản lý rạp (Manager), Quản trị viên hệ thống (Admin). Mỗi vai trò chỉ được truy cập đúng các tài nguyên và API được cấp phép.", "Phân quyền người dùng:");
    add_bullet("Dashboard thời gian thực trực quan hóa biểu đồ doanh thu theo ngày, theo tuần (Chart.js), thống kê top phim ăn khách và tính toán chính xác Tỷ lệ lấp đầy rạp (Occupancy Rate %) để đánh giá hiệu quả kinh doanh của từng suất chiếu.", "Thống kê báo cáo:");

    # 1.3. MỤC TIÊU CỦA ĐỀ TÀI
    add_heading_2("1.3. Mục tiêu của đề tài")

    add_heading_3("1.3.1. Mục tiêu tổng quát")
    add_p("Xây dựng thành công hệ thống ứng dụng Web 'Hệ thống đặt vé và quản lý suất chiếu rạp chiếu phim (Cinestar Cinema)' hoàn chỉnh, ổn định và bảo mật theo chuẩn kiến trúc MVC (Model - View - Controller). Hệ thống tự động hóa toàn diện chu trình bán vé đa kênh, tối ưu hóa công tác điều phối lịch chiếu, ngăn chặn triệt để tình trạng bán trùng ghế và gian lận vé, đồng thời cung cấp giao diện trực quan, thân thiện cho mọi đối tượng người dùng.")

    add_heading_3("1.3.2. Mục tiêu cụ thể theo từng tác nhân")
    add_bullet("Đăng ký, đăng nhập tài khoản an toàn; tra cứu danh mục 100+ bộ phim đang chiếu và sắp chiếu; xem trailer, tóm tắt nội dung và độ tuổi; tương tác chọn vị trí ghế ngồi trực quan trên sơ đồ ghế động; chọn combo bắp nước; thanh toán an toàn với cơ chế đếm ngược 5 phút; nhận vé điện tử kèm mã QR Code bảo mật; quản lý lịch sử đặt vé cá nhân.", "Đối với Khách hàng (Client):");
    add_bullet("Sở hữu giao diện bán vé quầy POS tối ưu hóa tốc độ nhập liệu; tra cứu và chọn suất chiếu tức thì; chọn ghế và in vé; phân hệ quét mã QR soát vé tích hợp camera WebCam/máy quét mã vạch; tự động xác thực và phát cảnh báo gian lận khi phát hiện vé bị sử dụng lại; xem lịch sử đối soát vé của ca trực.", "Đối với Nhân viên quầy (Staff):");
    add_bullet("Sở hữu Dashboard phân tích trực quan doanh thu theo 7 ngày gần nhất; theo dõi chỉ số tỷ lệ lấp đầy rạp (Occupancy Rate %); quản lý danh mục phim (thêm, sửa, đóng/mở chiếu); quản lý phòng chiếu và sơ đồ ma trận ghế; công cụ lập lịch suất chiếu thông minh tích hợp thuật toán kiểm tra xung đột thời gian thực; quản lý bảng giá vé và combo F&B.", "Đối với Quản lý rạp (Manager):");
    add_bullet("Quản lý toàn bộ tài khoản người dùng trong hệ thống; thực hiện phân quyền vai trò RBAC (Admin, Manager, Staff, Client); khóa/mở khóa tài khoản; cấu hình các tham số hệ thống rạp (thời gian đệm dọn phòng, thời gian khóa giữ ghế); giám sát nhật ký giao dịch và kiểm toán bảo mật (Audit Logs).", "Đối với Quản trị viên (Admin):");

    add_heading_3("1.3.3. Đối tượng và phạm vi nghiên cứu")
    add_bullet("Quy trình nghiệp vụ vận hành, bán vé và soát vé tại chuỗi rạp chiếu phim thương mại; các mô hình kiến trúc phần mềm MVC; các tiêu chuẩn quốc tế về đặc tả phần mềm (IEEE 830, ISO/IEC 25010); kỹ thuật kiểm soát xung đột tài nguyên và cơ chế mã hóa QR Code.", "Đối tượng nghiên cứu:");
    add_bullet("Phạm vi dữ liệu: Khảo sát và xây dựng cơ sở dữ liệu mẫu phản ánh thực tế chuỗi rạp Cinestar gồm 10 cụm rạp tiêu biểu tại Hà Nội (Cầu Giấy, Hoàn Kiếm, Thanh Xuân, Hai Bà Trưng, Đống Đa) và TP.HCM (Quận 1, Quận 3, Quận 4, Quận 5, Quận 10); bộ dữ liệu 100 bộ phim điện ảnh phong phú; 22 phòng chiếu đa định dạng; 1.584 ghế ngồi tự sinh theo ma trận chuẩn; 224 suất chiếu phân bổ thực tế.", "Phạm vi hệ thống:");
    add_bullet("Phạm vi triển khai: Ứng dụng Web chạy trên môi trường Node.js kết nối cơ sở dữ liệu quan hệ chuẩn hóa 3NF, đáp ứng truy cập đồng thời trên các trình duyệt hiện đại (Chrome, Edge, Firefox, Safari).", "Phạm vi công nghệ:");

    add_heading_3("1.3.4. Ý nghĩa khoa học và thực tiễn của đề tài")
    add_bullet("Đề tài là sự vận dụng tổng hợp và sáng tạo các kiến thức cốt lõi của ngành Công nghệ phần mềm: quy trình phân tích thiết kế hệ thống hướng đối tượng với UML, chuẩn hóa cơ sở dữ liệu quan hệ 3NF, áp dụng kiến trúc phần mềm phân tầng MVC, thiết kế giao diện người dùng theo chuẩn công thái học UI/UX, và xây dựng bộ kiểm thử phần mềm tự động (Automated Test Suite).", "Ý nghĩa khoa học và đào tạo:");
    add_bullet("Sản phẩm phần mềm có tính hoàn thiện cao, giải quyết triệt để các bài toán nhức nhối trong thực tế vận hành rạp chiếu phim. Thuật toán kiểm tra xung đột lịch chiếu và kỹ thuật khóa giữ ghế tạm thời có thể chuyển giao, ứng dụng ngay vào các hệ thống đặt chỗ trực tuyến tương tự (đặt vé xe, đặt phòng khách sạn, đặt bàn nhà hàng, vé sự kiện concert).", "Ý nghĩa thực tiễn ứng dụng:");

    # 1.4. ĐỀ XUẤT GIẢI PHÁP NGHIỆP VỤ VÀ CÔNG NGHỆ SỬ DỤNG
    add_heading_2("1.4. Đề xuất giải pháp nghiệp vụ và công nghệ sử dụng")

    add_p("Để hiện thực hóa các mục tiêu đã đề ra một cách khoa học và đạt chất lượng cao nhất theo bảng tiêu chí đánh giá, nhóm nghiên cứu đề xuất giải pháp kỹ thuật tổng thể kết hợp giữa tiêu chuẩn công nghiệp và công nghệ hiện đại:")

    add_heading_3("1.4.1. Áp dụng các tiêu chuẩn kỹ thuật phù hợp")
    add_bullet("Áp dụng tiêu chuẩn IEEE 830 và IEEE 29148 (Software and Systems Engineering - Requirements Engineering) để chuẩn hóa quy trình thu thập, phân loại và đặc tả các yêu cầu chức năng (Functional Requirements - FR) dưới dạng các ca sử dụng (Use Cases) có cấu trúc tường minh.", "Tiêu chuẩn đặc tả yêu cầu IEEE 830 / IEEE 29148:");
    add_bullet("Áp dụng mô hình chất lượng phần mềm quốc tế ISO/IEC 25010 (Systems and software Quality Requirements and Evaluation - SQuaRE) để xác định và đo lường toàn diện 8 đặc tính chất lượng phi chức năng: Tính phù hợp chức năng (Functional Suitability), Hiệu năng hoạt động (Performance Efficiency), Khả năng tương thích (Compatibility), Tính khả dụng (Usability), Độ tin cậy (Reliability), An toàn bảo mật (Security), Khả năng bảo trì (Maintainability) và Tính khả chuyển (Portability).", "Tiêu chuẩn chất lượng phần mềm ISO/IEC 25010:");

    add_heading_3("1.4.2. Kiến trúc giải pháp tổng thể MVC kết hợp RBAC")
    add_p("Hệ thống được thiết kế theo kiến trúc 3 tầng MVC phân định rạch ròi trách nhiệm:")
    add_bullet("Chứa các thực thể dữ liệu ánh xạ trực tiếp từ CSDL quan hệ (Movie, Room, Seat, Showtime, Booking, Ticket, Combo, User, Role, SeatLock). Đảm nhiệm các quy tắc nghiệp vụ cốt lõi và toàn vẹn dữ liệu.", "Tầng Dữ liệu & Nghiệp vụ (Model):");
    add_bullet("Đóng vai trò điều phối trung tâm. Tiếp nhận HTTP Request từ client, gọi các Service nghiệp vụ (ConflictDetector, SeatLock), tương tác với Model để lấy hoặc cập nhật dữ liệu và quyết định kết xuất View tương ứng.", "Tầng Điều khiển (Controller):");
    add_bullet("Sử dụng EJS Template Engine kết hợp HTML5, CSS3, JavaScript và Bootstrap 5 để hiển thị giao diện động, thân thiện, tương thích đa thiết bị (Responsive Design).", "Tầng Giao diện (View):");
    add_bullet("Cơ chế xác thực dựa trên Session và Cookie, kết hợp Middleware kiểm tra vai trò người dùng trước khi cấp quyền truy cập các đường dẫn quản trị (/manager/*, /admin/*, /staff/*). Mật khẩu người dùng được băm một chiều bằng giải thuật an toàn BCrypt (Salt rounds = 10).", "Cơ chế phân quyền RBAC:");

    add_heading_3("1.4.3. Bộ 3 giải pháp kỹ thuật và thuật toán đột phá")
    add_bullet("Khi Manager xếp lịch chiếu, hệ thống sử dụng giải thuật giao thoa khoảng thời gian để kiểm tra tự động xem suất chiếu mới [T_new_start, T_new_end] có trùng với bất kỳ suất chiếu nào đã tồn tại trong cùng phòng chiếu hay không. Nếu trùng, nút Lưu bị khóa và cảnh báo đỏ xuất hiện ngay lập tức.", "1. Thuật toán kiểm tra xung đột suất chiếu (Conflict Detection):");
    add_bullet("Khi khách hàng bấm chọn ghế, hệ thống cấp khóa tạm thời vào bảng SeatLock với thời gian sống TTL đúng 5 phút. Trong thời gian này, khách hàng khác không thể chọn cùng ghế đó (ngăn chặn Race Condition). Sau 5 phút, nếu đơn hàng chưa hoàn tất thanh toán, hệ thống tự động nhả ghế về trạng thái trống.", "2. Kỹ thuật khóa giữ ghế tạm thời (Temporary Seat Lock):");
    add_bullet("Mỗi vé xem phim được cấp một chuỗi mã hóa bảo mật định danh duy nhất (UUID/TKT Code) và biểu diễn dưới dạng mã QR độ phân giải cao. Nhân viên soát vé quét mã qua camera sẽ được hệ thống xác thực tức thì và đổi trạng thái vé sang 'checked_in'. Bất kỳ hành vi quét lại vé đã dùng đều kích hoạt còi cảnh báo gian lận màu đỏ.", "3. Vé điện tử QR Code & Soát vé chống gian lận:");

    # 1.5. THIẾT KẾ VÀ ĐÁNH GIÁ KIẾN TRÚC AN TOÀN BẢO MẬT HỆ THỐNG
    add_heading_2("1.5. Thiết kế và đánh giá kiến trúc an toàn bảo mật hệ thống")

    add_heading_3("1.5.1. Tầm quan trọng của an toàn thông tin trong hệ sinh thái rạp chiếu phim")
    add_p("Trong bối cảnh các cuộc tấn công mạng nhằm vào các nền tảng thương mại điện tử và dịch vụ số ngày càng gia tăng về quy mô lẫn mức độ tinh vi, an toàn thông tin (Information Security) trở thành tiêu chuẩn bắt buộc sống còn đối với một hệ thống quản lý và bán vé trực tuyến. Với đặc thù cụm rạp chiếu phim – nơi xử lý đồng thời hàng nghìn giao dịch tài chính, thông tin định danh cá nhân của khách hàng (PII), cũng như tài nguyên ghế ngồi phòng chiếu có giới hạn – bất kỳ lỗ hổng bảo mật nào cũng có thể dẫn đến thiệt hại nghiêm trọng:")
    add_bullet("Kẻ tấn công có thể nghe lén, đánh cắp mật khẩu hoặc phiên đăng nhập để mạo danh khách hàng hoặc đặc biệt là chiếm đoạt tài khoản Quản trị viên (Admin/Manager), từ đó sửa đổi giá vé, hủy suất chiếu hoặc chiếm đoạt doanh thu.", "Rủi ro lộ lọt thông tin tài khoản và leo thang đặc quyền trái phép:");
    add_bullet("Hacker sử dụng bot tự động gửi hàng loạt request để chiếm dụng toàn bộ các vị trí ghế VIP trong các suất chiếu 'giờ vàng' mà không thanh toán, gây thất thu trầm trọng cho rạp và tước đoạt cơ hội xem phim của khách hàng chân chính.", "Rủi ro chiếm dụng tài nguyên và tấn công từ chối dịch vụ (DoS/Race Condition):");
    add_bullet("Khách hàng hoặc nhân viên biến chất chụp lại mã QR vé hoặc in vé nhiều lần để nhiều người cùng vào phòng chiếu, hoặc sửa đổi tham số giá tiền trong request thanh toán nhằm trục lợi.", "Rủi ro gian lận vé và sửa đổi tham số trường (Field Tampering):");
    add_bullet("Các kỹ thuật tấn công kinh điển như SQL Injection (tiêm mã độc vào cơ sở dữ liệu), Cross-Site Scripting (XSS - chèn script độc hại vào trình duyệt), Cross-Site Request Forgery (CSRF) và Tấn công vét cạn mật khẩu (Brute-force).", "Các lỗ hổng ứng dụng web chuẩn OWASP Top 10:");

    add_heading_3("1.5.2. Khung đối chuẩn 20 tiêu chí an toàn thông tin theo chuẩn công nghiệp")
    add_p("Nhằm đảm bảo hệ thống Cinestar Cinema đáp ứng các tiêu chuẩn bảo mật khắt khe nhất theo khuyến nghị của các tổ chức an toàn thông tin quốc tế (OWASP, NIST), nhóm nghiên cứu đã áp dụng quy trình kiểm toán và tích hợp toàn diện bộ 20 tiêu chuẩn an toàn thông tin:")

    add_table_custom(
        "Bảng 1.1. Ma trận đối chuẩn 20 tiêu chuẩn an toàn bảo mật hệ thống Cinestar Cinema",
        ["STT", "Tiêu chuẩn an toàn", "Mô tả giải pháp kỹ thuật đã cài đặt trong hệ thống", "Đánh giá"],
        [
            ["1", "Hide API keys", "Tách toàn bộ chuỗi bí mật, token và tài khoản CSDL ra khỏi mã nguồn; không để lộ key trên repository công khai.", "Đạt chuẩn"],
            ["2", "Check env variables", "Sử dụng thư viện dotenv; khởi tạo file .env.example và .env quản lý tập trung toàn bộ biến môi trường của hệ thống.", "Đạt chuẩn"],
            ["3", "Purge Git secrets", "Cấu hình .gitignore toàn diện, ngăn chặn tuyệt đối việc commit file .env, node_modules, file temp Word (~$*.docx, *.tmp) lên Git.", "Đạt chuẩn"],
            ["4", "Protect admin routes", "Toàn bộ route /admin/* và /manager/* được khóa cứng bởi middleware requireRole(['admin']), requireRole(['manager', 'admin']).", "Đạt chuẩn"],
            ["5", "Enforce server-side auth", "Trạng thái xác thực được lưu trữ và kiểm tra 100% tại phía máy chủ (Session Server-side); Client chỉ lưu Session ID đã mã hóa.", "Đạt chuẩn"],
            ["6", "Check user permissions", "Kiểm soát phân quyền RBAC 4 cấp (Admin, Manager, Staff, Client). Bổ sung cơ chế chống Admin tự xóa hoặc tự khóa tài khoản của chính mình.", "Đạt chuẩn"],
            ["7", "Enable RLS / DB rules", "Ràng buộc toàn vẹn dữ liệu ở cấp CSDL MySQL (Foreign Keys, ON DELETE RESTRICT/CASCADE, trạng thái ENUM, bảng khóa ghế tự hết hạn).", "Đạt chuẩn"],
            ["8", "Hash passwords", "Mã hóa 1 chiều mật khẩu người dùng bằng giải thuật BCrypt với độ muối Salt Rounds = 10; không lưu mật khẩu dạng plain-text.", "Đạt chuẩn"],
            ["9", "Secure session cookies", "Cookie session cinestar_sid cấu hình cờ HttpOnly: true (chống trộm qua JS), SameSite: 'lax' (chống CSRF), Secure: true khi lên HTTPS.", "Đạt chuẩn"],
            ["10", "Encrypt sensitive data", "Mật khẩu băm Bcrypt 1 chiều; Session Secret và mật khẩu CSDL được mã hóa bảo vệ qua biến môi trường.", "Đạt chuẩn"],
            ["11", "Validate user input", "Kiểm tra định dạng Email (Regex), Số điện thoại (8-20 chữ số), độ dài mật khẩu >= 6 ký tự; chặn tấn công Open Redirect (isSafeRedirect).", "Đạt chuẩn"],
            ["12", "Prevent XSS", "Template Engine EJS tự động mã hóa ký tự HTML nguy hiểm (<%= %>); Tích hợp Content Security Policy (CSP) từ Helmet.", "Đạt chuẩn"],
            ["13", "Prevent SQL injection", "100% các câu lệnh truy vấn CSDL qua mysql2/promise sử dụng cú pháp tham số hóa Prepared Statements (?), loại bỏ nối chuỗi.", "Đạt chuẩn"],
            ["14", "Prevent CSRF / CORS", "Thiết lập SameSite=Lax cho cookie kết hợp middleware xác thực Host/Origin trên các HTTP Request thay đổi dữ liệu (POST/PUT/DELETE).", "Đạt chuẩn"],
            ["15", "Secure file uploads", "Multer giới hạn kích thước poster <= 5MB; kiểm tra whitelist định dạng ảnh; đổi tên ngẫu nhiên; gắn header nosniff cho /uploads.", "Đạt chuẩn"],
            ["16", "Prevent field tampering", "Giá vé và giá combo bắp nước lấy trực tiếp từ CSDL theo suất chiếu (không nhận từ client); giới hạn tối đa 8 ghế/đơn đặt chống DoS rạp.", "Đạt chuẩn"],
            ["17", "Add rate limiting", "Tích hợp express-rate-limit giới hạn tối đa 25 request/15 phút từ 1 IP cho các route xác thực /auth/login và /auth/register.", "Đạt chuẩn"],
            ["18", "Add security headers", "Cài đặt thư viện Helmet bổ sung các header: X-Frame-Options: SAMEORIGIN (chống Clickjacking), nosniff, HSTS, CSP chuẩn.", "Đạt chuẩn"],
            ["19", "Disable debug in prod", "Vô hiệu hóa header X-Powered-By: Express; Trang lỗi 500 tự động ẩn stack trace chi tiết khi chạy ở môi trường Production.", "Đạt chuẩn"],
            ["20", "Scan dependencies", "Kiểm toán toàn bộ cây phụ thuộc thư viện qua lệnh npm audit: ghi nhận 0 lỗ hổng bảo mật (0 vulnerabilities).", "Đạt chuẩn"]
        ],
        col_widths=[0.5, 1.6, 3.5, 0.9],
        source="Nhóm 10 - Kết quả kiểm toán an toàn thông tin hệ thống Cinestar Cinema"
    )

    add_heading_3("1.5.3. Chi tiết các cơ chế bảo mật then chốt đã triển khai")
    add_bullet("Hệ thống loại bỏ hoàn toàn cơ chế lưu trữ mật khẩu thuần túy. Khi người dùng đăng ký hoặc quản trị viên tạo tài khoản, mật khẩu được xử lý qua giải thuật BCrypt với 10 vòng sinh muối ngẫu nhiên (Salt rounds = 10). Giải thuật này tạo ra chuỗi băm 60 ký tự không thể dịch ngược, đồng thời chống lại kỹ thuật tấn công bằng Bảng cầu vồng (Rainbow Table). Phiên đăng nhập được quản trị qua cookie 'cinestar_sid' với cờ HttpOnly ngăn chặn mã độc JavaScript phía client truy xuất (chống XSS Cookie Theft), cờ SameSite='lax' bảo vệ trước các liên kết lừa đảo Cross-Site, và cờ Secure sẵn sàng kích hoạt khi triển khai trên giao thức bảo mật HTTPS.", "1. Bảo mật xác thực và phiên làm việc (Authentication & Session Security):");
    add_bullet("Áp dụng mô hình RBAC phân định nghiêm ngặt 4 cấp độ quyền hạn. Hệ thống xây dựng middleware 'requireRole' kiểm tra phiên làm việc trước mọi request. Bất kỳ nỗ lực truy cập trái phép nào vào các khu vực quản trị (/admin, /manager, /staff) đều bị từ chối ngay lập tức và trả về trang lỗi 403 Forbidden. Đặc biệt, để ngăn chặn rủi ro tự hủy hoại hệ thống do sơ suất của quản trị viên, controller quản trị được tích hợp cơ chế bảo vệ: Quản trị viên đang đăng nhập không thể tự ấn nút khóa hoặc xóa tài khoản của chính mình.", "2. Phân quyền đa cấp RBAC và cơ chế tự bảo vệ tài khoản (Self-Defense Mechanism):");
    add_bullet("Triệt tiêu hoàn toàn nguy cơ tấn công tiêm mã SQL (SQLi) bằng cách áp dụng nhất quán cơ chế Prepared Statements với tham số hóa '?' trên toàn bộ các lớp Model. Dữ liệu đầu vào từ người dùng được gửi riêng biệt với câu lệnh SQL, khiến các chuỗi tiêm nhiễm như \"' OR 1=1 --\" chỉ được coi là giá trị chuỗi thuần túy và không thể làm thay đổi cấu trúc truy vấn. Đối với nguy cơ XSS, hệ thống kết hợp cơ chế tự động HTML Escaping của EJS với chính sách Content Security Policy (CSP) chặt chẽ từ thư viện Helmet, ngăn chặn việc thực thi các đoạn mã kịch bản lạ từ bên ngoài.", "3. Phòng chống tấn công tiêm nhiễm (Anti-SQL Injection & Anti-XSS):");
    add_bullet("Để đối phó với các cuộc tấn công dò quét mật khẩu tự động (Brute-force Attack) hoặc các cuộc tấn công từ chối dịch vụ vào cổng xác thực, hệ thống tích hợp module Rate Limiting (express-rate-limit). Cơ chế này thiết lập ngưỡng giới hạn: một địa chỉ IP chỉ được phép thực hiện tối đa 25 thao tác xác thực trong vòng 15 phút. Khi vượt quá ngưỡng này, toàn bộ request tiếp theo từ IP đó sẽ bị tạm khóa với mã lỗi HTTP 429 và thông điệp cảnh báo bảo vệ tài khoản.", "4. Kiểm soát lưu lượng và chống tấn công vét cạn (Rate Limiting & Anti-Brute-Force):");
    add_bullet("Module upload poster phim (Multer) được siết chặt với 3 lớp bảo vệ: (1) Giới hạn dung lượng tệp tin tối đa 5MB; (2) Kiểm tra kép cả phần mở rộng (extension) và kiểu MIME (chỉ chấp nhận jpeg, jpg, png, webp, gif); (3) Tự động đổi tên tệp sang chuỗi thời gian ngẫu nhiên để chống tấn công ghi đè tệp tin và gắn header 'X-Content-Type-Options: nosniff'. Bên cạnh đó, để chống gian lận giá vé (Field Tampering), hệ thống tuyệt đối không tin tưởng giá tiền do client gửi lên mà luôn tính toán lại toàn bộ đơn giá vé và combo bắp nước trực tiếp từ cơ sở dữ liệu; đồng thời áp dụng trần giới hạn tối đa 8 ghế/lần đặt nhằm ngăn ngừa hành vi dùng script chiếm dụng toàn bộ phòng chiếu.", "5. Bảo mật tệp tin tải lên và chống gian lận dữ liệu (Upload Security & Anti-Tampering):");
    add_bullet("Hệ thống cài đặt thư viện bảo mật chuyên dụng Helmet nhằm cấu hình tự động bộ tiêu đề HTTP Security Headers đạt chuẩn doanh nghiệp: vô hiệu hóa hoàn toàn header công nghệ 'X-Powered-By' nhằm che giấu nền tảng Express/Node.js trước các công cụ quét lỗ hổng; thiết lập 'X-Frame-Options: SAMEORIGIN' để ngăn chặn hoàn toàn tấn công chèn giao diện vô hình (Clickjacking); bật chính sách HSTS (Strict-Transport-Security) bắt buộc trình duyệt sử dụng kết nối mã hóa; và quản lý ngoại lệ an toàn cho các tài nguyên CDN uy tín (Bootstrap, Font Awesome, Google Fonts, YouTube Trailers).", "6. Thiết lập tiêu đề bảo mật HTTP (HTTP Security Headers via Helmet):");

    doc.add_page_break()
    print("Chapter 1 generated successfully.")
