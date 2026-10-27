const { query, get, run } = require('../database/db');

class Movie {
    static async getAll() {
        return await query('SELECT * FROM movies ORDER BY id DESC');
    }

    static async getNowShowing() {
        return await query("SELECT * FROM movies WHERE status = 'now_showing' ORDER BY release_date DESC");
    }

    static async getComingSoon() {
        return await query("SELECT * FROM movies WHERE status = 'coming_soon' ORDER BY release_date ASC");
    }

    static async findById(id) {
        return await get('SELECT * FROM movies WHERE id = ?', [id]);
    }

    static async search({ keyword, genre, status }) {
        let sql = 'SELECT * FROM movies WHERE 1=1';
        const params = [];

        if (keyword) {
            sql += ' AND (title LIKE ? OR original_title LIKE ? OR director LIKE ? OR cast LIKE ?)';
            const k = `%${keyword}%`;
            params.push(k, k, k, k);
        }

        if (genre) {
            sql += ' AND genre LIKE ?';
            params.push(`%${genre}%`);
        }

        if (status) {
            sql += ' AND status = ?';
            params.push(status);
        }

        sql += ' ORDER BY id DESC';
        return await query(sql, params);
    }

    static async create(data) {
        const {
            title, original_title, genre, duration, release_date, end_date,
            age_rating, director, cast, description, poster_url, banner_url,
            trailer_url, language, status
        } = data;

        const result = await run(`
            INSERT INTO movies (
                title, original_title, genre, duration, release_date, end_date,
                age_rating, director, cast, description, poster_url, banner_url,
                trailer_url, language, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        `, [
            title, original_title || '', genre, duration, release_date, end_date || null,
            age_rating || 'P', director || '', cast || '', description || '',
            poster_url || '/images/default-poster.jpg',
            banner_url || poster_url || '/images/default-banner.jpg',
            trailer_url || '', language || 'Phụ đề Tiếng Việt', status || 'now_showing'
        ]);

        return result.lastInsertRowid;
    }

    static async update(id, data) {
        const {
            title, original_title, genre, duration, release_date, end_date,
            age_rating, director, cast, description, poster_url, banner_url,
            trailer_url, language, status
        } = data;

        return await run(`
            UPDATE movies SET
                title = ?, original_title = ?, genre = ?, duration = ?, release_date = ?, end_date = ?,
                age_rating = ?, director = ?, cast = ?, description = ?, poster_url = ?, banner_url = ?,
                trailer_url = ?, language = ?, status = ?
            WHERE id = ?
        `, [
            title, original_title || '', genre, duration, release_date, end_date || null,
            age_rating || 'P', director || '', cast || '', description || '',
            poster_url || '/images/default-poster.jpg',
            banner_url || poster_url || '/images/default-banner.jpg',
            trailer_url || '', language || 'Phụ đề Tiếng Việt', status || 'now_showing',
            id
        ]);
    }

    static async delete(id) {
        return await run('DELETE FROM movies WHERE id = ?', [id]);
    }
}

module.exports = Movie;
