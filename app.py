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
import re # 引入正则用于提取天数

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

# 数据库文件
DB_FILE = 'saas_data_v2.db'

# --- 数据库初始化 ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (phone TEXT PRIMARY KEY, password_hash TEXT, register_time TIMESTAMP, last_login_ip TEXT, last_login_time TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS access_codes (code TEXT PRIMARY KEY, duration_days INTEGER, activated_at TIMESTAMP, expire_at TIMESTAMP, status TEXT, create_time TIMESTAMP, bind_user TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS feedbacks (id INTEGER PRIMARY KEY AUTOINCREMENT, user_phone TEXT, content TEXT, reply TEXT, create_time TIMESTAMP, status TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)''')
    admin_pwd_hash = hashlib.sha256(ADMIN_INIT_PASSWORD.encode()).hexdigest()
    c.execute("REPLACE INTO users (phone, password_hash, register_time) VALUES (?, ?, ?)", (ADMIN_PHONE, admin_pwd_hash, datetime.datetime.now()))
    conn.commit(); conn.close()

init_db()

# --- CSS 样式 (v6.6 紧凑版) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@500&display=swap');

    .stApp { font-family: 'Inter', sans-serif; background-color: #f8fafc; }
    
    /* 隐藏锚点 */
    [data-testid="stHeader"] a, .stMarkdown h1 a, .stMarkdown h2 a, .stMarkdown h3 a, .stMarkdown h4 a { display: none !important; pointer-events: none; }
    
    /* 容器 */
    div.block-container { max-width: 90% !important; background-color: #ffffff; padding: 3rem !important; border-radius: 24px; box-shadow: 0 20px 60px -20px rgba(0,0,0,0.1); margin-bottom: 50px; }
    
    /* 按钮全局优化 */
    div.stButton > button { border-radius: 10px; font-weight: 600; height: 48px; transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1); width: 100%; font-size: 15px; }
    
    /* 主按钮 */
    div.stButton > button[kind="primary"] { 
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); 
        border: none; color: white !important; 
        box-shadow: 0 4px 10px rgba(59, 130, 246, 0.2);
    }
    div.stButton > button[kind="primary"]:hover { 
        transform: translateY(-2px); box-shadow: 0 10px 20px rgba(59, 130, 246, 0.4);
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
    }
    
    /* 次级按钮 */
    div.stButton > button[kind="secondary"] { background-color: #f1f5f9; color: #475569; border: 1px solid transparent; }
    div.stButton > button[kind="secondary"]:hover { background-color: #e2e8f0; color: #1e293b; border-color: #cbd5e1; }

    /* --- 🔥 侧边栏极致紧凑美化 (v6.6) 🔥 --- */
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
    /* 压缩侧边栏顶部留白 */
    [data-testid="stSidebar"] .block-container {
        padding-top: 2rem !important;
        padding-bottom: 1rem !important;
    }
    
    /* 用户身份卡片 (紧凑型 + 充值入口) */
    .sidebar-user-card {
        background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 12px; 
        display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px;
        box-shadow: 0 2px 4px -1px rgba(0,0,0,0.02);
    }
    .user-left { display: flex; align-items: center; }
    .user-avatar { font-size: 20px; margin-right: 10px; background: #eff6ff; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
    .user-info { display: flex; flex-direction: column; }
    .user-name { font-weight: 700; font-size: 13px; color: #1e293b; line-height: 1.2; }
    .user-role { font-size: 10px; color: #d97706; font-weight: 600; background: #fffbeb; padding: 1px 5px; border-radius: 4px; border: 1px solid #fcd34d; margin-top: 2px; width: fit-content; }
    
    /* 侧边栏购买按钮 */
    .buy-btn-sidebar {
        text-decoration: none; background: #10b981; color: white !important; 
        font-size: 11px; font-weight: bold; padding: 4px 8px; border-radius: 6px; 
        transition: all 0.2s; white-space: nowrap;
    }
    .buy-btn-sidebar:hover { background: #059669; transform: translateY(-1px); box-shadow: 0 2px 5px rgba(16, 185, 129, 0.2); }

    /* 侧边栏导航条改造 (更紧凑) */
    .stRadio > div { gap: 0px; }
    .stRadio > div > label {
        background: transparent; padding: 8px 10px; border-radius: 6px; margin-bottom: 1px;
        color: #475569; font-weight: 500; transition: all 0.2s; cursor: pointer; border: 1px solid transparent;
        font-size: 14px !important;
    }
    .stRadio > div > label:hover { background: #f1f5f9; color: #1e293b; }
    .stRadio > div > label[data-checked="true"] {
        background: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; font-weight: 600;
    }
    .stRadio div[role="radiogroup"] > label > div:first-child { display: none; }

    /* 侧边栏项目卡片 (紧凑) */
    .sidebar-project-card {
        background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px; margin-bottom: 8px;
        border-left: 3px solid #3b82f6; transition: all 0.2s; cursor: default;
    }
    .sidebar-project-card:hover { transform: translateX(2px); box-shadow: 0 2px 8px rgba(0,0,0,0.03); border-color: #cbd5e1; }
    .sp-title { font-weight: 700; font-size: 12px; color: #334155; margin-bottom: 2px; }
    .sp-desc { font-size: 10px; color: #94a3b8; line-height: 1.3; }

    /* --- 🔥 首页功能卡片样式 🔥 --- */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px !important;
        border: 1px solid #e2e8f0 !important;
        background-color: #ffffff;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.01);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        padding: 24px !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px -5px rgba(59, 130, 246, 0.15);
        border-color: #bfdbfe !important;
    }
    .card-icon-box {
        width: 56px; height: 56px;
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 28px; margin: 0 auto 15px auto;
        color: #2563eb;
    }
    .card-title { font-size: 18px; font-weight: 800; color: #1e293b; text-align: center; margin-bottom: 6px; }
    .card-desc { font-size: 13px; color: #64748b; text-align: center; margin-bottom: 20px; min-height: 40px; line-height: 1.5; }
    
    /* 海报 Banner */
    .poster-hero-container { background: #ffffff; border-radius: 20px; padding: 24px; box-shadow: 0 15px 40px rgba(0,0,0,0.05); border: 1px solid #edf2f7; display: flex; align-items: center; margin-bottom: 25px; position: relative; overflow: hidden; }
    .poster-hero-container::before { content: ''; position: absolute; top: -50%; right: -10%; width: 400px; height: 400px; background: radial-gradient(circle, rgba(167, 139, 250, 0.15) 0%, rgba(255,255,255,0) 70%); border-radius: 50%; z-index: 0; pointer-events: none; }
    .hero-icon-wrapper { width: 68px; height: 68px; background: linear-gradient(135deg, #c4b5fd, #818cf8); border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 34px; margin-right: 24px; box-shadow: 0 10px 20px -5px rgba(129, 140, 248, 0.5); z-index: 1; color: white; }
    .hero-title { font-size: 22px; font-weight: 800; color: #1e293b; margin: 0 0 8px 0; letter-spacing: -0.5px; z-index: 1; position: relative; }
    .hero-desc { font-size: 15px; color: #64748b; margin: 0; font-weight: 500; z-index: 1; position: relative; }

    /* 教程 */
    .step-card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 18px; margin-bottom: 12px; display: flex; align-items: flex-start; transition: transform 0.2s; }
    .step-card:hover { border-color: #bfdbfe; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.05); transform: translateX(5px); }
    .step-icon { background: #eff6ff; color: #2563eb; width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 15px; flex-shrink: 0; }
    .step-content h4 { margin: 0 0 4px; font-size: 15px; color: #1e293b; font-weight: 700; }
    .step-content p { margin: 0; font-size: 13px; color: #64748b; }

    /* 通用 */
    .footer-legal { margin-top: 40px; padding-top: 20px; border-top: 1px solid #e2e8f0; text-align: center; color: #94a3b8; font-size: 12px; }
    .footer-links a { color: #64748b; text-decoration: none; margin: 0 10px; transition: color 0.2s; }
    .auth-title { text-align: center; font-weight: 800; font-size: 24px; color: #1e293b; margin-bottom: 20px; }
    .login-spacer { height: 5vh; }
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

def render_footer():
    st.markdown("""<div class="footer-legal"><div class="footer-links"><a href="#">用户协议</a> | <a href="#">隐私政策</a> | <a href="#">免责声明</a> | <a href="#">关于我们</a></div><div style="margin-top: 10px;">© 2026 爆款工场 Pro | 鄂ICP备2024XXXXXX号-1 | 违法和不良信息举报：TG777188</div><div style="font-size: 11px; color: #cbd5e1; margin-top: 5px;">本站仅提供技术工具，请勿用于任何非法用途，用户生成内容文责自负。</div></div>""", unsafe_allow_html=True)

# 🔥 全新微信组件 🔥
def render_wechat_box(label, wx_id):
    html = f"""
    <!DOCTYPE html><html><head><style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;600&display=swap');
    body{{margin:0;padding:0;background:transparent;overflow:hidden;font-family:'Inter',sans-serif;}}
    .wx-pill{{
        display:flex;align-items:center;justify-content:space-between;
        background:white;border:1px solid #e2e8f0;border-radius:8px; /* 紧凑圆角 */
        padding:0 10px;height:36px; /* 紧凑高度 */
        cursor:pointer;transition:all 0.2s;box-sizing:border-box;color:#334155;
    }}
    .wx-pill:hover{{border-color:#07c160;background:#07c160;}}
    .wx-pill:hover .label{{color:white;}}
    .wx-pill:hover .right-part{{color:white;}}
    .wx-pill:hover svg{{fill:white;}}
    .label{{font-size:12px;font-weight:600;transition:0.2s;}}
    .right-part{{display:flex;align-items:center;gap:4px;font-family:monospace;font-weight:500;font-size:12px;transition:0.2s;color:#07c160;}}
    .copied-msg{{display:none;font-size:11px;font-weight:bold;color:white;}}
    .wx-pill:hover .copied-msg{{color:white;}}
    </style></head><body>
    <div class="wx-pill" onclick="copyText(this)">
        <span class="label" id="lbl">{label}</span>
        <div class="right-part" id="val">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="#07c160" xmlns="http://www.w3.org/2000/svg"><path d="M8.5 13.5L11 15L10 17.5C10 17.5 10.5 17.5 12.5 15C15 15 17 13 17 10.5C17 8 15 6 12.5 6C10 6 8 8 8 10.5C8 12 8.5 13.5 8.5 13.5ZM16.5 5.5C14 5.5 12 7 12 9C12 11 14 12.5 16.5 12.5C17 12.5 17.5 12.5 18 12L19.5 13L19 11C20 10.5 20.5 9.5 20.5 9C20.5 7 18.5 5.5 16.5 5.5Z" fill="currentColor"/></svg>
            <span>{wx_id}</span>
        </div>
        <span class="copied-msg" id="msg">✅ 已复制</span>
    </div>
    <script>
    function copyText(e){{
        const id = '{wx_id}';
        const lbl = document.getElementById('lbl');
        const val = document.getElementById('val');
        const msg = document.getElementById('msg');
        const textArea = document.createElement("textarea");
        textArea.value = id;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        lbl.style.display = 'none'; val.style.display = 'none'; msg.style.display = 'block';
        setTimeout(()=>{{ lbl.style.display = 'block'; val.style.display = 'flex'; msg.style.display = 'none'; }}, 1500);
    }}
    </script></body></html>
    """
    components.html(html, height=40)

def render_copy_button_html(text, k):
    safe = text.replace("`", "\`").replace("'", "\\'")
    html = f"""<!DOCTYPE html><html><head><style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@600&display=swap');body{{margin:0;padding:0;background:transparent;overflow:hidden;}}.btn{{width:100%;height:42px;background:linear-gradient(135deg,#2563eb,#1d4ed8);color:#fff;border:none;border-radius:8px;font-family:'Inter';font-weight:600;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all 0.2s;}}.btn:hover{{transform:translateY(-1px);box-shadow:0 6px 16px rgba(37,99,235,0.4);}}.btn:active{{transform:translateY(0);}}.btn.ok{{background:linear-gradient(135deg,#10b981,#059669);}}</style></head><body><button class="btn" onclick="cp(this)">📋 一键复制</button><script>function cp(e){{navigator.clipboard.writeText(`{safe}`).then(()=>{{e.classList.add("ok");e.innerText="✅ 成功";setTimeout(()=>{{e.classList.remove("ok");e.innerText="📋 一键复制"}},2000)}})}}</script></body></html>"""
    components.html(html, height=50)

# --- 业务逻辑 ---
def register_user(phone, password):
    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
    try:
        c.execute("INSERT INTO users (phone, password_hash, register_time) VALUES (?, ?, ?)", (phone, hash_password(password), datetime.datetime.now()))
        conn.commit(); return True, "注册成功"
    except sqlite3.IntegrityError: return False, "该手机号已注册"
    finally: conn.close()

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
    if not row: conn.close(); return False, "❌ 卡密不存在"
    if row[4] == 'unused':
        duration = row[1]; now = datetime.datetime.now(); expire_date = now + datetime.timedelta(days=duration)
        c.execute("UPDATE access_codes SET status='active', activated_at=?, expire_at=?, bind_user=? WHERE code=?", (now, expire_date, user_phone, code))
        conn.commit(); conn.close()
        return True, f"✅ 激活成功！增加 {duration} 天"
    else: conn.close(); return False, "⛔ 卡密已失效"

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
        return True, f"VIP (剩{days_left}天)" # 🔥 简化显示，用于侧边栏提取
    return False, "会员已过期"

def submit_feedback(phone, content):
    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
    c.execute("INSERT INTO feedbacks (user_phone, content, create_time, status) VALUES (?, ?, ?, ?)", (phone, content, datetime.datetime.now(), 'pending'))
    conn.commit(); conn.close()

# ==========================================
# 1. 认证模块
# ==========================================
if 'user_phone' not in st.session_state:
    auto = check_ip_auto_login()
    if auto: st.session_state['user_phone'] = auto; st.toast(f"欢迎回来 {auto}", icon="👋"); time.sleep(0.5); st.rerun()

def auth_page():
    st.markdown("<div class='login-spacer'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        with st.container():
            st.markdown("<div class='auth-title'>💠 爆款工场 Pro</div>", unsafe_allow_html=True)
            t1, t2, t3 = st.tabs(["🔐 登录", "✨ 注册", "🆘 找回"])
            with t1:
                with st.form("login"):
                    ph = st.text_input("手机号"); pw = st.text_input("密码", type="password")
                    if st.form_submit_button("登录", type="primary", use_container_width=True):
                        s, m = login_user(ph, pw)
                        if s: st.session_state['user_phone'] = ph; st.rerun()
                        else: st.error(m)
            with t2:
                ph = st.text_input("手机号", key="r_ph")
                c_c1, c_c2 = st.columns([2,1])
                if c_c2.button("发验证码", key="r_btn"): st.session_state['mk'] = send_mock_sms(ph); st.toast(f"验证码: {st.session_state['mk']}", icon="📩")
                cd = c_c1.text_input("验证码", key="r_cd")
                pw1 = st.text_input("密码", type="password", key="r_p1")
                pw2 = st.text_input("确认密码", type="password", key="r_p2")
                if st.button("注册", type="primary", use_container_width=True):
                    if pw1 != pw2: st.error("两次密码不一致")
                    elif st.session_state.get('mk') == cd:
                        s, m = register_user(ph, pw1)
                        if s: st.success("注册成功"); st.info("请切换到登录页登录")
                        else: st.error(m)
                    else: st.error("验证码错误")
            with t3: st.info("请联系客服重置密码")
    render_footer()

if 'user_phone' not in st.session_state:
    auth_page(); st.stop()

CURRENT_USER = st.session_state['user_phone']
IS_ADMIN = (CURRENT_USER == ADMIN_PHONE)
IS_VIP, VIP_MSG = get_user_vip_status(CURRENT_USER)

# --- 导航核心逻辑 ---
if 'nav_menu' not in st.session_state: st.session_state['nav_menu'] = "🏠 首页"

def go_to(page):
    st.session_state['nav_menu'] = page
    st.session_state['sb_radio'] = page

# --- 侧边栏 (终极紧凑 + 商业化) ---
with st.sidebar:
    # 1. 用户身份卡片 (带充值按钮)
    shop_url = get_setting("shop_url")
    buy_btn_html = f"""<a href="{shop_url}" target="_blank" class="buy-btn-sidebar">💎 充值</a>""" if shop_url else ""
    
    # 提取 VIP 天数信息
    role_display = VIP_MSG if IS_VIP else "🌑 普通用户"
    
    st.markdown(f"""
    <div class="sidebar-user-card">
        <div class="user-left">
            <div class="user-avatar">👤</div>
            <div class="user-info">
                <div class="user-name">{CURRENT_USER[:3]}****{CURRENT_USER[-4:]}</div>
                <div class="user-role">{role_display}</div>
            </div>
        </div>
        {buy_btn_html}
    </div>
    """, unsafe_allow_html=True)
    
    if not IS_VIP:
        with st.expander("🔑 激活卡密", expanded=True):
            c = st.text_input("卡密", type="password", key="side_cd", label_visibility="collapsed", placeholder="输入卡密...")
            if st.button("立即激活", use_container_width=True):
                s, m = activate_code(CURRENT_USER, c)
                if s: st.success(m); time.sleep(1); st.rerun()
                else: st.error(m)
    
    st.markdown("---")
    
    # 2. 导航菜单
    ops = ["🏠 首页", "📝 文案改写", "💡 爆款选题库", "🎨 海报生成", "🏷️ 账号起名", "👤 个人中心"]
    if IS_ADMIN: ops.append("🕵️‍♂️ 管理后台")
    
    try: curr_idx = ops.index(st.session_state['nav_menu'])
    except: curr_idx = 0; st.session_state['nav_menu'] = ops[0]

    selected = st.radio("功能导航", ops, index=curr_idx, label_visibility="collapsed", key="sb_radio")
    if selected != st.session_state['nav_menu']: st.session_state['nav_menu'] = selected; st.rerun()

    st.markdown("---")
    
    # 3. 热门变现项目 (紧凑卡片)
    st.markdown("<div style='font-size:12px;font-weight:700;color:#94a3b8;margin-bottom:8px;'>🔥 热门变现项目</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="sidebar-project-card">
        <div class="sp-title">📹 素人 KOC 孵化</div>
        <div class="sp-desc">真人出镜口播 · 红果/番茄拉新 · 0基础陪跑</div>
    </div>
    <div class="sidebar-project-card" style="border-left-color: #8b5cf6;">
        <div class="sp-title">🎨 御灵 AI 动漫</div>
        <div class="sp-desc">小说转动漫 · 端原生流量 · 版权分销</div>
    </div>
    <div class="sidebar-project-card" style="border-left-color: #10b981;">
        <div class="sp-title">🌍 文娱出海</div>
        <div class="sp-desc">短剧出海 · 工具拉新 · 资源变现</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    
    # 4. 变现咨询 (微信组件)
    render_wechat_box("💰 变现咨询", "W7774X")
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    
    # 5. 技术合作 (辅助)
    render_wechat_box("🛠️ 技术合作", "TG777188")
    
    st.markdown("---")
    if st.button("🚪 退出登录", use_container_width=True, type="secondary"): del st.session_state['user_phone']; st.rerun()

menu = st.session_state['nav_menu']

# --- 首页 (Embedded Button Design) ---
def page_home():
    st.markdown("## 💠 抖音爆款工场 Pro")
    st.caption("专为素人 KOC 打造的 AI 提效神器 | 文案 · 选题 · 海报 · 变现")
    st.markdown("---")
    
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        with st.container(border=True):
            st.markdown("""<div class="card-icon-box">📝</div><div class="card-title">文案改写</div><div class="card-desc">5路并发 · 爆款重组<br>解决文案枯竭</div>""", unsafe_allow_html=True)
            st.button("立即使用 ➜", key="h_btn1", on_click=go_to, args=("📝 文案改写",), type="primary", use_container_width=True)
            
    with c2:
        with st.container(border=True):
            st.markdown("""<div class="card-icon-box">💡</div><div class="card-title">爆款选题</div><div class="card-desc">流量焦虑 · 一键解决<br>精准击中痛点</div>""", unsafe_allow_html=True)
            st.button("立即使用 ➜", key="h_btn2", on_click=go_to, args=("💡 爆款选题库",), type="primary", use_container_width=True)
            
    with c3:
        with st.container(border=True):
            st.markdown("""<div class="card-icon-box">🎨</div><div class="card-title">海报生成</div><div class="card-desc">小提大作 · 影视质感<br>好莱坞级光影</div>""", unsafe_allow_html=True)
            st.button("立即使用 ➜", key="h_btn3", on_click=go_to, args=("🎨 海报生成",), type="primary", use_container_width=True)
            
    with c4:
        with st.container(border=True):
            st.markdown("""<div class="card-icon-box">🏷️</div><div class="card-title">账号起名</div><div class="card-desc">AI 算命 · 爆款玄学<br>赛道垂直定制</div>""", unsafe_allow_html=True)
            st.button("立即使用 ➜", key="h_btn4", on_click=go_to, args=("🏷️ 账号起名",), type="primary", use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("#### 📢 系统公告")
        st.info("🎉 欢迎使用 Pro 版！如需开通会员，请联系侧边栏客服获取卡密。", icon="👋")

# --- 文案改写 ---
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
                        with st.spinner("生成中..."):
                            st.session_state['results'][i] = rewrite_logic(val)
                            st.rerun()
            with col_out:
                res = st.session_state['results'].get(i, "")
                if res:
                    st.text_area("结果", value=res, height=200, label_visibility="collapsed", key=f"res_area_{i}")
                    render_copy_button_html(res, f"cp_{i}")
                    st.markdown("""<div style="margin-top:5px;padding:8px;background:#fff1f2;border-radius:6px;border:1px solid #fecdd3;font-size:12px;color:#be123c;display:flex;justify-content:space-between;align-items:center;"><span>🔥 <b>不会拍？</b>领《素人KOC出镜SOP》</span><span style="color:#e11d48;font-weight:bold;">👉 微信 W7774X</span></div>""", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='empty-state-box'><div style='font-size: 24px;'>⏳</div><div>等待指令...</div><div style='font-size: 12px; color: #94a3b8;'>Input content to generate</div></div>", unsafe_allow_html=True)

def page_poster():
    st.markdown("## 🎨 海报生成 (专业版)")
    st.markdown("""<div class="poster-hero-container"><div class="hero-icon-wrapper">🚀</div><div class="hero-text-content"><h2 class="hero-title">算力全面升级！好莱坞级光影引擎</h2><p class="hero-desc">为了提供极致的渲染效果，海报功能已迁移至性能更强的独立工作站。</p></div></div>""", unsafe_allow_html=True)
    
    components.html("""
    <!DOCTYPE html><html><head><style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;600;800&display=swap');
    body{margin:0;padding:20px;font-family:'Inter',sans-serif;overflow:hidden;background:transparent;} 
    .container{display:flex;gap:20px;width:100%;}
    .card{flex:1;border-radius:16px;height:120px;display:flex;flex-direction:column;justify-content:center;align-items:center;cursor:pointer;transition:all 0.3s;box-sizing:border-box;}
    .invite{background:#fff;border:2px dashed #cbd5e1;position:relative;}
    .invite:hover{border-color:#6366f1;background:#f5f3ff;transform:translateY(-5px);box-shadow:0 10px 20px rgba(0,0,0,0.03);}
    .invite-label{font-size:13px;color:#64748b;margin-bottom:5px;}
    .invite-code{font-size:28px;font-weight:800;color:#4f46e5;letter-spacing:1px;}
    .invite-hint{font-size:12px;color:#94a3b8;margin-top:5px;opacity:0;transition:0.2s;}
    .invite:hover .invite-hint{opacity:1;color:#6366f1;}
    .jump{flex:1.5;background:linear-gradient(135deg,#4f46e5,#7c3aed);text-decoration:none;box-shadow:0 4px 15px rgba(124,58,237,0.1);border:1px solid rgba(255,255,255,0.15);}
    .jump:hover{transform:translateY(-5px);box-shadow:0 8px 20px rgba(124,58,237,0.25);filter:brightness(1.05);}
    .jump-title{color:#fff;font-size:24px;font-weight:800;margin-bottom:4px;text-shadow:0 2px 4px rgba(0,0,0,0.1);}
    .jump-sub{color:rgba(255,255,255,0.9);font-size:14px;}
    </style></head><body>
    <div class="container">
        <div class="card invite" onclick="copyInvite(this)">
            <div class="invite-label">👇 第一步：点击复制邀请码</div>
            <div class="invite-code">5yzMbpxn</div>
            <div class="invite-hint" id="status">点击立即复制</div>
        </div>
        <a href="https://aixtdz.com/" target="_blank" class="card jump">
            <div class="jump-title">🚀 前往小提大作</div>
            <div class="jump-sub">第二步：点击跳转，开启创作</div>
        </a>
    </div>
    <script>
    function copyInvite(e){
        const text = '5yzMbpxn';
        const textArea = document.createElement("textarea");
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        try { document.execCommand('copy'); const hint = e.querySelector('#status'); hint.innerText = '✅ 复制成功！'; hint.style.opacity = '1'; hint.style.color = '#10b981'; setTimeout(()=>{ hint.innerText = '点击立即复制'; hint.style.opacity = '0'; hint.style.color = '#94a3b8'; }, 2000); } catch (err) {}
        document.body.removeChild(textArea);
    }
    </script></body></html>
    """, height=180) 
    
    st.write("")
    st.markdown("#### 📖 新手保姆级教程")
    steps = [("注册登录", "点击上方大按钮前往，注册时记得填写邀请码。"), ("创建画布", "登录后，在首页点击 <b>“创建自由画布”</b>。"), ("上传原图", "在画布中，点击组件栏的 <b>“+”</b> 号，上传剧照。"), ("一键改图", "点击 <b>右侧边框</b>，复制下方指令输入，等待奇迹！")]
    for idx, (title, desc) in enumerate(steps, 1):
        st.markdown(f"""<div class="step-card"><div class="step-icon">{idx}</div><div class="step-content"><h4>{title}</h4><p>{desc}</p></div></div>""", unsafe_allow_html=True)

    cmd_text = "将原图剧名：[原剧名] 改为：[你的新剧名]"
    components.html(f"""
    <!DOCTYPE html><html><head><style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@500&display=swap');
    body{{margin:0;padding:20px;font-family:'Fira Code',monospace;overflow:hidden;background:transparent;}}
    .terminal{{background:#0f172a;border-radius:12px;border:1px solid #334155;overflow:hidden;cursor:pointer;transition:0.3s;box-shadow:0 5px 15px rgba(0,0,0,0.1);}}
    .terminal:hover{{border-color:#6366f1;transform:translateY(-2px);box-shadow:0 8px 20px rgba(0,0,0,0.15);}}
    .header{{background:#1e293b;padding:10px 16px;display:flex;align-items:center;border-bottom:1px solid #334155;}}
    .dots{{display:flex;gap:6px;margin-right:12px;}}
    .dot{{width:10px;height:10px;border-radius:50%;}}
    .red{{background:#ef4444;}} .yellow{{background:#f59e0b;}} .green{{background:#22c55e;}}
    .title{{color:#64748b;font-size:12px;}}
    .body{{padding:20px;color:#e2e8f0;font-size:14px;display:flex;align-items:center;}}
    .prompt{{color:#22c55e;margin-right:10px;}}
    .hl{{color:#a78bfa;font-weight:bold;}}
    .success-overlay{{position:absolute;top:0;left:0;width:100%;height:100%;background:rgba(16,185,129,0.95);display:flex;align-items:center;justify-content:center;color:white;font-weight:bold;font-size:16px;opacity:0;pointer-events:none;transition:0.2s;}}
    .terminal:active .success-overlay{{opacity:1;}}
    </style></head><body>
    <div class="terminal" onclick="copyCmd()">
        <div class="header"><div class="dots"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div><div class="title">root@ai-generator ~ % (点击复制)</div></div>
        <div class="body"><span class="prompt">➜</span><span>将原图剧名：<span class="hl">[原剧名]</span> 改为：<span class="hl">[你的新剧名]</span></span></div>
        <div class="success-overlay" id="overlay">✅ 指令已复制到剪贴板</div>
    </div>
    <script>
    function copyCmd(){{
        const text = `{cmd_text}`;
        const textArea = document.createElement("textarea");
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        const overlay = document.getElementById('overlay');
        overlay.style.opacity = '1';
        setTimeout(()=>{{ overlay.style.opacity = '0'; }}, 1500);
    }}
    </script></body></html>
    """, height=160) 

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
    t1, t2 = st.tabs(["💳 账户", "💬 反馈"])
    with t1:
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
    with t2:
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
    st.markdown("## 🕵️‍♂️ 管理后台"); 
    pwd = st.text_input("二级密码", type="password")
    if pwd == ADMIN_INIT_PASSWORD:
        t1, t2, t3 = st.tabs(["设置", "卡密", "反馈"])
        with t1:
            st.write("#### 系统设置")
            url = st.text_input("发卡网链接", value=get_setting("shop_url"))
            if st.button("保存设置"): update_setting("shop_url", url); st.success("已保存")
        with t2:
            q = st.number_input("数量", 1, 100, 10); d = st.number_input("天数", 1, 365, 30)
            if st.button("生成卡密"):
                conn = sqlite3.connect(DB_FILE); c = conn.cursor()
                codes = []
                for _ in range(q):
                    code = "VIP-" + str(uuid.uuid4())[:8].upper()
                    c.execute("INSERT INTO access_codes (code, duration_days, status, create_time) VALUES (?, ?, ?, ?)", (code, d, 'unused', datetime.datetime.now()))
                    codes.append(code)
                conn.commit(); conn.close(); st.success(f"已生成 {q} 个")
            conn = sqlite3.connect(DB_FILE)
            df = pd.read_sql("SELECT * FROM access_codes ORDER BY create_time DESC", conn)
            st.dataframe(df, height=300)
            st.download_button("下载 CSV", df.to_csv(index=False).encode('utf-8'), "codes.csv", "text/csv")
            conn.close()
        with t3:
            conn = sqlite3.connect(DB_FILE); pending = pd.read_sql("SELECT * FROM feedbacks WHERE status='pending'", conn); conn.close()
            for i, r in pending.iterrows():
                with st.container(border=True):
                    st.write(f"用户: {r['user_phone']} | 内容: {r['content']}")
                    reply = st.text_input("回复", key=f"rep_{r['id']}")
                    if st.button("发送", key=f"send_{r['id']}"):
                        conn = sqlite3.connect(DB_FILE); c = conn.cursor()
                        c.execute("UPDATE feedbacks SET reply=?, status='replied' WHERE id=?", (reply, r['id']))
                        conn.commit(); conn.close(); st.rerun()

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
