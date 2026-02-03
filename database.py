# database.py
import sqlite3
import datetime
import uuid
import hashlib
from config import DB_FILE, ADMIN_ACCOUNT, ADMIN_INIT_PASSWORD, REWARD_DAYS_NEW_USER, REWARD_DAYS_REFERRER, GLOBAL_INVITE_CODE
from utils import hash_password, generate_invite_code

# --- 基础连接 ---
def get_conn():
    return sqlite3.connect(DB_FILE)

# --- 初始化 ---
def init_db():
    conn = get_conn()
    c = conn.cursor()
    # 建表
    c.execute('''CREATE TABLE IF NOT EXISTS users (phone TEXT PRIMARY KEY, password_hash TEXT, register_time TIMESTAMP, last_login_ip TEXT, last_login_time TIMESTAMP, own_invite_code TEXT UNIQUE, invited_by TEXT, invite_count INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS access_codes (code TEXT PRIMARY KEY, duration_days INTEGER, activated_at TIMESTAMP, expire_at TIMESTAMP, status TEXT, create_time TIMESTAMP, bind_user TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS feedbacks (id INTEGER PRIMARY KEY AUTOINCREMENT, user_phone TEXT, content TEXT, reply TEXT, create_time TIMESTAMP, status TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)''')
    
    # 兼容性更新 (静默处理)
    for col in ["own_invite_code", "invited_by"]:
        try: c.execute(f"ALTER TABLE users ADD COLUMN {col} TEXT")
        except: pass
    try: c.execute("ALTER TABLE users ADD COLUMN invite_count INTEGER DEFAULT 0")
    except: pass
    
    # 初始化管理员
    c.execute("SELECT phone FROM users WHERE phone=?", (ADMIN_ACCOUNT,))
    if not c.fetchone():
        pwd_hash = hash_password(ADMIN_INIT_PASSWORD)
        c.execute("INSERT INTO users (phone, password_hash, register_time, own_invite_code) VALUES (?, ?, ?, ?)", 
                  (ADMIN_ACCOUNT, pwd_hash, datetime.datetime.now(), "ADMIN888"))
    
    conn.commit()
    conn.close()

# --- 用户逻辑 ---
def login_user(account, password):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE phone=?", (account,))
    row = c.fetchone()
    conn.close()
    if row and row[0] == hash_password(password):
        return True, "登录成功"
    return False, "账号或密码错误"

def register_user(account, password, invite_code_used):
    conn = get_conn()
    c = conn.cursor()
    try:
        # 生成唯一邀请码
        new_own_code = generate_invite_code()
        while True:
            c.execute("SELECT phone FROM users WHERE own_invite_code=?", (new_own_code,))
            if not c.fetchone(): break
            new_own_code = generate_invite_code()
        
        # 查找邀请人
        referrer = None
        if invite_code_used != GLOBAL_INVITE_CODE:
            c.execute("SELECT phone FROM users WHERE own_invite_code=?", (invite_code_used,))
            row = c.fetchone()
            if row: referrer = row[0]
            
        c.execute("INSERT INTO users (phone, password_hash, register_time, own_invite_code, invited_by) VALUES (?, ?, ?, ?, ?)", 
                  (account, hash_password(password), datetime.datetime.now(), new_own_code, referrer))
        conn.commit()
        
        # 发放奖励
        add_vip_days(account, REWARD_DAYS_NEW_USER, "NEW_USER")
        if referrer:
            add_vip_days(referrer, REWARD_DAYS_REFERRER, "REFERRAL")
            conn.execute("UPDATE users SET invite_count = invite_count + 1 WHERE phone=?", (referrer,))
            conn.commit()
            
        return True, "注册成功"
    except Exception as e:
        return False, f"注册失败: {str(e)}"
    finally:
        conn.close()

# --- VIP 逻辑 ---
def add_vip_days(account, days, source="system"):
    conn = get_conn()
    c = conn.cursor()
    # 计算新的过期时间
    c.execute("SELECT expire_at FROM access_codes WHERE bind_user=? AND status='active'", (account,))
    rows = c.fetchall()
    now = datetime.datetime.now()
    if rows:
        max_expire = max([datetime.datetime.strptime(str(r[0]).split('.')[0], '%Y-%m-%d %H:%M:%S') for r in rows])
        start_time = max_expire if max_expire > now else now
    else:
        start_time = now
    
    expire_at = start_time + datetime.timedelta(days=days)
    new_code = f"GIFT-{source}-{str(uuid.uuid4())[:6].upper()}"
    c.execute("INSERT INTO access_codes (code, duration_days, activated_at, expire_at, status, create_time, bind_user) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (new_code, days, now, expire_at, 'active', now, account))
    conn.commit()
    conn.close()

def get_user_vip_status(phone):
    if phone == ADMIN_ACCOUNT: return True, "👑 超级管理员"
    conn = get_conn()
    c = conn.cursor()
    now = datetime.datetime.now()
    c.execute("SELECT expire_at FROM access_codes WHERE bind_user=? AND status='active'", (phone,))
    rows = c.fetchall()
    conn.close()
    
    if not rows: return False, "未开通会员"
    
    max_expire = max([datetime.datetime.strptime(str(r[0]).split('.')[0], '%Y-%m-%d %H:%M:%S') for r in rows])
    if max_expire > now:
        days_left = (max_expire - now).days
        return True, f"VIP (剩{days_left}天)" 
    return False, "会员已过期"

# --- 杂项 ---
def get_user_invite_info(phone):
    conn = get_conn()
    c = conn.cursor()
    try:
        c.execute("SELECT own_invite_code, invite_count FROM users WHERE phone=?", (phone,))
        row = c.fetchone()
    except: row = None
    conn.close()
    if row: return row[0], row[1]
    return "...", 0

def get_setting(key):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT value FROM settings WHERE key=?", (key,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else ""

def update_setting(key, value):
    conn = get_conn()
    c = conn.cursor()
    c.execute("REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()