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
    
    # 1. 基础重置 (字体与核心组件)
    base_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        html, body, [class*="css"] { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
        
        header[data-testid="stHeader"] { visibility: hidden; height: 0; }
        #MainMenu { visibility: hidden; }
        [data-testid="stSidebarCollapsedControl"] { display: none; }
        [data-testid="InputInstructions"] { display: none !important; }

        /* 全局按钮美化 */
        div.stButton > button {
            border-radius: 8px; font-weight: 600; border: none;
            padding: 0.5rem 1rem; font-size: 14px;
            transition: all 0.2s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        div.stButton > button:hover { transform: translateY(-1px); box-shadow: 0 6px 12px rgba(0,0,0,0.1); }
    </style>
    """
    
    # 2. 登录页专用样式
    auth_css = """
    <style>
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
            background-attachment: fixed;
        }
        div.block-container {
            background-color: rgba(255, 255, 255, 0.98);
            border-radius: 24px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            padding: 60px 50px !important;
            max-width: 960px;
            margin: auto;
            position: absolute;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            overflow: hidden;
        }
        @media (max-width: 768px) {
            div.block-container {
                position: relative; top: 0; left: 0; transform: none;
                width: 95%; margin: 20px auto; padding: 20px !important;
            }
        }
        .stTextInput div[data-baseweb="input"] {
            background-color: #f8fafc !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 8px !important;
            color: #1e293b !important;
            height: 44px !important;
            box-shadow: none !important;
            overflow: hidden;
        }
        .stTextInput div[data-baseweb="input"] > div { background-color: transparent !important; }
        .stTextInput div[data-baseweb="input"]:focus-within {
            border-color: #3b82f6 !important;
            background-color: #ffffff !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
        }
        .stTextInput > div { border: none !important; box-shadow: none !important; }
        [data-testid="stForm"] { background: transparent !important; padding: 0 !important; border: none !important; box-shadow: none !important; }
        
        .stTabs [data-baseweb="tab-list"] { gap: 24px; border-bottom: none !important; box-shadow: none !important; padding-bottom: 0px !important; margin-bottom: 25px; }
        .stTabs [data-baseweb="tab"] { height: 40px; color: #64748b; font-weight: 500; font-size: 15px; background-color: transparent !important; border: none !important; outline: none !important; padding-left: 0 !important; padding-right: 0 !important; margin-right: 10px !important; }
        .stTabs [aria-selected="true"] { color: #2563eb !important; font-weight: 700 !important; border-bottom: 3px solid #2563eb !important; }

        .hero-decoration { width: 60px; height: 6px; background: #3b82f6; border-radius: 3px; margin-bottom: 25px; }
        .hero-title { font-size: 42px; font-weight: 800; color: #0f172a; line-height: 1.2; margin-bottom: 15px; letter-spacing: -0.5px; }
        .hero-subtitle { font-size: 16px; color: #64748b; margin-bottom: 40px; line-height: 1.6; }
        .auth-footer { margin-top: 40px; border-top: 1px solid #f1f5f9; padding-top: 20px; text-align: center; color: #94a3b8; font-size: 12px; }
        .auth-footer a { color: #64748b; text-decoration: none; margin: 0 10px; transition: 0.2s; }
        .auth-footer a:hover { color: #3b82f6; }
    </style>
    """
    
    # 3. 系统内页专用样式 (App UI - 终极美化版)
    app_css = """
    <style>
        /* 全局背景：干净的灰白 */
        .stApp { background-color: #f8fafc; }
        
        /* 侧边栏美化 */
        [data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #e2e8f0;
            box-shadow: 4px 0 15px rgba(0,0,0,0.02);
        }
        
        /* 隐藏 Radio 组件默认的圆圈，将其变成菜单按钮样式 */
        div[role="radiogroup"] > label > div:first-child {
            display: none !important;
        }
        div[role="radiogroup"] {
            gap: 8px; /* 菜单项间距 */
        }
        div[role="radiogroup"] label {
            padding: 10px 15px !important;
            border-radius: 8px !important;
            transition: all 0.2s ease;
            margin-bottom: 4px;
            border: 1px solid transparent;
        }
        /* 鼠标悬停 */
        div[role="radiogroup"] label:hover {
            background-color: #f1f5f9 !important;
            color: #1e293b !important;
        }
        /* 选中状态 */
        div[role="radiogroup"] label[data-baseweb="radio"] > div:nth-child(2) {
             /* 修正文字对齐 */
             margin-left: 0 !important;
        }
        /* 选中的 Label 高亮 */
        div[role="radiogroup"] label[aria-checked="true"] {
            background-color: #eff6ff !important; /* 浅蓝背景 */
            color: #2563eb !important; /* 深蓝文字 */
            font-weight: 600 !important;
            border: 1px solid #bfdbfe;
        }

        /* 主内容区域卡片化 */
        div.block-container { 
            padding-top: 2rem; 
            max-width: 1100px; 
        }
        
        /* 顶部欢迎语样式 */
        h1 {
            font-family: 'Inter', sans-serif;
            font-weight: 800;
            letter-spacing: -0.5px;
            color: #0f172a;
        }
        
        /* 通用卡片容器 */
        .app-card {
            background: white;
            padding: 24px;
            border-radius: 16px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            margin-bottom: 20px;
        }
    </style>
    """
    
    st.markdown(base_css, unsafe_allow_html=True)
    if mode == "auth": st.markdown(auth_css, unsafe_allow_html=True)
    else: st.markdown(app_css, unsafe_allow_html=True)

# 👇 新增：侧边栏用户卡片渲染函数 (解决乱码问题)
def render_sidebar_user_card(username, role_tag="普通用户"):
    """在侧边栏渲染一个漂亮的用户卡片"""
    # 根据角色显示不同颜色
    tag_bg = "#dbeafe" if "VIP" in role_tag or "管理员" in role_tag else "#f1f5f9"
    tag_color = "#1e40af" if "VIP" in role_tag or "管理员" in role_tag else "#475569"
    
    html = f"""
    <div style="
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
    ">
        <div style="font-size: 12px; color: #94a3b8; margin-bottom: 4px;">当前登录</div>
        <div style="font-size: 16px; font-weight: 700; color: #0f172a; margin-bottom: 8px; overflow: hidden; text-overflow: ellipsis;">
            {username}
        </div>
        <span style="
            background-color: {tag_bg};
            color: {tag_color};
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
            display: inline-block;
        ">{role_tag}</span>
    </div>
    """
    st.sidebar.markdown(html, unsafe_allow_html=True)

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
