# ==============================================================================
# PHẦN: TRANG BÌA, TRANG PHỤ BÌA, LỜI CẢM ƠN, LỜI MỞ ĐẦU, MỤC LỤC, DANH MỤC
# ==============================================================================
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def add_cover_and_intro(doc, add_p, add_heading_1, add_heading_2, add_heading_3, add_bullet, add_figure, add_table_custom):
    # -------------------------------------------------------------
    # 1. TRANG BÌA CHÍNH (COVER PAGE)
    # -------------------------------------------------------------
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO\nTRƯỜNG ĐẠI HỌC CÔNG NGHỆ ĐÔNG Á")
    run.bold = True
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)

    p_khoa = doc.add_paragraph()
    p_khoa.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_khoa.paragraph_format.space_before = Pt(2)
    p_khoa.paragraph_format.space_after = Pt(20)
    run_k = p_khoa.add_run("KHOA CÔNG NGHỆ THÔNG TIN\n-------------------***-------------------")
    run_k.bold = True
    run_k.font.name = 'Times New Roman'
    run_k.font.size = Pt(13)

    # Thêm icon / logo rạp hoặc placeholder
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(30)
    p_sp.paragraph_format.space_after = Pt(10)

    p_type = doc.add_paragraph()
    p_type.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_type.paragraph_format.space_before = Pt(10)
    p_type.paragraph_format.space_after = Pt(12)
    run_t = p_type.add_run("BÁO CÁO BÀI TẬP LỚN\nHỌC PHẦN: ĐỒ ÁN CHUYÊN NGÀNH CÔNG NGHỆ PHẦN MỀM")
    run_t.bold = True
    run_t.font.name = 'Times New Roman'
    run_t.font.size = Pt(16)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(20)
    p_title.paragraph_format.space_after = Pt(24)
    run_tit = p_title.add_run("ĐỀ TÀI:\nHỆ THỐNG ĐẶT VÉ VÀ QUẢN LÝ SUẤT CHIẾU\nRẠP CHIẾU PHIM (CINESTAR CINEMA)")
    run_tit.bold = True
    run_tit.font.name = 'Times New Roman'
    run_tit.font.size = Pt(20)

    p_sp2 = doc.add_paragraph()
    p_sp2.paragraph_format.space_before = Pt(40)
    p_sp2.paragraph_format.space_after = Pt(10)

    # Khung thông tin tác giả
    table_author = doc.add_table(rows=6, cols=2)
    table_author.alignment = docx.enum.table.WD_TABLE_ALIGNMENT.CENTER
    
    info_data = [
        ("Giảng viên hướng dẫn:", "ThS. Giảng viên phụ trách học phần"),
        ("Nhóm thực hiện:", "Nhóm 10"),
        ("Sinh viên thực hiện 1:", "Nguyễn Mạnh Quyết - MSV: 20231053"),
        ("Sinh viên thực hiện 2:", "Hà Thái Bảo - MSV: 20231045"),
        ("Lớp chuyên ngành:", "DCCNTT.14.3"),
        ("Lớp tín chỉ:", "Đồ án chuyên ngành CNPM-1-1-26(N05)")
    ]

    for idx, (label, val) in enumerate(info_data):
        r = table_author.rows[idx]
        c0, c1 = r.cells[0], r.cells[1]
        c0.width = Inches(2.5)
        c1.width = Inches(3.6)
        
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(label)
        r0.bold = True
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(13)
        
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(val)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(13)

    # Footer trang bìa
    p_ft = doc.add_paragraph()
    p_ft.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ft.paragraph_format.space_before = Pt(60)
    p_ft.paragraph_format.space_after = Pt(0)
    r_ft = p_ft.add_run("HÀ NỘI - NĂM 2026")
    r_ft.bold = True
    r_ft.font.name = 'Times New Roman'
    r_ft.font.size = Pt(13)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 2. TRANG PHỤ BÌA & BẢNG PHÂN CÔNG NHIỆM VỤ
    # -------------------------------------------------------------
    add_heading_1("THÔNG TIN ĐỒ ÁN VÀ PHÂN CÔNG NHIỆM VỤ")

    add_p("Học phần: Đồ án chuyên ngành Công nghệ phần mềm", bold=True)
    add_p("Tên đề tài: Hệ thống đặt vé và quản lý suất chiếu rạp chiếu phim (Cinestar Cinema)", bold=True)
    add_p("Chủ đề: Xây dựng Website, Web Application theo mô hình kiến trúc MVC", italic=True)

    add_table_custom(
        "Bảng 0.1. Phân công nhiệm vụ chi tiết giữa các thành viên Nhóm 10",
        ["STT", "Họ và tên", "Mã sinh viên", "Nhiệm vụ phụ trách", "Tỷ lệ đóng góp"],
        [
            ["1", "Nguyễn Mạnh Quyết\n(Trưởng nhóm)", "20231053", 
             "- Phụ trách phân hệ Quản lý (Manager) & Quản trị viên (Admin).\n"
             "- Thiết kế kiến trúc MVC Backend, thiết kế CSDL chuẩn hóa 3NF.\n"
             "- Cài đặt thuật toán kiểm tra xung đột suất chiếu (Conflict Detector).\n"
             "- Xây dựng Dashboard thống kê doanh thu, tỷ lệ lấp đầy rạp (Chart.js).\n"
             "- Viết và thực thi bộ kiểm thử tự động (Automated Test Suite).", "100%"],
            ["2", "Hà Thái Bảo\n(Thành viên)", "20231045", 
             "- Phụ trách phân hệ Khách hàng (Client) & Nhân viên quầy (Staff).\n"
             "- Thiết kế giao diện UI/UX Responsive, Master Layout EJS.\n"
             "- Lập trình module Sơ đồ chọn ghế động và cơ chế khóa giữ ghế 5 phút.\n"
             "- Xây dựng phân hệ Soát vé QR Code và kiểm tra gian lận vé tại quầy POS.\n"
             "- Chuẩn bị kịch bản demo, quay video và rà soát tài liệu báo cáo.", "100%"]
        ],
        col_widths=[0.6, 1.4, 1.0, 2.5, 0.8],
        source="Nhóm 10 - Biên bản họp phân công công việc"
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # 3. LỜI CẢM ƠN
    # -------------------------------------------------------------
    add_heading_1("LỜI CẢM ƠN")

    add_p("Lời đầu tiên, nhóm tác giả xin được gửi lời cảm ơn chân thành và sâu sắc nhất tới Ban Giám hiệu Trường Đại học Công nghệ Đông Á, Ban Chủ nhiệm Khoa Công nghệ Thông tin đã tạo điều kiện học tập thuận lợi và đưa học phần Đồ án chuyên ngành Công nghệ phần mềm vào chương trình đào tạo. Học phần này là cơ hội vô cùng quý báu giúp sinh viên củng cố kiến thức lý thuyết, rèn luyện kỹ năng thực hành phân tích, thiết kế và phát triển phần mềm theo chuẩn mực công nghiệp hiện đại.")

    add_p("Đặc biệt, nhóm chúng em xin bày tỏ lòng biết ơn sâu sắc tới các Thầy/Cô giảng viên phụ trách học phần Đồ án chuyên ngành Công nghệ phần mềm. Trong suốt quá trình thực hiện đồ án 7 tuần, Thầy/Cô đã luôn tận tình hướng dẫn, định hướng nghiên cứu, chỉ bảo cặn kẽ những phương pháp tiếp cận đúng đắn từ khâu khảo sát hiện trạng, đặc tả yêu cầu theo chuẩn ISO/IEC và IEEE, đến kỹ thuật thiết kế biểu đồ UML, chuẩn hóa cơ sở dữ liệu và tối ưu hóa giải thuật.")

    add_p("Mặc dù nhóm đã dành trọn vẹn tâm huyết và nỗ lực tối đa để hoàn thiện sản phẩm cũng như cuốn báo cáo thuyết minh này, song do kiến thức và kinh nghiệm thực tế còn hạn chế, đồ án chắc chắn không thể tránh khỏi những thiếu sót nhất định. Nhóm chúng em rất mong nhận được những ý kiến đóng góp, nhận xét và phê bình quý báu từ quý Thầy/Cô hội đồng để đề tài được hoàn thiện hơn nữa và có thể ứng dụng thực tiễn trong tương lai.")

    add_p("Chúng em xin kính chúc quý Thầy/Cô luôn dồi dào sức khỏe, hạnh phúc và gặt hái được nhiều thành công rực rỡ trong sự nghiệp trồng người cao quý!", italic=True)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 4. LỜI MỞ ĐẦU
    # -------------------------------------------------------------
    add_heading_1("LỜI MỞ ĐẦU")

    add_p("Trong kỷ nguyên chuyển đổi số và công nghệ 4.0 hiện nay, ngành công nghiệp điện ảnh và giải trí tại Việt Nam đang có những bước chuyển mình mạnh mẽ. Các cụm rạp chiếu phim hiện đại như Cinestar, CGV, Lotte Cinema không chỉ đóng vai trò là nơi giải trí phục vụ công chúng mà còn là những doanh nghiệp dịch vụ có quy mô vận hành phức tạp với lưu lượng khách hàng khổng lồ mỗi ngày. Phương thức bán vé truyền thống tại quầy với việc ghi chép thủ công, in vé đơn lẻ và xếp lịch chiếu trên giấy tờ hoặc bảng tính rời rạc đã bộc lộ hàng loạt bất cập nghiêm trọng: hiện tượng quá tải và ùn tắc tại quầy vé vào các khung giờ cao điểm, nguy cơ xung đột lịch chiếu giữa các phim trong cùng phòng chiếu, sự cố bán trùng ghế ngồi và khó khăn trong việc kiểm soát doanh thu thời gian thực.")

    add_p("Để giải quyết triệt để những thách thức trên, việc số hóa toàn diện quy trình vận hành rạp thông qua một hệ thống Web Application tích hợp là yêu cầu sống còn. Đề tài 'Hệ thống đặt vé và quản lý suất chiếu rạp chiếu phim (Cinestar Cinema)' được nhóm chúng em lựa chọn nghiên cứu và phát triển nhằm mang đến giải pháp toàn diện cho cả 4 nhóm tác nhân: Khách hàng có thể dễ dàng tra cứu phim, chọn vị trí ghế ngồi trực quan theo phòng chiếu thực tế, đặt combo bắp nước, thanh toán trực tuyến an toàn và nhận vé điện tử mã QR Code tức thì; Nhân viên có công cụ bán vé tại quầy (POS) và soát vé QR siêu tốc bằng camera; Quản lý rạp sở hữu Dashboard phân tích doanh thu, tỷ lệ lấp đầy rạp và công cụ xếp lịch suất chiếu thông minh tích hợp thuật toán tự động ngăn chặn xung đột phòng/giờ chiếu; Quản trị viên quản lý chặt chẽ người dùng và phân quyền RBAC.")

    add_p("Báo cáo thuyết minh này được xây dựng bám sát theo Đề cương Kế hoạch 7 tuần của học phần Đồ án chuyên ngành CNPM, đáp ứng đầy đủ các tiêu chí kỹ thuật chuẩn mực (ISO/IEC 25010, IEEE 830) và các hướng dẫn trình bày học thuật. Báo cáo được cấu trúc thành 5 chương chính như sau:")

    add_bullet("Trình bày thực trạng quản lý rạp chiếu phim truyền thống, yêu cầu nghiệp vụ đa tác nhân, mục tiêu tổng quát và cụ thể, đối tượng phạm vi nghiên cứu và đề xuất giải pháp kỹ thuật tổng thể.", "Chương I: Tổng quan về đề tài -");
    add_bullet("Trình bày kết quả khảo sát thực tế các cụm rạp, thu thập bộ dữ liệu phim ảnh, phòng chiếu, bảng giá vé; phân tích chi tiết tác nhân người dùng, đặc tả 20 yêu cầu chức năng (FR) và các yêu cầu phi chức năng (NFR) theo chuẩn ISO/IEC 25010.", "Chương II: Tổng hợp, phân tích và đánh giá thực tế -");
    add_bullet("Trình bày kiến thức nền tảng về kiến trúc MVC (Model - View - Controller), quy trình Agile/Scrum, hệ sinh thái công nghệ sử dụng và nghiên cứu chuyên sâu về 3 thuật toán kỹ thuật cốt lõi: Thuật toán kiểm tra xung đột suất chiếu, Kỹ thuật khóa giữ ghế tạm thời (5 phút) và Kỹ thuật soát vé QR chống gian lận.", "Chương III: Cơ sở lý thuyết -");
    add_bullet("Trình bày phân tích ca sử dụng (8 bảng đặc tả Use Case chi tiết), biểu đồ phân rã chức năng (FDD), các biểu đồ Use Case, biểu đồ hoạt động (Activity Diagrams); thiết kế kiến trúc MVC với Class Diagrams, Sequence Diagrams, State Diagrams; thiết kế CSDL chuẩn hóa 3NF có RBAC, Từ điển dữ liệu 12 bảng và Thiết kế giao diện phác thảo (Wireframes) màn hình chọn ghế, trang chủ, dashboard, POS.", "Chương IV: Phân tích và thiết kế hệ thống -");
    add_bullet("Trình bày việc cài đặt môi trường, cấu trúc mã nguồn MVC, kết quả triển khai giao diện và chức năng của 4 phân hệ (11 chức năng chính); kết quả kiểm thử phần mềm toàn diện với bộ 17 Test Cases tự động đạt 100% PASS; đánh giá chỉ số phi chức năng và bộ câu hỏi định hướng vấn đáp bảo vệ.", "Chương V: Cài đặt và triển khai -");

    doc.add_page_break()

    # -------------------------------------------------------------
    # 5. MỤC LỤC TỔNG QUAN
    # -------------------------------------------------------------
    add_heading_1("MỤC LỤC")

    toc_entries = [
        ("LỜI CẢM ƠN", "3"),
        ("LỜI MỞ ĐẦU", "4"),
        ("DANH MỤC CÁC TỪ VIẾT TẮT", "8"),
        ("DANH MỤC HÌNH VẼ", "9"),
        ("DANH MỤC BẢNG BIỂU", "10"),
        ("CHƯƠNG I. TỔNG QUAN VỀ ĐỀ TÀI", "11"),
        ("  1.1. Đặt vấn đề", "11"),
        ("  1.2. Yêu cầu nghiệp vụ", "12"),
        ("  1.3. Mục tiêu của đề tài", "14"),
        ("    1.3.1. Mục tiêu tổng quát", "14"),
        ("    1.3.2. Mục tiêu cụ thể", "14"),
        ("    1.3.3. Đối tượng và phạm vi nghiên cứu", "14"),
        ("    1.3.4. Ý nghĩa khoa học và thực tiễn của đề tài", "15"),
        ("  1.4. Đề xuất giải pháp nghiệp vụ và công nghệ sử dụng", "15"),
        ("  1.5. Thiết kế và đánh giá kiến trúc an toàn bảo mật hệ thống", "16"),
        ("CHƯƠNG II. TỔNG HỢP, PHÂN TÍCH VÀ ĐÁNH GIÁ THỰC TẾ", "21"),
        ("  2.1. Tổng hợp và thu thập dữ liệu", "21"),
        ("    2.1.1. Mục tiêu khảo sát", "21"),
        ("    2.1.2. Phương pháp khảo sát và thu thập dữ liệu", "22"),
        ("    2.1.3. Nội dung khảo sát", "24"),
        ("    2.1.4. Kết quả khảo sát", "25"),
        ("  2.2. Phân tích dữ liệu", "26"),
        ("    2.2.1. Người dùng (Tác nhân hệ thống)", "26"),
        ("    2.2.2. Yêu cầu chức năng", "28"),
        ("    2.2.3. Yêu cầu phi chức năng", "31"),
        ("CHƯƠNG III. CƠ SỞ LÝ THUYẾT", "34"),
        ("  3.1. Kiến thức phần mềm", "34"),
        ("    3.1.1. Kiến trúc MVC (Model - View - Controller)", "34"),
        ("    3.1.2. Quy trình phát triển phần mềm theo mô hình Agile/Scrum", "34"),
        ("  3.2. Các công nghệ sử dụng", "35"),
        ("  3.3. Thuật toán và kỹ thuật chuyên sâu áp dụng", "36"),
        ("    3.3.1. Thuật toán kiểm tra xung đột suất chiếu", "36"),
        ("    3.3.2. Kỹ thuật khóa giữ ghế tạm thời (Temporary Seat Lock)", "37"),
        ("    3.3.3. Kỹ thuật vé điện tử QR Code & Ngăn chặn gian lận", "38"),
        ("CHƯƠNG IV. PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG", "39"),
        ("  4.1. Phân tích hệ thống", "39"),
        ("    4.1.1. Xác định Use Case cho các tác nhân", "39"),
        ("    4.1.2. Mô tả Use Case chi tiết (Use Case Specifications)", "39"),
        ("    4.1.3. Biểu đồ phân cấp chức năng (FDD)", "43"),
        ("    4.1.4. Biểu đồ Use Case (Tổng quát & Phân rã 4 tác nhân)", "44"),
        ("    4.1.5. Biểu đồ hoạt động (Activity Diagrams)", "47"),
        ("  4.2. Thiết kế hệ thống theo mô hình MVC", "50"),
        ("    4.2.1. Thiết kế hướng đối tượng và kiến trúc phân tầng MVC", "50"),
        ("    4.2.2. Thiết kế cơ sở dữ liệu chuẩn hóa 3NF có phân quyền RBAC", "55"),
        ("    4.2.3. Thiết kế giao diện người dùng (Wireframes phác thảo)", "63"),
        ("CHƯƠNG V. CÀI ĐẶT VÀ TRIỂN KHAI", "67"),
        ("  5.1. Cài đặt hệ sinh thái MVC", "67"),
        ("  5.2. Kết quả triển khai chức năng và giao diện", "69"),
        ("  5.3. Kiểm thử hệ thống", "70"),
        ("  5.4. Chuẩn bị nội dung vấn đáp bảo vệ đồ án", "73"),
        ("KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", "76"),
        ("TÀI LIỆU THAM KHẢO", "78"),
        ("PHỤ LỤC: HƯỚNG DẪN CÀI ĐẶT & TÀI KHOẢN MẪU", "79")
    ]

    for title, pg in toc_entries:
        p_toc = doc.add_paragraph()
        p_toc.paragraph_format.line_spacing = 1.15
        p_toc.paragraph_format.space_before = Pt(1)
        p_toc.paragraph_format.space_after = Pt(2)
        r_t = p_toc.add_run(title)
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(12)
        if not title.startswith("  "):
            r_t.bold = True
        # Dot leader simulation
        dots_len = max(5, 75 - len(title))
        r_d = p_toc.add_run(" " + "." * dots_len + " ")
        r_d.font.name = 'Times New Roman'
        r_d.font.size = Pt(11)
        r_p = p_toc.add_run(pg)
        r_p.font.name = 'Times New Roman'
        r_p.font.size = Pt(12)
        if not title.startswith("  "):
            r_p.bold = True

    doc.add_page_break()

    # -------------------------------------------------------------
    # 6. DANH MỤC CÁC TỪ VIẾT TẮT
    # -------------------------------------------------------------
    add_heading_1("DANH MỤC CÁC TỪ VIẾT TẮT")

    abbr_data = [
        ["1", "MVC", "Model - View - Controller (Mô hình kiến trúc phần mềm 3 thành phần)"],
        ["2", "RBAC", "Role-Based Access Control (Mô hình kiểm soát truy cập dựa trên vai trò)"],
        ["3", "CSDL", "Cơ sở dữ liệu (Database)"],
        ["4", "DBMS", "Database Management System (Hệ quản trị cơ sở dữ liệu)"],
        ["5", "3NF", "Third Normal Form (Dạng chuẩn 3 của Cơ sở dữ liệu quan hệ)"],
        ["6", "DDL", "Data Definition Language (Ngôn ngữ định nghĩa dữ liệu SQL)"],
        ["7", "DML", "Data Manipulation Language (Ngôn ngữ thao tác dữ liệu SQL)"],
        ["8", "PK", "Primary Key (Khóa chính trong bảng CSDL)"],
        ["9", "FK", "Foreign Key (Khóa ngoại trong bảng CSDL)"],
        ["10", "UC", "Use Case (Ca sử dụng trong phân tích phần mềm UML)"],
        ["11", "FDD", "Functional Decomposition Diagram (Biểu đồ phân cấp chức năng)"],
        ["12", "ERD", "Entity - Relationship Diagram (Sơ đồ quan hệ thực thể)"],
        ["13", "UML", "Unified Modeling Language (Ngôn ngữ mô hình hóa thống nhất)"],
        ["14", "POS", "Point Of Sale (Điểm bán vé tại quầy của nhân viên)"],
        ["15", "QR Code", "Quick Response Code (Mã phản hồi nhanh 2 chiều)"],
        ["16", "API", "Application Programming Interface (Giao diện lập trình ứng dụng)"],
        ["17", "UI / UX", "User Interface / User Experience (Giao diện / Trải nghiệm người dùng)"],
        ["18", "FR", "Functional Requirements (Yêu cầu chức năng)"],
        ["19", "NFR", "Non-Functional Requirements (Yêu cầu phi chức năng)"],
        ["20", "TTL", "Time To Live (Thời gian sống / tồn tại của dữ liệu khóa giữ ghế)"],
        ["21", "ISO", "International Organization for Standardization (Tổ chức Tiêu chuẩn hóa Quốc tế)"],
        ["22", "IEEE", "Institute of Electrical and Electronics Engineers (Viện Kỹ sư Điện & Điện tử)"],
        ["23", "EJS", "Embedded JavaScript templates (Bộ máy sinh mẫu giao diện HTML)"]
    ]

    add_table_custom(
        "Bảng 0.2. Danh mục thuật ngữ và các từ viết tắt trong đồ án",
        ["STT", "Từ viết tắt", "Giải thích nghĩa đầy đủ và ngữ cảnh sử dụng"],
        abbr_data,
        col_widths=[0.6, 1.4, 4.3],
        align_cols=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT],
        source="Nhóm 10 - Tổng hợp chuẩn thuật ngữ chuyên ngành"
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # 7. DANH MỤC HÌNH VẼ
    # -------------------------------------------------------------
    add_heading_1("DANH MỤC HÌNH VẼ")

    figures_list = [
        ("Hình 4.1. Biểu đồ phân cấp chức năng hệ thống (FDD - Draw.io)", "44"),
        ("Hình 4.2. Biểu đồ Use Case tổng quát hệ thống rạp chiếu phim (Draw.io)", "45"),
        ("Hình 4.3. Biểu đồ Use Case phân rã phân hệ Khách hàng (Draw.io)", "46"),
        ("Hình 4.4. Biểu đồ Use Case phân rã phân hệ Nhân viên quầy (Draw.io)", "46"),
        ("Hình 4.5. Biểu đồ Use Case phân rã phân hệ Quản lý rạp (Draw.io)", "47"),
        ("Hình 4.6. Biểu đồ Use Case phân rã phân hệ Quản trị viên (Draw.io)", "47"),
        ("Hình 4.7. Biểu đồ hoạt động: Quy trình Đặt vé và chọn ghế của Khách hàng (PlantUML)", "48"),
        ("Hình 4.8. Biểu đồ hoạt động: Quy trình Lập lịch suất chiếu của Manager (PlantUML)", "49"),
        ("Hình 4.9. Biểu đồ hoạt động: Quy trình Soát vé tại quầy của Staff (PlantUML)", "50"),
        ("Hình 4.10. Biểu đồ lớp (Class Diagram) theo MVC: Nhóm Model và Thực thể CSDL (PlantUML)", "52"),
        ("Hình 4.11. Biểu đồ lớp (Class Diagram) theo MVC: Nhóm Controller và Service (PlantUML)", "52"),
        ("Hình 4.12. Biểu đồ tuần tự: Quy trình Đặt vé và Thanh toán của Khách hàng (PlantUML)", "52"),
        ("Hình 4.13. Biểu đồ tuần tự: Quy trình Lập suất chiếu mới & Chống xung đột (PlantUML)", "53"),
        ("Hình 4.14. Biểu đồ tuần tự: Quy trình Soát vé QR & Cảnh báo gian lận của Staff (PlantUML)", "53"),
        ("Hình 4.15. Biểu đồ chuyển trạng thái của Ghế ngồi (Seat State Machine - PlantUML)", "54"),
        ("Hình 4.16. Biểu đồ chuyển trạng thái của Vé xem phim (Ticket State Machine - PlantUML)", "55"),
        ("Hình 4.17. Sơ đồ quan hệ thực thể (ERD) chuẩn hóa 3NF có phân quyền RBAC (Draw.io)", "55"),
        ("Hình 4.18. Thiết kế giao diện phác thảo: Màn hình Sơ đồ chọn ghế xem phim (Wireframe)", "63"),
        ("Hình 4.19. Thiết kế giao diện phác thảo: Màn hình Trang chủ khách hàng (Wireframe)", "64"),
        ("Hình 4.20. Thiết kế giao diện phác thảo: Màn hình Lập suất chiếu chống xung đột (Wireframe)", "65"),
        ("Hình 4.21. Thiết kế giao diện phác thảo: Màn hình Soát vé QR và Bán vé quầy POS (Wireframe)", "66"),
        ("Hình 4.22. Thiết kế giao diện phác thảo: Màn hình Dashboard quản lý doanh thu (Wireframe)", "66")
    ]

    for cap, pg in figures_list:
        p_fig = doc.add_paragraph()
        p_fig.paragraph_format.line_spacing = 1.15
        p_fig.paragraph_format.space_before = Pt(1)
        p_fig.paragraph_format.space_after = Pt(2)
        r_c = p_fig.add_run(cap)
        r_c.font.name = 'Times New Roman'
        r_c.font.size = Pt(12)
        dots_len = max(5, 75 - len(cap))
        r_d = p_fig.add_run(" " + "." * dots_len + " ")
        r_d.font.name = 'Times New Roman'
        r_d.font.size = Pt(11)
        r_p = p_fig.add_run(pg)
        r_p.font.name = 'Times New Roman'
        r_p.font.size = Pt(12)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 8. DANH MỤC BẢNG BIỂU
    # -------------------------------------------------------------
    add_heading_1("DANH MỤC BẢNG BIỂU")

    tables_list = [
        ("Bảng 0.1. Phân công nhiệm vụ chi tiết giữa các thành viên Nhóm 10", "2"),
        ("Bảng 0.2. Danh mục thuật ngữ và các từ viết tắt trong đồ án", "8"),
        ("Bảng 1.1. Ma trận đối chuẩn 20 tiêu chuẩn an toàn bảo mật hệ thống Cinestar Cinema", "17"),
        ("Bảng 2.1. Bảng tổng hợp nội dung khảo sát hệ thống rạp chiếu phim", "24"),
        ("Bảng 2.2. Bảng tổng hợp kết quả phân tích khảo sát", "26"),
        ("Bảng 2.3. Ma trận phân quyền RBAC giữa các nhóm người dùng trong hệ thống", "28"),
        ("Bảng 2.4. Bảng đặc tả yêu cầu phi chức năng theo chuẩn quốc tế ISO/IEC 25010", "33"),
        ("Bảng 4.1. Đặc tả Use Case UC01: Đăng ký / Đăng nhập tài khoản", "39"),
        ("Bảng 4.2. Đặc tả Use Case UC02: Đặt vé trực tuyến & Chọn ghế ngồi", "40"),
        ("Bảng 4.3. Đặc tả Use Case UC03: Bán vé trực tiếp tại quầy POS", "40"),
        ("Bảng 4.4. Đặc tả Use Case UC04: Quét mã QR Soát vé & Báo gian lận", "41"),
        ("Bảng 4.5. Đặc tả Use Case UC05: Lập lịch suất chiếu chống trùng giờ", "41"),
        ("Bảng 4.6. Đặc tả Use Case UC06: Quản lý danh mục phim chiếu rạp", "42"),
        ("Bảng 4.7. Đặc tả Use Case UC07: Quản lý phòng chiếu & Cấu hình ghế", "43"),
        ("Bảng 4.8. Đặc tả Use Case UC08: Thống kê doanh thu & Tỷ lệ lấp đầy", "43"),
        ("Bảng 4.9. Cấu trúc bảng CSDL Roles (Vai trò người dùng)", "55"),
        ("Bảng 4.10. Cấu trúc bảng CSDL Users (Tài khoản người dùng)", "56"),
        ("Bảng 4.11. Cấu trúc bảng CSDL Movies (Thông tin phim chiếu)", "56"),
        ("Bảng 4.12. Cấu trúc bảng CSDL Rooms (Phòng chiếu phim)", "57"),
        ("Bảng 4.13. Cấu trúc bảng CSDL Seats (Ghế ngồi trong phòng)", "57"),
        ("Bảng 4.14. Cấu trúc bảng CSDL Showtimes (Lịch suất chiếu)", "58"),
        ("Bảng 4.15. Cấu trúc bảng CSDL Combos (Combo bắp nước)", "58"),
        ("Bảng 4.16. Cấu trúc bảng CSDL Bookings (Đơn đặt vé)", "59"),
        ("Bảng 4.17. Cấu trúc bảng CSDL Tickets (Chi tiết vé điện tử)", "60"),
        ("Bảng 4.18. Cấu trúc bảng CSDL Booking_Combos (Chi tiết combo theo đơn)", "60"),
        ("Bảng 4.19. Cấu trúc bảng CSDL Seat_Locks (Khóa giữ ghế tạm thời)", "61"),
        ("Bảng 4.20. Cấu trúc bảng CSDL System_Settings (Cấu hình rạp)", "61"),
        ("Bảng 5.1. Bảng kịch bản 17 ca kiểm thử (Test Cases) chi tiết của hệ thống", "70"),
        ("Bảng 5.2. Kết quả kiểm thử tự động (Automated Test Suite) đạt 17/17 PASS", "72"),
        ("Bảng 5.3. Bảng đo lường thực tế các chỉ số phi chức năng của hệ thống", "73")
    ]

    for cap, pg in tables_list:
        p_tbl = doc.add_paragraph()
        p_tbl.paragraph_format.line_spacing = 1.15
        p_tbl.paragraph_format.space_before = Pt(1)
        p_tbl.paragraph_format.space_after = Pt(2)
        r_c = p_tbl.add_run(cap)
        r_c.font.name = 'Times New Roman'
        r_c.font.size = Pt(12)
        dots_len = max(5, 75 - len(cap))
        r_d = p_tbl.add_run(" " + "." * dots_len + " ")
        r_d.font.name = 'Times New Roman'
        r_d.font.size = Pt(11)
        r_p = p_tbl.add_run(pg)
        r_p.font.name = 'Times New Roman'
        r_p.font.size = Pt(12)

    doc.add_page_break()
    print("Cover, Intro, TOC, and Lists generated successfully.")
