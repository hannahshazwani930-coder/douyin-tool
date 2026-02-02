import streamlit as st
from openai import OpenAI
import time
from concurrent.futures import ThreadPoolExecutor
import streamlit.components.v1 as components 
import sqlite3
import datetime
import uuid

# ==========================================
# 0. 核心配置 & 数据库初始化
# ==========================================
st.set_page_config(
    page_title="抖音爆款工场 Pro", 
    layout="wide",
    page_icon="💠",
    initial_sidebar_state="expanded"
)

# --- 数据库操作函数 ---
DB_FILE = 'users.db'

def init_db():
    """初始化数据库表"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # 创建卡密表
    c.execute('''CREATE TABLE IF NOT EXISTS access_codes
                 (code TEXT PRIMARY KEY, 
                  duration_days INTEGER, 
                  activated_at TIMESTAMP, 
                  expire_at TIMESTAMP,
                  status TEXT)''') # status: 'unused', 'active', 'expired'
    conn.commit()
    conn.close()

# 初始化数据库
init_db()

def check_code(code):
    """验证卡密逻辑"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM access_codes WHERE code=?", (code,))
    row = c.fetchone()
    
    if not row:
        conn.close()
        return False, "❌ 卡密不存在，请检查输入"
    
    duration = row[1]
    activated_at = row[2]
    expire_at = row[3]
    status = row[4]
    
    now = datetime.datetime.now()
    
    # 情况1: 新卡未激活 -> 立即激活
    if status == 'unused':
        expire_date = now + datetime.timedelta(days=duration)
        c.execute("UPDATE access_codes SET status='active', activated_at=?, expire_at=? WHERE code=?", 
                  (now, expire_date, code))
        conn.commit()
        conn.close()
        return True, f"✅ 激活成功！有效期至：{expire_date.strftime('%Y-%m-%d')}"
    
    # 情况2: 已激活 -> 检查是否过期
    elif status == 'active':
        expire_date = datetime.datetime.strptime(str(expire_at).split('.')[0], '%Y-%m-%d %H:%M:%S')
        if now > expire_date:
            c.execute("UPDATE access_codes SET status='expired' WHERE code=?", (code,))
            conn.commit()
            conn.close()
            return False, "⛔ 卡密已过期，请购买新卡"
        else:
            days_left = (expire_date - now).days
            conn.close()
            return True, f"✅ 验证通过 (剩余 {days_left} 天)"
            
    # 情况3: 已过期
    else:
        conn.close()
        return False, "⛔ 卡密已过期"

# --- 临时：生成测试卡密的功能 (仅供管理员使用) ---
# 实际上线后，你可以写一个单独的脚本生成卡密，然后手动插入数据库
def generate_admin_codes(days=30, count=1):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    new_codes = []
    for _ in range(count):
        code = "VIP-" + str(uuid.uuid4())[:8].upper()
        c.execute("INSERT INTO access_codes (code, duration_days, status) VALUES (?, ?, ?)", (code, days, 'unused'))
        new_codes.append(code)
    conn.commit()
    conn.close()
    return new_codes

