-- 用户表
CREATE TABLE users (
  user_id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL UNIQUE,
  password VARCHAR(50) NOT NULL,
  phone VARCHAR(20),
  email VARCHAR(100),
  role ENUM('admin', 'buyer', 'seller') DEFAULT 'buyer'
);

-- 图书分类表
CREATE TABLE book_types (
  type_id INT PRIMARY KEY AUTO_INCREMENT,
  type_name VARCHAR(50) NOT NULL,
  description TEXT
);

-- 图书表
CREATE TABLE books (
  book_id INT PRIMARY KEY AUTO_INCREMENT,
  title VARCHAR(100) NOT NULL,
  author VARCHAR(50),
  price DECIMAL(10, 2) NOT NULL,
  description TEXT,
  seller_id INT,
  type_id INT,
  status ENUM('available', 'sold') DEFAULT 'available',
  FOREIGN KEY (seller_id) REFERENCES users(user_id) ON DELETE CASCADE,
  FOREIGN KEY (type_id) REFERENCES book_types(type_id) ON DELETE SET NULL
);

-- 订单表
CREATE TABLE orders (
  order_id INT PRIMARY KEY AUTO_INCREMENT,
  buyer_id INT,
  seller_id INT,
  book_id INT,
  order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  status ENUM('pending', 'completed', 'cancelled') DEFAULT 'pending',
  FOREIGN KEY (buyer_id) REFERENCES users(user_id) ON DELETE SET NULL,
  FOREIGN KEY (seller_id) REFERENCES users(user_id) ON DELETE SET NULL,
  FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE SET NULL
);
