const Movie = require('../models/Movie');
const Showtime = require('../models/Showtime');
const { query } = require('../database/db');

class HomeController {
    static async index(req, res) {
        try {
            const nowShowing = await Movie.getNowShowing();
            const comingSoon = await Movie.getComingSoon();

            // Lấy danh sách suất chiếu hôm nay
            const todayStr = new Date().toISOString().split('T')[0];
            const selectedCinemaId = req.cookies.selectedCinemaId || req.query.cinema_id || null;

            let todayShowtimes = [];
            let currentCinema = null;

            if (selectedCinemaId) {
                const cinRows = await query('SELECT * FROM cinemas WHERE id = ?', [selectedCinemaId]);
                if (cinRows.length > 0) currentCinema = cinRows[0];

                todayShowtimes = await query(`
                    SELECT st.*, m.title as movie_title, m.poster_url, m.age_rating, m.duration,
                           r.room_name, r.screen_type, r.cinema_id,
                           c.name as cinema_name, c.city as cinema_city, c.district as cinema_district
                    FROM showtimes st
                    JOIN movies m ON st.movie_id = m.id
                    JOIN rooms r ON st.room_id = r.id
                    LEFT JOIN cinemas c ON r.cinema_id = c.id
                    WHERE DATE(st.start_time) = DATE(?) AND st.status = 'scheduled' AND r.cinema_id = ?
                    ORDER BY st.start_time ASC
                    LIMIT 16
                `, [todayStr, selectedCinemaId]);
            }

            if (todayShowtimes.length === 0) {
                todayShowtimes = await query(`
                    SELECT st.*, m.title as movie_title, m.poster_url, m.age_rating, m.duration,
                           r.room_name, r.screen_type, r.cinema_id,
                           c.name as cinema_name, c.city as cinema_city, c.district as cinema_district
                    FROM showtimes st
                    JOIN movies m ON st.movie_id = m.id
                    JOIN rooms r ON st.room_id = r.id
                    LEFT JOIN cinemas c ON r.cinema_id = c.id
                    WHERE DATE(st.start_time) = DATE(?) AND st.status = 'scheduled'
                    ORDER BY st.start_time ASC
                    LIMIT 16
                `, [todayStr]);
            }

            res.render('client/home', {
                title: 'CINESTAR - Hệ Thống Đặt Vé Xem Phim & Quản Lý Suất Chiếu Trực Tuyến',
                nowShowing,
                comingSoon,
                todayShowtimes,
                todayStr,
                currentCinema,
                welcome: req.query.welcome || null
            });
        } catch (err) {
            console.error('Lỗi trang chủ:', err);
            res.status(500).render('client/404', {
                title: '500 - Lỗi',
                message: 'Không thể tải dữ liệu trang chủ: ' + err.message
            });
        }
    }

    static async showMovies(req, res) {
        try {
            const { keyword, genre, status } = req.query;
            let movies;

            if (keyword || genre || status) {
                movies = await Movie.search({ keyword, genre, status });
            } else {
                movies = await Movie.getAll();
            }

            // Danh sách các thể loại phim phổ biến
            const genres = [
                'Hành động', 'Khoa học viễn tưởng', 'Phiêu lưu', 'Hoạt hình',
                'Tâm lý', 'Tình cảm', 'Gia đình', 'Hài hước', 'Kinh dị'
            ];

            // Breadcrumbs chuẩn CGV (Tham khảo media_1791900552504.png)
            let breadcrumbs = [{ label: 'Phim', url: '/movies' }];
            let pageTitle = 'Phim Chiếu Rạp';
            if (status === 'coming_soon') {
                breadcrumbs.push({ label: 'Phim Sắp Chiếu' });
                pageTitle = 'Phim Sắp Chiếu - CINESTAR';
            } else if (status === 'now_showing') {
                breadcrumbs.push({ label: 'Phim Đang Chiếu' });
                pageTitle = 'Phim Đang Chiếu - CINESTAR';
            } else {
                breadcrumbs.push({ label: 'Toàn Bộ Phim' });
            }

            res.render('client/movies', {
                title: pageTitle,
                movies,
                genres,
                currentKeyword: keyword || '',
                currentGenre: genre || '',
                currentStatus: status || '',
                breadcrumbs
            });
        } catch (err) {
            console.error('Lỗi danh sách phim:', err);
            res.status(500).render('client/404', {
                title: '500 - Lỗi',
                message: 'Không thể tải danh sách phim: ' + err.message
            });
        }
    }

    static pricing(req, res) {
        res.render('client/pricing', {
            title: 'Bảng Giá Vé & Dịch Vụ - CINESTAR Cinema',
            breadcrumbs: [{ label: 'Bảng Giá Vé' }]
        });
    }

    static about(req, res) {
        res.render('client/about', {
            title: 'Giới Thiệu Đề Tài Đồ Án Chuyên Ngành CNPM',
            breadcrumbs: [{ label: 'Giới Thiệu' }]
        });
    }
}

module.exports = HomeController;
