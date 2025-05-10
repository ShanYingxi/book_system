from flask import Blueprint, request, jsonify
import db_config
import re

post_bp = Blueprint('post_bp', __name__)

# 添加图书（卖家发布）
@post_bp.route('/books', methods=['POST'])
def add_book():
    data = request.json
    conn = db_config.get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO books (title, author, price, description, seller_id, type_id, status) VALUES (%s, %s, %s, %s, %s, %s, 'available')"
    cursor.execute(sql, (
        data['title'], data['author'], data['price'], data['description'],
        data['seller_id'], data['type_id']
    ))
    conn.commit()
    conn.close()
    return jsonify({'message': '图书添加成功'})

# 用户注册
@post_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # 密码格式检查（6位，仅字母和数字）
    if not re.fullmatch(r'[A-Za-z0-9]{6}', password):
        return jsonify({"error": "密码必须为6位，仅包含字母和数字"}), 400

    conn = db_config.get_connection()
    cursor = conn.cursor()

    # 用户名是否已存在
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        conn.close()
        return jsonify({"error": "用户名已存在"}), 400

    # 插入新用户
    sql = "INSERT INTO users (username, password, phone, email, role) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (
        username, password, data['phone'],
        data['email'], data['role']
    ))
    conn.commit()
    conn.close()
    return jsonify({'message': '注册成功'})


# 下订单
@post_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    conn = db_config.get_connection()
    cursor = conn.cursor()

    # 检查图书是否还未被卖出
    cursor.execute("SELECT status FROM books WHERE book_id = %s", (data['book_id'],))
    result = cursor.fetchone()

    if not result:
        conn.close()
        return jsonify({"error": "图书不存在"}), 404

    if result['status'] != 'available':
        conn.close()
        return jsonify({"error": "图书已售出，无法下单"}), 400

    # 创建订单
    sql = """
        INSERT INTO orders (buyer_id, seller_id, book_id, status)
        VALUES (%s, %s, %s, 'pending')
    """
    cursor.execute(sql, (
        data['buyer_id'],
        data['seller_id'],
        data['book_id']
    ))

    # 更新图书状态
    cursor.execute("UPDATE books SET status = 'sold' WHERE book_id = %s", (data['book_id'],))

    conn.commit()
    conn.close()
    return jsonify({"message": "下单成功"})

# 添加新的图书分类
@post_bp.route('/book_types', methods=['POST'])
def add_book_type():
    data = request.json
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"error": "缺少 user_id 参数"}), 400

    conn = db_config.get_connection()
    cursor = conn.cursor()

    # 查询用户角色
    cursor.execute("SELECT role FROM users WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()

    if not result:
        conn.close()
        return jsonify({"error": "用户不存在"}), 404

    if result['role'] != 'admin':
        conn.close()
        return jsonify({"error": "无权限，仅管理员可添加分类"}), 403

    # 插入分类
    cursor.execute(
        "INSERT INTO book_types (type_name, description) VALUES (%s, %s)",
        (data['type_name'], data['description'])
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "图书分类添加成功"})