import streamlit as st
from openai import OpenAI
import time
from concurrent.futures import ThreadPoolExecutor
import streamlit.components.v1 as components 
import sqlite3
import datetime
import uuid
import hashlib
import random
import pandas as pd
import string

# ==========================================
# 0. 核心配置
# ==========================================
st.set_page_config(
    page_title="抖音爆款工场 Pro", 
    layout="wide",
    page_icon="💠",
    initial_sidebar_state="expanded"
)

# 🔑 管理员配置
ADMIN_PHONE = "13065080569"
ADMIN_INIT_PASSWORD = "ltren777188" 
GLOBAL_INVITE_CODE = "VIP888" 
REWARD_DAYS_NEW_USER = 3  
REWARD_DAYS_REFERRER = 3  

DB_FILE = 'saas_data_v2.db'

# --- 数据库初始化 ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (phone TEXT PRIMARY KEY, password_hash TEXT, register_time TIMESTAMP, last_login_ip TEXT, last_login_time TIMESTAMP, own_invite_code TEXT UNIQUE, invited_by TEXT, invite_count INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS access_codes (code TEXT PRIMARY KEY, duration_days INTEGER, activated_at TIMESTAMP, expire_at TIMESTAMP, status TEXT, create_time TIMESTAMP, bind_user TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS feedbacks (id INTEGER PRIMARY KEY AUTOINCREMENT, user_phone TEXT, content TEXT, reply TEXT, create_time TIMESTAMP, status TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)''')
    try: c.execute("ALTER TABLE users ADD COLUMN own_invite_code TEXT")
    except: pass
    try: c.execute("ALTER TABLE users ADD COLUMN invited_by TEXT")
    except: pass
    try: c.execute("ALTER TABLE users ADD COLUMN invite_count INTEGER DEFAULT 0")
    except: pass
    c.execute("SELECT phone FROM users WHERE phone=?", (ADMIN_PHONE,))
    if not c.fetchone():
        admin_pwd_hash = hashlib.sha256(ADMIN_INIT_PASSWORD.encode()).hexdigest()
        c.execute("INSERT INTO users (phone, password_hash, register_time, own_invite_code) VALUES (?, ?, ?, ?)", (ADMIN_PHONE, admin_pwd_hash, datetime.datetime.now(), "ADMIN888"))
    else:
        c.execute("UPDATE users SET own_invite_code='ADMIN888' WHERE phone=? AND own_invite_code IS NULL", (ADMIN_PHONE,))
    conn.commit(); conn.close()

init_db()

