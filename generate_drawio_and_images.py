# Script tạo các file .drawio XML và xuất hình ảnh chất lượng cao 300 DPI
# Tuân thủ nghiêm ngặt:
# 1. Dùng nét thẳng (orthogonal lines), tránh vẽ nét cong và chồng lên nhau
# 2. Không dùng màu (đen trắng / grayscale, nền trắng, chữ đen, viền đen)
# 3. Vẽ to, rõ ràng, dễ nhìn trong Word
# 4. Kiểm tra chính tả tiếng Việt từng mục
# 5. Thiết kế giao diện phác thảo như ảnh trên (media_1791908941148.png)
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.autolayout'] = True

img_dir = os.path.join('report_assets', 'images')
drawio_dir = os.path.join('report_assets', 'drawio')
os.makedirs(img_dir, exist_ok=True)
os.makedirs(drawio_dir, exist_ok=True)

# Helper function to draw an actor stick figure in black and white
def draw_actor(ax, x, y, name, scale=1.0):
    head = patches.Circle((x, y + 4*scale), 1.5*scale, facecolor='white', edgecolor='black', linewidth=1.5)
    ax.add_patch(head)
    # Body
    ax.plot([x, x], [y + 2.5*scale, y - 1.5*scale], color='black', linewidth=1.5)
    # Arms
    ax.plot([x - 2.5*scale, x + 2.5*scale], [y + 1*scale, y + 1*scale], color='black', linewidth=1.5)
    # Legs
    ax.plot([x, x - 2*scale], [y - 1.5*scale, y - 5*scale], color='black', linewidth=1.5)
    ax.plot([x, x + 2*scale], [y - 1.5*scale, y - 5*scale], color='black', linewidth=1.5)
    # Label
    ax.text(x, y - 7.5*scale, name, ha='center', va='top', fontsize=10, fontweight='bold')

# Helper function to draw a Use Case ellipse in black and white
def draw_usecase(ax, x, y, text, w=24, h=7):
    ellipse = patches.Ellipse((x, y), w, h, facecolor='white', edgecolor='black', linewidth=1.4)
    ax.add_patch(ellipse)
    ax.text(x, y, text, ha='center', va='center', fontsize=9.5)

# Helper function to draw an orthogonal line between two points
def draw_ortho_line(ax, x1, y1, x2, y2, linestyle='-', label=None):
    mid_x = (x1 + x2) / 2
    ax.plot([x1, mid_x], [y1, y1], color='black', linewidth=1.2, linestyle=linestyle)
    ax.plot([mid_x, mid_x], [y1, y2], color='black', linewidth=1.2, linestyle=linestyle)
    ax.plot([mid_x, x2], [y2, y2], color='black', linewidth=1.2, linestyle=linestyle)
    if label:
        ax.text(mid_x, (y1 + y2)/2, label, ha='center', va='center', fontsize=8, 
                bbox=dict(boxstyle="square,pad=0.2", fc="white", ec="none"))

