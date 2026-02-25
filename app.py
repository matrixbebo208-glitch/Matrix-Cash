from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

# دالة للاتصال بقاعدة البيانات
def get_db_connection():
    conn = sqlite3.connect('matrix_cash.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    # جلب الرصيد والمهمات لعرضهم على التابلت والكمبيوتر
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM user_wallet WHERE phone_number = ?', ("01224815487",)).fetchone()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template('index.html', user=user, tasks=tasks)

@app.route('/add_money', methods=['POST'])
def add_money():
    # دي الدالة اللي هيناديها ملف الكاميرا لما يصور الفلوس
    amount = request.json.get('amount')
    conn = get_db_connection()
    
    # تحديث الرصيد
    conn.execute('UPDATE user_wallet SET balance = balance + ? WHERE phone_number = ?', (amount, "01224815487"))
    
    # تحديث المهمة لو المبلغ طابق مهمة موجودة
    conn.execute('UPDATE tasks SET is_completed = 1 WHERE target_amount = ?', (amount,))
    
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "new_balance": "updated"})

if __name__ == "__main__":
    # تشغيل السيرفر ليكون متاحاً على الشبكة المحلية (التابلت والكمبيوتر)
    app.run(host='0.0.0.0', port=5000, debug=True)
