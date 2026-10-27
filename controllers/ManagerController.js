const Movie = require('../models/Movie');
const Room = require('../models/Room');
const Seat = require('../models/Seat');
const Showtime = require('../models/Showtime');
const Combo = require('../models/Combo');
const Booking = require('../models/Booking');
const ConflictDetector = require('../services/conflictDetector');
const { query } = require('../database/db');

class ManagerController {
    // 1. Dashboard Thống kê chuyên sâu & Tỷ lệ lấp đầy rạp
    static async dashboard(req, res) {
        try {
            const stats = await Booking.getDashboardStats();
            const allMovies = await Movie.getAll();
            const allRooms = await Room.getAll();
            const totalMovies = allMovies.length;
            const totalRooms = allRooms.length;

            // Suất chiếu hôm nay
            const todayStr = new Date().toISOString().split('T')[0];
            const todayShowtimes = await query(`
                SELECT st.*, m.title as movie_title, r.room_name,
                       (SELECT COUNT(*) FROM tickets t JOIN bookings b ON t.booking_id = b.id WHERE t.showtime_id = st.id AND b.booking_status != 'cancelled') as sold_seats,
                       (SELECT COUNT(*) FROM seats WHERE room_id = r.id) as total_seats
                FROM showtimes st
                JOIN movies m ON st.movie_id = m.id
                JOIN rooms r ON st.room_id = r.id
                WHERE DATE(st.start_time) = DATE(?) AND st.status = 'scheduled'
                ORDER BY st.start_time ASC
            `, [todayStr]);

            res.render('manager/dashboard', {
                title: 'Bảng Điều Khiển Quản Lý (Manager Dashboard)',
                stats,
                totalMovies,
                totalRooms,
                todayShowtimes,
                managerUser: req.session.user
            });
        } catch (err) {
            console.error('Lỗi manager dashboard:', err);
            res.status(500).render('client/404', {
                title: '500 - Lỗi',
                message: 'Không thể tải dashboard: ' + err.message
            });
        }
    }

    // 2. Quản lý Danh mục Phim (CRUD Phim)
    static async movies(req, res) {
        try {
            const movies = await Movie.getAll();
            res.render('manager/movies', {
                title: 'Quản Lý Danh Mục Phim',
                movies,
                error: req.query.error || null,
                success: req.query.success || null
            });
        } catch (err) {
            console.error('Lỗi quản lý phim:', err);
            res.redirect('/manager/dashboard');
        }
    }

    static createMovieForm(req, res) {
        res.render('manager/movie-form', {
            title: 'Thêm Phim Mới',
            movie: null,
            isEdit: false
        });
    }

    static async storeMovie(req, res) {
        try {
            const data = req.body;
            if (req.file) {
                data.poster_url = '/uploads/' + req.file.filename;
            }
            await Movie.create(data);
            res.redirect('/manager/movies?success=' + encodeURIComponent('Thêm phim mới thành công!'));
        } catch (err) {
            console.error('Lỗi thêm phim:', err);
            res.redirect('/manager/movies?error=' + encodeURIComponent('Lỗi thêm phim: ' + err.message));
        }
    }

    static async editMovieForm(req, res) {
        try {
            const movie = await Movie.findById(req.params.id);
            if (!movie) {
                return res.redirect('/manager/movies?error=' + encodeURIComponent('Không tìm thấy phim!'));
            }
            res.render('manager/movie-form', {
                title: `Sửa Thông Tin Phim - ${movie.title}`,
                movie,
                isEdit: true
            });
        } catch (err) {
            console.error('Lỗi sửa phim:', err);
            res.redirect('/manager/movies');
        }
    }

    static async updateMovie(req, res) {
        try {
            const data = req.body;
            if (req.file) {
                data.poster_url = '/uploads/' + req.file.filename;
            }
            await Movie.update(req.params.id, data);
            res.redirect('/manager/movies?success=' + encodeURIComponent('Cập nhật phim thành công!'));
        } catch (err) {
            console.error('Lỗi cập nhật phim:', err);
            res.redirect('/manager/movies?error=' + encodeURIComponent('Lỗi cập nhật phim: ' + err.message));
        }
    }

    static async deleteMovie(req, res) {
        try {
            await Movie.delete(req.params.id);
            res.redirect('/manager/movies?success=' + encodeURIComponent('Xóa phim thành công!'));
        } catch (err) {
            res.redirect('/manager/movies?error=' + encodeURIComponent('Không thể xóa phim đã có suất chiếu! Vui lòng chuyển trạng thái phim sang "Ngừng chiếu".'));
        }
    }

