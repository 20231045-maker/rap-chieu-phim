const { query, get, run } = require('../database/db');

class Combo {
    static async getAllActive() {
        return await query("SELECT * FROM combos WHERE status = 'active' ORDER BY price ASC");
    }

    static async getAll() {
        return await query('SELECT * FROM combos ORDER BY id DESC');
    }

    static async findById(id) {
        return await get('SELECT * FROM combos WHERE id = ?', [id]);
    }

    static async create({ name, description, price, image_url, status = 'active' }) {
        const result = await run(`
            INSERT INTO combos (name, description, price, image_url, status)
            VALUES (?, ?, ?, ?, ?)
        `, [name, description, price, image_url || '/images/default-combo.jpg', status]);
        return result.lastInsertRowid;
    }

    static async update(id, { name, description, price, image_url, status }) {
        return await run(`
            UPDATE combos SET name = ?, description = ?, price = ?, image_url = ?, status = ?
            WHERE id = ?
        `, [name, description, price, image_url, status, id]);
    }

    static async delete(id) {
        return await run('DELETE FROM combos WHERE id = ?', [id]);
    }
}

module.exports = Combo;
