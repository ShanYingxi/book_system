# 📚 二手书系统

这是一个基于 Python Flask + MySQL 的二手书买卖管理系统，支持图书发布、分类管理、下单、查询、修改与删除等核心功能。

## 🚀 项目结构

```
book_system/
├── app.py                 # 主程序入口
├── db_config.py           # 数据库连接配置（从 .env 加载）
├── routes/                # 各功能模块（GET/POST/PUT/DELETE）
├── templates/             # 所有 HTML 页面
├── .env.example           # 环境变量模板（请复制为 .env 使用）
└── .gitignore             # 忽略不上传的文件（如 .env、缓存等）
├── requirements.txt # 依赖库列表
└── book_system_schema.sql # 数据库建表语句（MySQL）

## ⚙️ 本地运行方式

1. 安装依赖：

```bash
pip install flask flask-cors pymysql python-dotenv
```

2. 创建 `.env` 文件：

```bash
cp .env.example .env
# 然后编辑 .env 填入你的数据库信息
```

3. 启动服务：

```bash
python app.py
```

访问地址：[http://localhost:5000](http://localhost:5000)

🗄️ 数据库说明
使用 MySQL

数据库名建议为 book_market

建表语句位于 book_system_schema.sql

快速执行建表语句：
CREATE DATABASE book_market DEFAULT CHARSET utf8mb4;
USE book_market;
-- 执行 book_system_schema.sql 中的 SQL