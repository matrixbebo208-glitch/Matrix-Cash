import sqlite3

def init_db():
    # الاتصال بقاعدة البيانات (سيتم إنشاؤها تلقائياً كملف)
    conn = sqlite3.connect('matrix_cash.db')
    cursor = conn.cursor()

    # 1. إنشاء جدول المستخدم (المحفظة)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_wallet (
            phone_number TEXT PRIMARY KEY,
            balance REAL DEFAULT 0.0
        )
    ''')

    # 2. إنشاء جدول المهمات (Tasks)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_desc TEXT,
            target_amount REAL,
            is_completed INTEGER DEFAULT 0
        )
    ''')

    # إضافة بياناتك الافتراضية لو الجدول لسه جديد
    cursor.execute('SELECT * FROM user_wallet WHERE phone_number = ?', ("01224815487",))
    if not cursor.fetchone():
        cursor.execute('INSERT INTO user_wallet (phone_number, balance) VALUES (?, ?)', ("01224815487", 0.0))

    # إضافة مهمات تجريبية (الـ 50 والـ 30 جنيه)
    cursor.execute('SELECT COUNT(*) FROM tasks')
    if cursor.fetchone()[0] == 0:
        missions = [
            ("أضف 50 جنيه للمحفظة عبر الكاميرا", 50.0),
            ("أضف 30 جنيه للمحفظة عبر الكاميرا", 30.0),
            ("توفير أول 100 جنيه في ماتركس كاش", 100.0)
        ]
        cursor.executemany('INSERT INTO tasks (task_desc, target_amount) VALUES (?, ?)', missions)

    conn.commit()
    conn.close()
    print("✅ Matrix Cash Database initialized successfully!")

if __name__ == "__main__":
    init_db()
