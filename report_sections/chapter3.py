# ==============================================================================
# CHƯƠNG III. CƠ SỞ LÝ THUYẾT
# ==============================================================================
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def add_chapter_3(doc, add_p, add_heading_1, add_heading_2, add_heading_3, add_bullet, add_figure, add_table_custom, add_code_snippet):
    add_heading_1("CHƯƠNG III. CƠ SỞ LÝ THUYẾT")

    # 3.1. KIẾN THỨC PHẦN MỀM
    add_heading_2("3.1. Kiến thức phần mềm")

    add_heading_3("3.1.1. Kiến trúc MVC (Model - View - Controller)")
    add_p("Kiến trúc phần mềm MVC (Model - View - Controller) là một trong những mẫu kiến trúc kinh điển và được áp dụng rộng rãi nhất trong công nghiệp phát triển phần mềm hiện đại, đặc biệt là các ứng dụng web phức hợp. Bản chất cốt lõi của MVC là nguyên lý phân tách mối quan tâm (Separation of Concerns - SoC), chia hệ thống thành 3 thành phần độc lập tương đối nhưng tương tác hài hòa với nhau:")

    add_bullet("Đại diện cho tầng dữ liệu và các quy tắc nghiệp vụ (Business Rules). Model chịu trách nhiệm truy xuất, thêm mới, sửa đổi dữ liệu từ hệ quản trị CSDL, đảm bảo tính toàn vẹn của dữ liệu và thực thi các logic tính toán nội tại. Trong đồ án, Model bao gồm các thực thể như Movie, Room, Seat, Showtime, Booking, Ticket, Combo, User, Role, SeatLock.", "1. Model (Mô hình dữ liệu & Nghiệp vụ):");
    add_bullet("Đại diện cho tầng trình diễn giao diện người dùng (User Interface). View nhận dữ liệu đã được xử lý từ Controller để kết xuất thành các trang HTML tĩnh hoặc động, hiển thị biểu đồ, bảng biểu và tiếp nhận hành động tương tác từ người dùng (click chuột, nhập form, quét mã QR). Trong đồ án, View được xây dựng bằng EJS Template Engine kết hợp Bootstrap 5.", "2. View (Giao diện trình diễn):");
    add_bullet("Đóng vai trò là bộ não điều phối trung tâm giữa Model và View. Controller tiếp nhận các yêu cầu HTTP Request (GET, POST, PUT, DELETE) gửi từ trình duyệt của người dùng, phân tích tham số, gọi các phương thức tương ứng trong Model hoặc Service nghiệp vụ, sau đó lựa chọn View phù hợp hoặc trả về dữ liệu định dạng JSON cho client.", "3. Controller (Bộ điều khiển):");

    add_p("Luồng xử lý dữ liệu (Data Flow) trong kiến trúc MVC diễn ra tuần tự và mạch lạc: Người dùng gửi yêu cầu từ trình duyệt tới Máy chủ -> Hệ thống định tuyến (Router) phân tích URL và điều hướng tới hàm xử lý trong Controller -> Controller gọi Model/Service để truy vấn hoặc cập nhật CSDL -> Model trả về kết quả cho Controller -> Controller nạp dữ liệu vào Template View và kết xuất trang HTML trả về cho người dùng.")

    add_heading_3("3.1.2. Quy trình phát triển phần mềm theo mô hình Agile/Scrum")
    add_p("Đồ án áp dụng quy trình phát triển phần mềm Agile theo khung làm việc Scrum, chia lộ trình thực hiện 7 tuần thành 7 Sprint liên tiếp:")
    add_bullet("Khảo sát hiện trạng, lập kế hoạch chi tiết, xác định yêu cầu nghiệp vụ và cấu trúc đề tài.", "Sprint 1 (Tuần 1):");
    add_bullet("Thu thập dữ liệu thực tế (10 cụm rạp, 100 phim), phân tích tác nhân, đặc tả yêu cầu chức năng (FR) và phi chức năng (NFR) theo chuẩn ISO/IEC 25010.", "Sprint 2 (Tuần 2):");
    add_bullet("Nghiên cứu cơ sở lý thuyết MVC, thiết kế giải thuật chống xung đột suất chiếu và cơ chế khóa giữ ghế 5 phút; dựng khung dự án GitHub.", "Sprint 3 (Tuần 3):");
    add_bullet("Phân tích ca sử dụng, vẽ bộ biểu đồ UML (FDD, Use Case, Activity Diagram); thiết kế Class Diagram, Sequence Diagram, State Diagram; thiết kế CSDL chuẩn hóa 3NF và phác thảo Wireframes.", "Sprint 4 (Tuần 4 & Tuần 5):");
    add_bullet("Cài đặt mã nguồn Backend, Frontend MVC, lập trình 4 phân hệ chức năng cho Khách hàng, Nhân viên, Quản lý và Quản trị viên.", "Sprint 5 (Tuần 6):");
    add_bullet("Xây dựng bộ kiểm thử tự động (Automated Test Suite), chạy 17 Test cases, đo lường chỉ số phi chức năng, tối ưu hóa truy vấn và hoàn thiện toàn bộ báo cáo thuyết minh.", "Sprint 6 (Tuần 7):");

    # 3.2. CÁC CÔNG NGHỆ SỬ DỤNG
    add_heading_2("3.2. Các công nghệ sử dụng")

    add_heading_3("3.2.1. Nền tảng Backend và Hệ sinh thái Node.js / Express")
    add_bullet("Môi trường thực thi JavaScript phía máy chủ mã nguồn mở, hoạt động dựa trên cơ chế đơn luồng phi đồng bộ hướng sự kiện (Non-blocking I/O Event-driven). Node.js v24+ mang lại tốc độ xử lý I/O cực cao, cho phép hệ thống đáp ứng hàng nghìn yêu cầu truy vấn vé và ghế ngồi đồng thời với mức tiêu tốn tài nguyên phần cứng tối thiểu.", "Node.js (v24+):");
    add_bullet("Framework phát triển web tối giản nhưng cực kỳ mạnh mẽ, cung cấp hệ thống định tuyến (Routing) linh hoạt và cơ chế Middleware mạnh mẽ để kiểm soát xác thực phiên đăng nhập, kiểm tra phân quyền RBAC và xử lý lỗi tập trung.", "Express.js Framework:");
    add_bullet("Thư viện băm mật khẩu chuẩn mã hóa học thuật an toàn với độ phức tạp tính toán salt rounds = 10, vô hiệu hóa hoàn toàn các cuộc tấn công vét cạn (Brute-force) hoặc tấn công bảng cầu vồng (Rainbow table).", "BCrypt Hashing:");
    add_bullet("Quản lý trạng thái phiên làm việc an toàn của người dùng qua Cookie mã hóa, hỗ trợ phân biệt chính xác phiên truy cập của Khách hàng, Nhân viên, Manager và Admin.", "Express-Session & Cookie-Parser:");

    add_heading_3("3.2.2. Nền tảng Frontend và Thư viện Trực quan hóa")
    add_bullet("Bộ máy sinh mẫu giao diện phía server, cho phép nhúng mã JavaScript trực tiếp vào mã HTML một cách tự nhiên và tách bạch Master Layout (header, footer, sidebar) dùng chung cho toàn bộ các trang.", "EJS (Embedded JavaScript):");
    add_bullet("Framework CSS phổ biến nhất thế giới, cung cấp hệ thống lưới Responsive Grid 12 cột, các thành phần giao diện chuẩn mực (Modal, Dropdown, Card, Alert, Form Validation) giúp website hiển thị hoàn hảo trên mọi kích thước màn hình.", "Bootstrap 5 & FontAwesome 6:");
    add_bullet("Thư viện vẽ đồ thị tương tác HTML5 Canvas, được ứng dụng tại Dashboard của Quản lý để trực quan hóa biểu đồ cột doanh thu 7 ngày và biểu đồ thanh tỷ lệ lấp đầy rạp.", "Chart.js:");
    add_bullet("Thư viện mã nguồn mở cho phép truy cập trực tiếp luồng camera của trình duyệt trên máy tính/điện thoại hoặc máy quét mã vạch để nhận diện, giải mã chuỗi mã QR Code vé xem phim thời gian thực với độ trễ < 100ms.", "HTML5-QRCode Scanner:");

    add_heading_3("3.2.3. Hệ quản trị Cơ sở dữ liệu và Công cụ phát triển")
    add_bullet("Hệ quản trị CSDL quan hệ chuẩn hóa 3NF, hỗ trợ cơ chế Connection Pool (tối đa 15 kết nối đồng thời), Transaction toàn vẹn dữ liệu và hệ thống chỉ mục (Index) tối ưu hóa truy vấn.", "MySQL / SQLite 3NF:");
    add_bullet("Visual Studio Code (IDE chính), Git & GitHub (quản lý mã nguồn phân tán), Draw.io (vẽ biểu đồ FDD, Use Case, ERD), PlantUML (vẽ biểu đồ hoạt động, tuần tự, lớp) và Postman (kiểm thử API).", "Công cụ hỗ trợ:");

    # 3.3. THUẬT TOÁN VÀ KỸ THUẬT CHUYÊN SÂU ÁP DỤNG
    add_heading_2("3.3. Thuật toán và kỹ thuật chuyên sâu áp dụng")

    add_heading_3("3.3.1. Thuật toán kiểm tra xung đột suất chiếu (Showtime Conflict Detection Algorithm)")
    add_p("Trong quản lý rạp chiếu phim, bài toán xếp lịch chiếu là bài toán tối ưu hóa tài nguyên thời gian và không gian phòng chiếu. Một sự cố xếp trùng giờ trong cùng một phòng sẽ dẫn đến hậu quả nghiêm trọng về mặt kinh doanh và uy tín của rạp. Nhóm đã nghiên cứu và phát triển module thuật toán độc lập ConflictDetector (`services/conflictDetector.js`).")

    add_p("Cơ sở toán học của thuật toán:", bold=True)
    add_p("Xét một phòng chiếu $R$. Giả sử phòng chiếu $R$ đã có một suất chiếu cũ $S_{old}$ với khoảng thời gian hoạt động là $[T_{old\_start}, T_{old\_end}]$. Khi người quản lý muốn thêm một suất chiếu mới $S_{new}$ vào cùng phòng chiếu $R$ với giờ bắt đầu dự kiến là $T_{new\_start}$, thời lượng phim là $Duration_{new}$ (phút) và thời gian đệm vệ sinh dọn phòng là $Buffer$ (phút).")

    add_p("Thời gian kết thúc chiếm dụng phòng của suất chiếu mới được xác định bởi công thức:")
    
    # Bảng phương trình theo chuẩn Cách trình bày.docx
    table_eq1 = doc.add_table(rows=1, cols=2)
    table_eq1.alignment = docx.enum.table.WD_TABLE_ALIGNMENT.CENTER
    c0, c1 = table_eq1.rows[0].cells[0], table_eq1.rows[0].cells[1]
    c0.width = Inches(5.0)
    c1.width = Inches(1.3)
    p_eq1 = c0.paragraphs[0]
    p_eq1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_eq1 = p_eq1.add_run("T_{new_end} = T_{new_start} + Duration_{new} + Buffer")
    r_eq1.bold = True
    r_eq1.font.name = 'Times New Roman'
    p_num1 = c1.paragraphs[0]
    p_num1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_num1 = p_num1.add_run("(3.1)")
    r_num1.bold = True
    r_num1.font.name = 'Times New Roman'

    add_p("Suất chiếu mới $S_{new}$ bị coi là XUNG ĐỘT (Overlapping) với suất chiếu $S_{old}$ trong cùng phòng chiếu khi và chỉ khi hai khoảng thời gian giao thoa nhau, tức là thỏa mãn đồng thời hai điều kiện sau:")

    table_eq2 = doc.add_table(rows=1, cols=2)
    table_eq2.alignment = docx.enum.table.WD_TABLE_ALIGNMENT.CENTER
    c0_2, c1_2 = table_eq2.rows[0].cells[0], table_eq2.rows[0].cells[1]
    c0_2.width = Inches(5.0)
    c1_2.width = Inches(1.3)
    p_eq2 = c0_2.paragraphs[0]
    p_eq2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_eq2 = p_eq2.add_run("T_{new_start} < T_{old_end}   VÀ   T_{new_end} > T_{old_start}")
    r_eq2.bold = True
    r_eq2.font.name = 'Times New Roman'
    p_num2 = c1_2.paragraphs[0]
    p_num2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_num2 = p_num2.add_run("(3.2)")
    r_num2.bold = True
    r_num2.font.name = 'Times New Roman'

    add_p("Phương trình (3.2) bao phủ hoàn toàn mọi khả năng xung đột trong thực tế, bao gồm:")
    add_bullet("Suất mới bắt đầu trước nhưng kết thúc sau khi suất cũ đã bắt đầu ($T_{new\_start} < T_{old\_start} < T_{new\_end}$).", "1. Giao thoa phần đầu:");
    add_bullet("Suất mới bắt đầu khi suất cũ chưa kết thúc ($T_{old\_start} < T_{new\_start} < T_{old\_end}$).", "2. Giao thoa phần đuôi:");
    add_bullet("Suất mới nằm lọt trọn vẹn bên trong khung giờ của suất cũ ($T_{old\_start} \\le T_{new\_start} < T_{new\_end} \\le T_{old\_end}$).", "3. Nằm bên trong:");
    add_bullet("Suất mới bao trùm hoàn toàn khoảng thời gian của suất cũ ($T_{new\_start} \\le T_{old\_start} < T_{old\_end} \\le T_{new\_end}$).", "4. Bao trùm bên ngoài:");

    add_p("Đoạn mã thực thi thuật toán trong hệ thống (`services/conflictDetector.js`):", italic=True)
    add_code_snippet("""// services/conflictDetector.js
async function checkConflict({ roomId, startTime, durationMinutes, bufferMinutes = 15, excludeId = null }) {
    const newStart = new Date(startTime).getTime();
    const newEnd = newStart + (durationMinutes + bufferMinutes) * 60 * 1000;

    // Truy vấn tất cả các suất chiếu đã lên lịch trong cùng phòng
    const existing = await query(
        `SELECT s.id, s.start_time, s.end_time, s.buffer_minutes, m.title AS movie_title, r.room_name 
         FROM showtimes s
         JOIN movies m ON s.movie_id = m.id
         JOIN rooms r ON s.room_id = r.id
         WHERE s.room_id = ? AND s.status != 'cancelled' ${excludeId ? 'AND s.id != ?' : ''}`,
        excludeId ? [roomId, excludeId] : [roomId]
    );

    for (const item of existing) {
        const oldStart = new Date(item.start_time).getTime();
        const oldEnd = new Date(item.end_time).getTime();

        // Kiểm tra điều kiện giao thoa khoảng thời gian theo công thức (3.2)
        if (newStart < oldEnd && newEnd > oldStart) {
            return {
                hasConflict: true,
                conflictWith: item,
                message: `⚠️ XUNG ĐỘT! Phòng ${item.room_name} đã có lịch chiếu phim "${item.movie_title}".`
            };
        }
    }
    return { hasConflict: false, message: 'Phòng chiếu còn trống, lịch chiếu hợp lệ!' };
}""")

    add_heading_3("3.3.2. Kỹ thuật khóa giữ ghế tạm thời (Temporary Seat Lock Mechanism)")
    add_p("Trong các hệ thống thương mại điện tử đặt vé xem phim có lưu lượng truy cập cao, bài toán tranh chấp tài nguyên đồng thời (Race Condition) thường xuyên xảy ra. Nếu hai khách hàng A và B cùng truy cập một suất chiếu và cùng bấm chọn ghế D07 vào cùng một giây, nếu không có cơ chế khóa trung gian, cả hai khách hàng đều có thể thanh toán thành công dẫn đến tình trạng bán trùng một ghế cho 2 người (Double Booking).")

    add_p("Nhóm nghiên cứu đã thiết kế cơ chế Khóa giữ ghế tạm thời (Temporary Seat Lock) hoạt động theo nguyên lý Khóa phiên với thời gian sống TTL:")
    add_bullet("Khi khách hàng chọn một hoặc nhiều ghế và bấm 'Tiếp tục', hệ thống gửi yêu cầu khóa ghế kèm theo Session ID của khách hàng. Hệ thống kiểm tra xem ghế đã có trong bảng `tickets` (đã bán) hoặc bảng `seat_locks` (đang bị người khác giữ và chưa hết hạn) hay chưa.", "1. Kiểm tra tính sẵn sàng:");
    add_bullet("Nếu ghế hoàn toàn tự do, hệ thống ghi bản ghi vào bảng `seat_locks` với trường `expires_at = CURRENT_TIMESTAMP + 5 phút`. Ghế chuyển sang trạng thái tạm khóa đối với tất cả những người dùng khác.", "2. Thiết lập khóa 5 phút:");
    add_bullet("Trên giao diện của khách hàng hiển thị đồng hồ đếm ngược 5:00. Khách hàng tiến hành chọn combo bắp nước và thanh toán.", "3. Đếm ngược phiên thanh toán:");
    add_bullet("Nếu khách hàng thanh toán thành công, hệ thống tạo bản ghi vé trong bảng `tickets` và xóa khóa tạm trong `seat_locks`. Nếu quá 5 phút mà khách hàng chưa hoàn tất thanh toán, bản ghi trong `seat_locks` tự động hết hiệu lực và ghế được nhả về trạng thái trống cho các khách hàng khác.", "4. Giải phóng khóa:");

    add_heading_3("3.3.3. Kỹ thuật vé điện tử QR Code và Ngăn chặn gian lận soát vé")
    add_p("Để số hóa hoàn toàn khâu kiểm soát ra vào rạp, mỗi vé xem phim khi được thanh toán thành công sẽ được hệ thống cấp một mã định danh duy nhất có cấu trúc: `TKT-[YYYYMMDD]-[MÃ_NGẪU_NHIÊN]` (ví dụ: `TKT-20261013-D05`). Chuỗi mã này được mã hóa thành mã phản hồi nhanh hai chiều (QR Code) chuẩn ISO/IEC 18004.")

    add_p("Cơ chế kiểm soát vé hai lớp chống gian lận (Anti-Fraud Dual Verification):")
    add_bullet("Nhân viên hướng camera vào mã QR của khách hàng. Thư viện HTML5-QRCode quét và trích xuất chuỗi ký tự vé trong thời gian < 100ms. Hệ thống truy vấn CSDL để xác định xem mã vé có tồn tại hay không. Nếu không có, lập tức báo động: 'VÉ GIẢ MẠO HOẶC KHÔNG HỢP LỆ!'.", "Lớp 1 - Xác thực tính tồn tại:");
    add_bullet("Nếu vé tồn tại, hệ thống kiểm tra trường trạng thái `status` trong bảng `tickets`. Nếu trạng thái là `unused` (chưa dùng), hệ thống cập nhật thành `checked_in`, lưu lại thời gian quét (`checked_in_at = NOW()`) và mã nhân viên soát vé (`checked_in_by = staff_id`). Trên màn hình hiển thị thông báo màu xanh: 'SOÁT VÉ THÀNH CÔNG!'.", "Lớp 2 - Xác thực trạng thái sử dụng:");
    add_bullet("Nếu vé đã có trạng thái `checked_in` từ trước đó (bị kẻ gian chụp màn hình gửi cho người khác hoặc quay vòng vé), hệ thống lập tức phát còi báo động màu đỏ: 'CẢNH BÁO GIAN LẬN: VÉ ĐÃ ĐƯỢC SỬ DỤNG VÀO LÚC... BỞI NHÂN VIÊN...!'. Cơ chế này loại bỏ 100% nguy cơ thất thoát doanh thu từ vé lậu.", "Cảnh báo gian lận tái sử dụng vé:");

    doc.add_page_break()
    print("Chapter 3 generated successfully.")
