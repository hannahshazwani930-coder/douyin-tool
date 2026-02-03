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
# 0. 核心配置 & 数据库 (后端逻辑保持稳健)
# ==========================================
st.set_page_config(
    page_title="抖音爆款工场 Pro", 
    layout="wide",
    page_icon="💠",
    initial_sidebar_state="expanded"
)

# 🔑 基础配置
ADMIN_ACCOUNT = "13065080569" 
ADMIN_INIT_PASSWORD = "ltren777188" 
GLOBAL_INVITE_CODE = "VIP888" 
REWARD_DAYS_NEW_USER = 3  
REWARD_DAYS_REFERRER = 3  
DB_FILE = 'saas_data_final.db'

# --- 数据库初始化 ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (phone TEXT PRIMARY KEY, password_hash TEXT, register_time TIMESTAMP, last_login_ip TEXT, last_login_time TIMESTAMP, own_invite_code TEXT UNIQUE, invited_by TEXT, invite_count INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS access_codes (code TEXT PRIMARY KEY, duration_days INTEGER, activated_at TIMESTAMP, expire_at TIMESTAMP, status TEXT, create_time TIMESTAMP, bind_user TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS feedbacks (id INTEGER PRIMARY KEY AUTOINCREMENT, user_phone TEXT, content TEXT, reply TEXT, create_time TIMESTAMP, status TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)''')
    
    # 兼容性更新字段
    try: c.execute("ALTER TABLE users ADD COLUMN own_invite_code TEXT"); except: pass
    try: c.execute("ALTER TABLE users ADD COLUMN invited_by TEXT"); except: pass
    try: c.execute("ALTER TABLE users ADD COLUMN invite_count INTEGER DEFAULT 0"); except: pass
    
    # 初始化管理员
    c.execute("SELECT phone FROM users WHERE phone=?", (ADMIN_ACCOUNT,))
    if not c.fetchone():
        admin_pwd_hash = hashlib.sha256(ADMIN_INIT_PASSWORD.encode()).hexdigest()
        c.execute("INSERT INTO users (phone, password_hash, register_time, own_invite_code) VALUES (?, ?, ?, ?)", (ADMIN_ACCOUNT, admin_pwd_hash, datetime.datetime.now(), "ADMIN888"))
    conn.commit(); conn.close()

init_db()

