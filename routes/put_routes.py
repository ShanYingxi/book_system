from flask import Blueprint, request, jsonify
import db_config, re

put_bp = Blueprint('put_bp', __name__)

# 更新订单状态
@put_bp.route('/orders/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    data = request.json
    user_id = data.get('user_id')
    new_status = data.get('status')

    # 合法状态检查
    valid_status = ['pending', 'completed', 'cancelled']
    if new_status not in valid_status:
        return jsonify({"error": "无效的订单状态"}), 400

    conn = db_config.get_connection()
    cursor = conn.cursor()

    # 查询发起人是否为管理员
    cursor.execute("SELECT role FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return jsonify({"error": "用户不存在"}), 404

    is_admin_user = user['role'] == 'admin'

    # 查询订单信息
    cursor.execute("SELECT seller_id FROM orders WHERE order_id = %s", (order_id,))
    order = cursor.fetchone()
    if not order:
        conn.close()
        return jsonify({"error": "订单不存在"}), 404

    seller_id = order['seller_id']

    # 权限判断：必须是管理员或订单对应卖家
    if not (is_admin_user or user_id == seller_id):
        conn.close()
        return jsonify({"error": "无权限修改该订单"}), 403

    # 执行更新
    cursor.execute(
        "UPDATE orders SET status = %s WHERE order_id = %s",
        (new_status, order_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": f"订单状态已更新为 {new_status}"})

# 修改图书价格（仅管理员）
@put_bp.route('/books/<int:book_id>/price', methods=['PUT'])
def update_book_price(book_id):
    data = request.json
    user_id = data.get('user_id')
    new_price = data.get('price')

    if new_price is None:
        return jsonify({"error": "请提供新价格"}), 400

    conn = db_config.get_connection()
    cursor = conn.cursor()

    # 获取图书所属卖家
    cursor.execute("SELECT seller_id FROM books WHERE book_id = %s", (book_id,))
    book = cursor.fetchone()
    if not book:
        conn.close()
        return jsonify({"error": "图书不存在"}), 404

    if book['seller_id'] != user_id:
        conn.close()
        return jsonify({"error": "无权限，只有卖家本人可修改图书价格"}), 403

    # 执行更新
    cursor.execute("UPDATE books SET price = %s WHERE book_id = %s", (new_price, book_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "图书价格已更新"})


# 修改图书名字&分类（仅管理员）
@put_bp.route('/books/<int:book_id>/basic', methods=['PUT'])
def update_book_title_and_type(book_id):
    data = request.json
    user_id = data.get('user_id')
    new_title = data.get('title')
    new_type_id = data.get('type_id')

    # 必须同时提供两个字段
    if not new_title or new_type_id is None:
        return jsonify({"error": "必须同时提供 title 和 type_id"}), 400

    conn = db_config.get_connection()
    cursor = conn.cursor()

    # 获取该图书的卖家 ID
    cursor.execute("SELECT seller_id FROM books WHERE book_id = %s", (book_id,))
    book = cursor.fetchone()
    if not book:
        conn.close()
        return jsonify({"error": "图书不存在"}), 404

    if book['seller_id'] != user_id:
        conn.close()
        return jsonify({"error": "无权限，只有卖家本人可修改图书信息"}), 403

    # 执行更新
    cursor.execute(
        "UPDATE books SET title = %s, type_id = %s WHERE book_id = %s",
        (new_title, new_type_id, book_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "图书标题与分类已更新"})

# 修改电话、密码、邮箱（本人）
@put_bp.route('/users/<int:target_user_id>', methods=['PUT'])
def update_user_info(target_user_id):
    data = request.json
    user_id = data.get('user_id')

    # 权限判断：只能本人修改
    if user_id != target_user_id:
        return jsonify({"error": "无权限，用户只能修改自己的信息"}), 403

    update_fields = []
    values = []

    # 可修改字段：phone、email、password
    if 'phone' in data:
        update_fields.append("phone = %s")
        values.append(data['phone'])

    if 'email' in data:
        update_fields.append("email = %s")
        values.append(data['email'])

    if 'password' in data:
        password = data['password']
        # 密码格式校验
        if not re.fullmatch(r'[A-Za-z0-9]{6}', password):
            return jsonify({"error": "密码必须为6位，仅包含字母和数字"}), 400
        update_fields.append("password = %s")
        values.append(password)

    if not update_fields:
        return jsonify({"error": "请至少提供要修改的字段"}), 400

    # 执行更新
    conn = db_config.get_connection()
    cursor = conn.cursor()
    sql = f"UPDATE users SET {', '.join(update_fields)} WHERE user_id = %s"
    values.append(target_user_id)
    cursor.execute(sql, values)
    conn.commit()
    conn.close()

    return jsonify({"message": "用户信息已更新"})