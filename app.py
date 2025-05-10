from flask import Flask, render_template, request, jsonify
import db_config
import re

from routes.get_routes import get_bp
from routes.post_routes import post_bp
from routes.put_routes import put_bp
from routes.delete_routes import delete_bp

app = Flask(__name__) 

# 注册蓝图
app.register_blueprint(get_bp)
app.register_blueprint(post_bp)
app.register_blueprint(put_bp)
app.register_blueprint(delete_bp)

# 首页：导航页
@app.route('/')
def index():
    return render_template("index.html")

# 图书列表页（原首页功能）
@app.route('/books_page')
def books_page():
    conn = db_config.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return render_template("books.html", books=books)


# 注册页面
@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

# 注册提交处理
@app.route('/register', methods=['POST'])
def register_submit():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not re.fullmatch(r'[A-Za-z0-9]{6}', password):
        return jsonify({"error": "密码必须为6位，仅包含字母和数字"}), 400

    conn = db_config.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        conn.close()
        return jsonify({"error": "用户名已存在"}), 400

    cursor.execute("""
        INSERT INTO users (username, password, phone, email, role)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        username, password,
        data.get('phone'), data.get('email'),
        data.get('role', 'buyer')
    ))

    conn.commit()
    conn.close()
    return jsonify({"message": "注册成功"})

# 其他功能页面
@app.route('/add_book')
def add_book_page():
    return render_template("add_book.html")

@app.route('/orders')
def orders_page():
    return render_template("orders.html")

@app.route('/update_user')
def update_user_page():
    return render_template("update_user.html")

@app.route('/book_types_view')
def view_types_page():
    return render_template("book_types.html")

@app.route('/delete_user')
def delete_user_page():
    return render_template("delete_user.html")

@app.route('/update_order')
def update_order_page():
    return render_template("update_order.html")

@app.route('/update_price')
def update_price_page():
    return render_template("update_price.html")

@app.route('/update_book_basic')
def update_book_basic_page():
    return render_template("update_book_basic.html")

@app.route('/books_by_type')
def books_by_type_page():
    return render_template("books_by_type.html")

@app.route('/all_types')
def all_types_page():
    return render_template("all_types.html")

@app.route('/user_info')
def user_info_page():
    return render_template("user_info.html")

@app.route('/delete_order')
def delete_order_page():
    return render_template("delete_order.html")

@app.route('/delete_book')
def delete_book_page():
    return render_template("delete_book.html")


if __name__ == '__main__':
    app.run(debug=True)