# --- 全局基础 CSS (内页通用，安全区) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@500&display=swap');

    .stApp { font-family: 'Inter', sans-serif; background-color: #f8fafc; }
    [data-testid="stHeader"] a, .stMarkdown h1 a, .stMarkdown h2 a, .stMarkdown h3 a, .stMarkdown h4 a { display: none !important; pointer-events: none; }
    
    /* 容器基础 */
    div.block-container { max-width: 90% !important; padding: 2rem !important; }
    
    /* 按钮优化 */
    div.stButton > button { border-radius: 10px; font-weight: 600; height: 45px; transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1); width: 100%; font-size: 15px; }
    div.stButton > button[kind="primary"] { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); border: none; color: white !important; box-shadow: 0 4px 10px rgba(59, 130, 246, 0.2); }
    div.stButton > button[kind="primary"]:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(59, 130, 246, 0.4); background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%); }
    div.stButton > button[kind="secondary"] { background-color: #f1f5f9; color: #475569; border: 1px solid transparent; }
    div.stButton > button[kind="secondary"]:hover { background-color: #e2e8f0; color: #1e293b; border-color: #cbd5e1; }

    /* --- 🔥 首页卡片式 Hero (v9.3) 🔥 --- */
    .hero-bg-animated {
        background: linear-gradient(-45deg, #eff6ff, #f0fdf4, #fff7ed, #eef2ff);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        border-radius: 24px;
        padding: 60px 40px; /* 增加内部空间 */
        text-align: center;
        box-shadow: 0 15px 40px -10px rgba(0,0,0,0.08);
        border: 1px solid rgba(255,255,255,0.5);
        margin-bottom: 40px;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .hero-title {
        font-size: 48px; font-weight: 900; letter-spacing: -1.5px; margin-bottom: 16px;
        background: -webkit-linear-gradient(120deg, #1e293b 0%, #2563eb 50%, #7c3aed 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 10px rgba(59, 130, 246, 0.1);
    }
    .hero-subtitle { font-size: 18px; color: #64748b; font-weight: 500; letter-spacing: 0.5px; }

    /* --- 首页功能卡片美化 --- */
    .home-card-inner { text-align: center; padding: 10px; }
    .home-card-icon {
        width: 64px; height: 64px; margin: 0 auto 15px auto;
        background: linear-gradient(135deg, #f0f9ff 0%, #dbeafe 100%);
        border-radius: 18px; display: flex; align-items: center; justify-content: center;
        font-size: 30px; color: #0284c7;
        box-shadow: 0 6px 15px -3px rgba(2, 132, 199, 0.15);
    }
    .home-card-title { font-size: 19px; font-weight: 800; color: #1e293b; margin-bottom: 8px; }
    .home-card-desc { font-size: 13px; color: #64748b; line-height: 1.5; min-height: 40px; }
    
    /* 首页容器悬浮特效 */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px !important; border: 1px solid #e2e8f0 !important;
        background-color: #ffffff; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.01);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); padding: 24px !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px -5px rgba(59, 130, 246, 0.12); border-color: #bfdbfe !important;
    }

    /* --- 侧边栏 --- */
    [data-testid="stSidebar"] { background-color: #f8fafc; border-right: 1px solid #e2e8f0; }
    [data-testid="stSidebar"] .block-container { padding-top: 2rem !important; }
    .sidebar-user-card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 12px; display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px; box-shadow: 0 2px 4px -1px rgba(0,0,0,0.02); }
    .user-left { display: flex; align-items: center; }
    .user-avatar { font-size: 20px; margin-right: 10px; background: #eff6ff; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
    .user-info { display: flex; flex-direction: column; }
    .user-name { font-weight: 700; font-size: 13px; color: #1e293b; line-height: 1.2; }
    .user-role { font-size: 10px; color: #d97706; font-weight: 600; background: #fffbeb; padding: 1px 5px; border-radius: 4px; border: 1px solid #fcd34d; margin-top: 2px; width: fit-content; }
    .buy-btn-sidebar { text-decoration: none; background: #10b981; color: white !important; font-size: 11px; font-weight: bold; padding: 4px 8px; border-radius: 6px; transition: all 0.2s; white-space: nowrap; }
    .buy-btn-sidebar:hover { background: #059669; transform: translateY(-1px); }
    .stRadio > div { gap: 0px; }
    .stRadio > div > label { background: transparent; padding: 8px 10px; border-radius: 6px; margin-bottom: 1px; color: #475569; font-weight: 500; transition: all 0.2s; cursor: pointer; border: 1px solid transparent; font-size: 14px !important; }
    .stRadio > div > label:hover { background: #f1f5f9; color: #1e293b; }
    .stRadio > div > label[data-checked="true"] { background: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; font-weight: 600; }
    .stRadio div[role="radiogroup"] > label > div:first-child { display: none; }
    .sidebar-project-card { background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px; margin-bottom: 8px; border-left: 3px solid #3b82f6; transition: all 0.2s; cursor: default; }
    .sidebar-project-card:hover { transform: translateX(2px); box-shadow: 0 2px 8px rgba(0,0,0,0.03); border-color: #cbd5e1; }
    .sp-title { font-weight: 700; font-size: 12px; color: #334155; margin-bottom: 2px; }
    .sp-desc { font-size: 10px; color: #94a3b8; line-height: 1.3; }

    /* 通用组件 */
    .poster-hero-container { background: #ffffff; border-radius: 20px; padding: 24px; box-shadow: 0 15px 40px rgba(0,0,0,0.05); border: 1px solid #edf2f7; display: flex; align-items: center; margin-bottom: 25px; position: relative; overflow: hidden; }
    .poster-hero-container::before { content: ''; position: absolute; top: -50%; right: -10%; width: 400px; height: 400px; background: radial-gradient(circle, rgba(167, 139, 250, 0.15) 0%, rgba(255,255,255,0) 70%); border-radius: 50%; z-index: 0; pointer-events: none; }
    .hero-icon-wrapper { width: 68px; height: 68px; background: linear-gradient(135deg, #c4b5fd, #818cf8); border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 34px; margin-right: 24px; box-shadow: 0 10px 20px -5px rgba(129, 140, 248, 0.5); z-index: 1; color: white; }
    .hero-title { font-size: 22px; font-weight: 800; color: #1e293b; margin: 0 0 8px 0; letter-spacing: -0.5px; z-index: 1; position: relative; }
    .hero-desc { font-size: 15px; color: #64748b; margin: 0; font-weight: 500; z-index: 1; position: relative; }
    .step-card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 18px; margin-bottom: 12px; display: flex; align-items: flex-start; transition: transform 0.2s; }
    .step-card:hover { border-color: #bfdbfe; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.05); transform: translateX(5px); }
    .step-icon { background: #eff6ff; color: #2563eb; width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 15px; flex-shrink: 0; }
    .step-content h4 { margin: 0 0 4px; font-size: 15px; color: #1e293b; font-weight: 700; }
    .step-content p { margin: 0; font-size: 13px; color: #64748b; }
    
    /* 个人中心 */
    .referral-box { background: linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%); border: 1px solid #fed7aa; border-radius: 16px; padding: 24px; text-align: center; margin-bottom: 20px; position: relative; overflow: hidden; }
    .referral-box::after { content: '🎁'; font-size: 80px; position: absolute; right: -10px; bottom: -20px; opacity: 0.1; transform: rotate(-20deg); }
    .referral-title { font-size: 18px; font-weight: 800; color: #9a3412; margin-bottom: 8px; }
    .referral-desc { font-size: 14px; color: #c2410c; margin-bottom: 20px; }
    .referral-code-display { font-family: monospace; font-size: 32px; font-weight: 800; color: #ea580c; background: rgba(255,255,255,0.6); padding: 10px 30px; border-radius: 12px; border: 2px dashed #f97316; display: inline-block; margin-bottom: 10px; cursor: pointer; }
    .stat-row { display: flex; justify-content: center; gap: 30px; margin-top: 15px; }
    .stat-item { text-align: center; }
    .stat-num { font-size: 20px; font-weight: 800; color: #c2410c; }
    .stat-lbl { font-size: 12px; color: #9a3412; }
    .footer-legal { margin-top: 40px; padding-top: 20px; border-top: 1px solid #e2e8f0; text-align: center; color: #94a3b8; font-size: 12px; }
    .footer-links a { color: #64748b; text-decoration: none; margin: 0 10px; transition: color 0.2s; }
    .info-box-aligned { height: 45px !important; background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; color: #1e40af; display: flex; align-items: center; padding: 0 16px; font-size: 14px; font-weight: 500; width: 100%; box-sizing: border-box; }
    .empty-state-box { height: 200px; background-image: repeating-linear-gradient(45deg, #f8fafc 25%, transparent 25%, transparent 75%, #f8fafc 75%, #f8fafc), repeating-linear-gradient(45deg, #f8fafc 25%, #ffffff 25%, #ffffff 75%, #f8fafc 75%, #f8fafc); background-size: 20px 20px; border: 2px dashed #e2e8f0; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #94a3b8; font-weight: 500; flex-direction: column; gap: 10px; }
</style>
""", unsafe_allow_html=True)

# --- 辅助函数 ---
def get_setting(key):
    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
    c.execute("SELECT value FROM settings WHERE key=?", (key,))
    row = c.fetchone(); conn.close()
    return row[0] if row else ""

def update_setting(key, value):
    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
    c.execute("REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit(); conn.close()

def hash_password(password): return hashlib.sha256(password.encode()).hexdigest()

def get_remote_ip():
    try:
        from streamlit.web.server.websocket_headers import _get_websocket_headers
        headers = _get_websocket_headers()
        return headers.get("X-Forwarded-For", headers.get("Remote-Addr", "unknown_ip"))
    except: return "unknown_ip"

def send_mock_sms(phone): return str(random.randint(1000, 9999))

def generate_invite_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def render_footer():
    st.markdown("""<div class="footer-legal"><div class="footer-links"><a href="#">用户协议</a> | <a href="#">隐私政策</a> | <a href="#">免责声明</a> | <a href="#">关于我们</a></div><div style="margin-top: 10px;">© 2026 爆款工场 Pro | 鄂ICP备2024XXXXXX号-1 | 违法和不良信息举报：TG777188</div><div style="font-size: 11px; color: #cbd5e1; margin-top: 5px;">本站仅提供技术工具，请勿用于任何非法用途，用户生成内容文责自负。</div></div>""", unsafe_allow_html=True)

def render_wechat_box(label, wx_id):
    html = f"""<!DOCTYPE html><html><head><style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;600&display=swap');body{{margin:0;padding:0;background:transparent;overflow:hidden;font-family:'Inter',sans-serif;}}.wx-pill{{display:flex;align-items:center;justify-content:space-between;background:white;border:1px solid #e2e8f0;border-radius:8px;padding:0 10px;height:36px;cursor:pointer;transition:all 0.2s;box-sizing:border-box;color:#334155;}}.wx-pill:hover{{border-color:#07c160;background:#07c160;}}.wx-pill:hover .label{{color:white;}}.wx-pill:hover .right-part{{color:white;}}.wx-pill:hover svg{{fill:white;}}.label{{font-size:12px;font-weight:600;transition:0.2s;}}.right-part{{display:flex;align-items:center;gap:4px;font-family:monospace;font-weight:500;font-size:12px;transition:0.2s;color:#07c160;}}.copied-msg{{display:none;font-size:11px;font-weight:bold;color:white;}}.wx-pill:hover .copied-msg{{color:white;}}</style></head><body><div class="wx-pill" onclick="copyText(this)"><span class="label" id="lbl">{label}</span><div class="right-part" id="val"><svg width="14" height="14" viewBox="0 0 24 24" fill="#07c160" xmlns="http://www.w3.org/2000/svg"><path d="M8.5 13.5L11 15L10 17.5C10 17.5 10.5 17.5 12.5 15C15 15 17 13 17 10.5C17 8 15 6 12.5 6C10 6 8 8 8 10.5C8 12 8.5 13.5 8.5 13.5ZM16.5 5.5C14 5.5 12 7 12 9C12 11 14 12.5 16.5 12.5C17 12.5 17.5 12.5 18 12L19.5 13L19 11C20 10.5 20.5 9.5 20.5 9C20.5 7 18.5 5.5 16.5 5.5Z" fill="currentColor"/></svg><span>{wx_id}</span></div><span class="copied-msg" id="msg">✅ 已复制</span></div><script>function copyText(e){{const id='{wx_id}';const lbl=document.getElementById('lbl');const val=document.getElementById('val');const msg=document.getElementById('msg');const textArea=document.createElement("textarea");textArea.value=id;document.body.appendChild(textArea);textArea.select();document.execCommand('copy');document.body.removeChild(textArea);lbl.style.display='none';val.style.display='none';msg.style.display='block';setTimeout(()=>{{lbl.style.display='block';val.style.display='flex';msg.style.display='none';}},1500);}}</script></body></html>"""
    components.html(html, height=40)

def render_copy_button_html(text, k):
    safe = text.replace("`", "\`").replace("'", "\\'")
    html = f"""<!DOCTYPE html><html><head><style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@600&display=swap');body{{margin:0;padding:0;background:transparent;overflow:hidden;}}.btn{{width:100%;height:42px;background:linear-gradient(135deg,#2563eb,#1d4ed8);color:#fff;border:none;border-radius:8px;font-family:'Inter';font-weight:600;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all 0.2s;}}.btn:hover{{transform:translateY(-1px);box-shadow:0 6px 16px rgba(37,99,235,0.4);}}.btn:active{{transform:translateY(0);}}.btn.ok{{background:linear-gradient(135deg,#10b981,#059669);}}</style></head><body><button class="btn" onclick="cp(this)">📋 一键复制</button><script>function cp(e){{navigator.clipboard.writeText(`{safe}`).then(()=>{{e.classList.add("ok");e.innerText="✅ 成功";setTimeout(()=>{{e.classList.remove("ok");e.innerText="📋 一键复制"}},2000)}})}}</script></body></html>"""
    components.html(html, height=50)

def render_hover_copy_box(text, label="点击复制"):
    safe = text.replace("`", "\`").replace("'", "\\'")
    html = f"""<!DOCTYPE html><html><head><style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;600&display=swap');body{{margin:0;padding:0;background:transparent;overflow:hidden;font-family:'Inter';}}.code-box{{display:flex;align-items:center;justify-content:space-between;background-color:#f8fafc;border:1px solid #cbd5e1;border-radius:6px;padding:0 10px;height:36px;cursor:pointer;transition:all 0.2s;color:#1e293b;font-weight:600;font-size:13px;box-sizing:border-box;}}.code-box:hover{{border-color:#3b82f6;background:#fff;box-shadow:0 0 0 2px rgba(59,130,246,0.1);}}.hint{{font-size:12px;color:#94a3b8;}}.code-box:hover .hint{{color:#3b82f6;}}.code-box.success{{background:#ecfdf5;border-color:#10b981;color:#065f46;}}.code-box.success .hint{{color:#059669;}}</style></head><body><div class="code-box" onclick="copyText(this)"><span id="content">{safe}</span><span class="hint" id="status">{label}</span></div><script>function copyText(e){{const t=`{safe}`,s=e.querySelector("#status");navigator.clipboard.writeText(t).then(()=>{{e.classList.add("success");const o=s.innerText;s.innerText="✅";setTimeout(()=>{{e.classList.remove("success");s.innerText=o}},1500)}}).catch(()=>{{s.innerText="❌"}})}}</script></body></html>"""
    components.html(html, height=40)

# --- 业务逻辑 ---
def add_vip_days(phone, days, source="system"):
    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
    c.execute("SELECT expire_at FROM access_codes WHERE bind_user=? AND status='active'", (phone,))
    rows = c.fetchall()
    now = datetime.datetime.now()
    if rows:
        max_expire_str = max([r[0] for r in rows])
        max_expire = datetime.datetime.strptime(max_expire_str.split('.')[0], '%Y-%m-%d %H:%M:%S')
        start_time = max_expire if max_expire > now else now
    else:
        start_time = now
    expire_at = start_time + datetime.timedelta(days=days)
    new_code = f"GIFT-{source}-{str(uuid.uuid4())[:6].upper()}"
    c.execute("INSERT INTO access_codes (code, duration_days, activated_at, expire_at, status, create_time, bind_user) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (new_code, days, now, expire_at, 'active', now, phone))
    conn.commit(); conn.close()

def register_user(phone, password, invite_code_used):
    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
    try:
        new_own_code = generate_invite_code()
        while True:
            c.execute("SELECT phone FROM users WHERE own_invite_code=?", (new_own_code,))
            if not c.fetchone(): break
            new_own_code = generate_invite_code()
        
        referrer_phone = None
        if invite_code_used != GLOBAL_INVITE_CODE:
            c.execute("SELECT phone FROM users WHERE own_invite_code=?", (invite_code_used,))
            row = c.fetchone()
            if row: referrer_phone = row[0]
            
        c.execute("INSERT INTO users (phone, password_hash, register_time, own_invite_code, invited_by) VALUES (?, ?, ?, ?, ?)", 
                  (phone, hash_password(password), datetime.datetime.now(), new_own_code, referrer_phone))
        conn.commit(); conn.close()
        
        add_vip_days(phone, REWARD_DAYS_NEW_USER, "NEW_USER")
        msg = f"注册成功！新人福利 +{REWARD_DAYS_NEW_USER} 天 🎉"
        if referrer_phone:
            add_vip_days(referrer_phone, REWARD_DAYS_REFERRER, "REFERRAL")
            conn = sqlite3.connect(DB_FILE); c = conn.cursor()
            c.execute("UPDATE users SET invite_count = invite_count + 1 WHERE phone=?", (referrer_phone,))
            conn.commit(); conn.close()
            msg += f" (已通过邀请码 {invite_code_used} 加入)"
        return True, msg
    except sqlite3.IntegrityError: return False, "该手机号已注册"
    except Exception as e: return False, str(e)
    finally: 
        try: conn.close()
        except: pass

def login_user(phone, password):
    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE phone=?", (phone,))
    row = c.fetchone(); conn.close()
    if row and row[0] == hash_password(password):
        conn = sqlite3.connect(DB_FILE); c = conn.cursor()
        c.execute("UPDATE users SET last_login_ip=?, last_login_time=? WHERE phone=?", (get_remote_ip(), datetime.datetime.now(), phone))
        conn.commit(); conn.close()
        return True, "登录成功"
    return False, "手机号或密码错误"

def check_ip_auto_login():
    ip = get_remote_ip(); 
    if ip == "unknown_ip": return None
    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
    seven_days_ago = datetime.datetime.now() - datetime.timedelta(days=7)
    c.execute("SELECT phone FROM users WHERE last_login_ip=? AND last_login_time > ?", (ip, seven_days_ago))
    row = c.fetchone(); conn.close()
    return row[0] if row else None

def activate_code(user_phone, code):
    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
    c.execute("SELECT * FROM access_codes WHERE code=?", (code,))
    row = c.fetchone()
    conn.close()
    if not row: return False, "❌ 卡密不存在"
    if row[4] == 'unused':
        add_vip_days(user_phone, row[1], "CDKEY")
        conn = sqlite3.connect(DB_FILE); c = conn.cursor()
        now = datetime.datetime.now()
        c.execute("UPDATE access_codes SET status='active', activated_at=?, bind_user=? WHERE code=?", (now, user_phone, code))
        conn.commit(); conn.close()
        return True, f"✅ 激活成功！增加 {row[1]} 天"
    else: return False, "⛔ 卡密已失效"

def get_user_vip_status(phone):
    if phone == ADMIN_PHONE: return True, "👑 超级管理员 (永久有效)"
    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
    now = datetime.datetime.now()
    c.execute("SELECT expire_at FROM access_codes WHERE bind_user=? AND status='active'", (phone,))
    rows = c.fetchall(); conn.close()
    if not rows: return False, "未开通会员"
    max_expire = max([datetime.datetime.strptime(str(r[0]).split('.')[0], '%Y-%m-%d %H:%M:%S') for r in rows])
    if max_expire > now:
        days_left = (max_expire - now).days
        return True, f"VIP (剩{days_left}天)" 
    return False, "会员已过期"

def get_user_invite_info(phone):
    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
    try:
        c.execute("SELECT own_invite_code, invite_count FROM users WHERE phone=?", (phone,))
        row = c.fetchone()
    except:
        row = None
    conn.close()
    if row: return row[0], row[1]
    return "系统升级中", 0

def submit_feedback(phone, content):
    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
    c.execute("INSERT INTO feedbacks (user_phone, content, create_time, status) VALUES (?, ?, ?, ?)", (phone, content, datetime.datetime.now(), 'pending'))
    conn.commit(); conn.close()

# ==========================================
# 1. 认证模块 (登录页终极美化)
# ==========================================
if 'user_phone' not in st.session_state:
    auto = check_ip_auto_login()
    if auto: st.session_state['user_phone'] = auto; st.toast(f"欢迎回来 {auto}", icon="👋"); time.sleep(0.5); st.rerun()

def auth_page():
    # 🔥 登录页专属 CSS (隔离: 仅在登录态生效，且通过特定类名控制) 🔥
    st.markdown("""
    <style>
        /* 动态流光背景 - 仅针对登录页 */
        .stApp {
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
        }
        @keyframes gradientBG { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
        
        [data-testid="stSidebarCollapsedControl"] { display: none; }
        
        .login-glass-card {
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(25px); -webkit-backdrop-filter: blur(25px);
            border: 1px solid rgba(255, 255, 255, 0.6);
            border-radius: 24px; padding: 40px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
            animation: fadein 0.8s;
        }
        @keyframes fadein { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        
        .lp-header { font-size: 36px; font-weight: 800; color: #1e293b; letter-spacing: -1px; margin-bottom: 8px; }
        .lp-sub { font-size: 16px; color: #475569; margin-bottom: 30px; font-weight: 500; }
        .lp-feature { display: flex; align-items: center; margin-bottom: 18px; font-size: 15px; color: #334155; font-weight: 600; }
        .lp-icon { width: 32px; height: 32px; background: rgba(255,255,255,0.8); border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 15px; font-size: 18px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 5vh;'></div>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 10, 1])
    with c2:
        with st.container():
            # 使用自定义HTML结构模拟左右分栏
            c_left, c_right = st.columns([1.1, 1], gap="large")
            
            with c_left:
                st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
                st.markdown("<div class='lp-header'>抖音爆款工场 Pro</div>", unsafe_allow_html=True)
                st.markdown("<div class='lp-sub'>全网首个 AI + KOC 商业变现操作系统</div>", unsafe_allow_html=True)
                st.markdown("""
                <div class='lp-feature'><div class='lp-icon'>🚀</div>5路并发 · 极速文案清洗改写</div>
                <div class='lp-feature'><div class='lp-icon'>💡</div>爆款选题 · 击穿流量焦虑</div>
                <div class='lp-feature'><div class='lp-icon'>🎨</div>海报生成 · 影视级光影质感</div>
                <div class='lp-feature'><div class='lp-icon'>💰</div>裂变系统 · 邀请好友免费续杯</div>
                """, unsafe_allow_html=True)
            
            with c_right:
                # 登录框容器
                st.markdown('<div class="login-glass-card">', unsafe_allow_html=True)
                t1, t2, t3 = st.tabs(["🔐 登录", "✨ 注册", "🆘 找回"])
                with t1:
                    with st.form("login_form"):
                        ph = st.text_input("手机号", placeholder="请输入手机号")
                        pw = st.text_input("密码", type="password", placeholder="请输入密码")
                        if st.form_submit_button("立即登录", type="primary", use_container_width=True):
                            s, m = login_user(ph, pw)
                            if s: st.session_state['user_phone'] = ph; st.rerun()
                            else: st.error(m)
                with t2:
                    st.info(f"🎁 新人福利：注册即送 {REWARD_DAYS_NEW_USER} 天 VIP")
                    ph = st.text_input("手机号", key="r_ph")
                    pw1 = st.text_input("设置密码", type="password", key="r_p1")
                    pw2 = st.text_input("确认密码", type="password", key="r_p2")
                    with st.expander("❓ 没有邀请码？"):
                        st.markdown(f"<div class='wx-invite-box'>添加客服 <b>W7774X</b> 回复“注册”获取</div>", unsafe_allow_html=True)
                        render_hover_copy_box("W7774X", "点击复制微信号")
                    invite_code = st.text_input("邀请码", key="r_invite", placeholder="VIP888")
                    if st.button("立即注册", type="primary", use_container_width=True):
                        if pw1 != pw2: st.error("两次密码不一致")
                        elif not invite_code: st.error("请输入邀请码")
                        else:
                            is_valid = False
                            if invite_code == GLOBAL_INVITE_CODE: is_valid = True
                            else:
                                conn = sqlite3.connect(DB_FILE); c = conn.cursor()
                                c.execute("SELECT phone FROM users WHERE own_invite_code=?", (invite_code,))
                                if c.fetchone(): is_valid = True
                                conn.close()
                            if is_valid:
                                s, m = register_user(ph, pw1, invite_code)
                                if s: st.success(m); st.balloons(); time.sleep(2); st.session_state['user_phone'] = ph; st.rerun()
                                else: st.error(m)
                            else: st.error("❌ 邀请码无效")
                with t3: st.info("请联系客服微信：W7774X 重置密码")
                st.markdown('</div>', unsafe_allow_html=True) # Close card

    render_footer()

if 'user_phone' not in st.session_state:
    auth_page(); st.stop()

CURRENT_USER = st.session_state['user_phone']
IS_ADMIN = (CURRENT_USER == ADMIN_PHONE)
IS_VIP, VIP_MSG = get_user_vip_status(CURRENT_USER)

# --- 导航 ---
if 'nav_menu' not in st.session_state: st.session_state['nav_menu'] = "🏠 首页"
def go_to(page):
    st.session_state['nav_menu'] = page
    st.session_state['sb_radio'] = page

# --- 侧边栏 ---
with st.sidebar:
    shop_url = get_setting("shop_url")
    buy_btn_html = f"""<a href="{shop_url}" target="_blank" class="buy-btn-sidebar">💎 充值</a>""" if shop_url else ""
    role_display = VIP_MSG if IS_VIP else "🌑 普通用户"
    st.markdown(f"""<div class="sidebar-user-card"><div class="user-left"><div class="user-avatar">👤</div><div class="user-info"><div class="user-name">{CURRENT_USER[:3]}****{CURRENT_USER[-4:]}</div><div class="user-role">{role_display}</div></div></div>{buy_btn_html}</div>""", unsafe_allow_html=True)
    if not IS_VIP:
        with st.expander("🔑 激活卡密", expanded=True):
            c = st.text_input("卡密", type="password", key="side_cd", label_visibility="collapsed", placeholder="输入卡密...")
            if st.button("立即激活", use_container_width=True):
                s, m = activate_code(CURRENT_USER, c)
                if s: st.success(m); time.sleep(1); st.rerun()
                else: st.error(m)
    st.markdown("---")
    ops = ["🏠 首页", "📝 文案改写", "💡 爆款选题库", "🎨 海报生成", "🏷️ 账号起名", "👤 个人中心"]
    if IS_ADMIN: ops.append("🕵️‍♂️ 管理后台")
    try: curr_idx = ops.index(st.session_state['nav_menu'])
    except: curr_idx = 0; st.session_state['nav_menu'] = ops[0]
    selected = st.radio("功能导航", ops, index=curr_idx, label_visibility="collapsed", key="sb_radio")
    if selected != st.session_state['nav_menu']: st.session_state['nav_menu'] = selected; st.rerun()
    st.markdown("---")
    st.markdown("<div style='font-size:12px;font-weight:700;color:#94a3b8;margin-bottom:8px;'>🔥 热门变现项目</div>", unsafe_allow_html=True)
    st.markdown("""<div class="sidebar-project-card"><div class="sp-title">📹 素人 KOC 孵化</div><div class="sp-desc">真人出镜口播 · 红果/番茄拉新 · 0基础陪跑</div></div><div class="sidebar-project-card" style="border-left-color: #8b5cf6;"><div class="sp-title">🎨 御灵 AI 动漫</div><div class="sp-desc">小说转动漫 · 端原生流量 · 版权分销</div></div><div class="sidebar-project-card" style="border-left-color: #10b981;"><div class="sp-title">🌍 文娱出海</div><div class="sp-desc">短剧出海 · 工具拉新 · 资源变现</div></div>""", unsafe_allow_html=True)
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    render_wechat_box("🎁 领取资料", "W7774X")
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    render_wechat_box("🛠️ 技术合作", "TG777188")
    st.markdown("---")
    if st.button("🚪 退出登录", use_container_width=True, type="secondary"): del st.session_state['user_phone']; st.rerun()

menu = st.session_state['nav_menu']

# --- 首页 (Hero Card Style) ---
def page_home():
    # 顶部留白
    st.markdown("<div style='height: 4rem;'></div>", unsafe_allow_html=True)
    
    # 🔥 首页专属卡片式 Hero 🔥
    st.markdown("""
    <div class="hero-bg-animated">
        <div class="hero-title">抖音爆款工场 Pro</div>
        <div class="hero-subtitle">让流量不再是玄学 · 专为素人 KOC 打造的 AI 变现神器</div>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        with st.container(border=True):
            st.markdown("""<div class="home-card-inner"><div class="home-card-icon">📝</div><div class="home-card-title">文案改写</div><div class="home-card-desc">5路并发 · 爆款重组<br>告别文案枯竭</div></div>""", unsafe_allow_html=True)
            st.button("立即使用 ➜", key="h_btn1", on_click=go_to, args=("📝 文案改写",), type="primary", use_container_width=True)
    with c2:
        with st.container(border=True):
            st.markdown("""<div class="home-card-inner"><div class="home-card-icon">💡</div><div class="home-card-title">爆款选题</div><div class="home-card-desc">流量焦虑 · 一键解决<br>精准击中痛点</div></div>""", unsafe_allow_html=True)
            st.button("立即使用 ➜", key="h_btn2", on_click=go_to, args=("💡 爆款选题库",), type="primary", use_container_width=True)
    with c3:
        with st.container(border=True):
            st.markdown("""<div class="home-card-inner"><div class="home-card-icon">🎨</div><div class="home-card-title">海报生成</div><div class="home-card-desc">小提大作 · 影视质感<br>好莱坞级光影</div></div>""", unsafe_allow_html=True)
            st.button("立即使用 ➜", key="h_btn3", on_click=go_to, args=("🎨 海报生成",), type="primary", use_container_width=True)
    with c4:
        with st.container(border=True):
            st.markdown("""<div class="home-card-inner"><div class="home-card-icon">🏷️</div><div class="home-card-title">账号起名</div><div class="home-card-desc">AI 算命 · 爆款玄学<br>赛道垂直定制</div></div>""", unsafe_allow_html=True)
            st.button("立即使用 ➜", key="h_btn4", on_click=go_to, args=("🏷️ 账号起名",), type="primary", use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("#### 📢 系统公告")
        st.info("🎉 欢迎使用 Pro 版！如需开通会员，请联系侧边栏客服获取卡密。", icon="👋")

# --- 文案 ---
def page_rewrite():
    st.markdown("## 📝 爆款文案改写"); st.markdown("---")
    if 'results' not in st.session_state: st.session_state['results'] = {}
    client = OpenAI(api_key=st.secrets.get("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
    def rewrite_logic(content):
        if not content or len(content.strip()) < 5: return "⚠️ 内容过短"
        prompt = f"你是一个抖音千万粉的口播博主。原始素材：{content}。任务：清洗数据，改写为原创爆款文案。公式：黄金3秒开头+中间情绪饱满+结尾强引导。输出：直接输出文案，不要任何markdown格式。"
        try: return client.chat.completions.create(model="deepseek-chat", messages=[{"role":"user","content":prompt}], temperature=1.3).choices[0].message.content
        except: return "请配置 API Key"
    def clear_text(k): st.session_state[k] = ""
    c1, c2 = st.columns([1, 2], gap="medium")
    with c1:
        if st.button("🚀 5路并发执行", type="primary", use_container_width=True):
            tasks, indices = [], []
            for i in range(1, 6):
                val = st.session_state.get(f"input_{i}", "")
                if val.strip(): tasks.append(val); indices.append(i)
            if not tasks: st.toast("请至少输入一条文案", icon="⚠️")
            else:
                with st.status("☁️ 正在疯狂计算中...", expanded=True):
                    with ThreadPoolExecutor(5) as ex: res = list(ex.map(rewrite_logic, tasks))
                    for idx, r in zip(indices, res): st.session_state['results'][idx] = r
                    st.rerun()
    with c2: st.markdown("""<div class="info-box-aligned">💡 提示：将文案粘贴到下方窗口，点击左侧蓝色按钮可批量处理。</div>""", unsafe_allow_html=True)
    st.write("")
    for i in range(1, 6):
        with st.container(border=True):
            st.markdown(f"**📝 工作台 #{i}**")
            col_in, col_out = st.columns([1, 1], gap="large")
            with col_in:
                input_key = f"input_{i}"
                st.text_area("原始文案", height=200, key=input_key, placeholder="粘贴文案到这里...", label_visibility="collapsed")
                b1, b2 = st.columns([1, 2])
                b1.button("🗑️ 清空", key=f"clr_{i}", on_click=clear_text, args=(input_key,), use_container_width=True)
                if b2.button(f"⚡ 仅生成 #{i}", key=f"gen_{i}", type="primary", use_container_width=True):
                    val = st.session_state.get(input_key, "")
                    if val:
                        with st.spinner("生成中..."): st.session_state['results'][i] = rewrite_logic(val); st.rerun()
            with col_out:
                res = st.session_state['results'].get(i, "")
                if res:
                    st.text_area("结果", value=res, height=200, label_visibility="collapsed", key=f"res_area_{i}")
                    render_copy_button_html(res, f"cp_{i}")
                    st.markdown("""<div style="margin-top:5px;padding:8px;background:#fff1f2;border-radius:6px;border:1px solid #fecdd3;font-size:12px;color:#be123c;display:flex;justify-content:space-between;align-items:center;"><span>🔥 <b>不会拍？</b>领《素人KOC出镜SOP》</span><span style="color:#e11d48;font-weight:bold;">👉 微信 W7774X</span></div>""", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='empty-state-box'><div style='font-size: 24px;'>⏳</div><div>等待指令...</div><div style='font-size: 12px; color: #94a3b8;'>Input content to generate</div></div>", unsafe_allow_html=True)

# --- 海报 ---
def page_poster():
    st.markdown("## 🎨 海报生成 (专业版)")
    st.markdown("""<div class="poster-hero-container"><div class="hero-icon-wrapper">🚀</div><div class="hero-text-content"><h2 class="hero-title">算力全面升级！好莱坞级光影引擎</h2><p class="hero-desc">为了提供极致的渲染效果，海报功能已迁移至性能更强的独立工作站。</p></div></div>""", unsafe_allow_html=True)
    components.html("""<!DOCTYPE html><html><head><style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;600;800&display=swap');body{margin:0;padding:20px;font-family:'Inter',sans-serif;overflow:hidden;background:transparent;}.container{display:flex;gap:20px;width:100%;}.card{flex:1;border-radius:16px;height:120px;display:flex;flex-direction:column;justify-content:center;align-items:center;cursor:pointer;transition:all 0.3s;box-sizing:border-box;}.invite{background:#fff;border:2px dashed #cbd5e1;position:relative;}.invite:hover{border-color:#6366f1;background:#f5f3ff;transform:translateY(-5px);box-shadow:0 10px 20px rgba(0,0,0,0.03);}.invite-label{font-size:13px;color:#64748b;margin-bottom:5px;}.invite-code{font-size:28px;font-weight:800;color:#4f46e5;letter-spacing:1px;}.invite-hint{font-size:12px;color:#94a3b8;margin-top:5px;opacity:0;transition:0.2s;}.invite:hover .invite-hint{opacity:1;color:#6366f1;}.jump{flex:1.5;background:linear-gradient(135deg,#4f46e5,#7c3aed);text-decoration:none;box-shadow:0 4px 15px rgba(124,58,237,0.1);border:1px solid rgba(255,255,255,0.15);}.jump:hover{transform:translateY(-5px);box-shadow:0 8px 20px rgba(124,58,237,0.25);filter:brightness(1.05);}.jump-title{color:#fff;font-size:24px;font-weight:800;margin-bottom:4px;text-shadow:0 2px 4px rgba(0,0,0,0.1);}.jump-sub{color:rgba(255,255,255,0.9);font-size:14px;}</style></head><body><div class="container"><div class="card invite" onclick="copyInvite(this)"><div class="invite-label">👇 第一步：点击复制邀请码</div><div class="invite-code">5yzMbpxn</div><div class="invite-hint" id="status">点击立即复制</div></div><a href="https://aixtdz.com/" target="_blank" class="card jump"><div class="jump-title">🚀 前往小提大作</div><div class="jump-sub">第二步：点击跳转，开启创作</div></a></div><script>function copyInvite(e){const text='5yzMbpxn';const textArea=document.createElement("textarea");textArea.value=text;document.body.appendChild(textArea);textArea.select();try{document.execCommand('copy');const hint=e.querySelector('#status');hint.innerText='✅ 复制成功！';hint.style.opacity='1';hint.style.color='#10b981';setTimeout(()=>{hint.innerText='点击立即复制';hint.style.opacity='0';hint.style.color='#94a3b8';},2000);}catch(err){}document.body.removeChild(textArea);}</script></body></html>""", height=180) 
    st.write("")
    st.markdown("#### 📖 新手保姆级教程")
    steps = [("注册登录", "点击上方大按钮前往，注册时记得填写邀请码。"), ("创建画布", "登录后，在首页点击 <b>“创建自由画布”</b>。"), ("上传原图", "在画布中，点击组件栏的 <b>“+”</b> 号，上传剧照。"), ("一键改图", "点击 <b>右侧边框</b>，复制下方指令输入，等待奇迹！")]
    for idx, (title, desc) in enumerate(steps, 1):
        st.markdown(f"""<div class="step-card"><div class="step-icon">{idx}</div><div class="step-content"><h4>{title}</h4><p>{desc}</p></div></div>""", unsafe_allow_html=True)
    cmd_text = "将原图剧名：[原剧名] 改为：[你的新剧名]"
    components.html(f"""<!DOCTYPE html><html><head><style>@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@500&display=swap');body{{margin:0;padding:20px;font-family:'Fira Code',monospace;overflow:hidden;background:transparent;}}.terminal{{background:#0f172a;border-radius:12px;border:1px solid #334155;overflow:hidden;cursor:pointer;transition:0.3s;box-shadow:0 5px 15px rgba(0,0,0,0.1);}}.terminal:hover{{border-color:#6366f1;transform:translateY(-2px);box-shadow:0 8px 20px rgba(0,0,0,0.15);}}.header{{background:#1e293b;padding:10px 16px;display:flex;align-items:center;border-bottom:1px solid #334155;}}.dots{{display:flex;gap:6px;margin-right:12px;}}.dot{{width:10px;height:10px;border-radius:50%;}}.red{{background:#ef4444;}}.yellow{{background:#f59e0b;}}.green{{background:#22c55e;}}.title{{color:#64748b;font-size:12px;}}.body{{padding:20px;color:#e2e8f0;font-size:14px;display:flex;align-items:center;}}.prompt{{color:#22c55e;margin-right:10px;}}.hl{{color:#a78bfa;font-weight:bold;}}.success-overlay{{position:absolute;top:0;left:0;width:100%;height:100%;background:rgba(16,185,129,0.95);display:flex;align-items:center;justify-content:center;color:white;font-weight:bold;font-size:16px;opacity:0;pointer-events:none;transition:0.2s;}}.terminal:active .success-overlay{{opacity:1;}}</style></head><body><div class="terminal" onclick="copyCmd()"><div class="header"><div class="dots"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div><div class="title">root@ai-generator ~ % (点击复制)</div></div><div class="body"><span class="prompt">➜</span><span>将原图剧名：<span class="hl">[原剧名]</span> 改为：<span class="hl">[你的新剧名]</span></span></div><div class="success-overlay" id="overlay">✅ 指令已复制到剪贴板</div></div><script>function copyCmd(){{const text=`{cmd_text}`;const textArea=document.createElement("textarea");textArea.value=text;document.body.appendChild(textArea);textArea.select();document.execCommand('copy');document.body.removeChild(textArea);const overlay=document.getElementById('overlay');overlay.style.opacity='1';setTimeout(()=>{{overlay.style.opacity='0';}},1500);}}</script></body></html>""", height=160) 

# --- 其他功能 ---
def page_brainstorm():
    st.markdown("## 💡 爆款选题灵感库"); st.markdown("---")
    client = OpenAI(api_key=st.secrets.get("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
    c1, c2 = st.columns([3, 1])
    with c1: topic = st.text_input("🔍 输入你的赛道/关键词", placeholder="例如：职场、美妆、减肥、副业...")
    with c2: st.write(""); st.write(""); generate_btn = st.button("🧠 帮我想选题", type="primary", use_container_width=True)
    if generate_btn and topic:
        prompt = f"我是做【{topic}】领域的。现在文案枯竭，请帮我生成 10 个绝对会火的爆款选题。要求：1. 必须反直觉，打破认知。2. 必须直击痛点，引发焦虑或强烈好奇。3. 格式：1. 标题：xxxx | 钩子：xxxx"
        try:
            with st.spinner("AI 正在疯狂头脑风暴..."):
                res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}], temperature=1.5)
                st.session_state['brainstorm_result'] = res.choices[0].message.content
        except Exception as e: st.error(str(e))
    if 'brainstorm_result' in st.session_state:
        res = st.session_state['brainstorm_result']
        st.text_area("灵感列表", value=res, height=400, label_visibility="collapsed")
        render_copy_button_html(res, "brain_copy_btn")

def page_naming():
    st.markdown("## 🏷️ 账号/IP 起名大师"); st.markdown("---")
    client = OpenAI(api_key=st.secrets.get("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
    c1, c2 = st.columns(2)
    with c1: niche = st.selectbox("🎯 赛道", ["短剧", "小说", "口播", "情感", "带货"])
    with c2: style = st.selectbox("🎨 风格", ["高冷", "搞笑", "文艺", "粗暴", "反差"])
    keywords = st.text_input("🔑 关键词 (选填)")
    if st.button("🎲 生成名字", type="primary", use_container_width=True):
        prompt = f"为【{niche}】赛道生成10个{style}风格账号名，含关键词：{keywords}。格式：1. 名字+解释。"
        try:
            with st.spinner("生成中..."):
                res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}], temperature=1.5)
                st.session_state['naming_result'] = res.choices[0].message.content
        except Exception as e: st.error(str(e))
    if 'naming_result' in st.session_state:
        res = st.session_state['naming_result']
        st.text_area("结果", value=res, height=400, label_visibility="collapsed")
        render_copy_button_html(res, "name_copy_btn")

def page_account():
    st.markdown("## 👤 个人中心"); st.markdown("---")
    t1, t2, t3 = st.tabs(["🎁 邀请有礼", "💳 账户", "💬 反馈"])
    with t1:
        my_code, invite_count = get_user_invite_info(CURRENT_USER)
        st.markdown(f"""
        <div class="referral-box">
            <div class="referral-title">🎉 邀请好友，无限续杯 VIP！</div>
            <div class="referral-desc">每成功邀请 1 位好友注册，双方各得 <b>{REWARD_DAYS_REFERRER} 天</b> 尊贵 VIP 时长。</div>
            <div class="referral-code-display" onclick="copyCode(this)">{my_code}<div style="font-size:10px;margin-top:5px;color:#9a3412;">(点击复制)</div></div>
            <div class="stat-row">
                <div class="stat-item"><div class="stat-num">{invite_count}</div><div class="stat-lbl">已邀请人数</div></div>
                <div class="stat-item"><div class="stat-num">{invite_count * REWARD_DAYS_REFERRER}</div><div class="stat-lbl">获得天数</div></div>
            </div>
        </div>
        <script>function copyCode(e){{navigator.clipboard.writeText('{my_code}').then(()=>{{st.toast('复制成功！快去分享吧',{{icon:'🎁'}})}});}}</script>
        """, unsafe_allow_html=True)
        render_copy_button_html(my_code, "referral_copy_btn")
    with t2:
        st.metric("账号", CURRENT_USER)
        st.metric("状态", "VIP" if IS_VIP else "普通用户", delta=VIP_MSG)
        shop_url = get_setting("shop_url")
        if shop_url: st.markdown(f"""<a href="{shop_url}" target="_blank" style="display:block;text-align:center;background:#10b981;color:white;padding:12px;border-radius:8px;text-decoration:none;font-weight:bold;margin:10px 0">💳 在线购买/续费卡密</a>""", unsafe_allow_html=True)
        st.write("#### 激活卡密")
        c = st.text_input("卡密", placeholder="VIP-xxxxx")
        if st.button("立即激活", type="primary"):
            s, m = activate_code(CURRENT_USER, c)
            if s: st.success(m); time.sleep(1); st.rerun()
            else: st.error(m)
    with t3:
        txt = st.text_area("请输入您的建议...")
        if st.button("提交"): submit_feedback(CURRENT_USER, txt); st.success("已提交！")
        conn = sqlite3.connect(DB_FILE); c = conn.cursor()
        c.execute("SELECT content, reply, create_time FROM feedbacks WHERE user_phone=? ORDER BY create_time DESC", (CURRENT_USER,))
        rows = c.fetchall(); conn.close()
        for c, r, t in rows:
            with st.container(border=True):
                st.caption(f"📅 {t}"); st.write(f"**我**: {c}")
                if r: st.write(f"**回复**: :green[{r}]")

def page_admin():
    st.markdown("## 🕵️‍♂️ 管理后台")
    if 'admin_unlocked' not in st.session_state: st.session_state['admin_unlocked'] = False
    if not st.session_state['admin_unlocked']:
        pwd = st.text_input("请输入管理员密码", type="password")
        if pwd == ADMIN_INIT_PASSWORD:
            st.session_state['admin_unlocked'] = True
            st.rerun()
    else:
        st.success("✅ 已登录管理员权限")
        t1, t2, t3 = st.tabs(["待处理反馈", "历史记录", "系统设置"])
        with t1:
            conn = sqlite3.connect(DB_FILE)
            pending = pd.read_sql("SELECT * FROM feedbacks WHERE status='pending'", conn)
            conn.close()
            if pending.empty: st.info("暂无待处理反馈")
            else:
                for i, r in pending.iterrows():
                    with st.container(border=True):
                        st.write(f"**用户**: {r['user_phone']} | **时间**: {r['create_time']}")
                        st.info(f"内容: {r['content']}")
                        reply = st.text_input("回复内容", key=f"rep_{r['id']}")
                        if st.button("发送回复", key=f"send_{r['id']}"):
                            conn = sqlite3.connect(DB_FILE); c = conn.cursor()
                            c.execute("UPDATE feedbacks SET reply=?, status='replied' WHERE id=?", (reply, r['id']))
                            conn.commit(); conn.close(); st.success("已回复"); time.sleep(1); st.rerun()
        with t2:
            conn = sqlite3.connect(DB_FILE)
            history = pd.read_sql("SELECT * FROM feedbacks WHERE status='replied' ORDER BY create_time DESC", conn)
            conn.close()
            for i, r in history.iterrows():
                with st.expander(f"已回复: {r['user_phone']} - {str(r['create_time'])[:10]}"):
                    st.write(f"**用户内容**: {r['content']}")
                    st.write(f"**当前回复**: :green[{r['reply']}]")
                    c1, c2 = st.columns([3, 1])
                    new_reply = c1.text_input("修改回复", value=r['reply'], key=f"edit_rep_{r['id']}")
                    if c1.button("更新回复", key=f"upd_{r['id']}"):
                        conn = sqlite3.connect(DB_FILE); c = conn.cursor()
                        c.execute("UPDATE feedbacks SET reply=? WHERE id=?", (new_reply, r['id']))
                        conn.commit(); conn.close(); st.success("更新成功"); st.rerun()
                    if c2.button("🗑️ 删除记录", key=f"del_{r['id']}"):
                        conn = sqlite3.connect(DB_FILE); c = conn.cursor()
                        c.execute("DELETE FROM feedbacks WHERE id=?", (r['id'],))
                        conn.commit(); conn.close(); st.warning("已删除"); st.rerun()
        with t3:
            st.write("#### 卡密生成")
            q = st.number_input("数量", 1, 100, 10); d = st.number_input("天数", 1, 365, 30)
            if st.button("一键生成"):
                conn = sqlite3.connect(DB_FILE); c = conn.cursor()
                for _ in range(q):
                    code = "VIP-" + str(uuid.uuid4())[:8].upper()
                    c.execute("INSERT INTO access_codes (code, duration_days, status, create_time) VALUES (?, ?, ?, ?)", (code, d, 'unused', datetime.datetime.now()))
                conn.commit(); conn.close(); st.success(f"已生成 {q} 个")
            conn = sqlite3.connect(DB_FILE)
            df = pd.read_sql("SELECT * FROM access_codes ORDER BY create_time DESC LIMIT 50", conn)
            st.dataframe(df, height=300)
            st.download_button("下载所有卡密", df.to_csv(index=False).encode('utf-8'), "codes.csv", "text/csv")
            conn.close()
            st.markdown("---")
            url = st.text_input("发卡网链接", value=get_setting("shop_url"))
            if st.button("保存链接"): update_setting("shop_url", url); st.success("已保存")

# --- 路由逻辑 ---
if not IS_VIP and menu not in ["🏠 首页", "👤 个人中心", "🕵️‍♂️ 管理后台"]:
    st.warning("⚠️ 会员功能，请先激活"); st.stop()

if menu == "🏠 首页": page_home()
elif menu == "📝 文案改写": page_rewrite()
elif menu == "🎨 海报生成": page_poster()
elif menu == "💡 爆款选题库": page_brainstorm()
elif menu == "🏷️ 账号起名": page_naming()
elif menu == "👤 个人中心": page_account()
elif menu == "🕵️‍♂️ 管理后台": page_admin()
else: st.info("功能开发中...")

render_footer()
