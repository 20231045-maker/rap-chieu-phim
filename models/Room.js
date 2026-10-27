const { query, get, run } = require('../database/db');

class Room {
    static async getAll() {
        return await query(`
            SELECT r.*,
                   (SELECT COUNT(*) FROM seats s WHERE s.room_id = r.id) as actual_seats_count
            FROM rooms r
            ORDER BY r.id ASC
        `);
    }

    static async findById(id) {
        return await get('SELECT * FROM rooms WHERE id = ?', [id]);
    }

    static async create({ room_name, screen_type = '2D', total_rows = 7, seats_per_row = 12 }) {
        const total_seats = total_rows * seats_per_row;
        const result = await run(`
            INSERT INTO rooms (room_name, screen_type, total_rows, seats_per_row, total_seats, status)
            VALUES (?, ?, ?, ?, ?, 'active')
        `, [room_name, screen_type, total_rows, seats_per_row, total_seats]);
        
        const roomId = result.lastInsertRowid;

        // Tự động sinh danh sách ghế cho phòng
        const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

        for (let r = 0; r < total_rows; r++) {
            const rowChar = alphabet[r];
            for (let num = 1; num <= seats_per_row; num++) {
                let seatType = 'regular';
                let mult = 1.0;
                // Nếu là các hàng giữa -> VIP
                if (r >= 2 && r <= total_rows - 2) {
                    seatType = 'vip';
                    mult = 1.25;
                } else if (r === total_rows - 1) { // Hàng cuối -> Sweetbox
                    seatType = 'sweetbox';
                    mult = 2.0;
                }
                await run(`
                    INSERT INTO seats (room_id, seat_row, seat_number, seat_code, seat_type, price_multiplier)
                    VALUES (?, ?, ?, ?, ?, ?)
                `, [roomId, rowChar, num, `${rowChar}${num}`, seatType, mult]);
            }
        }

        return roomId;
    }

    static async update(id, { room_name, screen_type, status }) {
        return await run(`
            UPDATE rooms SET room_name = ?, screen_type = ?, status = ? WHERE id = ?
        `, [room_name, screen_type, status, id]);
    }

    static async delete(id) {
        return await run('DELETE FROM rooms WHERE id = ?', [id]);
    }
}

module.exports = Room;
