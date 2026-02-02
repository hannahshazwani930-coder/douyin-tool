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
# 🔐 1. 登录与安全系统 (修复版：48小时+防刷新)
# ==========================================

PASSWORD = "taoge888"

# 定义清空的回调函数（修复报错的关键）
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
    # 1. 先检查本次浏览器的 Session（刷新网页不掉线）
    if st.session_state.get('is_logged_in', False):
        return True

    user_ip = get_remote_ip()
    current_time = time.time()
    login_cache = get_login_cache()
    
    # 2. 再检查 IP 缓存（48小时内免密）
    # 48小时 = 48 * 60 * 60 = 172800 秒
    if user_ip in login_cache and (current_time - login_cache[user_ip] < 172800):
        st.session_state['is_logged_in'] = True # 同步到 Session
        return True 
        
    # --- 登录界面 ---
    st.markdown("<br><br>", unsafe_allow_html=True) 
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center;'>🔒 访问受限</h2>", unsafe_allow_html=
