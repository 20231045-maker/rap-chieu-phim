const fs = require('fs');
const path = require('path');
const mysql = require('mysql2/promise');

async function importDatabase() {
    console.log('====================================================');
    console.log('🔄 BẮT ĐẦU NHẬP CƠ SỞ DỮ LIỆU CINEMA_DB VÀO MYSQL');
    console.log('====================================================');

    const config = {
        host: process.env.DB_HOST || '127.0.0.1',
        user: process.env.DB_USER || 'root',
        password: process.env.DB_PASSWORD || '',
        port: Number(process.env.DB_PORT) || 3306,
        multipleStatements: true,
        charset: 'utf8mb4'
    };

    console.log(`📌 Kết nối tới MySQL: ${config.user}@${config.host}:${config.port}...`);

    let conn;
    try {
        conn = await mysql.createConnection(config);
        console.log('✅ Kết nối MySQL thành công!');

        const dumpPath = path.join(__dirname, 'cinema_db_full.sql');
        if (!fs.existsSync(dumpPath)) {
            throw new Error(`Không tìm thấy tệp dump tại: ${dumpPath}`);
        }

        console.log('📌 Đang đọc tệp database/cinema_db_full.sql...');
        const sql = fs.readFileSync(dumpPath, 'utf8');

        console.log('📌 Đang thực thi nạp toàn bộ bảng và dữ liệu mẫu...');
        await conn.query(sql);

        // Tự động nạp lịch chiếu cho tất cả phim đang chiếu đến 31/12/2026
        const seedShowtimes = require('./seed_showtimes_to_20261231');
        await seedShowtimes();

        console.log('\n====================================================');
        console.log('🎉 NHẬP CSDL THÀNH CÔNG 100%!');
        console.log('- Đã tạo CSDL: cinema_db');
        console.log('- Đã nạp: 100 bộ phim, 10 cụm rạp, 22 phòng chiếu, 1584 ghế, các tài khoản và suất chiếu.');
        console.log('====================================================\n');
    } catch (err) {
        console.error('❌ LỖI KHI NHẬP CSDL:', err.message);
        console.error('👉 Vui lòng kiểm tra lại dịch vụ MySQL (XAMPP/Laragon) đã được bật chưa.');
    } finally {
        if (conn) await conn.end();
        process.exit(0);
    }
}

importDatabase();
