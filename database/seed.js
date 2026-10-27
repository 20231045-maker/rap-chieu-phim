const bcrypt = require('bcryptjs');
const { pool, query, run } = require('./db');

async function seedDatabase() {
    console.log('--- Đang khởi tạo dữ liệu mẫu cho hệ thống rạp chiếu phim (MySQL cinema_db) ---');

    const conn = await pool.getConnection();

    try {
        await conn.query('SET FOREIGN_KEY_CHECKS = 0;');

        // 1. Vai trò (Roles)
        await conn.query('TRUNCATE TABLE roles;');
        const roles = [
            [1, 'admin', 'Quản trị viên', 'Quản trị toàn bộ người dùng, quyền hạn và hệ thống'],
            [2, 'manager', 'Quản lý rạp', 'Quản lý danh mục phim, phòng chiếu, suất chiếu và báo cáo doanh thu'],
            [3, 'staff', 'Nhân viên rạp', 'Bán vé tại quầy (POS) và thực hiện soát vé QR Code'],
            [4, 'client', 'Khách hàng', 'Đặt vé trực tuyến, chọn ghế, chọn combo và thanh toán']
        ];
        for (const r of roles) {
            await conn.query('INSERT INTO roles (id, name, display_name, description) VALUES (?, ?, ?, ?)', r);
        }

        // 2. Tài khoản người dùng (Users)
        await conn.query('TRUNCATE TABLE users;');
        const salt = bcrypt.genSaltSync(10);
        const passAdmin = bcrypt.hashSync('admin123', salt);
        const passManager = bcrypt.hashSync('manager123', salt);
        const passStaff = bcrypt.hashSync('staff123', salt);
        const passClient = bcrypt.hashSync('client123', salt);

        const users = [
            [1, 1, 'Nguyễn Mạnh Quyết (Admin)', 'admin@cinema.com', '0912345678', passAdmin, 'active'],
            [2, 2, 'Hà Thái Bảo (Manager)', 'manager@cinema.com', '0987654321', passManager, 'active'],
            [3, 3, 'Trần Thu Ngân (Staff Quầy)', 'staff@cinema.com', '0901122334', passStaff, 'active'],
            [4, 4, 'Nguyễn Văn An (Khách Hàng)', 'client@cinema.com', '0933445566', passClient, 'active'],
            [5, 4, 'Lê Thị Mai (Khách Hàng)', 'mai.le@cinema.com', '0944556677', passClient, 'active'],
            [6, 4, 'Phạm Quốc Cường', 'cuong.pham@gmail.com', '0966778899', passClient, 'active']
        ];
        for (const u of users) {
            await conn.query('INSERT INTO users (id, role_id, full_name, email, phone, password_hash, status) VALUES (?, ?, ?, ?, ?, ?, ?)', u);
        }

        // 3. Phòng chiếu (Rooms)
        await conn.query('TRUNCATE TABLE rooms;');
        const rooms = [
            [1, 'Phòng Chiếu 01 (IMAX Laser)', 'IMAX', 7, 12, 84, 'active'],
            [2, 'Phòng Chiếu 02 (3D Dolby Atmos)', '3D', 7, 12, 84, 'active'],
            [3, 'Phòng Chiếu 03 (2D Digital)', '2D', 6, 10, 60, 'active'],
            [4, 'Phòng Chiếu 04 (Phim Việt Nam Gold)', '2D', 6, 10, 60, 'active']
        ];
        for (const rm of rooms) {
            await conn.query('INSERT INTO rooms (id, room_name, screen_type, total_rows, seats_per_row, total_seats, status) VALUES (?, ?, ?, ?, ?, ?, ?)', rm);
        }

        // Tạo ghế cho các phòng
        await conn.query('TRUNCATE TABLE seats;');
        // Phòng 1 & 2: 7 hàng (A-G), 12 cột
        for (const roomId of [1, 2]) {
            const rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G'];
            for (const r of rows) {
                for (let num = 1; num <= 12; num++) {
                    let seatType = 'regular';
                    let mult = 1.0;
                    if (['C', 'D', 'E', 'F'].includes(r)) {
                        seatType = 'vip';
                        mult = 1.25;
                    } else if (r === 'G') {
                        seatType = 'sweetbox';
                        mult = 2.0;
                    }
                    await conn.query('INSERT INTO seats (room_id, seat_row, seat_number, seat_code, seat_type, price_multiplier) VALUES (?, ?, ?, ?, ?, ?)',
                        [roomId, r, num, `${r}${num}`, seatType, mult]);
                }
            }
        }
        // Phòng 3 & 4: 6 hàng (A-F), 10 cột
        for (const roomId of [3, 4]) {
            const pRows = ['A', 'B', 'C', 'D', 'E', 'F'];
            for (const r of pRows) {
                for (let num = 1; num <= 10; num++) {
                    let seatType = 'regular';
                    let mult = 1.0;
                    if (['C', 'D', 'E'].includes(r)) {
                        seatType = 'vip';
                        mult = 1.25;
                    } else if (r === 'F') {
                        seatType = 'sweetbox';
                        mult = 2.0;
                    }
                    await conn.query('INSERT INTO seats (room_id, seat_row, seat_number, seat_code, seat_type, price_multiplier) VALUES (?, ?, ?, ?, ?, ?)',
                        [roomId, r, num, `${r}${num}`, seatType, mult]);
                }
            }
        }

        // 4. Phim (Movies) - Bao gồm các siêu phẩm nổi tiếng nhất của điện ảnh Việt Nam
        await conn.query('TRUNCATE TABLE movies;');
        const movies = [
            [
                1, 'Đào, Phở và Piano', 'Peach Blossom, Pho and Piano', 'Lịch sử, Chiến tranh, Lãng mạn', 100,
                '2024-02-10', '2026-11-30', 'T13', 'Phi Tiến Sơn',
                'Doãn Quốc Đam, Cao Thùy Linh, Trần Lực, Tuấn Hưng, NSND Trung Hiếu',
                'Bộ phim tái hiện không khí bi tráng của Hà Nội trong những ngày cuối năm 1946, khi quân dân thủ đô chiến đấu kiên cường bảo vệ từng góc phố. Giữa bom đạn khốc liệt, tình yêu đôi lứa và nét văn hóa ẩm thực truyền thống vẫn vẹn nguyên, làm nổi bật chất hào hoa, anh dũng của người Tràng An.',
                '/images/posters/movie-1.jpg',
                '/images/banners/banner-1.jpg',
                'https://www.youtube.com/embed/qn1t_biQigc', 'now_showing'
            ],
            [
                2, 'Mai', 'Mai', 'Tâm lý, Tình cảm, Gia đình', 131,
                '2024-02-10', '2026-11-20', 'T18', 'Trấn Thành',
                'Phương Anh Đào, Tuấn Trần, Trấn Thành, Hồng Đào, Uyển Ân, Quốc Khánh',
                'Mai kể về cuộc đời một người phụ nữ làm nghề mát-xa chịu nhiều định kiến xã hội. Cuộc sống của cô rẽ hướng khi gặp chàng nhạc công kém tuổi Dương - một chàng trai đào hoa nhưng chân thành. Chuyện tình của họ vấp phải rào cản từ quá khứ và sự phản đối của gia đình, phản ánh sâu sắc hiện thực đời sống và khát khao hạnh phúc.',
                '/images/posters/movie-2.jpg',
                '/images/banners/banner-2.jpg',
                'https://www.youtube.com/embed/EX6clvId19s', 'now_showing'
            ],
            [
                3, 'Lật Mặt 7: Một Điều Ước', 'Face Off 7: One Wish', 'Gia đình, Tình cảm, Tâm lý', 138,
                '2024-04-26', '2026-11-25', 'K', 'Lý Hải',
                'Thanh Hiền, Trương Minh Cường, Đinh Y Nhung, Quách Ngọc Tuyên, Trâm Anh',
                'Bộ phim xoay quanh câu chuyện gia đình bà Hai (73 tuổi) sống một mình ở vùng núi Lạc Dương, Lâm Đồng. Khi bà gặp tai nạn gãy chân, 5 người con đã trưởng thành ở khắp mọi miền đất nước phải đùn đẩy, chia ca chăm sóc mẹ. Tác phẩm lấy đi nước mắt khán giả với thông điệp lay động về chữ hiếu và tình mẫu tử thiêng liêng.',
                '/images/posters/movie-3.jpg',
                '/images/banners/banner-3.jpg',
                'https://www.youtube.com/embed/0J51aUryra4', 'now_showing'
            ],
            [
                4, 'Nhà Bà Nữ', 'The House of No Man', 'Gia đình, Hài hước, Tâm lý', 102,
                '2023-01-22', '2026-12-15', 'T16', 'Trấn Thành',
                'Lê Giang, Uyển Ân, Song Luân, Trấn Thành, Khả Như, NSND Ngọc Giàu',
                'Bộ phim gia đình làm mưa làm gió phòng vé với doanh thu hơn 475 tỷ đồng, xoay quanh gia đình 3 thế hệ của bà Nữ bán bánh canh cua, nơi mâu thuẫn thế hệ và tình yêu tự do va chạm dữ dội.',
                '/images/posters/movie-4.jpg',
                '/images/banners/banner-4.jpg',
                'https://www.youtube.com/embed/IkaP0KJWTsQ', 'now_showing'
            ],
            [
                5, 'Bố Già', 'Dad, I\'m Sorry', 'Gia đình, Hài, Chính kịch', 128,
                '2021-03-05', '2026-11-15', 'T13', 'Trấn Thành, Vũ Ngọc Đãng',
                'Trấn Thành, Tuấn Trần, Ngân Chi, NSND Ngọc Giàu, Lê Giang, Lan Phương',
                'Câu chuyện cảm động sâu sắc về Ba Sang - người cha bao đồng ở xóm nghèo Sài Gòn luôn hy sinh cho con trai Quắn và các anh chị em họ hàng.',
                '/images/posters/movie-5.jpg',
                '/images/banners/banner-5.jpg',
                'https://www.youtube.com/embed/jluSu8Rw6YE', 'now_showing'
            ],
            [
                6, 'Lật Mặt 6: Tấm Vé Định Mệnh', 'Face Off 6: The Ticket', 'Hành động, Hồi hộp, Tâm lý', 132,
                '2023-04-28', '2026-11-20', 'T16', 'Lý Hải',
                'Quốc Cường, Trung Dũng, Huy Khánh, Thanh Thức, Diệp Bảo Ngọc',
                'Nhóm bạn thân 6 người trúng tờ vé số độc đắc 136,8 tỷ đồng nhưng người giữ vé không may qua đời, đẩy tình bạn vào vòng xoáy nghi kỵ và tham vọng.',
                '/images/posters/movie-6.jpg',
                '/images/banners/banner-6.jpg',
                'https://www.youtube.com/embed/o3FoowSoNr4', 'now_showing'
            ],
            [
                7, 'Mắt Biếc', 'Dreamy Eyes', 'Lãng mạn, Tuổi trẻ, Tâm lý', 117,
                '2019-12-20', '2026-11-25', 'T13', 'Victor Vũ',
                'Trần Nghĩa, Trúc Anh, Trần Phong, Đỗ Khánh Vân, Thảo Tâm',
                'Chuyển thể từ tác phẩm kinh điển của nhà văn Nguyễn Nhật Ánh, kể về tình yêu đơn phương day dứt cả cuộc đời của Ngạn dành cho cô bạn thanh mai trúc mã Hà Lan.',
                '/images/posters/movie-7.jpg',
                '/images/banners/banner-7.jpg',
                'https://www.youtube.com/embed/ITlQ0oU7tDA', 'now_showing'
            ],
            [
                8, 'Hai Phượng', 'Furie', 'Hành động, Võ thuật, Hồi hộp', 98,
                '2019-02-22', '2026-12-10', 'T18', 'Lê Văn Kiệt',
                'Ngô Thanh Vân, Mai Cát Vy, Phan Thanh Nhiên, Phạm Anh Khoa',
                'Đả nữ Ngô Thanh Vân trong hành trình nghẹt thở 14 tiếng truy đuổi đường dây buôn người xuyên quốc gia để cứu đứa con gái bé bỏng bị bắt cóc.',
                '/images/posters/movie-8.jpg',
                '/images/banners/banner-8.jpg',
                'https://www.youtube.com/embed/THXPCF6UHh8', 'now_showing'
            ],
            [
                9, 'Kẻ Ăn Hồn', 'The Soul Reaper', 'Kinh dị, Bí ẩn, Dân gian', 109,
                '2023-12-15', '2026-11-28', 'T18', 'Trần Hữu Tấn',
                'Hoàng Hà, Võ Điền Gia Huy, Huỳnh Thanh Trực, NSƯT Chiều Xuân, Lan Phương',
                'Tiền truyện của series Tết Ở Làng Địa Ngục, hé lộ nguồn gốc loại cổ thuật luyện rượu sọ người tà ác với bối cảnh rùng rợn, đậm đà màu sắc dân gian Việt.',
                '/images/posters/movie-9.jpg',
                '/images/banners/banner-9.jpg',
                'https://www.youtube.com/embed/xWh0g4rKGjI', 'now_showing'
            ],
            [
                10, 'Tiệc Trăng Máu', 'Blood Moon Party', 'Tâm lý, Hài đen, Xã hội', 118,
                '2020-10-23', '2026-12-05', 'T18', 'Nguyễn Quang Dũng',
                'Thái Hòa, Hồng Ánh, Thu Trang, Kiều Minh Tuấn, Kaity Nguyễn, Hứa Vĩ Văn',
                'Bữa tiệc hội ngộ của nhóm bạn thân biến thành thảm họa bóc trần những bí mật dối trá khi tất cả đồng ý công khai toàn bộ tin nhắn, cuộc gọi trên bàn ăn.',
                '/images/posters/movie-10.jpg',
                '/images/banners/banner-10.jpg',
                'https://www.youtube.com/embed/IabqTjvJt-4', 'now_showing'
            ],
            [
                11, 'Cám: Dị Bản Kinh Dị', 'Cam: Dark Tale', 'Kinh dị, Giật gân, Cổ trang', 122,
                '2024-09-20', '2026-12-30', 'T18', 'Trần Hữu Tấn',
                'Quốc Cường, Thúy Diễm, Rima Thanh Vy, Lâm Thanh Mỹ, Hải Nam',
                'Dị bản đen tối và đẫm máu xoay quanh câu chuyện cổ tích Tấm Cám quen thuộc, vén màn những bí mật kinh hoàng phía sau số phận cô Cám dị tật.',
                '/images/posters/movie-11.jpg',
                '/images/banners/banner-11.jpg',
                'https://www.youtube.com/embed/gW0b5Bsa34o', 'coming_soon'
            ],
            [
                12, 'Em Chưa 18', 'Jailbait', 'Hài, Lãng mạn, Học đường', 95,
                '2017-04-28', '2026-12-31', 'T16', 'Lê Thanh Sơn',
                'Kaity Nguyễn, Kiều Minh Tuấn, Will 365, Châu Bùi, Kathy Uyên',
                'Hiện tượng phim học đường phá kỷ lục phòng vé, kể về phi vụ "gài bẫy" hài hước nhưng ngọt ngào giữa cô nữ sinh Linh Đan và tay chơi Hoàng.',
                '/images/posters/movie-12.jpg',
                '/images/banners/banner-12.jpg',
                'https://www.youtube.com/embed/_affkHceSj4', 'coming_soon'
            ],
            [
                13, 'Kung Fu Panda 4', 'Kung Fu Panda 4', 'Hoạt hình, Hành động, Hài', 94,
                '2024-03-08', '2026-12-20', 'P', 'Mike Mitchell',
                'Jack Black, Awkwafina, Viola Davis',
                'Gấu Po trở lại trong hành trình mới để trở thành Thủ Lĩnh Tinh Thần của Thung Lũng Bình Yên.',
                '/images/posters/movie-13.jpg',
                '/images/banners/banner-13.jpg',
                'https://www.youtube.com/embed/_inKs4eeHiI', 'now_showing'
            ],
            [
                14, 'Dune: Hành Tinh Cát 2', 'Dune: Part Two', 'Khoa học viễn tưởng, Phiêu lưu', 166,
                '2024-03-01', '2026-12-25', 'T16', 'Denis Villeneuve',
                'Timothée Chalamet, Zendaya, Rebecca Ferguson',
                'Paul Atreides hợp lực cùng Chani và tộc người Fremen để trả thù những kẻ đã hủy hoại gia tộc mình.',
                '/images/posters/movie-14.jpg',
                '/images/banners/banner-14.jpg',
                'https://www.youtube.com/embed/U2Qp5pL3ovA', 'now_showing'
            ]
        ];

        for (const m of movies) {
            await conn.query(`
                INSERT INTO movies (
                    id, title, original_title, genre, duration, release_date, end_date,
                    age_rating, director, cast, description, poster_url, banner_url,
                    trailer_url, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            `, m);
        }

        // 5. Suất chiếu (Showtimes)
        await conn.query('TRUNCATE TABLE showtimes;');
        const now = new Date();
        const formatDate = (daysAhead) => {
            const d = new Date(now);
            d.setDate(d.getDate() + daysAhead);
            const pad = n => String(n).padStart(2, '0');
            return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
        };

        const d0 = formatDate(0);
        const d1 = formatDate(1);
        const d2 = formatDate(2);
        const d3 = formatDate(3);

        const showtimes = [
            // Phòng 1 (IMAX): Đào, Phở và Piano (100p) & Mai (131p)
            [1, 1, 1, `${d0} 09:00:00`, `${d0} 10:55:00`, 15, 120000, 'scheduled'],
            [2, 2, 1, `${d0} 11:30:00`, `${d0} 13:56:00`, 15, 140000, 'scheduled'],
            [3, 1, 1, `${d0} 14:30:00`, `${d0} 16:25:00`, 15, 120000, 'scheduled'],
            [4, 2, 1, `${d0} 17:00:00`, `${d0} 19:26:00`, 15, 150000, 'scheduled'],
            [5, 1, 1, `${d0} 20:00:00`, `${d0} 21:55:00`, 15, 130000, 'scheduled'],
            // Phòng 2 (3D Atmos): Lật Mặt 7 (138p) & Nhà Bà Nữ (102p)
            [6, 3, 2, `${d0} 09:15:00`, `${d0} 11:48:00`, 15, 100000, 'scheduled'],
            [7, 4, 2, `${d0} 12:15:00`, `${d0} 14:12:00`, 15, 90000, 'scheduled'],
            [8, 3, 2, `${d0} 14:45:00`, `${d0} 17:18:00`, 15, 110000, 'scheduled'],
            [9, 4, 2, `${d0} 17:45:00`, `${d0} 19:42:00`, 15, 95000, 'scheduled'],
            [10, 3, 2, `${d0} 20:15:00`, `${d0} 22:48:00`, 15, 115000, 'scheduled'],
            // Phòng 3 (2D Digital): Bố Già (128p) & Lật Mặt 6 (132p)
            [11, 5, 3, `${d0} 09:00:00`, `${d0} 11:23:00`, 15, 80000, 'scheduled'],
            [12, 6, 3, `${d0} 12:00:00`, `${d0} 14:27:00`, 15, 85000, 'scheduled'],
            [13, 5, 3, `${d0} 15:00:00`, `${d0} 17:23:00`, 15, 85000, 'scheduled'],
            [14, 6, 3, `${d0} 18:00:00`, `${d0} 20:27:00`, 15, 90000, 'scheduled'],
            [15, 5, 3, `${d0} 21:00:00`, `${d0} 23:23:00`, 15, 90000, 'scheduled'],
            // Phòng 4 (2D Gold Class): Mắt Biếc & Hai Phượng & Tiệc Trăng Máu & Kẻ Ăn Hồn
            [16, 7, 4, `${d0} 09:30:00`, `${d0} 11:42:00`, 15, 80000, 'scheduled'],
            [17, 8, 4, `${d0} 12:15:00`, `${d0} 14:08:00`, 15, 80000, 'scheduled'],
            [18, 10, 4, `${d0} 14:45:00`, `${d0} 16:58:00`, 15, 85000, 'scheduled'],
            [19, 9, 4, `${d0} 17:30:00`, `${d0} 19:34:00`, 15, 85000, 'scheduled'],
            [20, 7, 4, `${d0} 20:15:00`, `${d0} 22:27:00`, 15, 90000, 'scheduled'],
            // Ngày mai (d1)
            [21, 1, 1, `${d1} 10:00:00`, `${d1} 11:55:00`, 15, 110000, 'scheduled'],
            [22, 2, 1, `${d1} 13:00:00`, `${d1} 15:26:00`, 15, 120000, 'scheduled'],
            [23, 1, 1, `${d1} 16:30:00`, `${d1} 18:25:00`, 15, 120000, 'scheduled'],
            [24, 3, 2, `${d1} 10:30:00`, `${d1} 13:03:00`, 15, 95000, 'scheduled'],
            [25, 7, 4, `${d1} 14:00:00`, `${d1} 16:12:00`, 15, 85000, 'scheduled'],
            [26, 9, 4, `${d1} 19:00:00`, `${d1} 21:04:00`, 15, 90000, 'scheduled'],
            // Ngày kia (d2, d3)
            [27, 1, 1, `${d2} 18:00:00`, `${d2} 19:55:00`, 15, 120000, 'scheduled'],
            [28, 2, 1, `${d2} 20:30:00`, `${d2} 22:56:00`, 15, 130000, 'scheduled'],
            [29, 3, 2, `${d3} 19:00:00`, `${d3} 21:33:00`, 15, 115000, 'scheduled']
        ];

        for (const st of showtimes) {
            await conn.query('INSERT INTO showtimes (id, movie_id, room_id, start_time, end_time, buffer_minutes, base_price, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', st);
        }

        // 6. Combos Bắp Nước
        await conn.query('TRUNCATE TABLE combos;');
        const combos = [
            [1, 'Combo Solo Star', '1 Bắp ngọt lớn (60oz) + 1 Nước ngọt lớn (32oz)', 65000, 'https://images.unsplash.com/photo-1585647347483-22b66260dfff?w=500', 'active'],
            [2, 'Combo Couple Gold', '1 Bắp phô mai lớn + 2 Nước ngọt lớn + 1 Snack khoai tây', 99000, 'https://images.unsplash.com/photo-1578849278619-e73505e9610f?w=500', 'active'],
            [3, 'Combo Family VIP', '2 Bắp rang bơ caramel lớn + 4 Nước ngọt + 2 Xúc xích Đức nướng', 179000, 'https://images.unsplash.com/photo-1512149177596-f817c7ef5d4c?w=500', 'active'],
            [4, 'Combo Trà Đào & Bắp Rang', '1 Bắp rang mặn thơm ngon + 1 Trà Đào Cam Sả mát lạnh', 75000, 'https://images.unsplash.com/photo-1556881286-fc6915169721?w=500', 'active']
        ];
        for (const c of combos) {
            await conn.query('INSERT INTO combos (id, name, description, price, image_url, status) VALUES (?, ?, ?, ?, ?, ?)', c);
        }

        // 7. Cài đặt hệ thống
        await conn.query('TRUNCATE TABLE system_settings;');
        const settings = [
            ['cinema_name', 'CINESTAR CINEMA COMPLEX', 'Tên thương hiệu hệ thống rạp'],
            ['address', 'Tòa nhà Landmark, 720A Điện Biên Phủ, Phường 22, Bình Thạnh, TP.HCM', 'Địa chỉ rạp chính'],
            ['hotline', '1900 6017', 'Số điện thoại hỗ trợ'],
            ['buffer_time', '15', 'Thời gian giãn cách dọn dẹp phòng chiếu (phút)'],
            ['seat_lock_time', '5', 'Thời gian khóa giữ ghế tạm thời (phút)']
        ];
        for (const s of settings) {
            await conn.query('INSERT INTO system_settings (`key`, value, description) VALUES (?, ?, ?)', s);
        }

        // 8. Đơn Đặt Vé & Vé mẫu
        await conn.query('TRUNCATE TABLE bookings;');
        await conn.query('TRUNCATE TABLE tickets;');
        await conn.query('TRUNCATE TABLE booking_combos;');

        const [seatsD5] = await conn.query("SELECT id FROM seats WHERE room_id = 1 AND seat_code = 'D5'");
        const [seatsD6] = await conn.query("SELECT id FROM seats WHERE room_id = 1 AND seat_code = 'D6'");
        const [seatsE7] = await conn.query("SELECT id FROM seats WHERE room_id = 1 AND seat_code = 'E7'");
        const [seatsG1] = await conn.query("SELECT id FROM seats WHERE room_id = 1 AND seat_code = 'G1'");

        if (seatsD5[0] && seatsD6[0]) {
            await conn.query(`
                INSERT INTO bookings (id, booking_code, user_id, customer_name, customer_email, customer_phone,
                    showtime_id, total_amount, payment_method, payment_status, booking_status, booking_type, created_at)
                VALUES (1, 'BKG-20261013-DEMO01', 4, 'Nguyễn Văn An', 'client@cinema.com', '0933445566',
                    1, 374000, 'vnpay', 'paid', 'confirmed', 'online', '${d0} 08:15:00')
            `);
            await conn.query(`
                INSERT INTO tickets (id, ticket_code, booking_id, showtime_id, seat_id, price, qr_data, status, checked_in_at, checked_in_by)
                VALUES (1, 'TKT-20261013-D05', 1, 1, ?, 137500, 'TKT-20261013-D05', 'unused', NULL, NULL)
            `, [seatsD5[0].id]);
            await conn.query(`
                INSERT INTO tickets (id, ticket_code, booking_id, showtime_id, seat_id, price, qr_data, status, checked_in_at, checked_in_by)
                VALUES (2, 'TKT-20261013-D06', 1, 1, ?, 137500, 'TKT-20261013-D06', 'unused', NULL, NULL)
            `, [seatsD6[0].id]);
            await conn.query(`
                INSERT INTO booking_combos (booking_id, combo_id, quantity, unit_price, total_price)
                VALUES (1, 2, 1, 99000, 99000)
            `);
        }

        if (seatsE7[0]) {
            await conn.query(`
                INSERT INTO bookings (id, booking_code, user_id, customer_name, customer_email, customer_phone,
                    showtime_id, total_amount, payment_method, payment_status, booking_status, booking_type, created_at)
                VALUES (2, 'BKG-20261013-DEMO02', 5, 'Lê Thị Mai', 'mai.le@cinema.com', '0944556677',
                    1, 137500, 'momo', 'paid', 'confirmed', 'online', '${d0} 08:30:00')
            `);
            await conn.query(`
                INSERT INTO tickets (id, ticket_code, booking_id, showtime_id, seat_id, price, qr_data, status, checked_in_at, checked_in_by)
                VALUES (3, 'TKT-20261013-E07', 2, 1, ?, 137500, 'TKT-20261013-E07', 'checked_in', '${d0} 08:50:00', 3)
            `, [seatsE7[0].id]);
        }

        if (seatsG1[0]) {
            await conn.query(`
                INSERT INTO bookings (id, booking_code, user_id, customer_name, customer_email, customer_phone,
                    showtime_id, total_amount, payment_method, payment_status, booking_status, booking_type, created_at)
                VALUES (3, 'BKG-20261013-POS001', NULL, 'Khách vãng lai (Quầy)', 'pos@cinema.com', '0900000000',
                    1, 220000, 'cash', 'paid', 'confirmed', 'pos', '${d0} 08:45:00')
            `);
            await conn.query(`
                INSERT INTO tickets (id, ticket_code, booking_id, showtime_id, seat_id, price, qr_data, status, checked_in_at, checked_in_by)
                VALUES (4, 'TKT-20261013-G01', 3, 1, ?, 220000, 'TKT-20261013-G01', 'unused', NULL, NULL)
            `, [seatsG1[0].id]);
        }

        await conn.query('SET FOREIGN_KEY_CHECKS = 1;');
        console.log('✅ Khởi tạo CSDL MySQL cinema_db và nạp dữ liệu phim Việt Nam hoàn tất 100%!');
    } catch (err) {
        console.error('Lỗi seed MySQL:', err);
    } finally {
        conn.release();
    }
}

if (require.main === module) {
    seedDatabase().then(() => process.exit(0));
}

module.exports = seedDatabase;