    // 3. Quản lý Phòng chiếu & Sơ đồ ghế
    static async rooms(req, res) {
        try {
            const rooms = await Room.getAll();
            res.render('manager/rooms', {
                title: 'Quản Lý Phòng Chiếu & Sơ Đồ Ghế',
                rooms,
                error: req.query.error || null,
                success: req.query.success || null
            });
        } catch (err) {
            console.error('Lỗi phòng chiếu:', err);
            res.redirect('/manager/dashboard');
        }
    }

    static async createRoom(req, res) {
        try {
            const { room_name, screen_type, total_rows, seats_per_row } = req.body;
            await Room.create({
                room_name,
                screen_type,
                total_rows: Number(total_rows) || 7,
                seats_per_row: Number(seats_per_row) || 12
            });
            res.redirect('/manager/rooms?success=' + encodeURIComponent('Tạo phòng chiếu và tự sinh sơ đồ ghế thành công!'));
        } catch (err) {
            res.redirect('/manager/rooms?error=' + encodeURIComponent('Lỗi tạo phòng chiếu: ' + err.message));
        }
    }

    static async roomDetail(req, res) {
        try {
            const room = await Room.findById(req.params.id);
            if (!room) {
                return res.redirect('/manager/rooms?error=' + encodeURIComponent('Không tìm thấy phòng!'));
            }

            const seats = await Seat.getByRoomId(room.id);
            const seatsByRow = {};
            seats.forEach(s => {
                if (!seatsByRow[s.seat_row]) {
                    seatsByRow[s.seat_row] = [];
                }
                seatsByRow[s.seat_row].push(s);
            });

            res.render('manager/room-detail', {
                title: `Sơ Đồ Ghế - ${room.room_name}`,
                room,
                seatsByRow,
                rows: Object.keys(seatsByRow)
            });
        } catch (err) {
            console.error('Lỗi chi tiết phòng:', err);
            res.redirect('/manager/rooms');
        }
    }

    static async updateSeat(req, res) {
        try {
            const { seat_id, seat_type, price_multiplier } = req.body;
            await Seat.updateType(seat_id, seat_type, Number(price_multiplier));
            res.json({ success: true, message: 'Cập nhật loại ghế thành công!' });
        } catch (err) {
            res.status(500).json({ success: false, message: err.message });
        }
    }

    // 4. Quản lý Suất chiếu & Thuật toán chống xung đột
    static async showtimes(req, res) {
        try {
            const filterDate = req.query.date || '';
            let showtimes = await Showtime.getAll();

            if (filterDate) {
                showtimes = showtimes.filter(st => {
                    const stDate = typeof st.start_time === 'string' ? st.start_time : st.start_time.toISOString();
                    return stDate.startsWith(filterDate);
                });
            }

            res.render('manager/showtimes', {
                title: 'Quản Lý Suất Chiếu & Lịch Trình',
                showtimes,
                filterDate,
                error: req.query.error || null,
                success: req.query.success || null
            });
        } catch (err) {
            console.error('Lỗi suất chiếu:', err);
            res.redirect('/manager/dashboard');
        }
    }

    static async createShowtimeForm(req, res) {
        try {
            const allMovies = await Movie.getAll();
            const movies = allMovies.filter(m => m.status !== 'ended');
            const rooms = await Room.getAll();

            res.render('manager/showtime-create', {
                title: 'Lập Lịch Suất Chiếu Mới (Kiểm Tra Xung Đột)',
                movies,
                rooms,
                error: null
            });
        } catch (err) {
            console.error('Lỗi form tạo suất chiếu:', err);
            res.redirect('/manager/showtimes');
        }
    }

    // API AJAX Kiểm tra xung đột thời gian thực trước khi submit
    static async apiCheckConflict(req, res) {
        try {
            const { room_id, start_time, duration, buffer_minutes } = req.query;

            if (!room_id || !start_time || !duration) {
                return res.status(400).json({ success: false, message: 'Thiếu dữ liệu để kiểm tra xung đột!' });
            }

            const conflictCheck = await ConflictDetector.checkConflict({
                roomId: Number(room_id),
                startTime: start_time,
                durationMinutes: Number(duration),
                bufferMinutes: Number(buffer_minutes) || 15
            });

            res.json(conflictCheck);
        } catch (err) {
            res.status(500).json({ success: false, message: err.message });
        }
    }