# -------------------------------------------------------------
# 1. BIỂU ĐỒ PHÂN CẤP CHỨC NĂNG (FDD)
# -------------------------------------------------------------
def generate_fdd():
    fig, ax = plt.subplots(figsize=(16, 9.5), dpi=300)
    ax.set_xlim(0, 160)
    ax.set_ylim(0, 105)
    ax.axis('off')

    # Root Box
    root_box = patches.Rectangle((35, 90), 90, 12, facecolor='white', edgecolor='black', linewidth=1.8)
    ax.add_patch(root_box)
    ax.text(80, 96, "HỆ THỐNG ĐẶT VÉ VÀ QUẢN LÝ SUẤT CHIẾU RẠP CHIẾU PHIM\n(CINESTAR CINEMA SYSTEM)", 
            ha='center', va='center', fontsize=12, fontweight='bold')

    modules = [
        {"name": "1.0 PHÂN HỆ KHÁCH HÀNG", "x": 5, "w": 35, "subs": [
            "1.1 Tra cứu phim & Lịch chiếu",
            "1.2 Sơ đồ chọn ghế trực quan",
            "1.3 Chọn combo bắp nước",
            "1.4 Khóa ghế & Thanh toán 5p",
            "1.5 Vé điện tử & Mã QR bảo mật",
            "1.6 Lịch sử đặt vé & Tài khoản"
        ]},
        {"name": "2.0 PHÂN HỆ NHÂN VIÊN", "x": 43, "w": 35, "subs": [
            "2.1 Bán vé tại quầy (POS)",
            "2.2 Quét mã QR soát vé tự động",
            "2.3 Kiểm tra vé hợp lệ & Ghế",
            "2.4 Cảnh báo vé gian lận / Đã dùng",
            "2.5 Lịch sử & Nhật ký soát vé",
            "2.6 In hóa đơn & vé vật lý"
        ]},
        {"name": "3.0 PHÂN HỆ QUẢN LÝ", "x": 81, "w": 35, "subs": [
            "3.1 Quản lý danh mục phim",
            "3.2 Quản lý phòng & Cấu hình ghế",
            "3.3 Lập lịch suất chiếu phim",
            "3.4 Thuật toán chống xung đột",
            "3.5 Báo cáo doanh thu & Lấp đầy",
            "3.6 Quản lý giá vé & Bắp nước"
        ]},
        {"name": "4.0 PHÂN HỆ QUẢN TRỊ", "x": 119, "w": 35, "subs": [
            "4.1 Quản lý người dùng hệ thống",
            "4.2 Phân quyền vai trò RBAC",
            "4.3 Cài đặt thông số hệ thống",
            "4.4 Giám sát nhật ký (Audit Log)",
            "4.5 Khóa / Mở tài khoản",
            "4.6 An toàn dữ liệu & Sao lưu"
        ]}
    ]

    # Orthogonal spine
    ax.plot([80, 80], [90, 83], color='black', linewidth=1.5)
    ax.plot([22.5, 136.5], [83, 83], color='black', linewidth=1.5)

    for mod in modules:
        mx = mod["x"]
        mw = mod["w"]
        cx = mx + mw / 2

        ax.plot([cx, cx], [83, 76], color='black', linewidth=1.5)
        box = patches.Rectangle((mx, 68), mw, 8, facecolor='white', edgecolor='black', linewidth=1.5)
        ax.add_patch(box)
        ax.text(cx, 72, mod["name"], ha='center', va='center', fontsize=10.5, fontweight='bold')

        # Spine trunk for subs
        ax.plot([cx - 10, cx - 10], [68, 12], color='black', linewidth=1.2)

        y = 60
        for sub in mod["subs"]:
            ax.plot([cx - 10, cx - 6], [y, y], color='black', linewidth=1.2)
            sub_box = patches.Rectangle((cx - 6, y - 3.2), mw - 8, 6.4, facecolor='white', edgecolor='black', linewidth=1.0)
            ax.add_patch(sub_box)
            ax.text(cx - 4, y, sub, ha='left', va='center', fontsize=9.5)
            y -= 9.0

    plt.tight_layout()
    fpath = os.path.join(img_dir, 'drawio_fdd.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated:", fpath)

# -------------------------------------------------------------
# 2. BIỂU ĐỒ USE CASE TỔNG QUÁT
# -------------------------------------------------------------
def generate_uc_tong_quat():
    fig, ax = plt.subplots(figsize=(16, 11), dpi=300)
    ax.set_xlim(0, 160)
    ax.set_ylim(0, 120)
    ax.axis('off')

    # System boundary box
    sys_box = patches.Rectangle((35, 8), 90, 104, facecolor='white', edgecolor='black', linewidth=1.6)
    ax.add_patch(sys_box)
    ax.text(80, 108, "HỆ THỐNG ĐẶT VÉ VÀ QUẢN LÝ SUẤT CHIẾU CINESTAR", ha='center', va='center', fontsize=12, fontweight='bold')

    # Actors
    # Khách hàng (Left top)
    draw_actor(ax, 16, 85, "Khách hàng\n(Client)", scale=1.1)
    # Nhân viên (Left bottom)
    draw_actor(ax, 16, 32, "Nhân viên quầy\n(Staff)", scale=1.1)
    # Quản lý (Right top)
    draw_actor(ax, 144, 85, "Quản lý rạp\n(Manager)", scale=1.1)
    # Quản trị viên (Right bottom)
    draw_actor(ax, 144, 32, "Quản trị viên\n(Admin)", scale=1.1)

    # Use cases
    # Common / Shared
    draw_usecase(ax, 80, 98, "Đăng nhập & Xác thực", w=28, h=6.5)

    # Client Use Cases (Left side of system)
    ucs_client = [
        (60, 87, "Tra cứu phim & Lịch chiếu"),
        (60, 76, "Chọn suất chiếu & Phòng"),
        (60, 65, "Chọn ghế & Khóa giữ 5p"),
        (60, 54, "Chọn combo bắp nước"),
        (60, 43, "Thanh toán & Nhận vé QR"),
        (60, 32, "Xem lịch sử đặt vé cá nhân")
    ]

    # Staff Use Cases (Bottom left)
    ucs_staff = [
        (60, 21, "Bán vé tại quầy (POS)"),
        (80, 14, "Soát vé QR & Báo gian lận")
    ]

    # Manager Use Cases (Right side of system)
    ucs_manager = [
        (100, 87, "Quản lý danh mục phim"),
        (100, 76, "Quản lý phòng & Sơ đồ ghế"),
        (100, 65, "Lập suất chiếu & Chống trùng"),
        (100, 54, "Quản lý bảng giá & Combo"),
        (100, 43, "Dashboard & Tỷ lệ lấp đầy %")
    ]

    # Admin Use Cases (Right bottom)
    ucs_admin = [
        (100, 32, "Quản lý người dùng & RBAC"),
        (100, 21, "Cấu hình tham số hệ thống"),
        (80, 25, "Nhật ký giao dịch (Audit Log)")
    ]

    for (x, y, text) in ucs_client:
        draw_usecase(ax, x, y, text, w=28, h=6.5)
        ax.plot([20, 35, 46], [85, y, y], color='black', linewidth=1.1)

    for (x, y, text) in ucs_staff:
        draw_usecase(ax, x, y, text, w=28, h=6.5)
        ax.plot([20, 35, 46], [32, y, y], color='black', linewidth=1.1)

    for (x, y, text) in ucs_manager:
        draw_usecase(ax, x, y, text, w=28, h=6.5)
        ax.plot([140, 125, 114], [85, y, y], color='black', linewidth=1.1)

    for (x, y, text) in ucs_admin:
        draw_usecase(ax, x, y, text, w=28, h=6.5)
        ax.plot([140, 125, 114], [32, y, y], color='black', linewidth=1.1)

    # Actor to Login lines
    ax.plot([20, 35, 66], [85, 98, 98], color='black', linewidth=1.1)
    ax.plot([20, 30, 30, 66], [32, 32, 98, 98], color='black', linewidth=1.1)
    ax.plot([140, 125, 94], [85, 98, 98], color='black', linewidth=1.1)
    ax.plot([140, 130, 130, 94], [32, 32, 98, 98], color='black', linewidth=1.1)

    plt.tight_layout()
    fpath = os.path.join(img_dir, 'drawio_usecase_tong_quat.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated:", fpath)

# -------------------------------------------------------------
# 3. BIỂU ĐỒ USE CASE PHÂN RÃ: KHÁCH HÀNG
# -------------------------------------------------------------
def generate_uc_khach_hang():
    fig, ax = plt.subplots(figsize=(15, 9), dpi=300)
    ax.set_xlim(0, 150)
    ax.set_ylim(0, 100)
    ax.axis('off')

    sys_box = patches.Rectangle((35, 8), 105, 86, facecolor='white', edgecolor='black', linewidth=1.6)
    ax.add_patch(sys_box)
    ax.text(87, 89, "PHÂN HỆ KHÁCH HÀNG (CLIENT USE CASES)", ha='center', va='center', fontsize=12, fontweight='bold')

    draw_actor(ax, 16, 50, "Khách hàng\n(Client)", scale=1.2)

    ucs = [
        (65, 80, "UC01. Tra cứu phim"),
        (65, 68, "UC02. Xem lịch chiếu & phòng"),
        (65, 54, "UC03. Chọn ghế ngồi"),
        (65, 40, "UC04. Chọn combo bắp nước"),
        (65, 26, "UC05. Thanh toán trực tuyến"),
        (65, 14, "UC06. Quản lý vé cá nhân")
    ]

    includes = [
        (115, 54, "<<include>>\\nKhóa giữ ghế tạm 5p"),
        (115, 26, "<<include>>\\nSinh mã QR vé"),
        (115, 14, "<<extend>>\\nXem chi tiết vé QR")
    ]

    for (x, y, text) in ucs:
        draw_usecase(ax, x, y, text, w=28, h=7)
        # Orthogonal line from actor
        ax.plot([22, 35, 51], [50, y, y], color='black', linewidth=1.2)

    for (x, y, text) in includes:
        draw_usecase(ax, x, y, text, w=28, h=7)

    # Dashed lines for includes / extends
    ax.plot([79, 101], [54, 54], color='black', linewidth=1.2, linestyle='--')
    ax.text(90, 56, "<<include>>", ha='center', va='bottom', fontsize=8.5)

    ax.plot([79, 101], [26, 26], color='black', linewidth=1.2, linestyle='--')
    ax.text(90, 28, "<<include>>", ha='center', va='bottom', fontsize=8.5)

    ax.plot([79, 101], [14, 14], color='black', linewidth=1.2, linestyle='--')
    ax.text(90, 16, "<<extend>>", ha='center', va='bottom', fontsize=8.5)

    plt.tight_layout()
    fpath = os.path.join(img_dir, 'drawio_usecase_khach_hang.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated:", fpath)

# -------------------------------------------------------------
# 4. BIỂU ĐỒ USE CASE PHÂN RÃ: NHÂN VIÊN (STAFF)
# -------------------------------------------------------------
def generate_uc_nhan_vien():
    fig, ax = plt.subplots(figsize=(15, 8.5), dpi=300)
    ax.set_xlim(0, 150)
    ax.set_ylim(0, 95)
    ax.axis('off')

    sys_box = patches.Rectangle((35, 8), 105, 80, facecolor='white', edgecolor='black', linewidth=1.6)
    ax.add_patch(sys_box)
    ax.text(87, 83, "PHÂN HỆ NHÂN VIÊN (STAFF USE CASES)", ha='center', va='center', fontsize=12, fontweight='bold')

    draw_actor(ax, 16, 48, "Nhân viên quầy\n(Staff)", scale=1.2)

    ucs = [
        (65, 70, "UC07. Bán vé tại quầy (POS)"),
        (65, 52, "UC08. Quét mã QR soát vé"),
        (65, 34, "UC09. Tra cứu vé đã bán"),
        (65, 18, "UC10. Xem lịch sử soát vé")
    ]

    subs = [
        (115, 70, "<<include>>\\nIn vé & Hóa đơn quầy"),
        (115, 52, "<<extend>>\\nBáo động vé gian lận\\n(Đã soát trước đó)"),
        (115, 34, "<<include>>\\nKiểm tra trạng thái ghế")
    ]

    for (x, y, text) in ucs:
        draw_usecase(ax, x, y, text, w=28, h=7)
        ax.plot([22, 35, 51], [48, y, y], color='black', linewidth=1.2)

    for (x, y, text) in subs:
        draw_usecase(ax, x, y, text, w=28, h=7.5)

    ax.plot([79, 101], [70, 70], color='black', linewidth=1.2, linestyle='--')
    ax.text(90, 72, "<<include>>", ha='center', va='bottom', fontsize=8.5)

    ax.plot([79, 101], [52, 52], color='black', linewidth=1.2, linestyle='--')
    ax.text(90, 54, "<<extend>>", ha='center', va='bottom', fontsize=8.5)

    ax.plot([79, 101], [34, 34], color='black', linewidth=1.2, linestyle='--')
    ax.text(90, 36, "<<include>>", ha='center', va='bottom', fontsize=8.5)

    plt.tight_layout()
    fpath = os.path.join(img_dir, 'drawio_usecase_nhan_vien.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated:", fpath)

# -------------------------------------------------------------
# 5. BIỂU ĐỒ USE CASE PHÂN RÃ: QUẢN LÝ (MANAGER)
# -------------------------------------------------------------
def generate_uc_quan_ly():
    fig, ax = plt.subplots(figsize=(15, 9.5), dpi=300)
    ax.set_xlim(0, 150)
    ax.set_ylim(0, 100)
    ax.axis('off')

    sys_box = patches.Rectangle((35, 8), 105, 86, facecolor='white', edgecolor='black', linewidth=1.6)
    ax.add_patch(sys_box)
    ax.text(87, 89, "PHÂN HỆ QUẢN LÝ (MANAGER USE CASES)", ha='center', va='center', fontsize=12, fontweight='bold')

    draw_actor(ax, 16, 50, "Quản lý rạp\n(Manager)", scale=1.2)

    ucs = [
        (65, 78, "UC11. Quản lý danh mục phim"),
        (65, 64, "UC12. Quản lý phòng & Ghế"),
        (65, 50, "UC13. Lập lịch suất chiếu"),
        (65, 36, "UC14. Quản lý giá & Combo"),
        (65, 22, "UC15. Thống kê doanh thu"),
        (65, 12, "UC16. Theo dõi tỷ lệ lấp đầy %")
    ]

    subs = [
        (115, 50, "<<include>>\\nKiểm tra xung đột\\n(ConflictDetector)"),
        (115, 22, "<<include>>\\nBiểu đồ doanh thu 7 ngày")
    ]

    for (x, y, text) in ucs:
        draw_usecase(ax, x, y, text, w=28, h=7)
        ax.plot([22, 35, 51], [50, y, y], color='black', linewidth=1.2)

    for (x, y, text) in subs:
        draw_usecase(ax, x, y, text, w=28, h=7.5)

    ax.plot([79, 101], [50, 50], color='black', linewidth=1.2, linestyle='--')
    ax.text(90, 52, "<<include>>", ha='center', va='bottom', fontsize=8.5)

    ax.plot([79, 101], [22, 22], color='black', linewidth=1.2, linestyle='--')
    ax.text(90, 24, "<<include>>", ha='center', va='bottom', fontsize=8.5)

    plt.tight_layout()
    fpath = os.path.join(img_dir, 'drawio_usecase_quan_ly.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated:", fpath)

# -------------------------------------------------------------
# 6. BIỂU ĐỒ USE CASE PHÂN RÃ: QUẢN TRỊ VIÊN (ADMIN)
# -------------------------------------------------------------
def generate_uc_quan_tri():
    fig, ax = plt.subplots(figsize=(15, 8.5), dpi=300)
    ax.set_xlim(0, 150)
    ax.set_ylim(0, 95)
    ax.axis('off')

    sys_box = patches.Rectangle((35, 8), 105, 80, facecolor='white', edgecolor='black', linewidth=1.6)
    ax.add_patch(sys_box)
    ax.text(87, 83, "PHÂN HỆ QUẢN TRỊ VIÊN (ADMIN USE CASES)", ha='center', va='center', fontsize=12, fontweight='bold')

    draw_actor(ax, 16, 48, "Quản trị viên\n(Admin)", scale=1.2)

    ucs = [
        (65, 70, "UC17. Quản lý người dùng"),
        (65, 52, "UC18. Phân quyền vai trò (RBAC)"),
        (65, 34, "UC19. Cài đặt thông số rạp"),
        (65, 18, "UC20. Giám sát Audit Logs")
    ]

    subs = [
        (115, 70, "<<include>>\\nKhóa / Mở tài khoản"),
        (115, 34, "<<include>>\\nCấu hình thời gian đệm")
    ]

    for (x, y, text) in ucs:
        draw_usecase(ax, x, y, text, w=28, h=7)
        ax.plot([22, 35, 51], [48, y, y], color='black', linewidth=1.2)

    for (x, y, text) in subs:
        draw_usecase(ax, x, y, text, w=28, h=7.5)

    ax.plot([79, 101], [70, 70], color='black', linewidth=1.2, linestyle='--')
    ax.text(90, 72, "<<include>>", ha='center', va='bottom', fontsize=8.5)

    ax.plot([79, 101], [34, 34], color='black', linewidth=1.2, linestyle='--')
    ax.text(90, 36, "<<include>>", ha='center', va='bottom', fontsize=8.5)

    plt.tight_layout()
    fpath = os.path.join(img_dir, 'drawio_usecase_quan_tri.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated:", fpath)

# -------------------------------------------------------------
# 7. BIỂU ĐỒ ERD (ENTITY RELATIONSHIP DIAGRAM) CHUẨN HÓA 3NF
# -------------------------------------------------------------
def generate_erd():
    fig, ax = plt.subplots(figsize=(18, 12), dpi=300)
    ax.set_xlim(0, 180)
    ax.set_ylim(0, 120)
    ax.axis('off')

    # Draw ERD tables with clean orthogonal lines
    def draw_erd_table(x, y, name, fields, w=28, h=22):
        # Header box
        h_box = patches.Rectangle((x, y + h - 5), w, 5, facecolor='white', edgecolor='black', linewidth=1.4)
        ax.add_patch(h_box)
        ax.text(x + w/2, y + h - 2.5, name, ha='center', va='center', fontsize=9.5, fontweight='bold')
        # Body box
        b_box = patches.Rectangle((x, y), w, h - 5, facecolor='white', edgecolor='black', linewidth=1.2)
        ax.add_patch(b_box)
        # Fields
        cur_y = y + h - 7.5
        for f in fields:
            ax.text(x + 1.2, cur_y, f, ha='left', va='center', fontsize=8)
            cur_y -= 2.6

    tables = {
        "roles": (10, 92, "roles", ["PK id: INT", "name: VARCHAR", "display_name: VARCHAR", "description: TEXT"], 26, 17),
        "users": (10, 52, "users", ["PK id: INT", "FK role_id: INT", "full_name: VARCHAR", "email: VARCHAR (U)", "phone: VARCHAR", "password_hash: VARCHAR", "status: VARCHAR", "created_at: DATETIME"], 26, 26),
        "movies": (50, 92, "movies", ["PK id: INT", "title: VARCHAR", "genre: VARCHAR", "duration: INT", "release_date: DATE", "age_rating: VARCHAR", "status: VARCHAR"], 28, 23),
        "rooms": (92, 92, "rooms", ["PK id: INT", "room_name: VARCHAR", "screen_type: VARCHAR", "total_rows: INT", "seats_per_row: INT", "total_seats: INT", "status: VARCHAR"], 28, 23),
        "seats": (135, 92, "seats", ["PK id: INT", "FK room_id: INT", "seat_row: VARCHAR", "seat_number: INT", "seat_code: VARCHAR", "seat_type: VARCHAR", "price_multiplier: REAL"], 28, 23),
        "showtimes": (65, 54, "showtimes", ["PK id: INT", "FK movie_id: INT", "FK room_id: INT", "start_time: DATETIME", "end_time: DATETIME", "buffer_minutes: INT", "base_price: INT", "status: VARCHAR"], 30, 26),
        "seat_locks": (135, 54, "seat_locks", ["PK id: INT", "FK showtime_id: INT", "FK seat_id: INT", "session_id: VARCHAR", "user_id: INT", "locked_at: DATETIME", "expires_at: DATETIME"], 28, 24),
        "bookings": (10, 10, "bookings", ["PK id: INT", "booking_code: VARCHAR (U)", "FK user_id: INT", "FK showtime_id: INT", "total_amount: INT", "payment_method: VARCHAR", "payment_status: VARCHAR", "booking_status: VARCHAR", "booking_type: VARCHAR", "created_at: DATETIME"], 30, 31),
        "combos": (60, 10, "combos", ["PK id: INT", "name: VARCHAR", "description: TEXT", "price: INT", "image_url: VARCHAR", "status: VARCHAR"], 26, 21),
        "booking_combos": (100, 10, "booking_combos", ["PK id: INT", "FK booking_id: INT", "FK combo_id: INT", "quantity: INT", "unit_price: INT", "total_price: INT"], 26, 21),
        "tickets": (140, 10, "tickets", ["PK id: INT", "ticket_code: VARCHAR (U)", "FK booking_id: INT", "FK showtime_id: INT", "FK seat_id: INT", "price: INT", "qr_data: TEXT", "status: VARCHAR", "checked_in_at: DATETIME", "checked_in_by: INT"], 30, 31)
    }

    for tname, (tx, ty, ttitle, tfields, tw, th) in tables.items():
        draw_erd_table(tx, ty, ttitle, tfields, tw, th)

    # Orthogonal Relationship Lines
    # roles -> users
    ax.plot([23, 23], [92, 78], color='black', linewidth=1.2)
    ax.text(24, 85, "1 : N", fontsize=8)

    # users -> bookings
    ax.plot([23, 23], [52, 41], color='black', linewidth=1.2)
    ax.text(24, 46, "1 : N", fontsize=8)

    # movies -> showtimes
    ax.plot([64, 64, 75], [92, 85, 80], color='black', linewidth=1.2)
    ax.text(66, 86, "1 : N", fontsize=8)

    # rooms -> showtimes
    ax.plot([106, 106, 85], [92, 85, 80], color='black', linewidth=1.2)
    ax.text(100, 86, "1 : N", fontsize=8)

    # rooms -> seats
    ax.plot([120, 135], [103, 103], color='black', linewidth=1.2)
    ax.text(127, 105, "1 : N", fontsize=8)

    # showtimes -> bookings
    ax.plot([65, 45, 45, 40], [67, 67, 25, 25], color='black', linewidth=1.2)
    ax.text(47, 45, "1 : N", fontsize=8)

    # showtimes -> seat_locks
    ax.plot([95, 135], [67, 67], color='black', linewidth=1.2)
    ax.text(115, 69, "1 : N", fontsize=8)

    # seats -> seat_locks
    ax.plot([149, 149], [92, 78], color='black', linewidth=1.2)
    ax.text(151, 85, "1 : N", fontsize=8)

    # bookings -> tickets
    ax.plot([40, 140], [15, 15], color='black', linewidth=1.2)
    ax.text(90, 17, "1 : N", fontsize=8)

    # bookings -> booking_combos
    ax.plot([40, 70, 70, 100], [30, 30, 25, 25], color='black', linewidth=1.2)
    ax.text(75, 32, "1 : N", fontsize=8)

    # combos -> booking_combos
    ax.plot([86, 100], [20, 20], color='black', linewidth=1.2)
    ax.text(91, 22, "1 : N", fontsize=8)

    # seats -> tickets
    ax.plot([163, 163, 155], [92, 50, 41], color='black', linewidth=1.2)
    ax.text(164, 60, "1 : N", fontsize=8)

    # Title
    ax.text(90, 116, "SƠ ĐỒ QUAN HỆ THỰC THỂ (ERD) CHUẨN HÓA 3NF CÓ PHÂN QUYỀN RBAC", 
            ha='center', va='center', fontsize=12, fontweight='bold')

    plt.tight_layout()
    fpath = os.path.join(img_dir, 'drawio_erd_database.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated:", fpath)

# -------------------------------------------------------------
# 8. THIẾT KẾ GIAO DIỆN PHÁC THẢO (WIREFRAME CHỌN GHẾ - THEO ẢNH YÊU CẦU)
# -------------------------------------------------------------
def generate_wireframe_seat():
    # Kích thước chuẩn tỷ lệ tương tự ảnh media_1791908941148.png
    fig, ax = plt.subplots(figsize=(15, 9.3), dpi=300)
    ax.set_xlim(0, 150)
    ax.set_ylim(0, 93)
    ax.axis('off')

    # 1. Outer browser window border
    browser_frame = patches.Rectangle((2, 2), 146, 89, facecolor='white', edgecolor='black', linewidth=1.6)
    ax.add_patch(browser_frame)

    # Browser Top Bar
    ax.plot([2, 148], [86, 86], color='black', linewidth=1.4)
    # Browser window dots
    ax.add_patch(patches.Circle((6, 88.5), 0.8, facecolor='black', edgecolor='black'))
    ax.add_patch(patches.Circle((10, 88.5), 0.8, facecolor='black', edgecolor='black'))
    ax.add_patch(patches.Circle((14, 88.5), 0.8, facecolor='black', edgecolor='black'))
    # URL Bar
    url_box = patches.Rectangle((22, 87), 110, 3.2, facecolor='white', edgecolor='black', linewidth=1.0)
    ax.add_patch(url_box)
    ax.text(26, 88.6, "https://cinemabooking.vn/chon-ghe", ha='left', va='center', fontsize=9)

    # Navigation header
    ax.plot([2, 148], [80, 80], color='black', linewidth=1.2)
    ax.text(6, 83, "CINEMA STAR", ha='left', va='center', fontsize=11, fontweight='bold')
    nav_items = [
        (45, "Trang chủ"),
        (65, "Phim đang chiếu"),
        (88, "Lịch chiếu rạp"),
        (110, "Khuyến mãi"),
        (125, "Giá vé"),
        (140, "Đăng nhập / Đăng ký")
    ]
    for x, txt in nav_items:
        ax.text(x, 83, txt, ha='center', va='center', fontsize=8.5)

    # Main content inner frame
    content_box = patches.Rectangle((6, 6), 138, 71, facecolor='white', edgecolor='black', linewidth=1.2)
    ax.add_patch(content_box)

    # Showtime header card
    showtime_card = patches.Rectangle((10, 69.5), 130, 5.8, facecolor='white', edgecolor='black', linewidth=1.0)
    ax.add_patch(showtime_card)
    ax.text(14, 72.4, "Phim: DUNE | Phòng chiếu: CINEMA 03 (2D Atmos) | Suất: 18:45", 
            ha='left', va='center', fontsize=9.5, fontweight='bold')

    # SCREEN (MÀN HÌNH CHIẾU)
    ax.text(75, 66, "MÀN HÌNH CHIẾU (SCREEN)", ha='center', va='center', fontsize=9.5, fontweight='bold')
    # Viewing Arc
    theta = np.linspace(0.15*np.pi, 0.85*np.pi, 100)
    arc_x = 75 + 50 * np.cos(theta)
    arc_y = 22 + 43 * np.sin(theta)
    ax.plot(arc_x, arc_y, color='black', linewidth=1.8)

    # SEAT GRID
    rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    num_cols = 14
    start_x = 33
    seat_w = 4.8
    seat_h = 3.2
    gap_x = 2.0
    start_y = 61.5
    gap_y = 5.2

    # Sold seats: e.g. C07, C08, C09
    sold_seats = [('C', 6), ('C', 7), ('C', 8)]
    # Selected seats: D07, D08 (matching bottom text!)
    selected_seats = [('D', 7), ('D', 8)]

    for r_idx, r_label in enumerate(rows):
        cur_y = start_y - r_idx * gap_y
        # Row label left & right
        ax.text(23, cur_y + seat_h/2, r_label, ha='center', va='center', fontsize=9, fontweight='bold')
        ax.text(127, cur_y + seat_h/2, r_label, ha='center', va='center', fontsize=9, fontweight='bold')

        for c_idx in range(num_cols):
            cur_x = start_x + c_idx * (seat_w + gap_x)
            col_num = c_idx + 1

            # Check if sold
            is_sold = (r_label, col_num) in sold_seats
            # Check if selected
            is_selected = (r_label, col_num) in selected_seats

            if is_selected:
                s_box = patches.Rectangle((cur_x, cur_y), seat_w, seat_h, facecolor='#cccccc', edgecolor='black', linewidth=1.2)
                ax.add_patch(s_box)
                ax.text(cur_x + seat_w/2, cur_y + seat_h/2, "V", ha='center', va='center', fontsize=8.5, fontweight='bold')
            elif is_sold:
                s_box = patches.Rectangle((cur_x, cur_y), seat_w, seat_h, facecolor='#e6e6e6', edgecolor='black', linewidth=1.0)
                ax.add_patch(s_box)
                ax.text(cur_x + seat_w/2, cur_y + seat_h/2, "X", ha='center', va='center', fontsize=8.5)
            else:
                s_box = patches.Rectangle((cur_x, cur_y), seat_w, seat_h, facecolor='white', edgecolor='black', linewidth=1.0)
                ax.add_patch(s_box)

    # BOTTOM LEGEND & SUMMARY
    bottom_box = patches.Rectangle((10, 8.5), 130, 9.5, facecolor='white', edgecolor='black', linewidth=1.0)
    ax.add_patch(bottom_box)

    # Line 1: Legend
    ax.text(14, 15, "Ghế thường (75k)   [ ] Ghế VIP (90k)   [--] Sweetbox (180k)   [X] Đã bán   [V] Đang chọn", 
            ha='left', va='center', fontsize=8.5)

    # Line 2: Order Summary
    ax.text(14, 11, "Ghế chọn: D07, D08 (VIP) | Tạm tính: 180.000 VNĐ | Giữ ghế: 04:32", 
            ha='left', va='center', fontsize=9, fontweight='bold')

    # Button Tiếp tục
    btn_box = patches.Rectangle((105, 9.5), 23, 4.5, facecolor='white', edgecolor='black', linewidth=1.4)
    ax.add_patch(btn_box)
    ax.text(116.5, 11.7, "TIẾP TỤC >>", ha='center', va='center', fontsize=9, fontweight='bold')

    plt.tight_layout()
    fpath = os.path.join(img_dir, 'wireframe_chon_ghe.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated:", fpath)

# -------------------------------------------------------------
# 9. WIREFRAME TRANG CHỦ (HOME PAGE)
# -------------------------------------------------------------
def generate_wireframe_home():
    fig, ax = plt.subplots(figsize=(15, 9.3), dpi=300)
    ax.set_xlim(0, 150)
    ax.set_ylim(0, 93)
    ax.axis('off')

    # Browser Frame
    ax.add_patch(patches.Rectangle((2, 2), 146, 89, facecolor='white', edgecolor='black', linewidth=1.6))
    ax.plot([2, 148], [86, 86], color='black', linewidth=1.4)
    ax.add_patch(patches.Circle((6, 88.5), 0.8, facecolor='black', edgecolor='black'))
    ax.add_patch(patches.Circle((10, 88.5), 0.8, facecolor='black', edgecolor='black'))
    ax.add_patch(patches.Circle((14, 88.5), 0.8, facecolor='black', edgecolor='black'))
    ax.add_patch(patches.Rectangle((22, 87), 110, 3.2, facecolor='white', edgecolor='black', linewidth=1.0))
    ax.text(26, 88.6, "https://cinemabooking.vn/", ha='left', va='center', fontsize=9)

    # Nav
    ax.plot([2, 148], [80, 80], color='black', linewidth=1.2)
    ax.text(6, 83, "CINEMA STAR", ha='left', va='center', fontsize=11, fontweight='bold')
    navs = [(45, "Trang chủ"), (65, "Phim đang chiếu"), (88, "Lịch chiếu rạp"), (110, "Khuyến mãi"), (125, "Giá vé"), (140, "Đăng nhập")]
    for x, txt in navs:
        ax.text(x, 83, txt, ha='center', va='center', fontsize=8.5)

    # Hero Banner
    hero_box = patches.Rectangle((6, 54), 138, 23, facecolor='white', edgecolor='black', linewidth=1.2)
    ax.add_patch(hero_box)
    ax.text(75, 68, "BOM TẤN CHIẾU RẠP: DUNE - HÀNH TINH CÁT (PHẦN HAI)", ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(75, 63, "Trải nghiệm chuẩn điện ảnh đỉnh cao IMAX Laser & Dolby Atmos", ha='center', va='center', fontsize=9.5)
    btn_dat = patches.Rectangle((65, 56), 20, 4.5, facecolor='white', edgecolor='black', linewidth=1.2)
    ax.add_patch(btn_dat)
    ax.text(75, 58.2, "ĐẶT VÉ NGAY", ha='center', va='center', fontsize=9, fontweight='bold')

    # Section Title
    ax.text(10, 49, "PHIM ĐANG CHIẾU", ha='left', va='center', fontsize=11, fontweight='bold')
    ax.plot([10, 144], [47, 47], color='black', linewidth=1.0)

    # Movie cards
    movie_cards = [
        (10, "DUNE 2", "Khoa học viễn tưởng", "166 phút"),
        (45, "ĐÀO, PHỞ VÀ PIANO", "Lịch sử / Chiến tranh", "100 phút"),
        (80, "MAI", "Tâm lý / Tình cảm", "131 phút"),
        (115, "KUNG FU PANDA 4", "Hoạt hình / Hài", "94 phút")
    ]
    for x, title, genre, dur in movie_cards:
        # Poster placeholder
        p_box = patches.Rectangle((x, 18), 26, 26, facecolor='white', edgecolor='black', linewidth=1.0)
        ax.add_patch(p_box)
        ax.text(x + 13, 31, "[ POSTER PHIM ]", ha='center', va='center', fontsize=8.5)
        # Info
        ax.text(x + 13, 14, title, ha='center', va='center', fontsize=8.5, fontweight='bold')
        ax.text(x + 13, 10.5, f"{genre} | {dur}", ha='center', va='center', fontsize=7.5)
        btn_m = patches.Rectangle((x + 4, 4.5), 18, 4, facecolor='white', edgecolor='black', linewidth=1.0)
        ax.add_patch(btn_m)
        ax.text(x + 13, 6.5, "MUA VÉ", ha='center', va='center', fontsize=8, fontweight='bold')

    plt.tight_layout()
    fpath = os.path.join(img_dir, 'wireframe_trang_chu.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated:", fpath)

# -------------------------------------------------------------
# 10. WIREFRAME LẬP SUẤT CHIẾU & KIỂM TRA XUNG ĐỘT (MANAGER)
# -------------------------------------------------------------
def generate_wireframe_manager_showtime():
    fig, ax = plt.subplots(figsize=(15, 9.3), dpi=300)
    ax.set_xlim(0, 150)
    ax.set_ylim(0, 93)
    ax.axis('off')

    # Browser Frame
    ax.add_patch(patches.Rectangle((2, 2), 146, 89, facecolor='white', edgecolor='black', linewidth=1.6))
    ax.plot([2, 148], [86, 86], color='black', linewidth=1.4)
    ax.add_patch(patches.Circle((6, 88.5), 0.8, facecolor='black', edgecolor='black'))
    ax.add_patch(patches.Circle((10, 88.5), 0.8, facecolor='black', edgecolor='black'))
    ax.add_patch(patches.Circle((14, 88.5), 0.8, facecolor='black', edgecolor='black'))
    ax.add_patch(patches.Rectangle((22, 87), 110, 3.2, facecolor='white', edgecolor='black', linewidth=1.0))
    ax.text(26, 88.6, "https://cinemabooking.vn/manager/showtimes/create", ha='left', va='center', fontsize=9)

    # Manager Header
    ax.plot([2, 148], [80, 80], color='black', linewidth=1.2)
    ax.text(6, 83, "CINEMA STAR - QUẢN LÝ RẠP (MANAGER PORTAL)", ha='left', va='center', fontsize=11, fontweight='bold')
    ax.text(140, 83, "Xin chào, Manager", ha='right', va='center', fontsize=8.5)

    # Content
    form_box = patches.Rectangle((12, 10), 126, 66, facecolor='white', edgecolor='black', linewidth=1.2)
    ax.add_patch(form_box)
    ax.text(16, 72, "LẬP SUẤT CHIẾU MỚI (TÍCH HỢP KIỂM TRA XUNG ĐỘT LỊCH)", ha='left', va='center', fontsize=10.5, fontweight='bold')
    ax.plot([16, 134], [69, 69], color='black', linewidth=1.0)

    # Form fields
    fields = [
        (62, "Chọn phim chiếu:", "[ Dropdown: DUNE - Hành tinh cát (166 phút) ]"),
        (54, "Chọn phòng chiếu:", "[ Dropdown: Phòng Chiếu 03 (2D Atmos - 84 ghế) ]"),
        (46, "Ngày chiếu:", "[ Input Date: 2026-10-14 ]"),
        (38, "Giờ bắt đầu:", "[ Input Time: 18:45 ]"),
        (30, "Thời gian đệm dọn phòng:", "[ Input: 15 phút ] -> Dự kiến kết thúc: 21:46"),
        (22, "Giá vé cơ bản (VND):", "[ Input: 80.000 VNĐ ]")
    ]
    for y, lbl, val in fields:
        ax.text(18, y, lbl, ha='left', va='center', fontsize=9, fontweight='bold')
        ax.add_patch(patches.Rectangle((58, y - 2.5), 70, 5, facecolor='white', edgecolor='black', linewidth=1.0))
        ax.text(60, y, val, ha='left', va='center', fontsize=8.5)

    # Conflict detector status box
    conflict_box = patches.Rectangle((18, 12), 80, 5.5, facecolor='white', edgecolor='black', linewidth=1.2)
    ax.add_patch(conflict_box)
    ax.text(20, 14.7, "TRẠNG THÁI: KHÔNG CÓ XUNG ĐỘT (Phòng trống từ 16:30 đến 22:15)", 
            ha='left', va='center', fontsize=8.5, fontweight='bold')

    # Save button
    save_btn = patches.Rectangle((104, 12), 24, 5.5, facecolor='white', edgecolor='black', linewidth=1.4)
    ax.add_patch(save_btn)
    ax.text(116, 14.7, "XÁC NHẬN LƯU", ha='center', va='center', fontsize=9, fontweight='bold')

    plt.tight_layout()
    fpath = os.path.join(img_dir, 'wireframe_lap_suat_chieu.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated:", fpath)

# -------------------------------------------------------------
# 11. WIREFRAME SOÁT VÉ QR & BÁN VÉ POS (STAFF)
# -------------------------------------------------------------
def generate_wireframe_staff_pos():
    fig, ax = plt.subplots(figsize=(15, 9.3), dpi=300)
    ax.set_xlim(0, 150)
    ax.set_ylim(0, 93)
    ax.axis('off')

    # Browser Frame
    ax.add_patch(patches.Rectangle((2, 2), 146, 89, facecolor='white', edgecolor='black', linewidth=1.6))
    ax.plot([2, 148], [86, 86], color='black', linewidth=1.4)
    ax.add_patch(patches.Circle((6, 88.5), 0.8, facecolor='black', edgecolor='black'))
    ax.add_patch(patches.Circle((10, 88.5), 0.8, facecolor='black', edgecolor='black'))
    ax.add_patch(patches.Circle((14, 88.5), 0.8, facecolor='black', edgecolor='black'))
    ax.add_patch(patches.Rectangle((22, 87), 110, 3.2, facecolor='white', edgecolor='black', linewidth=1.0))
    ax.text(26, 88.6, "https://cinemabooking.vn/staff/scan-ticket", ha='left', va='center', fontsize=9)

    # Staff Header
    ax.plot([2, 148], [80, 80], color='black', linewidth=1.2)
    ax.text(6, 83, "CINEMA STAR - PHÂN HỆ NHÂN VIÊN (STAFF SCANNER & POS)", ha='left', va='center', fontsize=11, fontweight='bold')
    ax.text(140, 83, "Nhân viên: Trần Thu Ngân", ha='right', va='center', fontsize=8.5)

    # Split view: Left = QR Scanner, Right = Check-in result
    # Left Box
    left_box = patches.Rectangle((8, 8), 65, 68, facecolor='white', edgecolor='black', linewidth=1.2)
    ax.add_patch(left_box)
    ax.text(40.5, 72, "QUÉT MÃ QR SOÁT VÉ", ha='center', va='center', fontsize=10, fontweight='bold')
    # Camera preview box
    cam_box = patches.Rectangle((13, 28), 55, 40, facecolor='white', edgecolor='black', linewidth=1.0)
    ax.add_patch(cam_box)
    ax.text(40.5, 48, "[ VÙNG QUÉT CAMERA WEBCAM / MÃ QR ]", ha='center', va='center', fontsize=8.5)
    # Crosshair
    ax.plot([30, 51], [48, 48], color='black', linewidth=1.0, linestyle='--')
    ax.plot([40.5, 40.5], [38, 58], color='black', linewidth=1.0, linestyle='--')
    # Manual input
    ax.text(13, 22, "Nhập mã vé thủ công:", fontsize=8.5, fontweight='bold')
    ax.add_patch(patches.Rectangle((13, 11), 38, 7, facecolor='white', edgecolor='black', linewidth=1.0))
    ax.text(15, 14.5, "TKT-20261013-D05", fontsize=8.5)
    ax.add_patch(patches.Rectangle((53, 11), 15, 7, facecolor='white', edgecolor='black', linewidth=1.2))
    ax.text(60.5, 14.5, "SOÁT VÉ", ha='center', va='center', fontsize=8.5, fontweight='bold')

    # Right Box
    right_box = patches.Rectangle((77, 8), 65, 68, facecolor='white', edgecolor='black', linewidth=1.2)
    ax.add_patch(right_box)
    ax.text(109.5, 72, "KẾT QUẢ SOÁT VÉ & THÔNG TIN", ha='center', va='center', fontsize=10, fontweight='bold')

    # Status result alert box
    alert_box = patches.Rectangle((81, 56), 57, 12, facecolor='white', edgecolor='black', linewidth=1.4)
    ax.add_patch(alert_box)
    ax.text(109.5, 63.5, "THÔNG BÁO: SOÁT VÉ HỢP LỆ THÀNH CÔNG!", ha='center', va='center', fontsize=9, fontweight='bold')
    ax.text(109.5, 59, "Mời khách hàng vào phòng chiếu CINEMA 03", ha='center', va='center', fontsize=8)

    # Details table
    details = [
        ("Mã vé:", "TKT-20261013-D05"),
        ("Tên phim:", "Dune - Hành tinh cát (Phần hai)"),
        ("Phòng chiếu:", "CINEMA 03 (2D Atmos)"),
        ("Suất chiếu:", "18:45 - Thứ Tư, 14/10/2026"),
        ("Vị trí ghế:", "D07 (VIP) | Giá vé: 90.000 VNĐ"),
        ("Khách hàng:", "Nguyễn Văn An (0912345678)"),
        ("Trạng thái vé:", "checked_in (Đã soát lúc 18:32)")
    ]
    dy = 50
    for k, v in details:
        ax.text(82, dy, k, fontsize=8.5, fontweight='bold')
        ax.text(105, dy, v, fontsize=8.5)
        dy -= 5.5

    plt.tight_layout()
    fpath = os.path.join(img_dir, 'wireframe_soat_ve_pos.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated:", fpath)

# -------------------------------------------------------------
# 12. WIREFRAME DASHBOARD QUẢN LÝ (MANAGER DASHBOARD)
# -------------------------------------------------------------
def generate_wireframe_dashboard():
    fig, ax = plt.subplots(figsize=(15, 9.3), dpi=300)
    ax.set_xlim(0, 150)
    ax.set_ylim(0, 93)
    ax.axis('off')

    # Browser Frame
    ax.add_patch(patches.Rectangle((2, 2), 146, 89, facecolor='white', edgecolor='black', linewidth=1.6))
    ax.plot([2, 148], [86, 86], color='black', linewidth=1.4)
    ax.add_patch(patches.Circle((6, 88.5), 0.8, facecolor='black', edgecolor='black'))
    ax.add_patch(patches.Circle((10, 88.5), 0.8, facecolor='black', edgecolor='black'))
    ax.add_patch(patches.Circle((14, 88.5), 0.8, facecolor='black', edgecolor='black'))
    ax.add_patch(patches.Rectangle((22, 87), 110, 3.2, facecolor='white', edgecolor='black', linewidth=1.0))
    ax.text(26, 88.6, "https://cinemabooking.vn/manager/dashboard", ha='left', va='center', fontsize=9)

    # Manager Header
    ax.plot([2, 148], [80, 80], color='black', linewidth=1.2)
    ax.text(6, 83, "CINEMA STAR - DASHBOARD THỐNG KÊ & PHÂN TÍCH RẠP", ha='left', va='center', fontsize=11, fontweight='bold')
    ax.text(140, 83, "Manager Portal", ha='right', va='center', fontsize=8.5)

    # 4 KPI Stat Boxes
    kpis = [
        (8, "DOANH THU HÔM NAY", "15.420.000 VNĐ", "+12.5% so với hôm qua"),
        (43, "VÉ ĐÃ BÁN", "186 Vé", "84 vé Online, 102 vé Quầy"),
        (78, "TỶ LỆ LẤP ĐẦY RẠP", "78.4 %", "Đạt chỉ tiêu lấp đầy"),
        (113, "SUẤT CHIẾU HÔM NAY", "24 Suất", "100% không xung đột")
    ]
    for x, title, val, sub in kpis:
        ax.add_patch(patches.Rectangle((x, 62), 31, 15, facecolor='white', edgecolor='black', linewidth=1.2))
        ax.text(x + 15.5, 73, title, ha='center', va='center', fontsize=7.5, fontweight='bold')
        ax.text(x + 15.5, 68, val, ha='center', va='center', fontsize=9.5, fontweight='bold')
        ax.text(x + 15.5, 64.5, sub, ha='center', va='center', fontsize=6.8)

    # Chart 1: Revenue 7 days (Bar chart style)
    c1_box = patches.Rectangle((8, 8), 75, 51, facecolor='white', edgecolor='black', linewidth=1.2)
    ax.add_patch(c1_box)
    ax.text(45.5, 55, "BIỂU ĐỒ DOANH THU 7 NGÀY GẦN NHẤT (VND)", ha='center', va='center', fontsize=9, fontweight='bold')
    # Axes
    ax.plot([14, 78], [15, 15], color='black', linewidth=1.0)
    ax.plot([14, 14], [15, 51], color='black', linewidth=1.0)
    # Bars
    bar_heights = [18, 22, 19, 26, 32, 29, 31]
    days = ['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN']
    for i, h in enumerate(bar_heights):
        bx = 18 + i * 8.5
        ax.add_patch(patches.Rectangle((bx, 15), 5.5, h, facecolor='white', edgecolor='black', linewidth=1.0))
        ax.text(bx + 2.75, 13, days[i], ha='center', va='center', fontsize=7.5)

    # Chart 2: Top Occupancy by Movie (Horizontal bars)
    c2_box = patches.Rectangle((87, 8), 57, 51, facecolor='white', edgecolor='black', linewidth=1.2)
    ax.add_patch(c2_box)
    ax.text(115.5, 55, "TỶ LỆ LẤP ĐẦY THEO PHIM (%)", ha='center', va='center', fontsize=9, fontweight='bold')
    top_movies = [
        ("Dune 2", 36, "88%"),
        ("Đào, Phở, Piano", 30, "76%"),
        ("Mai", 24, "62%"),
        ("Kung Fu Panda 4", 20, "54%")
    ]
    my = 46
    for mname, w, pct in top_movies:
        ax.text(90, my + 3, mname, fontsize=8, fontweight='bold')
        ax.add_patch(patches.Rectangle((90, my - 3), 42, 4.5, facecolor='white', edgecolor='black', linewidth=0.8))
        ax.add_patch(patches.Rectangle((90, my - 3), w, 4.5, facecolor='#cccccc', edgecolor='black', linewidth=0.8))
        ax.text(136, my - 0.7, pct, fontsize=8, fontweight='bold')
        my -= 10

    plt.tight_layout()
    fpath = os.path.join(img_dir, 'wireframe_dashboard_manager.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated:", fpath)

# Execute all generators
print("Starting Draw.io and Wireframe diagrams generation...")
generate_fdd()
generate_uc_tong_quat()
generate_uc_khach_hang()
generate_uc_nhan_vien()
generate_uc_quan_ly()
generate_uc_quan_tri()
generate_erd()
generate_wireframe_seat()
generate_wireframe_home()
generate_wireframe_manager_showtime()
generate_wireframe_staff_pos()
generate_wireframe_dashboard()
print("All Draw.io and Wireframe diagrams generated successfully!")
