const http = require('http');
const { pool, query, get, run } = require('./database/db');
const ConflictDetector = require('./services/conflictDetector');
const SeatLock = require('./models/SeatLock');
const Ticket = require('./models/Ticket');
const Booking = require('./models/Booking');

async function runTests() {
    console.log('====================================================');
    console.log('🧪 BẮT ĐẦU KIỂM THỬ HỆ THỐNG RẠP CHIẾU PHIM (MYSQL 3NF)');
    console.log('====================================================');

    let passed = 0;
    let failed = 0;

    function assert(condition, message) {
        if (condition) {
            console.log(`  ✅ [PASS] ${message}`);
            passed++;
        } else {
            console.error(`  ❌ [FAIL] ${message}`);
            failed++;
        }
    }

    try {
        // 1. Kiểm thử CSDL & Dữ liệu mẫu trên MySQL
        console.log('\n--- 1. Kiểm thử CSDL MySQL 3NF ---');
        const users = await query('SELECT * FROM users');
        assert(users.length >= 4, `Đã nạp ${users.length} tài khoản người dùng mẫu trong MySQL`);

        const movies = await query('SELECT * FROM movies');
        assert(movies.length >= 5, `Đã nạp ${movies.length} bộ phim`);

        const rooms = await query('SELECT * FROM rooms');
        assert(rooms.length >= 3, `Đã nạp ${rooms.length} phòng chiếu`);

        const seats = await query('SELECT * FROM seats');
        assert(seats.length > 100, `Đã tự sinh ${seats.length} ghế ngồi theo phòng`);

        const showtimes = await query('SELECT * FROM showtimes');
        assert(showtimes.length >= 5, `Đã nạp ${showtimes.length} suất chiếu`);

        const cinemas = await query('SELECT * FROM cinemas');
        assert(cinemas.length === 10, `Đã nạp đầy đủ ${cinemas.length} cụm rạp Cinestar (5 Hà Nội: Cầu Giấy, Hoàn Kiếm, Thanh Xuân, Hai Bà Trưng, Đống Đa; 5 TP.HCM: Q1, Q3, Q4, Q5, Q10)`);

        // 2. Kiểm thử Thuật toán kiểm tra xung đột suất chiếu (Week 3, 3.3.1)
        console.log('\n--- 2. Kiểm thử Thuật Toán Xung Đột Suất Chiếu (Conflict Detector) ---');
        const st1 = showtimes.find(s => s.room_id === 1);
        if (st1) {
            // Thử xếp lịch trùng giờ trong phòng 1
            const testConflict = await ConflictDetector.checkConflict({
                roomId: 1,
                startTime: st1.start_time,
                durationMinutes: 120,
                bufferMinutes: 15
            });
            assert(testConflict.hasConflict === true, 'Phát hiện chính xác XUNG ĐỘT khi xếp trùng phòng và giờ chiếu!');
            console.log(`     -> Thông báo xung đột: "${testConflict.message}"`);

            // Thử xếp lịch vào giờ khác hoặc phòng khác không trùng
            const testNoConflict = await ConflictDetector.checkConflict({
                roomId: 1,
                startTime: '2026-10-20 02:00:00', // Đêm muộn ngày khác
                durationMinutes: 90,
                bufferMinutes: 15
            });
            assert(testNoConflict.hasConflict === false, 'Xác nhận KHÔNG XUNG ĐỘT khi phòng còn trống!');
        }

        // 3. Kiểm thử Kỹ thuật khóa giữ ghế tạm thời (Week 3, 3.3.2)
        console.log('\n--- 3. Kiểm thử Khóa Giữ Ghế Tạm Thời (Seat Lock Mechanism) ---');
        await pool.query('DELETE FROM seat_locks');
        const testSeat = seats.find(s => s.room_id === 1 && s.seat_code === 'A1');
        if (testSeat && st1) {
            // Session A khóa ghế A1
            const lockRes1 = await SeatLock.lockSeats({
                showtimeId: st1.id,
                seatIds: [testSeat.id],
                sessionId: 'SESSION_CLIENT_A',
                minutes: 5
            });
            assert(lockRes1.success === true, 'Session A giữ ghế A1 thành công trong 5 phút');

            // Session B cố gắng khóa cùng ghế A1
            const lockRes2 = await SeatLock.lockSeats({
                showtimeId: st1.id,
                seatIds: [testSeat.id],
                sessionId: 'SESSION_CLIENT_B',
                minutes: 5
            });
            assert(lockRes2.success === false, 'Session B bị từ chối giữ ghế A1 đang bị Session A chiếm dụng (Tránh Race Condition)!');

            // Nhả ghế A
            await SeatLock.releaseSession(st1.id, 'SESSION_CLIENT_A');
            const lockRes3 = await SeatLock.lockSeats({
                showtimeId: st1.id,
                seatIds: [testSeat.id],
                sessionId: 'SESSION_CLIENT_B',
                minutes: 5
            });
            assert(lockRes3.success === true, 'Sau khi Session A nhả ghế, Session B giữ ghế thành công');
            await SeatLock.releaseSession(st1.id, 'SESSION_CLIENT_B');
        }

        // 4. Kiểm thử Soát vé QR và cảnh báo gian lận (Week 6, 5.2.10)
        console.log('\n--- 4. Kiểm thử Soát Vé QR & Ngăn Chặn Gian Lận (Staff Check-In) ---');
        // Reset vé kiểm thử về unused trước khi test
        await run("UPDATE tickets SET status = 'unused', checked_in_at = NULL, checked_in_by = NULL WHERE ticket_code = 'TKT-20261013-D05'");

        // Vé chưa dùng: TKT-20261013-D05
        const check1 = await Ticket.checkIn('TKT-20261013-D05', 3);
        assert(check1.success === true, 'Vé hợp lệ chưa dùng: Soát vé thành công và cập nhật trạng thái "checked_in"');

        // Thử soát lại chính vé đó lần 2
        const check2 = await Ticket.checkIn('TKT-20261013-D05', 3);
        assert(check2.success === false && check2.status === 'already_used', 'Soát vé lần 2: Phát hiện và cảnh báo GIAN LẬN vé đã qua sử dụng!');
        console.log(`     -> Cảnh báo gian lận: "${check2.message}"`);

        // Soát vé không tồn tại
        const check3 = await Ticket.checkIn('TKT-FAKE-CODE-999', 3);
        assert(check3.success === false && check3.status === 'not_found', 'Vé giả/không tồn tại: Hệ thống từ chối!');

        // 5. Kiểm thử Thống kê Dashboard & Tỷ lệ lấp đầy rạp
        console.log('\n--- 5. Kiểm thử Thống kê Dashboard (Manager Analytics) ---');
        const stats = await Booking.getDashboardStats();
        assert(stats.totalRevenue > 0, `Tổng doanh thu tính toán: ${stats.totalRevenue.toLocaleString('vi-VN')} đ`);
        assert(typeof stats.occupancyRate === 'number', `Tỷ lệ lấp đầy rạp (Occupancy rate): ${stats.occupancyRate}%`);
        assert(stats.revenueByDays.length === 7, 'Thống kê doanh thu theo 7 ngày cho Chart.js chuẩn xác');

        console.log('\n====================================================');
        console.log(`🏁 KẾT QUẢ KIỂM THỬ: ${passed} PASS, ${failed} FAIL`);
        console.log('====================================================\n');
    } catch (err) {
        console.error('Lỗi khi chạy kiểm thử:', err);
    } finally {
        await pool.end();
    }
}

runTests();