    // Lưu suất chiếu mới (Có áp dụng thuật toán kiểm tra xung đột)
    static async storeShowtime(req, res) {
        try {
            const { movie_id, room_id, start_time, buffer_minutes, base_price } = req.body;
            const movie = await Movie.findById(movie_id);

            if (!movie) {
                return res.redirect('/manager/showtimes?error=' + encodeURIComponent('Phim không tồn tại!'));
            }

            // 1. Áp dụng Thuật toán kiểm tra xung đột
            const conflictCheck = await ConflictDetector.checkConflict({
                roomId: Number(room_id),
                startTime: start_time,
                durationMinutes: Number(movie.duration),
                bufferMinutes: Number(buffer_minutes) || 15
            });

            if (conflictCheck.hasConflict) {
                const allMovies = await Movie.getAll();
                const movies = allMovies.filter(m => m.status !== 'ended');
                const rooms = await Room.getAll();
                return res.render('manager/showtime-create', {
                    title: 'Lập Lịch Suất Chiếu Mới',
                    movies,
                    rooms,
                    error: conflictCheck.message
                });
            }

            // 2. Không xung đột -> Lưu vào CSDL
            await Showtime.create({
                movie_id: Number(movie_id),
                room_id: Number(room_id),
                start_time: start_time.replace('T', ' '),
                end_time: conflictCheck.calculatedEndTime,
                buffer_minutes: Number(buffer_minutes) || 15,
                base_price: Number(base_price) || 80000
            });

            res.redirect('/manager/showtimes?success=' + encodeURIComponent('Tạo suất chiếu thành công! Không có xung đột lịch chiếu.'));
        } catch (err) {
            console.error('Lỗi tạo suất chiếu:', err);
            res.redirect('/manager/showtimes?error=' + encodeURIComponent('Lỗi hệ thống: ' + err.message));
        }
    }

    static async cancelShowtime(req, res) {
        try {
            await Showtime.cancel(req.params.id);
            res.redirect('/manager/showtimes?success=' + encodeURIComponent('Đã hủy suất chiếu thành công!'));
        } catch (err) {
            res.redirect('/manager/showtimes?error=' + encodeURIComponent(err.message));
        }
    }

    static async deleteShowtime(req, res) {
        try {
            await Showtime.delete(req.params.id);
            res.redirect('/manager/showtimes?success=' + encodeURIComponent('Đã xóa suất chiếu!'));
        } catch (err) {
            res.redirect('/manager/showtimes?error=' + encodeURIComponent(err.message));
        }
    }

    // 5. Quản lý Combo Bắp Nước
    static async combos(req, res) {
        try {
            const combos = await Combo.getAll();
            res.render('manager/combos', {
                title: 'Quản Lý Bắp Nước & Combo',
                combos,
                error: req.query.error || null,
                success: req.query.success || null
            });
        } catch (err) {
            console.error('Lỗi combos:', err);
            res.redirect('/manager/dashboard');
        }
    }

    static async storeCombo(req, res) {
        try {
            const { name, description, price, image_url, status } = req.body;
            await Combo.create({ name, description, price: Number(price), image_url, status });
            res.redirect('/manager/combos?success=' + encodeURIComponent('Thêm combo thành công!'));
        } catch (err) {
            res.redirect('/manager/combos?error=' + encodeURIComponent(err.message));
        }
    }

    static async updateCombo(req, res) {
        try {
            const { name, description, price, image_url, status } = req.body;
            await Combo.update(req.params.id, { name, description, price: Number(price), image_url, status });
            res.redirect('/manager/combos?success=' + encodeURIComponent('Cập nhật combo thành công!'));
        } catch (err) {
            res.redirect('/manager/combos?error=' + encodeURIComponent(err.message));
        }
    }

    static async deleteCombo(req, res) {
        try {
            await Combo.delete(req.params.id);
            res.redirect('/manager/combos?success=' + encodeURIComponent('Xóa combo thành công!'));
        } catch (err) {
            res.redirect('/manager/combos?error=' + encodeURIComponent(err.message));
        }
    }

    // 6. Báo cáo Doanh thu & Chi tiết tỷ lệ lấp đầy
    static async reports(req, res) {
        try {
            const stats = await Booking.getDashboardStats();
            const bookings = await Booking.getAll();

            res.render('manager/reports', {
                title: 'Báo Cáo Doanh Thu & Tỷ Lệ Lấp Đầy',
                stats,
                bookings
            });
        } catch (err) {
            console.error('Lỗi báo cáo:', err);
            res.redirect('/manager/dashboard');
        }
    }
}

module.exports = ManagerController;
