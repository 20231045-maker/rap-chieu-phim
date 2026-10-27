const { query, get, run } = require('../database/db');

class SeatLock {
    static async cleanExpired() {
        const now = new Date().toISOString().replace('T', ' ').substring(0, 19);
        return await run('DELETE FROM seat_locks WHERE expires_at <= ?', [now]);
    }

    static async getActiveLocks(showtimeId) {
        await this.cleanExpired();
        const now = new Date().toISOString().replace('T', ' ').substring(0, 19);
        return await query('SELECT * FROM seat_locks WHERE showtime_id = ? AND expires_at > ?', [showtimeId, now]);
    }

    static async lockSeats({ showtimeId, seatIds, sessionId, userId = null, minutes = 5 }) {
        await this.cleanExpired();
        const now = new Date();
        const nowStr = now.toISOString().replace('T', ' ').substring(0, 19);
        
        const expireTime = new Date(now.getTime() + minutes * 60 * 1000);
        const expireStr = expireTime.toISOString().replace('T', ' ').substring(0, 19);

        // 1. Kiểm tra xem có ghế nào đã được bán chưa
        for (const seatId of seatIds) {
            const booked = await get(`
                SELECT t.id, s.seat_code FROM tickets t
                JOIN bookings b ON t.booking_id = b.id
                JOIN seats s ON t.seat_id = s.id
                WHERE t.showtime_id = ? AND t.seat_id = ? AND b.booking_status != 'cancelled'
            `, [showtimeId, seatId]);

            if (booked) {
                return {
                    success: false,
                    message: `Ghế ${booked.seat_code} vừa được người khác thanh toán! Vui lòng chọn ghế khác.`
                };
            }

            // 2. Kiểm tra xem có ghế nào đang bị người khác khóa không
            const locked = await get(`
                SELECT sl.*, s.seat_code FROM seat_locks sl
                JOIN seats s ON sl.seat_id = s.id
                WHERE sl.showtime_id = ? AND sl.seat_id = ? AND sl.session_id != ? AND sl.expires_at > ?
            `, [showtimeId, seatId, sessionId, nowStr]);

            if (locked) {
                return {
                    success: false,
                    message: `Ghế ${locked.seat_code} đang được khách khác giữ chỗ để thanh toán! Vui lòng chọn ghế khác.`
                };
            }
        }

        // Xóa các lock cũ của session này trong suất chiếu này
        await run('DELETE FROM seat_locks WHERE showtime_id = ? AND session_id = ?', [showtimeId, sessionId]);

        // Tạo khóa giữ ghế mới
        for (const seatId of seatIds) {
            await run(`
                INSERT INTO seat_locks (showtime_id, seat_id, session_id, user_id, locked_at, expires_at)
                VALUES (?, ?, ?, ?, ?, ?)
            `, [showtimeId, seatId, sessionId, userId, nowStr, expireStr]);
        }

        return {
            success: true,
            expiresAt: expireTime,
            minutes
        };
    }

    static async releaseSession(showtimeId, sessionId) {
        return await run('DELETE FROM seat_locks WHERE showtime_id = ? AND session_id = ?', [showtimeId, sessionId]);
    }
}

module.exports = SeatLock;
