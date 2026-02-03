# database.py
import sqlite3
import os
from datetime import datetime, timedelta
from config import (
    DB_FILE, 
    ADMIN_ACCOUNT, 
    ADMIN_PASSWORD, 
    DEFAULT_INVITE_CODE,
    REWARD_DAYS_NEW_USER
)

def init_db():
    """初始化数据库并创建管理员"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        account TEXT PRIMARY KEY,
        password TEXT,
        invite_code TEXT,
        referrer TEXT,
        vip_until DATE,
        created_at TIMESTAMP
    )''')
    # 插入默认管理员
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
    
    cursor.execute("SELECT account FROM users WHERE account=?", (account,))
    if cursor.fetchone():
        conn.close()
        return False, "账号已存在"
    
    # 赠送 VIP 天数
    vip_date = (datetime.now() + timedelta(days=REWARD_DAYS_NEW_USER)).strftime('%Y-%m-%d')
    my_invite_code = account[-6:] # 取账号后六位作为邀请码
    
    try:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)",
                       (account, password, my_invite_code, invite_code, vip_date, datetime.now()))
        conn.commit()
        return True, "注册成功"
    except Exception as e:
        return False, f"数据库错误: {str(e)}"
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
    # 统计有多少人的推荐人是我的邀请码
    if code:
        cursor.execute("SELECT COUNT(*) FROM users WHERE referrer=?", (code[0],))
        count = cursor.fetchone()
        conn.close()
        return code[0], count[0] if count else 0
    conn.close()
    return "N/A", 0
