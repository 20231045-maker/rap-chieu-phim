/**
 * ====================================================================
 * HỌC PHẦN: ĐỒ ÁN CHUYÊN NGÀNH CÔNG NGHỆ PHẦN MỀM - NHÓM 10
 * Sinh viên phụ trách: Nguyễn Mạnh Quyết (MSV: 20231053)
 * MỤC 3.3.1 & 5.1.2: THUẬT TOÁN KIỂM TRA XUNG ĐỘT SUẤT CHIẾU
 * (SHOWTIME CONFLICT DETECTION ALGORITHM)
 * ====================================================================
 * 
 * Ý tưởng thuật toán:
 * Hai khoảng thời gian [T1_start, T1_end] và [T2_start, T2_end] giao nhau
 * khi và chỉ khi:
 * (T1_start < T2_end) VÀ (T1_end > T2_start)
 * 
 * Trong đó:
 * - End_time của một suất chiếu = Start_time + Thời lượng phim + Buffer_minutes (thời gian dọn dẹp & vệ sinh phòng rạp)
 * - Xung đột xảy ra khi 2 suất chiếu trùng phòng (cùng room_id) và có khoảng thời gian giao thoa.
 */

const { query } = require('../database/db');

class ConflictDetector {
    /**
     * Kiểm tra xem suất chiếu dự kiến có bị trùng lịch trong phòng hay không
     * @param {Object} params
     * @param {number} params.roomId - ID phòng chiếu
     * @param {string|Date} params.startTime - Thời gian bắt đầu ('YYYY-MM-DD HH:MM:SS')
     * @param {number} params.durationMinutes - Thời lượng phim (phút)
     * @param {number} [params.bufferMinutes=15] - Thời gian đệm vệ sinh phòng (phút)
     * @param {number|null} [params.excludeShowtimeId=null] - Bỏ qua ID suất chiếu khi đang sửa (Update)
     * @returns {Promise<Object>} { hasConflict: boolean, message: string, conflictingShowtime?: Object, calculatedEndTime: string }
     */
    static async checkConflict({ roomId, startTime, durationMinutes, bufferMinutes = 15, excludeShowtimeId = null }) {
        const start = new Date(startTime);
        if (isNaN(start.getTime())) {
            throw new Error('Thời gian bắt đầu suất chiếu không hợp lệ!');
        }

        // Tính thời gian kết thúc (đã cộng thời lượng + thời gian đệm dọn phòng)
        const totalDurationMs = (Number(durationMinutes) + Number(bufferMinutes)) * 60 * 1000;
        const end = new Date(start.getTime() + totalDurationMs);

        // Chuẩn hóa định dạng 'YYYY-MM-DD HH:MM:SS'
        const formatDateTime = (d) => {
            const pad = (n) => String(n).padStart(2, '0');
            const year = d.getFullYear();
            const month = pad(d.getMonth() + 1);
            const day = pad(d.getDate());
            const hours = pad(d.getHours());
            const mins = pad(d.getMinutes());
            const secs = pad(d.getSeconds());
            return `${year}-${month}-${day} ${hours}:${mins}:${secs}`;
        };

        const newStartStr = formatDateTime(start);
        const newEndStr = formatDateTime(end);

        // Lấy tất cả các suất chiếu đang có trong cùng phòng (trừ các suất đã hủy)
        let sql = `
            SELECT st.*, m.title as movie_title, r.room_name
            FROM showtimes st
            JOIN movies m ON st.movie_id = m.id
            JOIN rooms r ON st.room_id = r.id
            WHERE st.room_id = ? 
              AND st.status != 'cancelled'
        `;
        const params = [roomId];

        if (excludeShowtimeId) {
            sql += ' AND st.id != ?';
            params.push(excludeShowtimeId);
        }

        const existingShowtimes = await query(sql, params);

        // Áp dụng điều kiện giao thoa khoảng thời gian:
        // (new_start < existing_end) AND (new_end > existing_start)
        for (const existing of existingShowtimes) {
            const existStart = new Date(existing.start_time);
            const existEnd = new Date(existing.end_time);

            const isOverlap = (start < existEnd) && (end > existStart);

            if (isOverlap) {
                const formatDisplay = (d) => {
                    const pad = (n) => String(n).padStart(2, '0');
                    return `${pad(d.getHours())}:${pad(d.getMinutes())} (${pad(d.getDate())}/${pad(d.getMonth() + 1)})`;
                };

                return {
                    hasConflict: true,
                    calculatedEndTime: newEndStr,
                    conflictingShowtime: existing,
                    message: `⚠️ XUNG ĐỘT SUẤT CHIẾU! ${existing.room_name} đã có lịch chiếu phim "${existing.movie_title}" từ ${formatDisplay(existStart)} đến ${formatDisplay(existEnd)} (đã gồm ${existing.buffer_minutes || 15}p dọn phòng). Vui lòng chọn khung giờ khác!`
                };
            }
        }

        return {
            hasConflict: false,
            calculatedEndTime: newEndStr,
            bufferMinutes,
            message: 'Khung giờ hợp lệ, không có xung đột!'
        };
    }
}

module.exports = ConflictDetector;