# 注入 CSS：全局样式 + 悬浮复制优化
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    .stApp { font-family: 'Inter', sans-serif; background-color: #f8fafc; }
    div.block-container { max-width: 90% !important; min-width: 90% !important; background-color: #ffffff; padding: 3rem !important; margin: 2rem auto !important; border-radius: 16px; box-shadow: 0 10px 40px -10px rgba(0,0,0,0.05); }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #f1f5f9; }
    [data-testid="stVerticalBlockBorderWrapper"] { background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 24px; transition: all 0.3s ease; }
    [data-testid="stVerticalBlockBorderWrapper"]:hover { border-color: #cbd5e1; box-shadow: 0 4px 12px rgba(0,0,0,0.03); }
    h1 { color: #0f172a !important; font-weight: 800 !important; margin-bottom: 1.5rem !important; }
    .stMarkdown p, label { color: #475569 !important; }
    
    /* 按钮美化 */
    div.stButton > button { border-radius: 8px; font-weight: 600; height: 40px; transition: all 0.2s; }
    div.stButton > button:not([kind="primary"]) { background-color: #f1f5f9; color: #475569 !important; border: 1px solid transparent; }
    div.stButton > button:not([kind="primary"]):hover { background-color: #e0f2fe; color: #0284c7 !important; border-color: #bae6fd; }
    div.stButton > button[kind="primary"] { background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3); border: none; color: #ffffff !important; }
    div.stButton > button[kind="primary"]:hover { box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4); transform: translateY(-1px); }
    
    /* 输入框 */
    .stTextArea textarea, .stTextInput input { border-radius: 8px; border: 1px solid #cbd5e1; background-color: #f8fafc !important; color: #1e293b !important; caret-color: #2563eb; font-weight: 500; }
    .stTextArea textarea:focus, .stTextInput input:focus { background-color: #ffffff !important; border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15); }
    
    /* 商业化侧边栏卡片 */
    .project-box { background-color: #f0f9ff; border: 1px solid #bae6fd; padding: 12px; border-radius: 8px; margin-bottom: 10px; }
    .project-title { font-weight: bold; color: #0369a1; font-size: 14px; }
    .project-desc { font-size: 12px; color: #334155; margin-top: 4px; }
    
    /* 微信联系方式样式 */
    .wechat-contact { margin-top: 20px; padding-top: 15px; border-top: 1px solid #e2e8f0; }
    .wechat-item { display: flex; align-items: center; justify-content: space-between; font-size: 13px; color: #475569; margin-bottom: 8px; }
    .wechat-label { font-weight: 600; }
    
    .login-spacer { height: 10vh; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# ⚡ 核心功能：前端 JS 复制组件
# ==========================================
def render_hover_copy_box(text, label="点击复制"):
    safe_text = text.replace("`", "\`").replace("${", "\${").replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;600&display=swap');
            body {{ margin: 0; padding: 0; background: transparent; font-family: 'Inter', sans-serif; overflow: hidden; }}
            .code-box {{ display: flex; align-items: center; justify-content: space-between; background-color: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 0 10px; height: 36px; cursor: pointer; transition: all 0.2s ease; color: #1e293b; font-weight: 600; font-size: 13px; box-sizing: border-box; }}
            .code-box:hover {{ border-color: #3b82f6; background-color: #ffffff; box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1); }}
            .hint {{ font-size: 12px; color: #94a3b8; font-weight: 400; }}
            .code-box:hover .hint {{ color: #3b82f6; }}
            .code-box.success {{ background-color: #ecfdf5; border-color: #10b981; color: #065f46; }}
            .code-box.success .hint {{ color: #059669; }}
        </style>
    </head>
    <body>
        <div class="code-box" onclick="copyText(this)">
            <span id="code-content">{safe_text}</span>
            <span class="hint" id="status-text">{label}</span>
        </div>
        <script>
            function copyText(box) {{
                const text = `{safe_text}`;
                const statusText = box.querySelector("#status-text");
                if (navigator.clipboard && window.isSecureContext) {{ navigator.clipboard.writeText(text).then(() => {{ showSuccess(box, statusText); }}).catch(err => {{ fallbackCopyText(text, box, statusText); }}); }} else {{ fallbackCopyText(text, box, statusText); }}
            }}
            function fallbackCopyText(text, box, statusText) {{
                const textArea = document.createElement("textarea"); textArea.value = text; textArea.style.position = "fixed"; textArea.style.left = "-9999px"; document.body.appendChild(textArea); textArea.focus(); textArea.select();
                try {{ const successful = document.execCommand('copy'); if (successful) showSuccess(box, statusText); }} catch (err) {{ statusText.innerText = "❌"; }} document.body.removeChild(textArea);
            }}
            function showSuccess(box, statusText) {{
                box.classList.add("success"); const originalHint = "{label}"; statusText.innerText = "✅ 成功";
                setTimeout(() => {{ box.classList.remove("success"); statusText.innerText = originalHint; }}, 1500);
            }}
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=40)

# ==========================================
# 1. 登录与安全系统 (使用数据库卡密)
# ==========================================

@st.cache_resource
def get_login_cache(): return {}

def get_remote_ip():
    try:
        from streamlit.web.server.websocket_headers import _get_websocket_headers
        headers = _get_websocket_headers()
        return headers.get("X-Forwarded-For", headers.get("Remote-Addr", "unknown_ip"))
    except: return "unknown_ip"

def check_login():
    if st.session_state.get('is_logged_in', False): return True
    
    # 自动登录逻辑 (IP缓存) - 商业版建议关闭IP缓存或缩短时间，防止共享
    # 这里为了用户体验保留，但每次刷新都会检查DB中的过期时间
    
    login_placeholder = st.empty()
    with login_placeholder.container():
        st.markdown("<div class='login-spacer'></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 1.5, 1])
        with c2:
            st.markdown("<h2 style='text-align: center; margin-bottom: 20px;'>💠 爆款工场 Pro</h2>", unsafe_allow_html=True)
            st.info("🔒 商业授权系统 | 请输入月卡/季卡卡密", icon="🔑")
            
            with st.form("login_form"):
                user_code = st.text_input("请输入卡密 (Access Code)", placeholder="例如：VIP-XXXXXXXX", type="password")
                st.markdown("<br>", unsafe_allow_html=True)
                submitted = st.form_submit_button("🚀 立即激活/登录", type="primary", use_container_width=True)
            
            if submitted:
                valid, msg = check_code(user_code.strip())
                if valid:
                    st.session_state['is_logged_in'] = True 
                    st.session_state['user_code'] = user_code.strip()
                    st.session_state['login_msg'] = msg
                    st.success(msg)
                    time.sleep(1)
                    login_placeholder.empty()
                    st.rerun()
                else:
                    st.error(msg)
            
            # 临时生成测试卡密 (仅限演示，正式上线请删除)
            if st.checkbox("我是管理员 (生成测试卡密)"):
                if st.button("生成一个30天卡密"):
                    codes = generate_admin_codes(30, 1)
                    st.code(codes[0], language='text')
                    st.success("已生成并写入数据库，请复制上方卡密登录")

    return False

if not check_login(): st.stop()

# ==========================================
# 2. API 配置
# ==========================================
try:
    api_key = st.secrets["DEEPSEEK_API_KEY"]
except:
    st.error("❌ 未检测到 DEEPSEEK_API_KEY，请在后台 Secrets 中配置。")
    st.stop()

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# ==========================================
# 3. 功能模块 (UI略，保持之前的功能)
# ==========================================
# (为节省篇幅，这里复用你之前的业务逻辑代码，只展示修改了的部分：侧边栏和海报导流)

# --- A. 文案改写 ---
def page_rewrite():
    st.markdown("## ⚡ 爆款文案改写中台")
    st.caption("AI 驱动的五路并发架构 | 40秒黄金完播率模型")
    st.markdown("---")
    # ... (此处代码逻辑保持不变，为了篇幅省略，请确保复制之前的完整逻辑) ...
    # 简单占位符供演示
    st.info("💡 指南：粘贴文案到下方窗口，点击一键执行。")
    st.text_area("文案输入", height=100)
    st.button("🚀 开始改写", type="primary")

# --- D. 选题灵感库 ---
def page_brainstorm():
    st.markdown("## 💡 爆款选题灵感库")
    st.write("... (功能保持不变) ...")

# --- E. 海报生成 (导流 + 教程) ---
def page_poster_gen():
    st.markdown("## 🎨 AI 智能海报改图 (专业版)")
    st.info("💡 提示：海报改图功能已升级至 **小提大作 独立站**。")
    with st.container(border=True):
        st.markdown("### 🚀 前往 小提大作 专业版控制台")
        c1, c2 = st.columns([1, 1.5], gap="large")
        with c1:
            st.markdown("##### 第 1 步：复制专属邀请码")
            st.caption("注册时填写，可获赠额外算力")
            render_hover_copy_box("5yzMbpxn", "点击复制")
        with c2:
            st.markdown("##### 第 2 步：前往生成")
            st.caption("点击下方按钮跳转")
            st.markdown("""<a href="https://aixtdz.com/" target="_blank" style="display:flex;align-items:center;justify-content:center;width:100%;height:52px;background:linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);color:white!important;border-radius:8px;text-decoration:none;font-weight:700;box-shadow:0 4px 15px rgba(139,92,246,0.3);">🚀 立即前往 小提大作</a>""", unsafe_allow_html=True)

# --- F. 个人中心 (显示有效期) ---
def page_account():
    st.markdown("## 👤 我的账户")
    st.markdown("---")
    
    # 获取当前卡密信息
    valid, msg = check_code(st.session_state.get('user_code'))
    
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.metric("会员状态", "VIP 正式版", delta="生效中" if valid else "已过期")
            st.text_input("当前卡密", value=st.session_state.get('user_code'), disabled=True)
            st.caption(msg) # 显示剩余天数
    with col2:
        with st.container(border=True):
            st.markdown("#### 💬 联系客服")
            st.markdown("遇到问题？请截图当前页面联系技术支持。")

# ==========================================
# 4. 侧边栏导航 (修改重点)
# ==========================================

with st.sidebar:
    st.markdown("### 💠 爆款工场 Pro")
    
    # 显示登录状态
    if st.session_state.get('is_logged_in'):
        valid, msg = check_code(st.session_state.get('user_code'))
        if valid:
            st.success(msg) # 显示：剩余 XX 天
        else:
            st.error("卡密已失效")
            
    st.markdown("---")
    
    # 🔥 核心引流广告位 🔥
    st.markdown("#### 🔥 热门搞钱项目")
    st.markdown("""
    <div class="project-box">
        <div class="project-title">📹 素人 KOC 孵化</div>
        <div class="project-desc">真人出镜口播，红果/番茄拉新，0基础陪跑。</div>
    </div>
    <div class="project-box">
        <div class="project-title">🎨 御灵 AI 动漫</div>
        <div class="project-desc">小说转动漫视频，端原生+版权分销，高收益。</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 👇 修改 1 & 2：更新联系方式 & 增加技术微信 👇
    st.markdown("<div class='wechat-contact'>", unsafe_allow_html=True)
    
    st.markdown("<div class='wechat-item'><span class='wechat-label'>💼 营销咨询:</span></div>", unsafe_allow_html=True)
    render_hover_copy_box("W7774X", "点击复制微信号")
    
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True) # 间距
    
    st.markdown("<div class='wechat-item'><span class='wechat-label'>🛠️ 技术/合作:</span></div>", unsafe_allow_html=True)
    render_hover_copy_box("TG777188", "点击复制微信号")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    menu_option = st.radio("功能导航", ["📝 文案改写", "💡 爆款选题库", "🎨 海报生成", "👤 我的账户"], index=0, label_visibility="collapsed")

if menu_option == "📝 文案改写": page_rewrite()
elif menu_option == "💡 爆款选题库": page_brainstorm()
elif menu_option == "🎨 海报生成": page_poster_gen()
elif menu_option == "👤 我的账户": page_account()
