const { query, get, run } = require('../database/db');

class Showtime {
    static async getAll() {
        return await query(`
            SELECT st.*, 
                   m.title as movie_title, m.poster_url, m.duration, m.age_rating,
                   r.room_name, r.screen_type, r.cinema_id,
                   c.name as cinema_name, c.city as cinema_city, c.district as cinema_district,
                   (SELECT COUNT(*) FROM seats WHERE room_id = r.id) as total_seats,
                   (SELECT COUNT(*) FROM tickets t 
                    JOIN bookings b ON t.booking_id = b.id 
                    WHERE t.showtime_id = st.id AND b.booking_status != 'cancelled') as booked_seats
            FROM showtimes st
            JOIN movies m ON st.movie_id = m.id
            JOIN rooms r ON st.room_id = r.id
            LEFT JOIN cinemas c ON r.cinema_id = c.id
            ORDER BY st.start_time DESC
        `);
    }

    static async findById(id) {
        return await get(`
            SELECT st.*, 
                   m.title as movie_title, m.original_title, m.poster_url, m.banner_url,
                   m.duration, m.genre, m.age_rating, m.trailer_url,
                   r.room_name, r.screen_type, r.total_rows, r.seats_per_row, r.cinema_id,
                   c.name as cinema_name, c.city as cinema_city, c.district as cinema_district, c.address as cinema_address,
                   (SELECT COUNT(*) FROM seats WHERE room_id = r.id) as total_seats,
                   (SELECT COUNT(*) FROM tickets t 
                    JOIN bookings b ON t.booking_id = b.id 
                    WHERE t.showtime_id = st.id AND b.booking_status != 'cancelled') as booked_seats
            FROM showtimes st
            JOIN movies m ON st.movie_id = m.id
            JOIN rooms r ON st.room_id = r.id
            LEFT JOIN cinemas c ON r.cinema_id = c.id
            WHERE st.id = ?
        `, [id]);
    }

    static async getByMovie(movieId, filterDate = null) {
        let sql = `
            SELECT st.*, 
                   r.room_name, r.screen_type, r.cinema_id,
                   c.name as cinema_name, c.city as cinema_city, c.district as cinema_district, c.address as cinema_address,
                   (SELECT COUNT(*) FROM seats WHERE room_id = r.id) as total_seats,
                   (SELECT COUNT(*) FROM tickets t 
                    JOIN bookings b ON t.booking_id = b.id 
                    WHERE t.showtime_id = st.id AND b.booking_status != 'cancelled') as booked_seats
            FROM showtimes st
            JOIN rooms r ON st.room_id = r.id
            LEFT JOIN cinemas c ON r.cinema_id = c.id
            WHERE st.movie_id = ? AND st.status = 'scheduled'
        `;
        const params = [movieId];

        if (filterDate) {
            sql += ` AND DATE(st.start_time) = DATE(?)`;
            params.push(filterDate);
        } else {
            // Suất chiếu từ hôm nay trở đi
            sql += ` AND st.start_time >= DATE_SUB(NOW(), INTERVAL 2 HOUR)`;
        }

        sql += ` ORDER BY st.start_time ASC`;
        return await query(sql, params);
    }

    static async getByDate(dateStr) {
        return await query(`
            SELECT st.*, 
                   m.title as movie_title, m.poster_url, m.duration, m.age_rating,
                   r.room_name, r.screen_type, r.cinema_id,
                   c.name as cinema_name, c.city as cinema_city, c.district as cinema_district
            FROM showtimes st
            JOIN movies m ON st.movie_id = m.id
            JOIN rooms r ON st.room_id = r.id
            LEFT JOIN cinemas c ON r.cinema_id = c.id
            WHERE DATE(st.start_time) = DATE(?) AND st.status = 'scheduled'
            ORDER BY st.start_time ASC
        `, [dateStr]);
    }

    static async create({ movie_id, room_id, start_time, end_time, buffer_minutes = 15, base_price = 80000 }) {
        const result = await run(`
            INSERT INTO showtimes (movie_id, room_id, start_time, end_time, buffer_minutes, base_price, status)
            VALUES (?, ?, ?, ?, ?, ?, 'scheduled')
        `, [movie_id, room_id, start_time, end_time, buffer_minutes, base_price]);
        return result.lastInsertRowid;
    }

    static async update(id, { movie_id, room_id, start_time, end_time, buffer_minutes, base_price, status }) {
        return await run(`
            UPDATE showtimes SET
                movie_id = ?, room_id = ?, start_time = ?, end_time = ?,
                buffer_minutes = ?, base_price = ?, status = ?
            WHERE id = ?
        `, [movie_id, room_id, start_time, end_time, buffer_minutes, base_price, status, id]);
    }

    static async delete(id) {
        // Kiểm tra xem đã có vé đặt chưa
        const ticketCount = await get(`
            SELECT COUNT(*) as count FROM tickets WHERE showtime_id = ?
        `, [id]);
        if (ticketCount && ticketCount.count > 0) {
            throw new Error('Không thể xóa suất chiếu đã có khách đặt vé! Bạn chỉ có thể hủy suất chiếu.');
        }
        return await run('DELETE FROM showtimes WHERE id = ?', [id]);
    }

    static async cancel(id) {
        return await run("UPDATE showtimes SET status = 'cancelled' WHERE id = ?", [id]);
    }
}

module.exports = Showtime;
