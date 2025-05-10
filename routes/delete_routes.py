from flask import Blueprint, request, jsonify
import db_config

delete_bp = Blueprint('delete_bp', __name__)

# 判断管理员权限（公共函数）
def is_admin(user_id):
    conn = db_config.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result and result['role'] == 'admin'

# 删除图书（仅管理员）
@delete_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    data = request.json
    user_id = data.get('user_id')

    if not is_admin(user_id):
        return jsonify({"error": "无权限，只有管理员可以删除图书"}), 403

    conn = db_config.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE book_id = %s", (book_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "图书已删除"})


# 删除图书分类
@delete_bp.route('/book_types/<int:type_id>', methods=['DELETE'])
def delete_book_type(type_id):
    data = request.json
    user_id = data.get('user_id')

    if not is_admin(user_id):
        return jsonify({"error": "无权限，只有管理员可以删除分类"}), 403

    conn = db_config.get_connection()
    cursor = conn.cursor()

    # 检查是否有关联图书
    cursor.execute("SELECT COUNT(*) AS count FROM books WHERE type_id = %s", (type_id,))
    count = cursor.fetchone()['count']
    if count > 0:
        conn.close()
        return jsonify({"error": "该分类仍有关联图书，无法删除"}), 400

    cursor.execute("DELETE FROM book_types WHERE type_id = %s", (type_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "图书分类已删除"})


# 删除订单
@delete_bp.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    data = request.json
    user_id = data.get('user_id')

    if not is_admin(user_id):
        return jsonify({"error": "无权限，只有管理员可以删除订单"}), 403

    conn = db_config.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "订单已删除"})


# 删除用户
@delete_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = db_config.get_connection()
    cursor = conn.cursor()

    # 可加判断用户是否有关联订单
    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "用户已删除"})