# ==========================================
# 1. 终极样式系统 (The Ultimate CSS)
# ==========================================
def inject_css(mode="app"):
    # 基础字体与重置
    base_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
        
        /* 隐藏顶部红线和菜单 */
        header[data-testid="stHeader"] { visibility: hidden; }
        #MainMenu { visibility: hidden; }
        [data-testid="stSidebarCollapsedControl"] { display: none; }
        
        /* 全局按钮美化 */
        div.stButton > button {
            border-radius: 10px; font-weight: 600; border: none; transition: all 0.2s;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        div.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 5px 10px rgba(0,0,0,0.1); }
        
        /* 输入框美化 - 解决看不清字的问题 */
        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
            color: #1e293b !important; /* 强制深色字体 */
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 8px !important;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
        }
    </style>
    """
    
    # 登录页专用 - 极光背景 + 玻璃拟态卡片
    auth_css = """
    <style>
        .stApp {
            background: linear-gradient(-45deg, #0f172a, #334155, #1e293b, #0f172a);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
        }
        @keyframes gradientBG { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
        
        /* 劫持 Streamlit Form 作为登录卡片 */
        [data-testid="stForm"] {
            background-color: rgba(255, 255, 255, 0.95);
            padding: 40px;
            border-radius: 24px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        /* 左侧文字 */
        .lp-header { font-size: 48px; font-weight: 900; color: white; letter-spacing: -1.5px; text-shadow: 0 10px 20px rgba(0,0,0,0.3); margin-bottom: 10px; }
        .lp-sub { font-size: 18px; color: #cbd5e1; margin-bottom: 40px; font-weight: 400; line-height: 1.6; }
        .lp-item { color: #e2e8f0; font-size: 15px; margin-bottom: 15px; display: flex; align-items: center; }
        .lp-icon { background: rgba(255,255,255,0.1); width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 15px; }
        
        /* Tab 样式 */
        .stTabs [data-baseweb="tab-list"] { gap: 10px; }
        .stTabs [data-baseweb="tab"] { background-color: transparent; color: #64748b; font-weight: 600; }
        .stTabs [aria-selected="true"] { color: #2563eb !important; border-bottom-color: #2563eb !important; }
    </style>
    """
    
    # 系统内页专用 - 极简 SaaS 白
    app_css = """
    <style>
        .stApp { background-color: #f8fafc; }
        
        /* 侧边栏优化 */
        [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
        
        /* 内容容器 */
        div.block-container { padding-top: 2rem; max-width: 1200px; }
        
        /* 公告栏 */
        .announcement-box {
            background: linear-gradient(90deg, #eff6ff, #ffffff);
            border: 1px solid #bfdbfe; color: #1e40af;
            padding: 10px 15px; border-radius: 8px; margin-bottom: 25px;
            display: flex; align-items: center; font-size: 14px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.02);
        }
        .ann-icon { margin-right: 10px; font-size: 16px; }
        
        /* 统计卡片 / 功能卡片 */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: white; border-radius: 16px; border: 1px solid #e2e8f0;
            padding: 20px; transition: transform 0.2s;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            transform: translateY(-3px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); border-color: #93c5fd;
        }
    </style>
    """
    
    st.markdown(base_css, unsafe_allow_html=True)
    if mode == "auth": st.markdown(auth_css, unsafe_allow_html=True)
    else: st.markdown(app_css, unsafe_allow_html=True)

# ==========================================
# 2. 逻辑层 (Logic Layer)
# ==========================================

# 辅助函数
def hash_password(password): return hashlib.sha256(password.encode()).hexdigest()
def get_remote_ip(): return "unknown_ip"
def generate_invite_code(): return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# 数据库操作
def get_setting(key):
    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
    c.execute("SELECT value FROM settings WHERE key=?", (key,))
    row = c.fetchone(); conn.close()
    return row[0] if row else ""

def update_setting(key, value):
    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
    c.execute("REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit(); conn.close()

def login_user(account, password):
    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE phone=?", (account,))
    row = c.fetchone(); conn.close()
    if row and row[0] == hash_password(password):
        return True, "登录成功"
    return False, "账号或密码错误"

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
        conn.commit()
        
        # 赠送 VIP
        add_vip_days(account, REWARD_DAYS_NEW_USER, "NEW_USER")
        if referrer:
            add_vip_days(referrer, REWARD_DAYS_REFERRER, "REFERRAL")
            conn.execute("UPDATE users SET invite_count = invite_count + 1 WHERE phone=?", (referrer,))
            conn.commit()
            
        conn.close()
        return True, "注册成功"
    except Exception as e: 
        return False, f"注册失败: {str(e)}"
    finally:
        try: conn.close()
        except: pass

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

# ==========================================
# 3. 视图组件 (View Components)
# ==========================================

def render_copy_btn(text, key_suffix):
    # 使用HTML/JS实现一键复制，不依赖Streamlit重载
    safe_text = text.replace("`", "\`").replace("'", "\\'")
    html = f"""
    <script>
    function copy_{key_suffix}() {{
        navigator.clipboard.writeText(`{safe_text}`);
        document.getElementById('btn_{key_suffix}').innerHTML = '✅ 已复制';
        setTimeout(() => {{ document.getElementById('btn_{key_suffix}').innerHTML = '📋 一键复制'; }}, 2000);
    }}
    </script>
    <button id="btn_{key_suffix}" onclick="copy_{key_suffix}()" style="
        width:100%; height:40px; background:#0f172a; color:white; 
        border:none; border-radius:8px; cursor:pointer; font-weight:600; font-family:'Inter';
    ">📋 一键复制</button>
    """
    components.html(html, height=50)

def render_wechat_pill(label, wx_id):
    components.html(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;background:white;border:1px solid #e2e8f0;border-radius:8px;padding:0 12px;height:38px;cursor:pointer;font-family:'Inter',sans-serif;font-size:13px;color:#334155;transition:0.2s;" onclick="navigator.clipboard.writeText('{wx_id}')">
        <span style="font-weight:600">{label}</span>
        <span style="color:#059669;font-family:monospace;background:#ecfdf5;padding:2px 6px;border-radius:4px;">📋 {wx_id}</span>
    </div>
    """, height=45)

def render_announcement():
    # 首页公告栏
    ann_text = get_setting("announcement")
    if not ann_text: ann_text = "🎉 欢迎使用抖音爆款工场 Pro，系统已升级至 V2.0 稳定版！"
    st.markdown(f"""
    <div class="announcement-box">
        <span class="ann-icon">📢</span>
        <span>{ann_text}</span>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 4. 页面视图 (Page Views)
# ==========================================

def view_auth():
    inject_css("auth")
    
    st.markdown("<div style='height: 10vh;'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 10, 1])
    
    with c2:
        col_text, col_form = st.columns([1.2, 1], gap="large")
        
        with col_text:
            st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
            st.markdown("<div class='lp-header'>抖音爆款工场 Pro</div>", unsafe_allow_html=True)
            st.markdown("<div class='lp-sub'>全网首个 AI + KOC 商业变现操作系统<br>让流量不再是玄学</div>", unsafe_allow_html=True)
            features = [
                ("🚀", "5路并发 · 极速文案清洗改写"),
                ("💡", "爆款选题 · 击穿流量焦虑"),
                ("🎨", "海报生成 · 影视级光影质感"),
                ("💰", "裂变系统 · 邀请好友免费续杯")
            ]
            for icon, text in features:
                st.markdown(f"<div class='lp-item'><div class='lp-icon'>{icon}</div>{text}</div>", unsafe_allow_html=True)
        
        with col_form:
            # 这里的 Tabs 和 Form 会被 CSS 包装成卡片样式
            t1, t2 = st.tabs(["🔐 登录账号", "📝 注册新号"])
            
            with t1:
                with st.form("login"):
                    st.text_input("账号", placeholder="手机号", key="l_u")
                    st.text_input("密码", placeholder="密码", type="password", key="l_p")
                    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
                    if st.form_submit_button("立即进入系统", type="primary", use_container_width=True):
                        if not st.session_state.l_u or not st.session_state.l_p:
                            st.error("请输入账号和密码")
                        else:
                            s, m = login_user(st.session_state.l_u, st.session_state.l_p)
                            if s: 
                                st.session_state['user_phone'] = st.session_state.l_u
                                st.rerun()
                            else: st.error(m)
            
            with t2:
                with st.form("register"):
                    st.info(f"🎁 新用户立送 {REWARD_DAYS_NEW_USER} 天 VIP")
                    r_u = st.text_input("手机号", placeholder="作为登录账号")
                    r_p = st.text_input("设置密码", type="password")
                    r_c = st.text_input("邀请码", placeholder="必填，无码请联系客服")
                    if st.form_submit_button("立即注册", use_container_width=True):
                        if not r_u or not r_p or not r_c:
                            st.warning("请填写完整信息")
                        else:
                            # 验证邀请码
                            valid = False
                            if r_c == GLOBAL_INVITE_CODE: valid = True
                            else:
                                conn = sqlite3.connect(DB_FILE); cu = conn.cursor()
                                cu.execute("SELECT phone FROM users WHERE own_invite_code=?", (r_c,))
                                if cu.fetchone(): valid = True
                                conn.close()
                            
                            if valid:
                                s, m = register_user(r_u, r_p, r_c)
                                if s: 
                                    st.success(m)
                                    st.session_state['user_phone'] = r_u
                                    time.sleep(1)
                                    st.rerun()
                                else: st.error(m)
                            else: st.error("❌ 邀请码无效，请联系客服获取")

    # 底部版权
    st.markdown("<div style='position:fixed; bottom:20px; width:100%; text-align:center; color:rgba(255,255,255,0.4); font-size:12px;'>© 2026 抖音爆款工场 Pro | 鄂ICP备2024XXXXXX号-1</div>", unsafe_allow_html=True)

def view_home():
    # 渲染公告栏
    render_announcement()
    
    # Hero Section
    st.markdown("""
    <div style="text-align:center; padding: 40px 20px; background:white; border-radius:20px; border:1px solid #e2e8f0; margin-bottom:30px; box-shadow:0 10px 30px -10px rgba(0,0,0,0.05);">
        <h1 style="color:#1e293b; font-size:36px; margin-bottom:10px;">抖音爆款工场 Pro</h1>
        <p style="color:#64748b; font-size:16px;">专为素人 KOC 打造的 AI 商业变现操作系统</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 功能卡片
    c1, c2, c3, c4 = st.columns(4)
    
    def home_card(col, emoji, title, desc, target):
        with col:
            with st.container(border=True):
                st.markdown(f"""
                <div style="text-align:center; height:140px;">
                    <div style="font-size:40px; margin-bottom:10px;">{emoji}</div>
                    <div style="font-weight:700; color:#1e293b; font-size:16px;">{title}</div>
                    <div style="font-size:12px; color:#94a3b8; margin-top:5px; line-height:1.4;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("立即使用", key=f"home_btn_{title}", use_container_width=True, type="primary"):
                    st.session_state['nav_menu'] = target
                    st.rerun()

    home_card(c1, "📝", "文案改写", "5路并发洗稿<br>告别文案枯竭", "📝 文案改写")
    home_card(c2, "💡", "爆款选题", "击穿流量焦虑<br>精准击中痛点", "💡 爆款选题库")
    home_card(c3, "🎨", "海报生成", "好莱坞级光影<br>极速渲染引擎", "🎨 海报生成")
    home_card(c4, "🏷️", "账号起名", "AI 算命玄学<br>赛道垂直定制", "🏷️ 账号起名")

def view_rewrite():
    st.markdown("### 📝 爆款文案改写")
    st.caption("基于 DeepSeek V3 模型，智能清洗重组文案结构")
    
    # API 初始化
    api_key = st.secrets.get("DEEPSEEK_API_KEY", "")
    client = None
    if api_key:
        try: client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        except: pass
    
    if not client:
        st.warning("⚠️ 未配置 API Key，系统将运行在演示模式（不返回真实结果）")

    # 逻辑函数
    def process_text(text):
        if not client: return "【演示模式】请在后台配置 API Key 后使用。\n\n模拟结果：\n这是改写后的爆款文案..."
        if len(text) < 5: return "❌ 文案太短"
        try:
            prompt = f"你是一个抖音千万粉博主。请将以下文案改写为爆款口播文案，要求：黄金3秒开头，情绪饱满，结尾强引导。原文：{text}"
            res = client.chat.completions.create(model="deepseek-chat", messages=[{"role":"user", "content":prompt}], temperature=1.3)
            return res.choices[0].message.content
        except Exception as e: return f"API Error: {str(e)}"

    c1, c2 = st.columns([1, 2])
    with c1:
        st.info("💡 操作提示：将竞品文案粘贴在下方，点击按钮即可批量生成。")
        if st.button("🚀 5路并发执行", type="primary", use_container_width=True):
            inputs = [st.session_state.get(f"in_{i}", "") for i in range(1,6)]
            valid_inputs = [(i+1, txt) for i, txt in enumerate(inputs) if txt.strip()]
            
            if not valid_inputs:
                st.toast("请至少输入一条文案")
            else:
                with st.status("正在极速改写中...", expanded=True):
                    with ThreadPoolExecutor(max_workers=5) as executor:
                        futures = {executor.submit(process_text, txt): idx for idx, txt in valid_inputs}
                        for future in futures:
                            idx = futures[future]
                            st.session_state[f"out_{idx}"] = future.result()
                    st.rerun()

    # 工作台
    if 'results' not in st.session_state: st.session_state['results'] = {}
    
    for i in range(1, 6):
        with st.container(border=True):
            st.markdown(f"**工作台 #{i}**")
            col_in, col_out = st.columns([1, 1], gap="medium")
            with col_in:
                st.text_area(f"原始文案 #{i}", key=f"in_{i}", height=150, placeholder="粘贴文案...", label_visibility="collapsed")
            with col_out:
                res = st.session_state.get(f"out_{i}", "")
                if res:
                    st.text_area(f"结果 #{i}", value=res, height=150, key=f"area_out_{i}", label_visibility="collapsed")
                    render_copy_button_html(res, f"cp_{i}")
                else:
                    st.markdown("<div style='height:150px; display:flex; align-items:center; justify-content:center; color:#cbd5e1; border:1px dashed #e2e8f0; border-radius:8px;'>等待生成...</div>", unsafe_allow_html=True)

def view_poster():
    st.markdown("### 🎨 海报生成 (专业版)")
    st.info("💡 因算力需求较大，海报生成功能已迁移至独立 GPU 集群。")
    
    # 漂亮的引导卡片
    st.markdown("""
    <div style="background:linear-gradient(135deg, #4f46e5, #7c3aed); padding:30px; border-radius:16px; color:white; display:flex; justify-content:space-between; align-items:center;">
        <div>
            <h2 style="margin:0; color:white;">前往「小提大作」工作站</h2>
            <p style="opacity:0.9; margin-top:5px;">请复制下方的专用邀请码，可获得额外的算力点数。</p>
        </div>
        <div style="font-size:40px;">🚀</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 第一步：复制邀请码")
        st.code("5yzMbpxn", language="text")
    with c2:
        st.markdown("#### 第二步：点击跳转")
        st.link_button("👉 前往海报生成工作站", "https://aixtdz.com/", type="primary", use_container_width=True)

def view_brainstorm():
    st.markdown("### 💡 爆款选题灵感库")
    
    topic = st.text_input("输入你的赛道/关键词", placeholder="例如：美妆、职场、副业、育儿...")
    if st.button("🧠 开始头脑风暴", type="primary"):
        if not topic: st.warning("请输入关键词")
        else:
            api_key = st.secrets.get("DEEPSEEK_API_KEY", "")
            if not api_key:
                st.error("请配置 API Key")
            else:
                try:
                    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
                    with st.spinner("AI 正在分析全网爆款数据..."):
                        prompt = f"我是做【{topic}】赛道的。请生成10个颠覆认知的爆款选题，格式：标题+钩子。要求：反直觉、引发焦虑或好奇。"
                        res = client.chat.completions.create(model="deepseek-chat", messages=[{"role":"user", "content":prompt}], temperature=1.5)
                        st.session_state['brain_res'] = res.choices[0].message.content
                except Exception as e:
                    st.error(str(e))
    
    if 'brain_res' in st.session_state:
        st.markdown("#### 灵感结果")
        st.text_area("结果", value=st.session_state['brain_res'], height=400)

def view_account():
    user = st.session_state.get('user_phone')
    if not user: 
        st.error("登录状态失效")
        return

    st.markdown("### 👤 个人中心")
    
    t1, t2 = st.tabs(["🎁 邀请有礼", "💳 账户状态"])
    
    with t1:
        code, count = get_user_invite_info(user)
        st.success(f"🎉 您的邀请码：{code}")
        st.markdown(f"**已邀请人数：{count} 人**（每邀请1人，双方各得 {REWARD_DAYS_REFERRER} 天 VIP）")
        render_copy_btn(code, "invite_code")
        
    with t2:
        is_vip, msg = get_user_vip_status(user)
        col1, col2 = st.columns(2)
        col1.metric("当前账号", user)
        col2.metric("会员状态", "VIP" if is_vip else "普通用户", delta=msg)
        
        st.markdown("---")
        st.write("#### 激活卡密")
        c_code = st.text_input("输入卡密", placeholder="VIP-XXXXXX")
        if st.button("立即激活"):
            conn = sqlite3.connect(DB_FILE); cur = conn.cursor()
            cur.execute("SELECT * FROM access_codes WHERE code=?", (c_code,))
            row = cur.fetchone()
            cur.close()
            
            if row and row[4] == 'unused':
                add_vip_days(user, row[1], "CDKEY")
                conn = sqlite3.connect(DB_FILE); cur = conn.cursor()
                cur.execute("UPDATE access_codes SET status='active', activated_at=?, bind_user=? WHERE code=?", (datetime.datetime.now(), user, c_code))
                conn.commit(); conn.close()
                st.success(f"✅ 激活成功！增加 {row[1]} 天")
                time.sleep(1); st.rerun()
            else:
                st.error("❌ 卡密无效或已使用")

def view_admin():
    if st.session_state.get('user_phone') != ADMIN_ACCOUNT:
        st.error("无权访问")
        return
        
    st.markdown("### 🕵️‍♂️ 管理后台")
    
    t1, t2 = st.tabs(["用户管理", "卡密生成"])
    with t1:
        conn = sqlite3.connect(DB_FILE)
        df = pd.read_sql("SELECT phone, invite_count, register_time FROM users ORDER BY register_time DESC LIMIT 50", conn)
        st.dataframe(df, use_container_width=True)
        conn.close()
        
    with t2:
        days = st.number_input("天数", value=30)
        count = st.number_input("数量", value=10)
        if st.button("生成卡密"):
            conn = sqlite3.connect(DB_FILE); c = conn.cursor()
            new_codes = []
            for _ in range(count):
                code = f"VIP-{uuid.uuid4().hex[:8].upper()}"
                c.execute("INSERT INTO access_codes (code, duration_days, status, create_time) VALUES (?, ?, ?, ?)", (code, days, 'unused', datetime.datetime.now()))
                new_codes.append([code, days])
            conn.commit(); conn.close()
            st.success(f"已生成 {count} 个卡密")
            st.dataframe(pd.DataFrame(new_codes, columns=["卡密", "天数"]))

# ==========================================
# 5. 主程序入口 (Main)
# ==========================================
def main():
    if 'user_phone' not in st.session_state:
        view_auth()
    else:
        inject_css("app") # 注入系统内页样式
        
        with st.sidebar:
            st.markdown(f"**👤 用户：{st.session_state['user_phone']}**")
            
            # 导航菜单
            nav = st.radio("导航", ["🏠 首页", "📝 文案改写", "💡 爆款选题", "🎨 海报生成", "🏷️ 账号起名", "👤 个人中心", "🕵️‍♂️ 管理后台" if st.session_state['user_phone'] == ADMIN_ACCOUNT else "None"], index=0, label_visibility="collapsed")
            if nav == "None": nav = "🏠 首页"
            
            st.markdown("---")
            render_wechat_pill("🎁 领取资料", "W7774X")
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            if st.button("🚪 退出登录", use_container_width=True):
                del st.session_state['user_phone']
                st.rerun()

        # 路由
        if nav == "🏠 首页": view_home()
        elif nav == "📝 文案改写": view_rewrite()
        elif nav == "💡 爆款选题": view_brainstorm()
        elif nav == "🎨 海报生成": view_poster()
        elif nav == "🏷️ 账号起名": view_naming()
        elif nav == "👤 个人中心": view_account()
        elif nav == "🕵️‍♂️ 管理后台": view_admin()
        
        # 底部 Footer
        st.markdown("<div style='margin-top:50px; text-align:center; color:#cbd5e1; font-size:12px;'>© 2026 抖音爆款工场 Pro System</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
