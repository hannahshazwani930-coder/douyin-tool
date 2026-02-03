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
import re

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
ADMIN_ACCOUNT = "13065080569" 
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
    c.execute("SELECT phone FROM users WHERE phone=?", (ADMIN_ACCOUNT,))
    if not c.fetchone():
        admin_pwd_hash = hashlib.sha256(ADMIN_INIT_PASSWORD.encode()).hexdigest()
        c.execute("INSERT INTO users (phone, password_hash, register_time, own_invite_code) VALUES (?, ?, ?, ?)", (ADMIN_ACCOUNT, admin_pwd_hash, datetime.datetime.now(), "ADMIN888"))
    else:
        c.execute("UPDATE users SET own_invite_code='ADMIN888' WHERE phone=? AND own_invite_code IS NULL", (ADMIN_ACCOUNT,))
    conn.commit(); conn.close()

init_db()

# ==========================================
# 1. 样式系统 (Style System)
# ==========================================

# A. 全局样式 (Global)
GLOBAL_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    .stApp { font-family: 'Inter', sans-serif; }
    header { visibility: hidden; }
    [data-testid="stSidebarCollapsedControl"] { display: none; }
    div.block-container { max-width: 1200px !important; padding: 2rem !important; }
    
    /* 按钮基础 */
    div.stButton > button { border-radius: 8px; font-weight: 600; height: 44px; border: none; transition: 0.2s; }
