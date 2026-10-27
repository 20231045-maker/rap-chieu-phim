require('dotenv').config();
const mysql = require('mysql2/promise');
const path = require('path');
const fs = require('fs');

// Cấu hình kết nối MySQL Database
const pool = mysql.createPool({
    host: process.env.DB_HOST || '127.0.0.1',
    user: process.env.DB_USER || 'root',
    password: process.env.DB_PASSWORD || '',
    database: process.env.DB_NAME || 'cinema_db',
    port: Number(process.env.DB_PORT) || 3306,
    waitForConnections: true,
    connectionLimit: 15,
    queueLimit: 0,
    charset: 'utf8mb4',
    multipleStatements: true,
    decimalNumbers: true
});

// Tự động kiểm tra và khởi tạo bảng MySQL nếu chưa có
async function initDatabase() {
    try {
        const [tables] = await pool.query("SHOW TABLES LIKE 'movies'");
        if (tables.length === 0) {
            console.log('📌 Chưa tìm thấy các bảng trong MySQL cinema_db, đang tự động nạp schema_mysql.sql...');
            const schemaPath = path.join(__dirname, 'schema_mysql.sql');
            if (fs.existsSync(schemaPath)) {
                const schemaSql = fs.readFileSync(schemaPath, 'utf8');
                await pool.query(schemaSql);
                console.log('✅ Khởi tạo cấu trúc bảng MySQL cinema_db thành công!');
            }
        }
    } catch (err) {
        console.error('⚠️ Lỗi kiểm tra / khởi tạo CSDL MySQL:', err.message);
    }
}

initDatabase();

module.exports = {
    pool,
    // Helper lấy danh sách nhiều bản ghi
    async query(sql, params = []) {
        const [rows] = await pool.query(sql, params);
        return rows;
    },
    // Helper lấy 1 bản ghi duy nhất
    async get(sql, params = []) {
        const [rows] = await pool.query(sql, params);
        return rows && rows.length > 0 ? rows[0] : null;
    },
    // Helper thực thi INSERT, UPDATE, DELETE
    async run(sql, params = []) {
        const [result] = await pool.query(sql, params);
        return {
            lastInsertRowid: result.insertId,
            changes: result.affectedRows,
            insertId: result.insertId,
            affectedRows: result.affectedRows
        };
    },
    // Helper chạy raw script hoặc multi-statements
    async exec(sql) {
        return pool.query(sql);
    },
    // Shim tương thích cú pháp db.prepare cho các truy vấn cũ
    db: {
        prepare(sql) {
            return {
                run: async (...params) => {
                    const [res] = await pool.query(sql, params);
                    return {
                        lastInsertRowid: res.insertId,
                        changes: res.affectedRows,
                        insertId: res.insertId,
                        affectedRows: res.affectedRows
                    };
                },
                all: async (...params) => {
                    const [rows] = await pool.query(sql, params);
                    return rows;
                },
                get: async (...params) => {
                    const [rows] = await pool.query(sql, params);
                    return rows && rows.length > 0 ? rows[0] : null;
                }
            };
        }
    }
};
