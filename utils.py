# utils.py
import streamlit as st
import streamlit.components.v1 as components
import hashlib
import random
import string

# --- 基础工具 ---

def hash_password(password):
    """SHA256加密"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_invite_code():
    """生成6位随机邀请码"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# --- UI 组件 & 样式 ---

def inject_css(mode="app"):
    """注入全局 CSS 样式"""
    
    # 1. 基础重置 (Reset)
    base_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        html, body, [class*="css"] { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
        
        /* 彻底隐藏顶部 Header 和 汉堡菜单 */
        header[data-testid="stHeader"] { visibility: hidden; height: 0; }
        #MainMenu { visibility: hidden; }
        [data-testid="stSidebarCollapsedControl"] { display: none; }
        
        /* 按钮美化：小巧精致 */
        div.stButton > button {
            border-radius: 8px; font-weight: 600; border: none;
            padding: 0.4rem 1rem; font-size: 14px;
            transition: all 0.2s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        div.stButton > button:hover { transform: translateY(-1px); box-shadow: 0 4px 8px rgba(0,0,0,0.15); }
    </style>
    """
    
    # 2. 登录页专用样式 (Login UI - 终极美化版)
    auth_css = """
    <style>
        /* 全局背景：深邃渐变 */
        .stApp {
            background: radial-gradient(circle at 10% 20%, #1e293b 0%, #0f172a 90%);
        }
        
        /* 布局调整：去除顶部空白，垂直居中 */
        div.block-container {
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
            max-width: 1000px;
        }
        
        /* 核心修复：输入框样式 */
        .stTextInput input, .stTextInput div[data-baseweb="input"] {
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 8px !important;
            color: #334155 !important;
            height: 42px !important;
            min-height: 42px !important;
            padding: 0 12px !important;
            font-size: 14px !important;
            line-height: 40px !important;
        }
        .stTextInput > div > div { box-shadow: none !important; }
        .stTextInput input:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
        }

        /* 登录表单容器 */
        [data-testid="stForm"] {
            background-color: rgba(255, 255, 255, 0.98) !important;
            padding: 30px 25px !important;
            border-radius: 16px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255,255,255,0.1);
            max-width: 380px !important;
            margin: 0 auto;
        }

        /* 左侧文字样式 */
        .hero-title {
            font-size: 48px; font-weight: 800; color: #f8fafc;
            line-height: 1.1; margin-bottom: 15px;
            text-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }
        .hero-subtitle {
            font-size: 16px; color: #94a3b8; font-weight: 400;
            margin-bottom: 30px; line-height: 1.6;
        }
        
        /* 左侧功能列表项 */
        .feature-item {
            display: flex; align-items: center; margin-bottom: 15px;
            color: #cbd5e1; font-size: 14px;
        }
        .feature-icon {
            width: 24px; height: 24px; background: rgba(59, 130, 246, 0.2);
            color: #60a5fa; border-radius: 50%; display: flex; 
            align-items: center; justify-content: center; margin-right: 12px;
            font-size: 12px;
        }

        /* Tab 样式微调 */
        .stTabs [data-baseweb="tab-list"] { 
            gap: 15px; margin-bottom: 10px; border-bottom: 1px solid #f1f5f9; 
        }
        .stTabs [data-baseweb="tab"] {
            height: 40px; padding: 0 5px; font-size: 14px;
        }
    </style>
    """
    
    # 3. 系统内页样式
    app_css = """
    <style>
        .stApp { background-color: #f8fafc; }
        [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
        div.block-container { padding-top: 2rem; max-width: 1200px; }
        
        .announcement-box {
            background: linear-gradient(90deg, #eff6ff, #ffffff);
            border: 1px solid #bfdbfe; color: #1e40af;
            padding: 10px 15px; border-radius: 8px; margin-bottom: 25px;
            display: flex; align-items: center; font-size: 14px;
        }
    </style>
    """
    
    st.markdown(base_css, unsafe_allow_html=True)
    if mode == "auth": st.markdown(auth_css, unsafe_allow_html=True)
    else: st.markdown(app_css, unsafe_allow_html=True)

# 👇👇👇 [这是刚才补回来的关键函数] 👇👇👇
def render_copy_btn(text, key_suffix):
    """渲染一键复制按钮"""
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
    """渲染微信复制胶囊"""
    components.html(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;background:white;border:1px solid #e2e8f0;border-radius:8px;padding:0 12px;height:38px;cursor:pointer;font-family:'Inter',sans-serif;font-size:13px;color:#334155;" onclick="navigator.clipboard.writeText('{wx_id}')">
        <span style="font-weight:600">{label}</span>
        <span style="color:#059669;font-family:monospace;background:#ecfdf5;padding:2px 6px;border-radius:4px;">📋 {wx_id}</span>
    </div>
    """, height=45)
