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
# 1. 核心配置与数据库 (Core Config & DB)
# ==========================================
st.set_page_config(
    page_title="抖音爆款工场 Pro", 
    layout="wide",
    page_icon="💠",
    initial_sidebar_state="expanded"
)

ADMIN_ACCOUNT = "13065080569" 
ADMIN_INIT_PASSWORD = "ltren777188" 
GLOBAL_INVITE_CODE = "VIP888" 
DB_FILE = 'saas_data_v2.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # 确保所有表结构正确
    c.execute('''CREATE TABLE IF NOT EXISTS users (phone TEXT PRIMARY KEY, password_hash TEXT, register_time TIMESTAMP, last_login_ip TEXT, last_login_time TIMESTAMP, own_invite_code TEXT UNIQUE, invited_by TEXT, invite_count INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS access_codes (code TEXT PRIMARY KEY, duration_days INTEGER, activated_at TIMESTAMP, expire_at TIMESTAMP, status TEXT, create_time TIMESTAMP, bind_user TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS feedbacks (id INTEGER PRIMARY KEY AUTOINCREMENT, user_phone TEXT, content TEXT, reply TEXT, create_time TIMESTAMP, status TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)''')
    # 补全字段防报错
    try: c.execute("ALTER TABLE users ADD COLUMN own_invite_code TEXT"); except: pass
    try: c.execute("ALTER TABLE users ADD COLUMN invited_by TEXT"); except: pass
    try: c.execute("ALTER TABLE users ADD COLUMN invite_count INTEGER DEFAULT 0"); except: pass
    # 预设管理员
    c.execute("SELECT phone FROM users WHERE phone=?", (ADMIN_ACCOUNT,))
    if not c.fetchone():
        pwd_hash = hashlib.sha256(ADMIN_INIT_PASSWORD.encode()).hexdigest()
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (ADMIN_ACCOUNT, pwd_hash, datetime.datetime.now(), None, None, "ADMIN888", None, 0))
    conn.commit(); conn.close()

init_db()

# --- 通用工具函数 ---
def hash_password(p): return hashlib.sha256(p.encode()).hexdigest()
def generate_code(): return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
def get_user_vip_status(u):
    if u == ADMIN_ACCOUNT: return True, "👑 超级管理员"
    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
    c.execute("SELECT expire_at FROM access_codes WHERE bind_user=? AND status='active'", (u,))
    rows = c.fetchall(); conn.close()
    if not rows: return False, "未开通会员"
    max_e = max([datetime.datetime.strptime(str(r[0]).split('.')[0], '%Y-%m-%d %H:%M:%S') for r in rows])
    return (True, f"VIP (剩{(max_e - datetime.datetime.now()).days}天)") if max_e > datetime.datetime.now() else (False, "会员已过期")

# ==========================================
# 2. 样式仓库 (Style Repository)
# ==========================================

# A. 全局基础样式 (Reset & Font)
GLOBAL_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    .stApp { font-family: 'Inter', sans-serif; }
    header { visibility: hidden; }
    [data-testid="stSidebarCollapsedControl"] { display: none; }
    div.block-container { padding-top: 2rem !important; }
    /* 按钮基础 */
    div.stButton > button { border-radius: 8px; font-weight: 600; height: 44px; border: none; transition: 0.2s; }
