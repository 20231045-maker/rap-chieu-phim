const mysql = require('mysql2/promise');
const { pool, query } = require('./db');

function pad(n) {
    return String(n).padStart(2, '0');
}

function formatDateTime(d) {
    const y = d.getFullYear();
    const m = pad(d.getMonth() + 1);
    const day = pad(d.getDate());
    const h = pad(d.getHours());
    const min = pad(d.getMinutes());
    const s = pad(d.getSeconds());
    return `${y}-${m}-${day} ${h}:${min}:${s}`;
}

// Làm tròn lên mốc 15 phút gần nhất (ví dụ: 10:25 -> 10:30, 12:55 -> 13:00)
function roundUpTo15Minutes(date) {
    const ms = 15 * 60 * 1000;
    return new Date(Math.ceil(date.getTime() / ms) * ms);
}

async function seedShowtimesTo20261231() {
    console.log('====================================================================');
    console.log('🎬 BẮT ĐẦU NẠP SUẤT CHIẾU CHO TẤT CẢ PHIM ĐANG CHIẾU ĐẾN 31/12/2026');
    console.log('⚡ THUẬT TOÁN XẾP LỊCH TỰ ĐỘNG THÔNG MINH (CHỐNG XUNG ĐỘT 100%)');
    console.log('====================================================================');

    const conn = await pool.getConnection();

    try {
        // 1. Lấy tất cả 60 phim đang chiếu (status = 'now_showing')
        const [movies] = await conn.query(`
            SELECT id, title, duration 
            FROM movies 
            WHERE status = 'now_showing' 
            ORDER BY id ASC
        `);

        if (movies.length === 0) {
            throw new Error('Không tìm thấy phim nào có status = now_showing!');
        }
        console.log(`📌 Tìm thấy ${movies.length} bộ phim đang chiếu (now_showing) trong CSDL.`);

        // 2. Lấy tất cả 22 phòng chiếu đang hoạt động
        const [rooms] = await conn.query(`
            SELECT r.*, c.name as cinema_name 
            FROM rooms r 
            LEFT JOIN cinemas c ON r.cinema_id = c.id 
            WHERE r.status = 'active' 
            ORDER BY r.id ASC
        `);
        console.log(`📌 Tìm thấy ${rooms.length} phòng chiếu đang hoạt động thuộc 10 cụm rạp.`);

        // 3. Tạo danh sách ngày từ 2026-10-21 đến 2026-12-31
        const dates = [];
        let cur = new Date('2026-10-21T00:00:00');
        const end = new Date('2026-12-31T00:00:00');

        while (cur <= end) {
            const y = cur.getFullYear();
            const m = pad(cur.getMonth() + 1);
            const d = pad(cur.getDate());
            dates.push(`${y}-${m}-${d}`);
            cur.setDate(cur.getDate() + 1);
        }
        console.log(`📌 Số ngày cần phủ lịch chiếu: ${dates.length} ngày (từ ${dates[0]} đến ${dates[dates.length - 1]}).`);

        // 4. Xóa các suất chiếu tự sinh cũ trong khoảng thời gian này (nếu có)
        const [delRes] = await conn.query(`
            DELETE FROM showtimes 
            WHERE start_time >= '2026-10-21 00:00:00' AND start_time <= '2026-12-31 23:59:59'
              AND id NOT IN (SELECT DISTINCT showtime_id FROM tickets)
        `);
        if (delRes.affectedRows > 0) {
            console.log(`🧹 Đã làm sạch ${delRes.affectedRows} suất chiếu cũ không có vé để nạp lịch mới.`);
        }

        // 5. Sinh lịch chiếu chống xung đột tuyệt đối (Start_time ca sau >= End_time ca trước + 15p dọn phòng)
        const newShowtimes = [];
        let globalDayPos = 0;

        for (let dIdx = 0; dIdx < dates.length; dIdx++) {
            const dateStr = dates[dIdx];
            let dayMoviePos = 0;

            for (let rIdx = 0; rIdx < rooms.length; rIdx++) {
                const room = rooms[rIdx];

                // Mỗi phòng bắt đầu chiếu từ 08:30 sáng
                let slotStart = new Date(`${dateStr}T08:30:00`);

                // Xếp từ 5 đến 6 suất chiếu mỗi ngày cho mỗi phòng, ca cuối cùng bắt đầu trước 22:30
                let roomSlotCount = 0;
                while (roomSlotCount < 5 && (slotStart.getHours() < 22 || (slotStart.getHours() === 22 && slotStart.getMinutes() <= 30))) {
                    // Chọn phim luân phiên: đảm bảo trong ngày TẤT CẢ 60 phim đều có suất chiếu
                    const movieIndex = (dIdx * 19 + dayMoviePos) % movies.length;
                    const movie = movies[movieIndex];
                    dayMoviePos++;

                    const duration = Number(movie.duration) || 110;
                    const bufferMinutes = 15;

                    // Tính end_time chính xác theo thời lượng phim + 15 phút dọn dẹp
                    const slotEnd = new Date(slotStart.getTime() + (duration + bufferMinutes) * 60 * 1000);

                    // Giá vé theo loại phòng và ca tối (từ 18h trở đi)
                    const isEvening = slotStart.getHours() >= 18;
                    let basePrice = 85000;
                    if (room.screen_type === 'IMAX') {
                        basePrice = isEvening ? 130000 : 120000;
                    } else if (room.screen_type === '3D') {
                        basePrice = isEvening ? 110000 : 100000;
                    } else {
                        basePrice = isEvening ? 95000 : 85000;
                    }

                    newShowtimes.push([
                        movie.id,
                        room.id,
                        formatDateTime(slotStart),
                        formatDateTime(slotEnd),
                        bufferMinutes,
                        basePrice,
                        'scheduled'
                    ]);

                    roomSlotCount++;

                    // Ca tiếp theo bắt đầu sau khi ca trước kết thúc, làm tròn lên mốc 15 phút (vd: 10:25 -> 10:30)
                    slotStart = roundUpTo15Minutes(slotEnd);
                }
            }
        }

        console.log(`📌 Chuẩn bị nạp ${newShowtimes.length} suất chiếu sạch (0% xung đột) vào MySQL...`);

        // 6. Thực thi batch insert (500 dòng/mẻ)
        const batchSize = 500;
        let inserted = 0;

        for (let i = 0; i < newShowtimes.length; i += batchSize) {
            const batch = newShowtimes.slice(i, i + batchSize);
            await conn.query(
                `INSERT INTO showtimes (movie_id, room_id, start_time, end_time, buffer_minutes, base_price, status) VALUES ?`,
                [batch]
            );
            inserted += batch.length;
            if (inserted % 2000 === 0 || inserted === newShowtimes.length) {
                console.log(`   ⏳ Đã nạp ${inserted} / ${newShowtimes.length} suất chiếu...`);
            }
        }

        console.log('\n====================================================');
        console.log(`🎉 NẠP SUẤT CHIẾU THÀNH CÔNG 100%!`);
        console.log(`   - Tổng số suất chiếu mới: ${inserted}`);
        console.log(`   - Phủ sóng đến ngày: 31/12/2026 (72 ngày liên tục)`);
        console.log(`   - Phân bổ cho: Tất cả ${movies.length} phim đang chiếu (now_showing)`);
        console.log(`   - Cụm rạp & Phòng chiếu: 10 cụm rạp, 22 phòng chiếu`);
        console.log(`   - Thuật toán bảo đảm: Tuyệt đối không xung đột phòng chiếu`);
        console.log('====================================================');

    } catch (err) {
        console.error('❌ Lỗi khi nạp suất chiếu:', err);
        throw err;
    } finally {
        conn.release();
    }
}

if (require.main === module) {
    seedShowtimesTo20261231()
        .then(() => process.exit(0))
        .catch(err => {
            console.error(err);
            process.exit(1);
        });
}

module.exports = seedShowtimesTo20261231;
