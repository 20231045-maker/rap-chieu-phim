const Movie = require('../models/Movie');
const Showtime = require('../models/Showtime');

class MovieController {
    static async detail(req, res) {
        try {
            const movieId = req.params.id;
            const movie = await Movie.findById(movieId);

            if (!movie) {
                return res.status(404).render('client/404', {
                    title: 'Không Tìm Thấy Phim',
                    message: 'Phim bạn đang tìm không tồn tại hoặc đã ngừng chiếu.'
                });
            }

            // Tạo danh sách 7 ngày tới
            const today = new Date();
            const dates = [];
            const daysOfWeek = ['Chủ Nhật', 'Thứ Hai', 'Thứ Ba', 'Thứ Tư', 'Thứ Năm', 'Thứ Sáu', 'Thứ Bảy'];

            for (let i = 0; i < 7; i++) {
                const d = new Date(today);
                d.setDate(d.getDate() + i);
                const pad = (n) => String(n).padStart(2, '0');
                const dateStr = `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
                const dayName = i === 0 ? 'Hôm nay' : (i === 1 ? 'Ngày mai' : daysOfWeek[d.getDay()]);
                const label = `${d.getDate()}/${d.getMonth() + 1}`;

                dates.push({
                    dateStr,
                    dayName,
                    label
                });
            }

            const selectedDate = req.query.date || dates[0].dateStr;

            // Nếu người dùng chọn ngày khác (đến 31/12/2026) chưa có trong danh sách 7 ngày nhanh
            if (!dates.some(d => d.dateStr === selectedDate)) {
                const selD = new Date(selectedDate);
                if (!isNaN(selD.getTime())) {
                    const pad = (n) => String(n).padStart(2, '0');
                    dates.push({
                        dateStr: selectedDate,
                        dayName: daysOfWeek[selD.getDay()],
                        label: `${pad(selD.getDate())}/${pad(selD.getMonth() + 1)}`
                    });
                }
            }

            const showtimes = await Showtime.getByMovie(movieId, selectedDate);

            // Nhóm suất chiếu theo định dạng phòng (IMAX, 3D, 2D)
            const groupedShowtimes = {};
            showtimes.forEach(st => {
                const key = st.screen_type || '2D';
                if (!groupedShowtimes[key]) {
                    groupedShowtimes[key] = [];
                }
                groupedShowtimes[key].push(st);
            });

            const statusLabel = movie.status === 'now_showing' ? 'Phim Đang Chiếu' : 'Phim Sắp Chiếu';
            const breadcrumbs = [
                { label: 'Phim', url: '/movies' },
                { label: statusLabel, url: `/movies?status=${movie.status}` },
                { label: movie.title }
            ];

            res.render('client/movie-detail', {
                title: `${movie.title} - Lịch Chiếu & Đặt Vé`,
                movie,
                dates,
                selectedDate,
                groupedShowtimes,
                totalShowtimes: showtimes.length,
                breadcrumbs
            });
        } catch (err) {
            console.error('Lỗi chi tiết phim:', err);
            res.status(500).render('client/404', {
                title: '500 - Lỗi',
                message: 'Không thể tải chi tiết phim: ' + err.message
            });
        }
    }
}

module.exports = MovieController;
