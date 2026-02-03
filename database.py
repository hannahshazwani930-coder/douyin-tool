# database.py
import sqlite3
import os
from datetime import datetime, timedelta
from config import ADMIN_ACCOUNT, ADMIN_PASSWORD, DEFAULT_INVITE_CODE

DB_FILE = "system_data.db"

def init_db():
    """初始化数据库表结构"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # 用户表：增加注册时间和邀请者字段
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        account TEXT PRIMARY KEY,
        password TEXT,
        invite_code TEXT,
        referrer TEXT,
        vip_until DATE,
        created_at TIMESTAMP
    )''')
    # 初始管理员账号
    cursor.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?, ?)",
                   (ADMIN_ACCOUNT, ADMIN_PASSWORD, "ADMIN888", "SYSTEM", "2099-12-31", datetime.now()))
    conn.commit()
    conn.close()

def login_user(account, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE account=?", (account,))
    result = cursor.fetchone()
    conn.close()
    if result and result[0] == password:
        return True, "登录成功"
    return False, "账号或密码错误"

def register_user(account, password, invite_code):
    if not account or not password:
        return False, "账号密码不能为空"
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 检查账号是否存在
    cursor.execute("SELECT account FROM users WHERE account=?", (account,))
    if cursor.fetchone():
        conn.close()
        return False, "账号已存在"
    
    # 默认赠送3天VIP
    vip_date = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
    my_invite_code = account[-6:] # 简单生成个邀请码
    
    try:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)",
                       (account, password, my_invite_code, invite_code, vip_date, datetime.now()))
        conn.commit()
        return True, "注册成功"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def get_user_vip_status(account):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT vip_until FROM users WHERE account=?", (account,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return True, f"VIP有效期至: {result[0]}"
    return False, "普通用户"

def get_user_invite_info(account):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT invite_code FROM users WHERE account=?", (account,))
    code = cursor.fetchone()
    cursor.execute("SELECT COUNT(*) FROM users WHERE referrer=(SELECT invite_code FROM users WHERE account=?)", (account,))
    count = cursor.fetchone()
    conn.close()
    return code[0] if code else "N/A", count[0] if count else 0
