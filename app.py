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
DB_FILE = 'saas_data.db'

# --- 数据库初始化 ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # 1. 用户表
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (phone TEXT PRIMARY KEY, password_hash TEXT, register_time TIMESTAMP,
                  last_login_ip TEXT, last_login_time TIMESTAMP)''')
                  
    # 2. 卡密表
    c.execute('''CREATE TABLE IF NOT EXISTS access_codes
                 (code TEXT PRIMARY KEY, duration_days INTEGER, activated_at TIMESTAMP, 
                  expire_at TIMESTAMP, status TEXT, create_time TIMESTAMP, bind_user TEXT)''')
    
    # 3. 反馈表
    c.execute('''CREATE TABLE IF NOT EXISTS feedbacks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, user_phone TEXT, content TEXT, 
                  reply TEXT, create_time TIMESTAMP, status TEXT)''')
                  
    # 4. 🔥 新增：系统设置表 (用于动态存储店铺链接等) 🔥
    c.execute('''CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)''')
    
    # 预设管理员
    c.execute("SELECT phone FROM users WHERE phone=?", (ADMIN_PHONE,))
    if not c.fetchone():
        c.execute("INSERT INTO users (phone, password_hash, register_time) VALUES (?, ?, ?)", 
                  (ADMIN_PHONE, hashlib.sha256(ADMIN_INIT_PASSWORD.encode()).hexdigest(), datetime.datetime.now()))
    
    # 预设默认店铺链接
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ("shop_url", "https://www.taobao.com")) # 默认占位
        
    conn.commit(); conn.close()

init_db()

# --- 工具函数 ---
def get_setting(key):
    """获取系统设置"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT value FROM settings WHERE key=?", (key,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else ""

def update_setting(key, value):
    """更新系统设置"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
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

# --- 业务逻辑 ---
def register_user(phone, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (phone, password_hash, register_time) VALUES (?, ?, ?)", 
                  (phone, hash_password(password), datetime.datetime.now()))
        conn.commit(); return True, "注册成功"
    except sqlite3.IntegrityError: return False, "该手机号已注册"
    finally: conn.close()

def login_user(phone, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE phone=?", (phone,))
    row = c.fetchone()
    conn.close()
    if row and row[0] == hash_password(password):
        # 更新 IP
        conn = sqlite3.connect(DB_FILE); c = conn.cursor()
        c.execute("UPDATE users SET last_login_ip=?, last_login_time=? WHERE phone=?", (get_remote_ip(), datetime.datetime.now(), phone))
        conn.commit(); conn.close()
        return True, "登录成功"
    return False, "手机号或密码错误"

def reset_password(phone, new_password):
    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
    c.execute("UPDATE users SET password_hash=? WHERE phone=?", (hash_password(new_password), phone))
    success = c.rowcount > 0
    conn.commit(); conn.close()
    return (True, "重置成功") if success else (False, "用户不存在")

def check_ip_auto_login():
    ip = get_remote_ip()
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
        duration = row[1]
        now = datetime.datetime.now()
        expire_date = now + datetime.timedelta(days=duration)
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
        return True, f"VIP 有效期至：{max_expire.strftime('%Y-%m-%d')} (剩余 {(max_expire - now).days} 天)"
    return False, "会员已过期"

def submit_feedback(phone, content):
    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
    c.execute("INSERT INTO feedbacks (user_phone, content, create_time, status) VALUES (?, ?, ?, ?)", (phone, content, datetime.datetime.now(), 'pending'))
    conn.commit(); conn.close()

# --- CSS 样式 ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    .stApp { font-family: 'Inter', sans-serif; background-color: #f8fafc; }
    
    /* 容器 */
    div.block-container { max-width: 90% !important; background-color: #ffffff; padding: 3rem !important; border-radius: 16px; box-shadow: 0 10px 40px -10px rgba(0,0,0,0.05); margin-bottom: 50px; }
    
    /* 按钮 */
    div.stButton > button { border-radius: 8px; font-weight: 600; height: 45px; transition: all 0.2s; }
    div.stButton > button[kind="primary"] { background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); border: none; color: white !important; }
    div.stButton > button[kind="primary"]:hover { transform: translateY(-2px); box-shadow: 0 6px 15px rgba(37, 99, 235, 0.3); }
    
    /* 底部版权栏 */
    .footer-legal {
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #e2e8f0;
        text-align: center;
        color: #94a3b8;
        font-size: 12px;
    }
    .footer-links a { color: #64748b; text-decoration: none; margin: 0 10px; transition: color 0.2s; }
    .footer-links a:hover { color: #2563eb; }
    
    /* 首页卡片 */
    .home-card {
        background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px;
        text-align: center; transition: all 0.3s; height: 100%; cursor: default;
    }
    .home-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.05); border-color: #bfdbfe; }
    .home-icon { font-size: 40px; margin-bottom: 10px; display: block; }
    .home-title { font-weight: 700; color: #1e293b; font-size: 16px; margin-bottom: 5px; }
    .home-desc { font-size: 13px; color: #64748b; }

    /* 商业化组件 */
    .project-box { background-color: #f0f9ff; border: 1px solid #bae6fd; padding: 12px; border-radius: 8px; margin-bottom: 10px; }
    .wechat-item { display: flex; align-items: center; justify-content: space-between; font-size: 13px; color: #475569; margin-bottom: 8px; }
    
    /* 认证页 */
    .auth-title { text-align: center; font-weight: 800; font-size: 24px; color: #1e293b; margin-bottom: 20px; }
    .login-spacer { height: 5vh; }
    
    .info-box-aligned { height: 50px !important; background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; color: #1e40af; display: flex; align-items: center; padding: 0 16px; font-size: 14px; font-weight: 500; width: 100%; box-sizing: border-box; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. 认证模块
# ==========================================
if 'user_phone' not in st.session_state:
    auto = check_ip_auto_login()
    if auto:
        st.session_state['user_phone'] = auto
        st.toast(f"欢迎回来 {auto}", icon="👋"); time.sleep(0.5); st.rerun()

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
            with t3:
                # 找回密码逻辑 (简略)
                st.info("请联系客服重置密码")

if 'user_phone' not in st.session_state:
    auth_page(); st.stop()

CURRENT_USER = st.session_state['user_phone']
IS_ADMIN = (CURRENT_USER == ADMIN_PHONE)
IS_VIP, VIP_MSG = get_user_vip_status(CURRENT_USER)

# --- 辅助组件 ---
def render_hover_copy_box(text, label="点击复制"):
    safe = text.replace("`", "\`").replace("'", "\\'")
    html = f"""<!DOCTYPE html><html><head><style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;600&display=swap');body{{margin:0;padding:0;background:transparent;overflow:hidden;font-family:'Inter';}}.code-box{{display:flex;align-items:center;justify-content:space-between;background-color:#f8fafc;border:1px solid #cbd5e1;border-radius:6px;padding:0 10px;height:36px;cursor:pointer;transition:all 0.2s;color:#1e293b;font-weight:600;font-size:13px;box-sizing:border-box;}}.code-box:hover{{border-color:#3b82f6;background:#fff;box-shadow:0 0 0 2px rgba(59,130,246,0.1);}}.hint{{font-size:12px;color:#94a3b8;}}.code-box:hover .hint{{color:#3b82f6;}}.code-box.success{{background:#ecfdf5;border-color:#10b981;color:#065f46;}}.code-box.success .hint{{color:#059669;}}</style></head><body><div class="code-box" onclick="copyText(this)"><span id="content">{safe}</span><span class="hint" id="status">{label}</span></div><script>function copyText(e){{const t=`{safe}`,s=e.querySelector("#status");navigator.clipboard.writeText(t).then(()=>{{e.classList.add("success");const o=s.innerText;s.innerText="✅";setTimeout(()=>{{e.classList.remove("success");s.innerText=o}},1500)}}).catch(()=>{{s.innerText="❌"}})}}</script></body></html>"""
    components.html(html, height=40)

def render_copy_button_html(text, k):
    safe = text.replace("`", "\`").replace("'", "\\'")
    html = f"""<!DOCTYPE html><html><head><style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@600&display=swap');body{{margin:0;padding:0;background:transparent;overflow:hidden;}}.btn{{width:100%;height:42px;background:linear-gradient(135deg,#2563eb,#1d4ed8);color:#fff;border:none;border-radius:8px;font-family:'Inter';font-weight:600;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all 0.2s;}}.btn:hover{{transform:translateY(-1px);box-shadow:0 6px 16px rgba(37,99,235,0.4);}}.btn:active{{transform:translateY(0);}}.btn.ok{{background:linear-gradient(135deg,#10b981,#059669);}}</style></head><body><button class="btn" onclick="cp(this)">📋 一键复制</button><script>function cp(e){{navigator.clipboard.writeText(`{safe}`).then(()=>{{e.classList.add("ok");e.innerText="✅ 成功";setTimeout(()=>{{e.classList.remove("ok");e.innerText="📋 一键复制"}},2000)}})}}</script></body></html>"""
    components.html(html, height=50)

def render_footer():
    st.markdown("""
    <div class="footer-legal">
        <div class="footer-links">
            <a href="#">用户协议</a> | <a href="#">隐私政策</a> | <a href="#">免责声明</a> | <a href="#">关于我们</a>
        </div>
        <div style="margin-top: 10px;">
            © 2024 爆款工场 Pro | 鄂ICP备2024XXXXXX号-1 | 违法和不良信息举报：TG777188
        </div>
        <div style="font-size: 11px; color: #cbd5e1; margin-top: 5px;">
            本站仅提供技术工具，请勿用于任何非法用途，用户生成内容文责自负。
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 侧边栏 ---
with st.sidebar:
    st.markdown(f"### 👋 Hi, {CURRENT_USER}")
    if IS_VIP: st.success(VIP_MSG)
    else:
        st.error("⚠️ 未激活会员")
        with st.expander("🔑 激活卡密", expanded=True):
            c = st.text_input("输入卡密", type="password", key="side_cd")
            if st.button("激活"):
                s, m = activate_code(CURRENT_USER, c)
                if s: st.success(m); time.sleep(1); st.rerun()
                else: st.error(m)
    
    st.markdown("---")
    st.markdown("#### 🔥 热门项目")
    st.markdown("""<div class="project-box"><div class="project-title">📹 素人 KOC 孵化</div><div class="project-desc">真人出镜口播，红果/番茄拉新，0基础陪跑。</div></div><div class="project-box"><div class="project-title">🎨 御灵 AI 动漫</div><div class="project-desc">小说转动漫视频，端原生+版权分销。</div></div>""", unsafe_allow_html=True)
    
    st.markdown("<div style='font-size:12px;color:#64748b;margin-bottom:5px'>💼 <b>项目咨询:</b></div>", unsafe_allow_html=True)
    render_hover_copy_box("W7774X", "点击复制")
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:12px;color:#64748b;margin-bottom:5px'>🛠️ <b>技术合作:</b></div>", unsafe_allow_html=True)
    render_hover_copy_box("TG777188", "点击复制")
    
    st.markdown("---")
    st.info("💡 想要新功能？\n请前往 **[👤 个人中心]** 提交反馈")
    
    ops = ["🏠 首页", "📝 文案改写", "💡 爆款选题库", "🎨 海报生成", "🏷️ 账号起名", "👤 个人中心"]
    if IS_ADMIN: ops.append("🕵️‍♂️ 管理后台")
    menu = st.radio("导航", ops, index=0, label_visibility="collapsed")
    
    st.markdown("---")
    if st.button("🚪 退出"): del st.session_state['user_phone']; st.rerun()

# --- 首页 ---
def page_home():
    st.markdown("## 💠 抖音爆款工场 Pro")
    st.caption("专为素人 KOC 打造的 AI 提效神器 | 文案 · 选题 · 海报 · 变现")
    st.markdown("---")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown("<div class='home-card'><span class='home-icon'>📝</span><div class='home-title'>文案改写</div><div class='home-desc'>5路并发，爆款逻辑重组</div></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='home-card'><span class='home-icon'>💡</span><div class='home-title'>爆款选题</div><div class='home-desc'>解决流量焦虑，日更不断</div></div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='home-card'><span class='home-icon'>🎨</span><div class='home-title'>海报生成</div><div class='home-desc'>对接小提大作，好莱坞级质感</div></div>", unsafe_allow_html=True)
    with c4: st.markdown("<div class='home-card'><span class='home-icon'>💰</span><div class='home-title'>变现陪跑</div><div class='home-desc'>KOC/御灵AI 项目实操SOP</div></div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("#### 📢 系统公告")
        st.info("🎉 欢迎使用 Pro 版！如需开通会员，请联系侧边栏客服获取卡密。", icon="👋")
        st.write("2026-02-03: 新增【海报改图教程】，优化移动端体验。")

# --- 文案 ---
def page_rewrite():
    st.markdown("## 📝 爆款文案改写"); st.markdown("---")
    client = OpenAI(api_key=st.secrets.get("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
    def run_ai(txt):
        try: return client.chat.completions.create(model="deepseek-chat", messages=[{"role":"user","content":f"改写文案：{txt}"}]).choices[0].message.content
        except: return "请配置 API Key"
    
    c1, c2 = st.columns([1, 2])
    with c1:
        if st.button("🚀 5路并发执行", type="primary", use_container_width=True):
            tasks = [st.session_state.get(f"in_{i}","") for i in range(1,6) if st.session_state.get(f"in_{i}","").strip()]
            if tasks:
                with st.status("生成中..."):
                    with ThreadPoolExecutor(5) as ex: res = list(ex.map(run_ai, tasks))
                    for i, r in enumerate(res): st.session_state[f"res_{i+1}"] = r
                    st.rerun()
    with c2: st.markdown("""<div class="info-box-aligned">💡 提示：左侧输入，点击蓝色按钮批量处理。</div>""", unsafe_allow_html=True)
    
    st.write("")
    for i in range(1, 6):
        with st.container(border=True):
            st.markdown(f"**工作台 #{i}**")
            cc1, cc2 = st.columns(2)
            cc1.text_area("输入", height=120, key=f"in_{i}", label_visibility="collapsed")
            res = st.session_state.get(f"res_{i}", "")
            if res: 
                cc2.text_area("结果", value=res, height=120, label_visibility="collapsed")
                with cc2: render_copy_button_html(res, f"cp_{i}")
            else: cc2.markdown("<div style='color:#ccc;text-align:center;line-height:120px'>等待生成...</div>", unsafe_allow_html=True)

# --- 海报 ---
def page_poster():
    st.markdown("## 🎨 海报生成 (专业版)")
    st.info("💡 算力升级：已接入 **小提大作** 独立站，请前往该站操作。")
    with st.container(border=True):
        c1, c2 = st.columns([1, 1.5], gap="large")
        with c1: st.markdown("##### 1. 复制专属邀请码"); render_hover_copy_box("5yzMbpxn", "点击复制")
        with c2: st.markdown("##### 2. 前往生成"); st.markdown("""<a href="https://aixtdz.com/" target="_blank" class="redirect-btn">🚀 跳转小提大作</a>""", unsafe_allow_html=True)
    st.markdown("#### 📖 操作教程")
    st.code("图生图 -> 上传原图 -> 输入：将剧名[原名]改为[新名]", language="text")

# --- 个人中心 ---
def page_account():
    st.markdown("## 👤 个人中心"); st.markdown("---")
    t1, t2 = st.tabs(["💳 账户", "💬 反馈"])
    with t1:
        st.metric("账号", CURRENT_USER)
        st.metric("状态", "VIP" if IS_VIP else "普通用户", delta=VIP_MSG)
        # 动态获取店铺链接
        shop_url = get_setting("shop_url")
        if shop_url:
            st.markdown(f"""<a href="{shop_url}" target="_blank" style="display:block;text-align:center;background:#10b981;color:white;padding:12px;border-radius:8px;text-decoration:none;font-weight:bold;margin:10px 0">💳 在线购买/续费卡密</a>""", unsafe_allow_html=True)
        
        st.write("#### 激活卡密")
        c = st.text_input("卡密", placeholder="VIP-xxxxx")
        if st.button("立即激活", type="primary"):
            s, m = activate_code(CURRENT_USER, c)
            if s: st.success(m); time.sleep(1); st.rerun()
            else: st.error(m)
    with t2:
        txt = st.text_area("请输入您的建议...")
        if st.button("提交"): 
            submit_feedback(CURRENT_USER, txt); st.success("已提交！")
        
        # 历史
        conn = sqlite3.connect(DB_FILE); c = conn.cursor()
        c.execute("SELECT content, reply, create_time FROM feedbacks WHERE user_phone=? ORDER BY create_time DESC", (CURRENT_USER,))
        rows = c.fetchall(); conn.close()
        for c, r, t in rows:
            with st.container(border=True):
                st.caption(f"📅 {t}")
                st.write(f"**我**: {c}")
                if r: st.write(f"**回复**: :green[{r}]")

# --- 管理后台 ---
def page_admin():
    st.markdown("## 🕵️‍♂️ 管理后台")
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
                conn.commit(); conn.close()
                st.success(f"已生成 {q} 个")
            
            # 下载
            conn = sqlite3.connect(DB_FILE)
            df = pd.read_sql("SELECT * FROM access_codes ORDER BY create_time DESC", conn)
            st.dataframe(df, height=300)
            st.download_button("下载 CSV", df.to_csv(index=False).encode('utf-8'), "codes.csv", "text/csv")
            conn.close()
        with t3:
            conn = sqlite3.connect(DB_FILE)
            pending = pd.read_sql("SELECT * FROM feedbacks WHERE status='pending'", conn)
            conn.close()
            for i, r in pending.iterrows():
                with st.container(border=True):
                    st.write(f"用户: {r['user_phone']} | 内容: {r['content']}")
                    reply = st.text_input("回复", key=f"rep_{r['id']}")
                    if st.button("发送", key=f"send_{r['id']}"):
                        conn = sqlite3.connect(DB_FILE); c = conn.cursor()
                        c.execute("UPDATE feedbacks SET reply=?, status='replied' WHERE id=?", (reply, r['id']))
                        conn.commit(); conn.close(); st.rerun()

# --- 路由 ---
if not IS_VIP and menu != "🏠 首页" and menu != "👤 个人中心" and menu != "🕵️‍♂️ 管理后台":
    st.warning("⚠️ 会员功能，请先激活"); st.stop()

if menu == "🏠 首页": page_home()
elif menu == "📝 文案改写": page_rewrite()
elif menu == "🎨 海报生成": page_poster()
elif menu == "👤 个人中心": page_account()
elif menu == "🕵️‍♂️ 管理后台": page_admin()
else: st.info("功能开发中...")

render_footer()
