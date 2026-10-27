const { query, get, run } = require('../database/db');
const bcrypt = require('bcryptjs');

class User {
    static async findByEmail(email) {
        return await get(`
            SELECT u.*, r.name as role_name, r.display_name as role_display
            FROM users u
            JOIN roles r ON u.role_id = r.id
            WHERE u.email = ?
        `, [email]);
    }

    static async findById(id) {
        return await get(`
            SELECT u.*, r.name as role_name, r.display_name as role_display
            FROM users u
            JOIN roles r ON u.role_id = r.id
            WHERE u.id = ?
        `, [id]);
    }

    static async getAll() {
        return await query(`
            SELECT u.id, u.full_name, u.email, u.phone, u.avatar, u.status, u.created_at,
                   r.id as role_id, r.name as role_name, r.display_name as role_display
            FROM users u
            JOIN roles r ON u.role_id = r.id
            ORDER BY u.id DESC
        `);
    }

    static async getAllRoles() {
        return await query('SELECT * FROM roles ORDER BY id ASC');
    }

    static async create({ role_id, full_name, email, phone, password, status = 'active' }) {
        const salt = bcrypt.genSaltSync(10);
        const password_hash = bcrypt.hashSync(password, salt);
        const result = await run(`
            INSERT INTO users (role_id, full_name, email, phone, password_hash, status)
            VALUES (?, ?, ?, ?, ?, ?)
        `, [role_id, full_name, email, phone, password_hash, status]);
        return result.lastInsertRowid;
    }

    static async update(id, { full_name, phone, role_id, status, password }) {
        if (password && password.trim() !== '') {
            const salt = bcrypt.genSaltSync(10);
            const password_hash = bcrypt.hashSync(password, salt);
            return await run(`
                UPDATE users
                SET full_name = ?, phone = ?, role_id = ?, status = ?, password_hash = ?
                WHERE id = ?
            `, [full_name, phone, role_id, status, password_hash, id]);
        } else {
            return await run(`
                UPDATE users
                SET full_name = ?, phone = ?, role_id = ?, status = ?
                WHERE id = ?
            `, [full_name, phone, role_id, status, id]);
        }
    }

    static async updateProfile(id, { full_name, phone }) {
        return await run(`
            UPDATE users SET full_name = ?, phone = ? WHERE id = ?
        `, [full_name, phone, id]);
    }

    static async changePassword(id, newPassword) {
        const salt = bcrypt.genSaltSync(10);
        const hash = bcrypt.hashSync(newPassword, salt);
        return await run(`UPDATE users SET password_hash = ? WHERE id = ?`, [hash, id]);
    }

    static async delete(id) {
        return await run('DELETE FROM users WHERE id = ?', [id]);
    }

    static verifyPassword(plainPassword, hashedPassword) {
        return bcrypt.compareSync(plainPassword, hashedPassword);
    }
}

module.exports = User;
