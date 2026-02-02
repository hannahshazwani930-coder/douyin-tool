import streamlit as st
from openai import OpenAI
import time
from concurrent.futures import ThreadPoolExecutor 

# ==========================================
# 🎨 0. 专业级 UI 配置
# ==========================================
st.set_page_config(page_title="🔥 抖音爆款改写中台", layout="wide", page_icon="⚡")

st.markdown("""
<style>
    .stApp { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    h1 { color: #FF4B4B; text-align: center; font-weight: 800 !important; }
    div.stButton > button { border-radius: 8px; height: 3em; font-weight: bold; transition: all 0.3s; }
    .stTextArea textarea { border-radius: 10px; }
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        padding: 20px;
        background-color: #f9f9f9;
    }
    @media (prefers-color-scheme: dark) {
        [data-testid="stVerticalBlockBorderWrapper"] { background-color: #262730; }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🔐 1. 登录与安全系统 (修复版)
# ==========================================

PASSWORD = "taoge888"

# 定义清空的回调函数
def clear_text_callback(key):
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
    # 1. 先检查本次浏览器的 Session
    if st.session_state.get('is_logged_in', False):
        return True

    user_ip = get_remote_ip()
    current_time = time.time()
    login_cache = get_login_cache()
    
    # 2. 再检查 IP 缓存（48小时内免密）
    if user_ip in login_cache and (current_time - login_cache[user_ip] < 172800):
        st.session_state['is_logged_in'] = True 
        return True 
        
    # --- 登录界面 ---
    st.markdown("<br><br>", unsafe_allow_html=True) 
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        with st.container(border=True):
            # 注意：这就是你之前报错的那一行，我已经补全了 True)
            st.markdown("<h2 style='text-align: center;'>🔒 访问受限</h2>", unsafe_allow_html=True)
            st.info("🔑 获取密码请联系微信：TG777188", icon="💬")
            
            pwd = st.text_input("请输入会员密码", type="password", key="login_pwd")
            if st.button("立即解锁", type="primary", use_container_width=True):
                if pwd == PASSWORD:
                    login_cache[user_ip] = current_time 
                    st.session_state['is_logged_in'] = True 
                    st.toast("验证成功！48小时内免密", icon="✅")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("❌ 密码错误")
    return False

if not check_login():
    st.stop()

# ==========================================
# 🛠️ 2. 核心逻辑区
# ==========================================

try:
    api_key = st.secrets["DEEPSEEK_API_KEY"]
except:
    st.error("⚠️ 请先在 Settings -> Secrets 里配置 DEEPSEEK_API_KEY")
    st.stop()

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

def rewrite_viral_script(content):
    if not content or len(content.strip()) < 5:
        return "⚠️ 内容太短，无法改写"
        
    prompt = f"""
    你是一个抖音千万粉的口播博主。
    【原始素材】：{content}
    【任务】：清洗数据，去除乱码时间轴，暴力改写为原创爆款文案。
    【公式】：
    1. 黄金3秒开头（反直觉/焦虑/好奇）。
    2. 中间说人话（情绪饱满，像跟朋友吐槽）。
    3. 结尾强引导。
    【输出】：直接输出文案，200字左右。
    """
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=1.3, 
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"生成出错：{e}"

if 'results' not in st.session_state:
    st.session_state['results'] = {}

# ==========================================
# 🖥️ 3. 页面布局 (美观大气版)
# =================
