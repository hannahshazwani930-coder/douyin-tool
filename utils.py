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
    # 基础字体与重置
    base_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
        
        /* 隐藏顶部红线和菜单 */
        header[data-testid="stHeader"] { visibility: hidden; }
        #MainMenu { visibility: hidden; }
        [data-testid="stSidebarCollapsedControl"] { display: none; }
        
        /* 全局按钮美化 - 更加圆润和现代 */
        div.stButton > button {
            border-radius: 8px; font-weight: 600; border: none; 
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            padding: 0.5rem 1rem;
        }
        div.stButton > button:hover { 
            transform: translateY(-2px); 
            box-shadow: 0 8px 15px rgba(0,0,0,0.15); 
        }
        
        /* 核心修复：强制输入框文字颜色为深黑，背景纯白 */
        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
            color: #1e293b !important; 
            background-color: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 8px !important;
            height: 48px; /* 增加输入框高度 */
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1) !important;
        }
    </style>
    """
    
    # 登录页专用样式 - 包含新的左侧卡片样式
    auth_css = """
    <style>
        /* 动态渐变背景 */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #172554 100%);
            background-size: 400% 400%; animation: gradientBG 15s ease infinite;
        }
        @keyframes gradientBG { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
        
        /* 登录框容器样式 */
        [data-testid="stForm"] {
            background-color: rgba(255, 255, 255, 0.98) !important;
            padding: 40px 30px; border-radius: 20px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.3);
            border: 1px solid rgba(255,255,255,0.1);
        }

        /* 左侧营销文案样式 */
        .hero-title {
            font-size: 56px; font-weight: 800; color: #ffffff;
            line-height: 1.1; margin-bottom: 20px;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
        .hero-subtitle {
            font-size: 20px; color: #94a3b8; font-weight: 400;
            margin-bottom: 40px; max-width: 90%;
        }
        
        /* 悬停卡片样式 (左侧) */
        .feature-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 20px; border-radius: 16px; margin-bottom: 15px;
            display: flex; align-items: center; cursor: default;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .feature-card:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateX(10px);
            border-color: rgba(255, 255, 255, 0.3);
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .feature-icon {
            font-size: 24px; margin-right: 15px;
            width: 45px; height: 45px;
            background: linear-gradient(135deg, #3b82f6, #2563eb);
            border-radius: 12px; display: flex; align-items: center; justify-content: center;
            color: white; box-shadow: 0 4px 6px rgba(37, 99, 235, 0.3);
        }
        .feature-text h4 { color: white; margin: 0; font-size: 16px; font-weight: 600; }
        .feature-text p { color: #cbd5e1; margin: 2px 0 0 0; font-size: 13px; }

        /* Tabs 样式优化 */
        .stTabs [data-baseweb="tab-list"] { 
            gap: 20px; border-bottom: 2px solid #f1f5f9; padding-bottom: 5px; 
        }
        .stTabs [data-baseweb="tab"] { 
            background-color: transparent; color: #64748b; font-weight: 600; font-size: 16px; 
        }
        .stTabs [aria-selected="true"] { 
            color: #2563eb !important; 
        }
    </style>
    """
    
    # 系统内页专用样式
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
            box-shadow: 0 2px 5px rgba(0,0,0,0.02);
        }
        .ann-icon { margin-right: 10px; font-size: 16px; }
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
    <div style="display:flex;justify-content:space-between;align-items:center;background:white;border:1px solid #e2e8f0;border-radius:8px;padding:0 12px;height:38px;cursor:pointer;font-family:'Inter',sans-serif;font-size:13px;color:#334155;transition:0.2s;" onclick="navigator.clipboard.writeText('{wx_id}')">
        <span style="font-weight:600">{label}</span>
        <span style="color:#059669;font-family:monospace;background:#ecfdf5;padding:2px 6px;border-radius:4px;">📋 {wx_id}</span>
    </div>
    """, height=45)