</style>
"""

# B. 登录页专用样式 (Login Page Only)
AUTH_CSS = """
<style>
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%; animation: gradientBG 15s ease infinite;
    }
    @keyframes gradientBG { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
    
    .login-card {
        background: rgba(255,255,255,0.95); border-radius: 20px; padding: 40px;
        box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
    }
    .stTextInput input {
        background-color: #fff !important; border: 1px solid #cbd5e1 !important; color: #0f172a !important;
    }
    .lp-header { font-size: 36px; font-weight: 800; color: white; text-shadow: 0 2px 10px rgba(0,0,0,0.2); }
    .lp-sub { font-size: 16px; color: rgba(255,255,255,0.9); margin-bottom: 30px; }
    .lp-item { color: white; margin-bottom: 15px; display: flex; align-items: center; font-weight: 500; text-shadow: 0 1px 2px rgba(0,0,0,0.1); }
    .lp-icon { background: rgba(255,255,255,0.2); width: 30px; height: 30px; border-radius: 6px; display: flex; align-items: center; justify-content: center; margin-right: 12px; }
</style>
"""

# C. 系统内页专用样式 (App Page Only)
# 包含：侧边栏、Hero卡片、功能区磨砂质感
APP_CSS = """
<style>
    .stApp { background-color: #f8fafc; }
    
    /* --- 侧边栏 --- */
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
    .sidebar-user-card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px; display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px; }
    .sidebar-project-card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px; margin-bottom: 8px; border-left: 3px solid #3b82f6; cursor: default; }
    .stRadio > div { gap: 0px; }
    .stRadio label { border-radius: 6px; padding: 8px 10px; transition: 0.2s; border: none; }
    .stRadio label:hover { background: #f1f5f9; }
    .stRadio label[data-checked="true"] { background: #eff6ff; color: #2563eb; font-weight: 600; }
    
    /* --- 首页 Hero --- */
    .hero-container {
        background: white; border-radius: 20px; padding: 40px; text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; margin-bottom: 30px;
        position: relative; overflow: hidden;
    }
    .hero-container::before {
        content: ''; position: absolute; top: -50%; left: -10%; width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(59,130,246,0.05) 0%, transparent 70%); z-index: 0;
    }
    .hero-title { font-size: 42px; font-weight: 900; color: #1e293b; position: relative; z-index: 1; }
    
    /* --- 功能页磨砂质感 (仅针对主区域) --- */
    section.main .stTextInput input, section.main textarea, section.main .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(255,255,255,0.8) !important;
        backdrop-filter: blur(8px);
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02) !important;
    }
    section.main [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255,255,255,0.9); border: 1px solid white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02); border-radius: 16px;
        transition: transform 0.2s;
    }
    section.main [data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    }
    
    /* 按钮 */
    div.stButton > button[kind="primary"] { background: linear-gradient(135deg, #0f172a, #334155); color: white !important; }
</style>
"""

# ==========================================
# 3. 模块化组件 (Components)
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

# ==========================================
# 4. 页面视图函数 (Page Views)
# ==========================================

# --- A. 登录注册模块 ---
def view_auth():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    st.markdown(AUTH_CSS, unsafe_allow_html=True) # 注入登录页专属CSS
    
    st.markdown("<div style='height: 10vh;'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 8, 1])
    with c2:
        col_l, col_r = st.columns([1.2, 1], gap="large")
        with col_l:
            st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
            st.markdown("<div class='lp-header'>抖音爆款工场 Pro</div>", unsafe_allow_html=True)
            st.markdown("<div class='lp-sub'>全网首个 AI + KOC 商业变现操作系统</div>", unsafe_allow_html=True)
            st.markdown("""
            <div class='lp-item'><div class='lp-icon'>🚀</div>5路并发 · 极速文案清洗改写</div>
            <div class='lp-item'><div class='lp-icon'>💡</div>爆款选题 · 击穿流量焦虑</div>
            <div class='lp-item'><div class='lp-icon'>🎨</div>海报生成 · 影视级光影质感</div>
            <div class='lp-item'><div class='lp-icon'>💰</div>裂变系统 · 邀请好友免费续杯</div>
            """, unsafe_allow_html=True)
            
        with col_r:
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            t1, t2 = st.tabs(["登录", "注册"])
            with t1:
                acc = st.text_input("账号", key="l_acc", placeholder="手机号/邮箱", label_visibility="collapsed")
                pw = st.text_input("密码", key="l_pw", type="password", placeholder="密码", label_visibility="collapsed")
                st.markdown("###")
                if st.button("立即登录", type="primary", use_container_width=True):
                    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
                    c.execute("SELECT password_hash FROM users WHERE phone=?", (acc,))
                    row = c.fetchone(); conn.close()
                    if row and row[0] == hash_password(pw):
                        st.session_state['user_phone'] = acc; st.rerun()
                    else: st.error("账号或密码错误")
            with t2:
                st.info("🎁 注册即送 3 天 VIP")
                acc = st.text_input("注册账号", key="r_acc", placeholder="手机号/邮箱", label_visibility="collapsed")
                pw = st.text_input("设置密码", key="r_pw", type="password", placeholder="设置密码", label_visibility="collapsed")
                inv = st.text_input("邀请码", key="r_inv", placeholder="VIP888", label_visibility="collapsed")
                st.markdown("###")
                if st.button("立即注册", type="primary", use_container_width=True):
                    if not inv: st.error("请输入邀请码")
                    else:
                        conn = sqlite3.connect(DB_FILE); c = conn.cursor()
                        # 检查邀请码
                        valid_inv = (inv == GLOBAL_INVITE_CODE)
                        if not valid_inv:
                            c.execute("SELECT phone FROM users WHERE own_invite_code=?", (inv,))
                            if c.fetchone(): valid_inv = True
                        
                        if valid_inv:
                            try:
                                # 注册逻辑
                                my_code = generate_code()
                                c.execute("INSERT INTO users (phone, password_hash, register_time, own_invite_code) VALUES (?, ?, ?, ?)", 
                                          (acc, hash_password(pw), datetime.datetime.now(), my_code))
                                # 赠送VIP
                                now = datetime.datetime.now()
                                exp = now + datetime.timedelta(days=3)
                                c.execute("INSERT INTO access_codes (code, duration_days, activated_at, expire_at, status, create_time, bind_user) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                          (f"GIFT-{uuid.uuid4()}", 3, now, exp, 'active', now, acc))
                                conn.commit(); st.success("注册成功！"); time.sleep(1); st.session_state['user_phone'] = acc; st.rerun()
                            except: st.error("该账号已注册")
                            finally: conn.close()
                        else: st.error("无效邀请码"); conn.close()
            st.markdown('</div>', unsafe_allow_html=True)

# --- B. 首页模块 ---
def view_home():
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">抖音爆款工场 Pro</div>
        <div style="font-size:16px;color:#64748b;">让流量不再是玄学 · 专为素人 KOC 打造的 AI 变现神器</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 纯CSS卡片布局
    c1, c2, c3, c4 = st.columns(4)
    def card(icon, title, desc, key, target):
        with st.container(border=True):
            st.markdown(f"<div style='text-align:center;font-size:30px;margin-bottom:10px'>{icon}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align:center;font-weight:800;color:#1e293b'>{title}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align:center;font-size:12px;color:#64748b;margin-bottom:15px;height:40px'>{desc}</div>", unsafe_allow_html=True)
            st.button("立即使用", key=key, on_click=lambda: st.session_state.update({'nav_menu': target, 'sb_radio': target}), type="primary")

    with c1: card("📝", "文案改写", "5路并发 · 爆款重组", "h1", "📝 文案改写")
    with c2: card("💡", "爆款选题", "击穿流量焦虑", "h2", "💡 爆款选题库")
    with c3: card("🎨", "海报生成", "好莱坞级光影", "h3", "🎨 海报生成")
    with c4: card("🏷️", "账号起名", "AI 算命 · 爆款玄学", "h4", "🏷️ 账号起名")

# --- C. 文案改写模块 (Glassmorphism Restored) ---
def view_rewrite():
    st.markdown("## 📝 爆款文案改写"); st.markdown("---")
    if 'results' not in st.session_state: st.session_state['results'] = {}
    client = OpenAI(api_key=st.secrets.get("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
    
    c1, c2 = st.columns([1, 2])
    with c1:
        if st.button("🚀 5路并发执行", type="primary"):
            # 模拟并发逻辑
            for i in range(1, 6):
                val = st.session_state.get(f"in_{i}", "")
                if val: st.session_state['results'][i] = f"【爆款重写】\n{val}\n(此处应调用API，演示模式忽略)"
            st.rerun()
            
    for i in range(1, 6):
        with st.container(border=True):
            st.markdown(f"**工作台 #{i}**")
            c_in, c_out = st.columns(2)
            with c_in: 
                st.text_area("输入", key=f"in_{i}", height=150, label_visibility="collapsed", placeholder="输入原始文案...")
            with c_out:
                res = st.session_state['results'].get(i, "")
                if res:
                    st.code(res, language="text")
                    render_copy_button_html(res, f"cp_{i}")
                else:
                    st.info("等待生成...")

# --- D. 海报生成模块 (Terminal Restored) ---
def view_poster():
    st.markdown("## 🎨 海报生成 (专业版)")
    st.markdown("""<div style="background:#0f172a;padding:20px;border-radius:12px;color:white;text-align:center;margin-bottom:20px;">🚀 算力全面升级！好莱坞级光影引擎</div>""", unsafe_allow_html=True)
    
    st.info("💡 教程：复制邀请码 -> 点击跳转 -> 使用 AI 作图")
    
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown("### 1. 获取权限")
            st.markdown("邀请码：**5yzMbpxn**")
            render_copy_button_html("5yzMbpxn", "code")
    with c2:
        with st.container(border=True):
            st.markdown("### 2. 开始创作")
            st.link_button("🚀 前往小提大作", "https://aixtdz.com/", type="primary")

    # 黑客终端风格指令
    components.html("""
    <div style="background:#1e1e1e;color:#00ff00;padding:15px;border-radius:8px;font-family:monospace;">
    > root@ai-gen: 将原图剧名 [xxx] 改为 [yyy] _<br>
    <span style="color:#666">（点击上方按钮复制指令）</span>
    </div>
    """, height=100)

# --- E. 个人中心 ---
def view_account():
    st.markdown("## 👤 个人中心")
    t1, t2 = st.tabs(["🎁 邀请有礼", "💳 账户信息"])
    
    user = st.session_state['user_phone']
    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
    c.execute("SELECT own_invite_code, invite_count FROM users WHERE phone=?", (user,))
    row = c.fetchone(); conn.close()
    my_code, count = (row[0], row[1]) if row else ("ERROR", 0)

    with t1:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#fff7ed,#ffedd5);padding:30px;border-radius:16px;text-align:center;border:1px solid #fed7aa;margin-bottom:20px;">
            <h3 style="color:#9a3412;margin:0">🎉 邀请好友，免费续杯 VIP</h3>
            <p style="color:#c2410c">每成功邀请 1 人，双方各得 3 天 VIP</p>
            <div style="background:white;padding:10px 30px;border-radius:8px;display:inline-block;font-size:24px;font-weight:bold;color:#ea580c;border:2px dashed #f97316;margin:15px 0;">{my_code}</div>
            <div style="display:flex;justify-content:center;gap:40px;margin-top:20px;">
                <div><div style="font-size:20px;font-weight:bold;color:#c2410c">{count}</div><div style="font-size:12px;color:#9a3412">已邀请</div></div>
                <div><div style="font-size:20px;font-weight:bold;color:#c2410c">{count*3}</div><div style="font-size:12px;color:#9a3412">获得天数</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        render_copy_button_html(my_code, "inv_copy")

    with t2:
        is_vip, msg = get_user_vip_status(user)
        st.metric("当前账号", user)
        st.metric("会员状态", "VIP" if is_vip else "普通用户", delta=msg)
        with st.expander("🔑 激活卡密"):
            code = st.text_input("输入卡密")
            if st.button("激活"):
                conn = sqlite3.connect(DB_FILE); c = conn.cursor()
                c.execute("SELECT * FROM access_codes WHERE code=?", (code,))
                r = c.fetchone()
                if r and r[4] == 'unused':
                    now = datetime.datetime.now()
                    # 简单增加逻辑略，实际应查原过期时间
                    c.execute("UPDATE access_codes SET status='active', bind_user=? WHERE code=?", (user, code))
                    conn.commit(); st.success("激活成功！"); st.rerun()
                else: st.error("无效卡密")
                conn.close()

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
            
            st.markdown(f"""
            <div class="sidebar-user-card">
                <div class="user-left"><div class="user-avatar">👤</div><div><div class="user-name">{display}</div><div class="user-role">{'👑 VIP' if is_vip else '🌑 普通'}</div></div></div>
            </div>
            """, unsafe_allow_html=True)
            
            # 导航
            ops = ["🏠 首页", "📝 文案改写", "💡 爆款选题库", "🎨 海报生成", "🏷️ 账号起名", "👤 个人中心"]
            if st.session_state['user_phone'] == ADMIN_ACCOUNT: ops.append("🕵️‍♂️ 管理后台")
            
            # 状态同步
            if 'nav_menu' not in st.session_state: st.session_state['nav_menu'] = ops[0]
            try: idx = ops.index(st.session_state['nav_menu'])
            except: idx = 0
            
            selected = st.radio("导航", ops, index=idx, label_visibility="collapsed", key="sb_radio")
            if selected != st.session_state['nav_menu']:
                st.session_state['nav_menu'] = selected
                st.rerun()
            
            st.markdown("---")
            st.markdown("<div style='font-size:12px;font-weight:bold;color:#94a3b8;margin-bottom:5px'>🔥 热门项目</div>", unsafe_allow_html=True)
            st.markdown("""<div class="sidebar-project-card"><div class="sp-title">📹 KOC 孵化</div><div class="sp-desc">真人出镜 · 0基础陪跑</div></div>""", unsafe_allow_html=True)
            
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            render_wechat_box("🎁 领取资料", "W7774X")
            st.markdown("<div style='height:5px'></div>", unsafe_allow_html=True)
            render_wechat_box("🛠️ 技术合作", "TG777188")
            
            st.markdown("---")
            if st.button("🚪 退出", type="secondary"):
                del st.session_state['user_phone']
                st.rerun()

        # 页面路由
        menu = st.session_state['nav_menu']
        if menu == "🏠 首页": view_home()
        elif menu == "📝 文案改写": view_rewrite()
        elif menu == "🎨 海报生成": view_poster()
        elif menu == "👤 个人中心": view_account()
        else: st.info(f"🚧 {menu} 功能升级中...")
        
        render_footer()

if __name__ == "__main__":
    main()
