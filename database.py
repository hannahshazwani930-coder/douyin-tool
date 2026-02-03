# database.py
import sqlite3
import datetime
import uuid
import hashlib
import random  # 新增
import string  # 新增
from config import DB_FILE, ADMIN_ACCOUNT, ADMIN_INIT_PASSWORD, REWARD_DAYS_NEW_USER, REWARD_DAYS_REFERRER, GLOBAL_INVITE_CODE

# --- 🔒 [LOCKED] 基础安全工具 (已从 utils 隔离) ---
def hash_password(password):
    """为密码提供 SHA-256 加密，不再依赖外部 utils"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_invite_code():
    """生成唯一邀请码，不再依赖外部 utils"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# --- 基础连接 ---

def get_conn():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def init_db():
    conn = get_conn()
    c = conn.cursor()
    # 用户表
    c.execute('''CREATE TABLE IF NOT EXISTS users (phone TEXT PRIMARY KEY, password_hash TEXT, register_time TIMESTAMP, last_login_ip TEXT, last_login_time TIMESTAMP, own_invite_code TEXT UNIQUE, invited_by TEXT, invite_count INTEGER DEFAULT 0)''')
    # 卡密表 (status: active=已激活/赠送, unused=待激活/卡密)
    c.execute('''CREATE TABLE IF NOT EXISTS access_codes (code TEXT PRIMARY KEY, duration_days INTEGER, activated_at TIMESTAMP, expire_at TIMESTAMP, status TEXT, create_time TIMESTAMP, bind_user TEXT)''')
    # 反馈表
    c.execute('''CREATE TABLE IF NOT EXISTS feedbacks (id INTEGER PRIMARY KEY AUTOINCREMENT, user_phone TEXT, content TEXT, reply TEXT, create_time TIMESTAMP, status TEXT)''')
    # 公告表
    c.execute('''CREATE TABLE IF NOT EXISTS announcements (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT, is_active INTEGER, create_time TIMESTAMP)''')
    # 设置表
    c.execute('''CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)''')
    
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
        new_own_code = generate_invite_code()
        while True:
            c.execute("SELECT phone FROM users WHERE own_invite_code=?", (new_own_code,))
            if not c.fetchone(): break
            new_own_code = generate_invite_code()
        
        referrer = None
        if invite_code_used and invite_code_used != "888888":
            if invite_code_used == GLOBAL_INVITE_CODE: pass
            else:
                c.execute("SELECT phone FROM users WHERE own_invite_code=?", (invite_code_used,))
                row = c.fetchone()
                if row: referrer = row[0]
            
        c.execute("INSERT INTO users (phone, password_hash, register_time, own_invite_code, invited_by) VALUES (?, ?, ?, ?, ?)", 
                  (account, hash_password(password), datetime.datetime.now(), new_own_code, referrer))
        conn.commit()
        
        # 注册赠送 (直接激活)
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

# --- VIP 系统 (核心修改) ---

def get_expire_date(account):
    """计算用户当前的过期时间"""
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT expire_at FROM access_codes WHERE bind_user=? AND status='active'", (account,))
    rows = c.fetchall()
    conn.close()
    
    now = datetime.datetime.now()
    if not rows: return now
    
    max_expire_str = max([str(r[0]) for r in rows])
    max_expire = datetime.datetime.strptime(max_expire_str.split('.')[0], '%Y-%m-%d %H:%M:%S')
    return max_expire if max_expire > now else now

def add_vip_days(account, days, source="system"):
    """直接给用户加时间 (用于系统奖励)"""
    start_time = get_expire_date(account)
    expire_at = start_time + datetime.timedelta(days=days)
    new_code = f"AUTO-{source}-{str(uuid.uuid4())[:6].upper()}"
    
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO access_codes (code, duration_days, activated_at, expire_at, status, create_time, bind_user) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (new_code, days, datetime.datetime.now(), expire_at, 'active', datetime.datetime.now(), account))
    conn.commit()
    conn.close()

def generate_bulk_cards(amount, days):
    """批量生成未激活的卡密 (用于管理员)"""
    conn = get_conn()
    c = conn.cursor()
    codes = []
    for _ in range(amount):
        # 生成格式: VIP-30D-XXXXXX
        code_str = f"VIP-{days}D-{''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}"
        c.execute("INSERT INTO access_codes (code, duration_days, status, create_time) VALUES (?, ?, 'unused', ?)",
                  (code_str, days, datetime.datetime.now()))
        codes.append(code_str)
    conn.commit()
    conn.close()
    return codes

def redeem_card(account, code):
    """用户激活卡密"""
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT duration_days, status FROM access_codes WHERE code=?", (code,))
    row = c.fetchone()
    
    if not row:
        conn.close()
        return False, "❌ 卡密无效"
    
    days, status = row
    if status != 'unused':
        conn.close()
        return False, "⚠️ 该卡密已被使用或失效"
    
    # 计算新日期
    start_time = get_expire_date(account) # 获取当前最大过期时间
    expire_at = start_time + datetime.timedelta(days=days)
    now = datetime.datetime.now()
    
    # 更新卡密状态
    c.execute("UPDATE access_codes SET status='active', activated_at=?, expire_at=?, bind_user=? WHERE code=?",
              (now, expire_at, account, code))
    conn.commit()
    conn.close()
    return True, f"✅ 激活成功！增加 {days} 天会员"

def get_user_vip_status(phone):
    if phone == ADMIN_ACCOUNT: return True, "👑 超级管理员"
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT expire_at FROM access_codes WHERE bind_user=? AND status='active'", (phone,))
    rows = c.fetchall()
    conn.close()
    
    now = datetime.datetime.now()
    if not rows: return False, "未开通会员"
    
    max_expire_str = max([str(r[0]) for r in rows])
    max_expire = datetime.datetime.strptime(max_expire_str.split('.')[0], '%Y-%m-%d %H:%M:%S')
    
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

def create_announcement(content):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO announcements (content, is_active, create_time) VALUES (?, 1, ?)", (content, datetime.datetime.now()))
    conn.commit()
    conn.close()

def get_active_announcements():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT content, create_time FROM announcements WHERE is_active=1 ORDER BY create_time DESC LIMIT 5")
    rows = c.fetchall()
    conn.close()
    return rows

def delete_announcement(content):
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE announcements SET is_active=0 WHERE content=?", (content,))
    conn.commit()
    conn.close()

def add_feedback(phone, content):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO feedbacks (user_phone, content, create_time, status) VALUES (?, ?, ?, 'pending')", 
              (phone, content, datetime.datetime.now()))
    conn.commit()
    conn.close()

def get_user_feedbacks(phone):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT content, reply, create_time, status FROM feedbacks WHERE user_phone=? ORDER BY create_time DESC", (phone,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_all_feedbacks_admin():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, user_phone, content, reply, create_time, status FROM feedbacks ORDER BY create_time DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def reply_feedback(id, reply_text):
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE feedbacks SET reply=?, status='replied' WHERE id=?", (reply_text, id))
    conn.commit()
    conn.close()

def get_stats():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    user_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM access_codes WHERE status='active'")
    vip_count = c.fetchone()[0]
    conn.close()
    return user_count, vip_count

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

