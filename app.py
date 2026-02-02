import streamlit as st
from openai import OpenAI
import time
from concurrent.futures import ThreadPoolExecutor 

# ==========================================
# 🎨 0. 企业级 UI/UX 配置 (核心美化)
# ==========================================
st.set_page_config(
    page_title="抖音爆款工场 Pro", 
    layout="wide",  # 先设为 wide，然后用 CSS 往回收
    page_icon="💠",
    initial_sidebar_state="expanded"
)

# 注入 CSS：黄金比例布局 + 现代化 SaaS 风格
st.markdown("""
<style>
    /* 1. 全局字体与背景优化 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    .stApp {
        font-family: 'Inter', 'PingFang SC', 'Helvetica Neue', sans-serif;
        background-color: #f8f9fa; /* 极淡的灰白底色，比纯白更护眼 */
    }

    /* 2. 黄金比例布局控制 (关键) */
    /* 强制将主内容区限制在黄金宽度 (约1200px)，并居中 */
    [data-testid="stAppViewContainer"] > .main > .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 5rem;
        margin-left: auto;
        margin-right: auto;
    }

    /* 3. 侧边栏美化 */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #eaeaea;
        box-shadow: 2px 0 10px rgba(0,0,0,0.02);
    }
    
    /* 4. 卡片容器：悬浮感设计 */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff;
        border: 1px solid #eeeeee;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03); /* 高级微阴影 */
        padding: 24px;
        transition: transform 0.2s ease;
    }
    
    /* 5. 标题与排版 */
    h1 {
        font-weight: 800 !important;
        background: -webkit-linear-gradient(45deg, #2C3E50, #4CA1AF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
    }
    h2, h3 { color: #34495e; font-weight: 700 !important; }
    
    /* 6. 按钮交互动效 */
    div.stButton > button {
        border-radius: 8px;
        border: none;
        font-weight: 600;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: all 0.2s;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.15);
    }
    /* 主按钮特殊样式 */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
    }

    /* 7. 输入框美化 */
    .stTextArea textarea, .stTextInput input {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        background-color: #fcfcfc;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #4b6cb7;
        box-shadow: 0 0 0 2px rgba(75, 108, 183, 0.2);
    }

    /* 8. 登录页特殊处理 */
    .login-container {
        margin-top: 10vh;
    }
    
    /* 暗黑模式适配 (自动检测) */
    @media (prefers-color-scheme: dark) {
        .stApp { background-color: #121212; }
        [data-testid="stSidebar"] { background-color: #1a1a1a; border-right: 1px solid #333; }
        [data-testid="stVerticalBlockBorderWrapper"] { 
            background-color: #1e1e1e; 
            border: 1px solid #333; 
        }
        h1 { -webkit-text-fill-color: #e0e0e0; }
        h2, h3 { color: #d0d0d0; }
        .stTextArea textarea, .stTextInput input {
            background-color: #2d2d2d;
            border-color: #444;
            color: white;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🔐 1. 登录与安全系统 (深度检测逻辑)
# ==========================================

PASSWORD = "taoge888"

# 回调函数：用于安全清空状态
def clear_text_callback(key):
    if key in st.session_state:
        st.session_state[key] = ""

@st.cache_resource
def get_login_cache():
    return {}

def get_remote_ip():
    try:
        from streamlit.web.server.websocket_headers import _get_websocket_headers
        headers = _get_websocket_headers()
        return headers.get("X-Forwarded-For", headers.get("Remote-Addr", "unknown_ip"))
    except:
        return "unknown_ip"

def check_login():
    # 1. 优先检查本地 Session 状态
    if st.session_state.get('is_logged_in', False):
        return True

    user_ip = get_remote_ip()
    current_time = time.time()
    login_cache = get_login_cache()
    
    # 2. 检查 IP 缓存 (48小时免密)
    if user_ip in login_cache and (current_time - login_cache[user_ip] < 172800):
        st.session_state['is_logged_in'] = True 
        return True 
        
    # --- 登录界面 (居中卡片式设计) ---
    login_placeholder = st.empty()
    
    with login_placeholder.container():
        # 强制空行，让登录框视觉居中
        st.markdown("<div class='login-container'></div>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1, 1.2, 1]) # 黄金比例挤压中间列
        with c2:
            with st.container(border=True):
                st.markdown("<h2 style='text-align: center; margin-bottom: 20px;'>💠 爆款工场 Pro</h2>", unsafe_allow_html=True)
                st.info("🔒 系统已加密，获取密码请联系微信：TG777188", icon="🔑")
                
                with st.form("login_form"):
                    pwd = st.text_input("请输入会员密码", type="password", placeholder="******")
                    # 使用 type="primary" 触发 CSS 中的渐变色
                    submitted = st.form_submit_button("🚀 立即解锁", type="primary", use_container_width=True)
                
                if submitted:
                    if pwd == PASSWORD:
                        login_cache[user_ip] = current_time 
                        st.session_state['is_logged_in'] = True 
                        st.success("✅ 验证成功！正在进入系统...")
                        time.sleep(0.5)
                        login_placeholder.empty() # 清除登录框
                        st.rerun() # 强制刷新
                    else:
                        st.error("❌ 密码错误，请检查大小写")
    
    return False

# 🛑 阻断非登录用户
if not check_login():
    st.stop()

# ==========================================
# ⚙️ 2. API 配置 (安全校验)
# ==========================================

try:
    api_key = st.secrets["DEEPSEEK_API_KEY"]
except:
    st.error("❌ 系统错误：未检测到 DEEPSEEK_API_KEY，请在后台 Secrets 中配置。")
    st.stop()

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# ==========================================
# 🧩 3. 功能模块 (专业化封装)
# ==========================================

# --- A. 爆款文案改写 ---
def page_rewrite():
    st.markdown("## ⚡ 爆款文案改写中台")
    st.caption("AI 驱动的五路并发架构 | 40秒黄金完播率模型")
    st.markdown("---")

    if 'results' not in st.session_state:
        st.session_state['results'] = {}
        
    def rewrite_logic(content):
        if not content or len(content.strip()) < 5: return "⚠️ 内容过短，无法处理"
        prompt = f"""
        你是一个抖音千万粉的口播博主。
        【原始素材】：{content}
        【任务】：清洗数据，暴力改写为原创爆款文案。
        【公式】：黄金3秒开头（反直觉/焦虑）+ 中间说人话（情绪饱满）+ 结尾强引导。
        【输出】：直接输出文案，200字左右，不要任何多余解释。
        """
        try:
            res = client.chat.completions.create(
                model="deepseek-chat", messages=[{"role": "user", "content": prompt}], temperature=1.3
            )
            return res.choices[0].message.content
        except Exception as e: return f"API Error: {e}"

    # 总控面板
    with st.container(border=True):
        col_main, col_tips = st.columns([1, 2])
        with col_main:
            if st.button("🚀 一键并发执行 (5路全开)", type="primary", use_container_width=True):
                tasks, indices = [], []
                for i in range(1, 6):
                    text = st.session_state.get(f"input_{i}", "")
                    if text.strip():
                        tasks.append(text)
                        indices.append(i)
                
                if not tasks:
                    st.toast("⚠️ 请先在下方窗口粘贴文案", icon="🛑")
                else:
                    with st.status("☁️ 云端计算中...", expanded=True) as status:
                        st.write(f"正在调动 {len(tasks)} 个 AI 线程同时作业...")
                        with ThreadPoolExecutor(max_workers=5) as executor:
                            results_list = list(executor.map(rewrite_logic, tasks))
                        for idx, res in zip(indices, results_list):
                            st.session_state['results'][idx] = res
                        status.update(label="✅ 全部生成完毕！", state="complete", expanded=False)
                        st.rerun()
        with col_tips:
            st.markdown("""
            <div style='background-color:#eef4ff; padding:10px; border-radius:8px; font-