</style>
"""

# B. 登录页专用样式 (Auth Page)
AUTH_CSS = """
<style>
    /* 动态极光背景 */
    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e293b, #334155, #0f172a);
        background-size: 400% 400%; animation: gradientBG 15s ease infinite;
    }
    @keyframes gradientBG { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
    
    /* 登录卡片容器 - 纯白玻璃 */
    .auth-card-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(255,255,255,0.1);
        color: #0f172a;
    }
    
    /* 输入框强制美化 (白底黑字) */
    .stTextInput input {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        color: #0f172a !important;
        border-radius: 8px !important;
        padding: 12px 15px !important;
    }
    .stTextInput input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
    }
    .stTextInput label { display: none !important; }
    
    /* 按钮 */
    div.stButton > button { background: #2563eb; color: white !important; }
    div.stButton > button:hover { background: #1d4ed8; }

    /* 左侧品牌区 */
    .lp-header { font-size: 42px; font-weight: 900; color: white; margin-bottom: 10px; letter-spacing: -1px; text-shadow: 0 4px 10px rgba(0,0,0,0.3); }
    .lp-sub { font-size: 16px; color: #cbd5e1; margin-bottom: 40px; font-weight: 400; line-height: 1.6; }
    .lp-feature { display: flex; align-items: center; margin-bottom: 20px; color: white; font-weight: 500; font-size: 15px; }
    .lp-icon { width: 32px; height: 32px; background: rgba(255,255,255,0.15); border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 15px; backdrop-filter: blur(5px); }
</style>
"""

# C. 系统内页专用样式 (App Page)
APP_CSS = """
<style>
    .stApp { background-color: #f8fafc; }
    
    /* 侧边栏 */
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
    .sidebar-user-card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px; display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px; }
    .user-left { display: flex; align-items: center; }
    .user-avatar { font-size: 18px; margin-right: 10px; background: white; border: 1px solid #e2e8f0; width: 34px; height: 34px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
    .user-name { font-weight: 700; font-size: 13px; color: #1e293b; }
    .user-role { font-size: 10px; color: #d97706; font-weight: 600; background: #fffbeb; padding: 1px 5px; border-radius: 4px; margin-top: 2px; }
    
    /* 侧边栏导航 */
    .stRadio > div { gap: 0px; }
    .stRadio label { background: transparent; padding: 8px 12px; border-radius: 6px; margin-bottom: 2px; color: #64748b; font-weight: 500; transition: all 0.2s; border: none; font-size: 14px !important; }
    .stRadio label:hover { background: #f1f5f9; color: #0f172a; }
    .stRadio label[data-checked="true"] { background: #eff6ff; color: #2563eb; font-weight: 600; }
    .stRadio div[role="radiogroup"] > label > div:first-child { display: none; }
    
    /* 功能页磨砂质感 */
    section.main .stTextInput input, section.main textarea, section.main .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(255,255,255,0.9) !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
        color: #1e293b !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    section.main [data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff; border: 1px solid #e2e8f0;
        box-shadow: 0 4px 10px -2px rgba(0,0,0,0.03); border-radius: 16px;
        transition: transform 0.2s;
    }
    section.main [data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-4px); box-shadow: 0 10px 20px -5px rgba(0,0,0,0.08); border-color: #bfdbfe;
    }
    
    /* 首页 Hero */
    .hero-container {
        background: white; border-radius: 20px; padding: 50px 40px; text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; margin-bottom: 30px;
        position: relative; overflow: hidden;
    }
    .hero-container::before {
        content: ''; position: absolute; top: -50%; left: -10%; width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(59,130,246,0.08) 0%, transparent 70%); z-index: 0;
    }
    .hero-title { font-size: 42px; font-weight: 900; color: #1e293b; position: relative; z-index: 1; }
    .hero-sub { font-size: 16px; color: #64748b; font-weight: 500; position: relative; z-index: 1; margin-top: 10px; }
    
    /* 首页卡片 */
    .home-card-inner { text-align: center; padding: 10px; }
    .home-card-icon { width: 64px; height: 64px; margin: 0 auto 15px auto; background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border-radius: 18px; display: flex; align-items: center; justify-content: center; font-size: 30px; color: #0284c7; }
    .home-card-title { font-size: 18px; font-weight: 800; color: #1e293b; margin-bottom: 8px; }
    .home-card-desc { font-size: 13px; color: #64748b; line-height: 1.5; min-height: 40px; }
</style>
"""

# ==========================================
# 2. 辅助组件与逻辑
# ==========================================
def render_wechat_pill(label, wx_id):
    components.html(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;background:white;border:1px solid #e2e8f0;border-radius:8px;padding:0 10px;height:36px;cursor:pointer;font-family:sans-serif;font-size:12px;color:#334155;" onclick="navigator.clipboard.writeText('{wx_id}')">
        <span style="font-weight:600">{label}</span>
        <span style="color:#07c160;font-family:monospace">📋 {wx_id}</span>
    </div>
    """, height=40)

def render_copy_btn(text):
    components.html(f"""<button style="width:100%;height:40px;background:#0f172a;color:white;border:none;border-radius:8px;cursor:pointer;font-weight:600" onclick="navigator.clipboard.writeText(`{text}`)">📋 一键复制结果</button>""", height=50)

def render_hover_copy_box(text, label="点击复制"):
    safe = text.replace("`", "\`").replace("'", "\\'")
    html = f"""<!DOCTYPE html><html><head><style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;600&display=swap');body{{margin:0;padding:0;background:transparent;overflow:hidden;font-family:'Inter';}}.box{{display:flex;align-items:center;justify-content:space-between;background:#f8fafc;border:1px solid #cbd5e1;border-radius:6px;padding:0 10px;height:36px;cursor:pointer;transition:0.2s;color:#1e293b;font-size:13px;}}.box:hover{{border-color:#3b82f6;background:#fff;}}.hint{{font-size:12px;color:#94a3b8;}}.box:hover .hint{{color:#3b82f6;}}.box.ok{{background:#ecfdf5;border-color:#10b981;color:#065f46;}}</style></head><body><div class="box" onclick="c(this)"><span>{safe}</span><span class="hint" id="s">{label}</span></div><script>function c(e){{navigator.clipboard.writeText(`{safe}`);e.classList.add("ok");const s=e.querySelector("#s");const o=s.innerText;s.innerText="✅";setTimeout(()=>{{e.classList.remove("ok");s.innerText=o}},1500)}}</script></body></html>"""
    components.html(html, height=40)

def render_copy_button_html(text, k):
    safe = text.replace("`", "\`").replace("'", "\\'")
    html = f"""<!DOCTYPE html><html><head><style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@600&display=swap');body{{margin:0;padding:0;background:transparent;overflow:hidden;}}.btn{{width:100%;height:42px;background:#0f172a;color:#fff;border:none;border-radius:8px;font-family:'Inter';font-weight:600;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all 0.2s;}}.btn:hover{{background:#334155;}}.btn:active{{transform:translateY(0);}}.btn.ok{{background:#10b981;}}</style></head><body><button class="btn" onclick="cp(this)">📋 一键复制</button><script>function cp(e){{navigator.clipboard.writeText(`{safe}`).then(()=>{{e.classList.add("ok");e.innerText="✅ 成功";setTimeout(()=>{{e.classList.remove("ok");e.innerText="📋 一键复制"}},2000)}})}}</script></body></html>"""
    components.html(html, height=50)

def render_footer():
    st.markdown("""<div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #e2e8f0; text-align: center; color: #94a3b8; font-size: 12px;">© 2026 抖音爆款工场 Pro | 鄂ICP备2024XXXXXX号-1</div>""", unsafe_allow_html=True)

# --- 数据库逻辑 ---
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
def get_remote_ip(): return "unknown_ip" # 简化
def generate_invite_code(): return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def add_vip_days(account, days, source="system"):
    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
    c.execute("SELECT expire_at FROM access_codes WHERE bind_user=? AND status='active'", (account,))
    rows = c.fetchall()
    now = datetime.datetime.now()
    if rows:
        max_expire = max([datetime.datetime.strptime(str(r[0]).split('.')[0], '%Y-%m-%d %H:%M:%S') for r in rows])
        start_time = max_expire if max_expire > now else now
    else: start_time = now
    expire_at = start_time + datetime.timedelta(days=days)
    new_code = f"GIFT-{source}-{str(uuid.uuid4())[:6].upper()}"
    c.execute("INSERT INTO access_codes (code, duration_days, activated_at, expire_at, status, create_time, bind_user) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (new_code, days, now, expire_at, 'active', now, account))
    conn.commit(); conn.close()

def register_user(account, password, invite_code_used):
    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
    try:
        new_own_code = generate_invite_code()
        while True:
            c.execute("SELECT phone FROM users WHERE own_invite_code=?", (new_own_code,))
            if not c.fetchone(): break
            new_own_code = generate_invite_code()
        
        referrer = None
        if invite_code_used != GLOBAL_INVITE_CODE:
            c.execute("SELECT phone FROM users WHERE own_invite_code=?", (invite_code_used,))
            row = c.fetchone()
            if row: referrer = row[0]
            
        c.execute("INSERT INTO users (phone, password_hash, register_time, own_invite_code, invited_by) VALUES (?, ?, ?, ?, ?)", 
                  (account, hash_password(password), datetime.datetime.now(), new_own_code, referrer))
        conn.commit(); conn.close()
        add_vip_days(account, REWARD_DAYS_NEW_USER, "NEW_USER")
        if referrer:
            add_vip_days(referrer, REWARD_DAYS_REFERRER, "REFERRAL")
            conn = sqlite3.connect(DB_FILE); c = conn.cursor()
            c.execute("UPDATE users SET invite_count = invite_count + 1 WHERE phone=?", (referrer,))
            conn.commit(); conn.close()
        return True, "注册成功"
    except Exception as e: return False, str(e)
    finally: 
        try: conn.close()
        except: pass

def login_user(account, password):
    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE phone=?", (account,))
    row = c.fetchone(); conn.close()
    if row and row[0] == hash_password(password):
        conn = sqlite3.connect(DB_FILE); c = conn.cursor()
        c.execute("UPDATE users SET last_login_ip=?, last_login_time=? WHERE phone=?", (get_remote_ip(), datetime.datetime.now(), account))
        conn.commit(); conn.close()
        return True, "登录成功"
    return False, "账号或密码错误"

def check_ip_auto_login():
    return None # 简化演示

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
    if phone == ADMIN_ACCOUNT: return True, "👑 超级管理员"
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
    except: row = None
    conn.close()
    if row: return row[0], row[1]
    return "...", 0

def submit_feedback(phone, content):
    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
    c.execute("INSERT INTO feedbacks (user_phone, content, create_time, status) VALUES (?, ?, ?, ?)", (phone, content, datetime.datetime.now(), 'pending'))
    conn.commit(); conn.close()

# ==========================================
# 3. 视图层 (View Layer)
# ==========================================

# --- 登录页 (修复版) ---
def view_auth():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    st.markdown(AUTH_CSS, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 8vh;'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 8, 1])
    
    with c2:
        col_l, col_r = st.columns([1.1, 1], gap="large")
        with col_l:
            st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
            st.markdown("<div class='lp-header'>抖音爆款工场 Pro</div>", unsafe_allow_html=True)
            st.markdown("<div class='lp-sub'>全网首个 AI + KOC 商业变现操作系统</div>", unsafe_allow_html=True)
            st.markdown("""<div class='lp-feature'><div class='lp-icon'>🚀</div>5路并发 · 极速文案清洗改写</div><div class='lp-feature'><div class='lp-icon'>💡</div>爆款选题 · 击穿流量焦虑</div><div class='lp-feature'><div class='lp-icon'>🎨</div>海报生成 · 影视级光影质感</div><div class='lp-feature'><div class='lp-icon'>💰</div>裂变系统 · 邀请好友免费续杯</div>""", unsafe_allow_html=True)
        
        with col_r:
            # 纯 CSS 卡片，无 st.container
            st.markdown('<div class="auth-card-container">', unsafe_allow_html=True)
            t1, t2, t3 = st.tabs(["登录", "注册", "找回"])
            
            with t1:
                st.write("")
                with st.form("login_form"):
                    acc = st.text_input("账号", placeholder="手机号 或 邮箱", label_visibility="collapsed")
                    pw = st.text_input("密码", type="password", placeholder="请输入密码", label_visibility="collapsed")
                    st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
                    if st.form_submit_button("立即登录", type="primary", use_container_width=True):
                        s, m = login_user(acc, pw)
                        if s: st.session_state['user_phone'] = acc; st.rerun()
                        else: st.error(m)
            
            with t2:
                st.info(f"🎁 新人注册即送 {REWARD_DAYS_NEW_USER} 天 VIP")
                acc = st.text_input("账号", key="r_acc", placeholder="手机号 或 邮箱", label_visibility="collapsed")
                pw1 = st.text_input("密码", type="password", key="r_p1", placeholder="设置密码", label_visibility="collapsed")
                pw2 = st.text_input("确认", type="password", key="r_p2", placeholder="确认密码", label_visibility="collapsed")
                with st.expander("❓ 获取邀请码"):
                    st.markdown(f"<div style='background:#f0fdf4;padding:10px;border-radius:6px;color:#15803d;font-size:12px;text-align:center;'>添加客服 <b>W7774X</b> 回复“注册”</div>", unsafe_allow_html=True)
                invite_code = st.text_input("邀请码", key="r_invite", placeholder="邀请码 (必填)", label_visibility="collapsed")
                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                if st.button("立即注册", type="primary", use_container_width=True):
                    if pw1 != pw2: st.error("密码不一致")
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
                            s, m = register_user(acc, pw1, invite_code)
                            if s: st.success(m); st.balloons(); time.sleep(2); st.session_state['user_phone'] = acc; st.rerun()
                            else: st.error(m)
                        else: st.error("❌ 邀请码无效")
            
            with t3:
                st.write("")
                st.warning("🔒 仅支持通过邮箱找回密码")
                email = st.text_input("注册邮箱", placeholder="name@example.com", label_visibility="collapsed")
                st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
                if st.button("发送重置邮件", use_container_width=True):
                    if "@" in email: st.success(f"邮件已发送至 {email}")
                    else: st.error("邮箱格式错误")
            
            st.markdown('</div>', unsafe_allow_html=True)
    render_footer()

# --- 首页 ---
def view_home():
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">抖音爆款工场 Pro</div>
        <div class="hero-sub">让流量不再是玄学 · 专为素人 KOC 打造的 AI 变现神器</div>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    def card(icon, title, desc, key, target):
        with st.container(border=True):
            st.markdown(f"<div class='home-card-inner'><div class='home-card-icon'>{icon}</div><div class='home-card-title'>{title}</div><div class='home-card-desc'>{desc}</div></div>", unsafe_allow_html=True)
            st.button("立即使用 ➜", key=key, on_click=lambda: st.session_state.update({'nav_menu': target, 'sb_radio': target}), type="primary", use_container_width=True)

    with c1: card("📝", "文案改写", "5路并发 · 爆款重组<br>告别文案枯竭", "h1", "📝 文案改写")
    with c2: card("💡", "爆款选题", "流量焦虑 · 一键解决<br>精准击中痛点", "h2", "💡 爆款选题库")
    with c3: card("🎨", "海报生成", "小提大作 · 影视质感<br>好莱坞级光影", "h3", "🎨 海报生成")
    with c4: card("🏷️", "账号起名", "AI 算命 · 爆款玄学<br>赛道垂直定制", "h4", "🏷️ 账号起名")

# --- 文案 ---
def view_rewrite():
    st.markdown("## 📝 爆款文案改写"); st.markdown("---")
    if 'results' not in st.session_state: st.session_state['results'] = {}
    
    # 修复 API key 初始化问题
    api_key = st.secrets.get("DEEPSEEK_API_KEY", "no-key")
    try:
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    except:
        client = None

    def rewrite_logic(content):
        if not client: return "⚠️ 请在 secrets.toml 配置 DEEPSEEK_API_KEY"
        if not content or len(content.strip()) < 5: return "⚠️ 内容过短"
        prompt = f"你是一个抖音千万粉的口播博主。原始素材：{content}。任务：清洗数据，改写为原创爆款文案。公式：黄金3秒开头+中间情绪饱满+结尾强引导。输出：直接输出文案，不要任何markdown格式。"
        try: return client.chat.completions.create(model="deepseek-chat", messages=[{"role":"user","content":prompt}], temperature=1.3).choices[0].message.content
        except Exception as e: return f"调用失败: {str(e)}"

    def clear_text(k): st.session_state[k] = ""
    c1, c2 = st.columns([1, 2], gap="medium")
    with c1:
        if st.button("🚀 5路并发执行", type="primary", use_container_width=True):
            tasks, indices = [], []
            for i in range(1, 6):
                val = st.session_state.get(f"in_{i}", "")
                if val.strip(): tasks.append(val); indices.append(i)
            if not tasks: st.toast("请至少输入一条文案", icon="⚠️")
            else:
                with st.status("☁️ 正在疯狂计算中...", expanded=True):
                    with ThreadPoolExecutor(5) as ex: res = list(ex.map(rewrite_logic, tasks))
                    for idx, r in zip(indices, res): st.session_state['results'][idx] = r
                    st.rerun()
    with c2: st.markdown("""<div style="background:#eff6ff;padding:12px;border-radius:8px;color:#1e40af;font-size:14px;">💡 提示：将文案粘贴到下方窗口，点击左侧蓝色按钮可批量处理。</div>""", unsafe_allow_html=True)
    st.write("")
    for i in range(1, 6):
        with st.container(border=True):
            st.markdown(f"**📝 工作台 #{i}**")
            col_in, col_out = st.columns([1, 1], gap="large")
            with col_in:
                input_key = f"in_{i}"
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
                    st.markdown("<div style='height:200px;background:#f8fafc;border:2px dashed #e2e8f0;border-radius:10px;display:flex;align-items:center;justify-content:center;color:#94a3b8;'>等待指令...</div>", unsafe_allow_html=True)

# --- 海报 ---
def view_poster():
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

# --- 选题 ---
def view_brainstorm():
    st.markdown("## 💡 爆款选题灵感库"); st.markdown("---")
    try:
        client = OpenAI(api_key=st.secrets.get("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
    except: client = None

    c1, c2 = st.columns([3, 1])
    with c1: topic = st.text_input("🔍 输入你的赛道/关键词", placeholder="例如：职场、美妆、减肥、副业...")
    with c2: st.write(""); st.write(""); generate_btn = st.button("🧠 帮我想选题", type="primary", use_container_width=True)
    if generate_btn and topic:
        if not client: st.error("请配置 API Key")
        else:
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

# --- 起名 ---
def view_naming():
    st.markdown("## 🏷️ 账号/IP 起名大师"); st.markdown("---")
    try:
        client = OpenAI(api_key=st.secrets.get("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
    except: client = None
    c1, c2 = st.columns(2)
    with c1: niche = st.selectbox("🎯 赛道", ["短剧", "小说", "口播", "情感", "带货"])
    with c2: style = st.selectbox("🎨 风格", ["高冷", "搞笑", "文艺", "粗暴", "反差"])
    keywords = st.text_input("🔑 关键词 (选填)")
    if st.button("🎲 生成名字", type="primary", use_container_width=True):
        if not client: st.error("请配置 API Key")
        else:
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

# --- 个人中心 (严重错误修复：添加变量定义) ---
def view_account():
    # 修复：获取当前用户
    CURRENT_USER = st.session_state.get('user_phone')
    if not CURRENT_USER:
        st.error("请重新登录")
        return
        
    IS_VIP, VIP_MSG = get_user_vip_status(CURRENT_USER)

    st.markdown("## 👤 个人中心"); st.markdown("---")
    t1, t2, t3 = st.tabs(["🎁 邀请有礼", "💳 账户信息", "💬 提交反馈"])
    with t1:
        my_code, invite_count = get_user_invite_info(CURRENT_USER)
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#fff7ed,#ffedd5);padding:30px;border-radius:16px;text-align:center;border:1px solid #fed7aa;margin-bottom:20px;'>
            <h3 style='color:#9a3412;margin:0'>🎉 邀请好友，免费续杯 VIP</h3>
            <p style='color:#c2410c'>每成功邀请 1 人，双方各得 3 天 VIP</p>
            <div style='background:white;padding:10px 30px;border-radius:8px;display:inline-block;font-size:24px;font-weight:bold;color:#ea580c;border:2px dashed #f97316;margin:15px 0;cursor:pointer' onclick="navigator.clipboard.writeText('{my_code}').then(()=>{{alert('已复制')}})">{my_code}</div>
            <div style='display:flex;justify-content:center;gap:40px;margin-top:20px;'>
                <div><div style='font-size:20px;font-weight:bold;color:#c2410c'>{invite_count}</div><div style='font-size:12px;color:#9a3412'>已邀请</div></div>
                <div><div style='font-size:20px;font-weight:bold;color:#c2410c'>{invite_count*3}</div><div style='font-size:12px;color:#9a3412'>获得天数</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        render_copy_button_html(my_code, "inv_copy")
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

# --- 后台 ---
def view_admin():
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

# ==========================================
# 5. 主程序入口 (Main Router)
# ==========================================
def main():
    if 'user_phone' not in st.session_state:
        view_auth()
    else:
        # 登录后加载系统 CSS
        st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
        st.markdown(APP_CSS, unsafe_allow_html=True)
        
        # 侧边栏
        with st.sidebar:
            is_vip, msg = get_user_vip_status(st.session_state['user_phone'])
            display = st.session_state['user_phone']
            if len(display)>7: display = display[:3]+"****"+display[-4:]
            
            st.markdown(f"""<div class="sidebar-user-card"><div class="user-left"><div class="user-avatar">👤</div><div><div class="user-name">{display}</div><div class="user-role">{'👑 VIP' if is_vip else '🌑 普通'}</div></div></div></div>""", unsafe_allow_html=True)
            
            ops = ["🏠 首页", "📝 文案改写", "💡 爆款选题库", "🎨 海报生成", "🏷️ 账号起名", "👤 个人中心"]
            if st.session_state['user_phone'] == ADMIN_ACCOUNT: ops.append("🕵️‍♂️ 管理后台")
            
            if 'nav_menu' not in st.session_state: st.session_state['nav_menu'] = ops[0]
            try: idx = ops.index(st.session_state['nav_menu'])
            except: idx = 0
            
            selected = st.radio("导航", ops, index=idx, label_visibility="collapsed", key="sb_radio")
            if selected != st.session_state['nav_menu']:
                st.session_state['nav_menu'] = selected
                st.rerun()
            
            st.markdown("---")
            st.markdown("<div style='font-size:12px;font-weight:bold;color:#94a3b8;margin-bottom:5px'>🔥 热门项目</div>", unsafe_allow_html=True)
            st.markdown("""<div class="sidebar-project-card"><div class="sp-title">📹 KOC 孵化</div><div class="sp-desc">真人出镜 · 0基础陪跑</div></div><div class="sidebar-project-card" style="border-left-color:#8b5cf6"><div class="sp-title">🎨 御灵 AI 动漫</div><div class="sp-desc">小说转动漫 · 端原生流量</div></div>""", unsafe_allow_html=True)
            
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            # 修复：调用正确的函数 render_wechat_pill
            render_wechat_pill("🎁 领取资料", "W7774X")
            st.markdown("<div style='height:5px'></div>", unsafe_allow_html=True)
            render_wechat_pill("🛠️ 技术合作", "TG777188")
            
            st.markdown("---")
            if st.button("🚪 退出", type="secondary"):
                del st.session_state['user_phone']
                st.rerun()

        # 页面路由
        menu = st.session_state['nav_menu']
        if menu == "🏠 首页": view_home()
        elif menu == "📝 文案改写": view_rewrite()
        elif menu == "🎨 海报生成": view_poster()
        elif menu == "💡 爆款选题库": view_brainstorm()
        elif menu == "🏷️ 账号起名": view_naming()
        elif menu == "👤 个人中心": view_account()
        elif menu == "🕵️‍♂️ 管理后台": view_admin()
        else: st.info(f"🚧 {menu} 功能升级中...")
        
        render_footer()

if __name__ == "__main__":
    main()
