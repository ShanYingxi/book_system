from flask import Blueprint, request, jsonify
import db_config

get_bp = Blueprint('get_bp', __name__)

# 获取图书
@get_bp.route('/books', methods=['GET'])
def get_books():
    conn = db_config.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return jsonify(books)

# 用户查看买过的订单
@get_bp.route('/orders/user/<int:user_id>', methods=['GET'])
def get_user_orders(user_id):
    conn = db_config.get_connection()
    cursor = conn.cursor()
    
    sql = """
    SELECT 
        o.order_id,
        o.order_time,
        o.status,
        b.title AS book_title,
        b.price,
        u.username AS seller_name
    FROM orders o
    JOIN books b ON o.book_id = b.book_id
    JOIN users u ON o.seller_id = u.user_id
    WHERE o.buyer_id = %s
    ORDER BY o.order_time DESC
    """
    
    cursor.execute(sql, (user_id,))
    orders = cursor.fetchall()
    
    conn.close()
    return jsonify(orders)

# 用户查看卖出的订单
@get_bp.route('/orders/seller/<int:user_id>', methods=['GET'])
def get_seller_orders(user_id):
    conn = db_config.get_connection()
    cursor = conn.cursor()

    sql = """
    SELECT 
        o.order_id,
        o.order_time,
        o.status,
        b.title AS book_title,
        b.price,
        u.username AS buyer_name
    FROM orders o
    JOIN books b ON o.book_id = b.book_id
    JOIN users u ON o.buyer_id = u.user_id
    WHERE o.seller_id = %s
    ORDER BY o.order_time DESC
    """

    cursor.execute(sql, (user_id,))
    orders = cursor.fetchall()
    conn.close()
    return jsonify(orders)

# 获取指定类型的图书
@get_bp.route('/books/type/<int:type_id>', methods=['GET'])
def get_books_by_type(type_id):
    conn = db_config.get_connection()
    cursor = conn.cursor()

    sql = """
    SELECT 
        b.book_id,
        b.title,
        b.author,
        b.price,
        b.description,
        b.status,
        t.type_name
    FROM books b
    JOIN book_types t ON b.type_id = t.type_id
    WHERE b.type_id = %s
    """

    cursor.execute(sql, (type_id,))
    books = cursor.fetchall()
    conn.close()
    return jsonify(books)

# 获取所有图书分类
@get_bp.route('/book_types', methods=['GET'])
def get_all_book_types():
    conn = db_config.get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM book_types")
    types = cursor.fetchall()

    conn.close()
    return jsonify(types)

# 获取用户信息（新增）
@get_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user_info(user_id):
    conn = db_config.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, username, phone, email, role FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "用户不存在"}), 404