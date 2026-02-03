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
    
    # 1. 基础重置
    base_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        html, body, [class*="css"] { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
        
        header[data-testid="stHeader"] { visibility: hidden; height: 0; }
        #MainMenu { visibility: hidden; }
        [data-testid="stSidebarCollapsedControl"] { display: none; }
        
        /* 隐藏输入框按回车提交的小字提示 (Issue 4) */
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
    
    # 2. 登录页专用样式 (大卡片悬浮风格)
    auth_css = """
    <style>
        /* 背景：时尚的深色渐变 (Issue 5) */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
            background-attachment: fixed;
        }
        
        /* 核心布局：将整个内容区变成一个大卡片 (Issue 5) */
        div.block-container {
            background-color: rgba(255, 255, 255, 0.98); /* 卡片背景 */
            border-radius: 24px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); /* 深度投影 */
            padding: 60px 50px !important; /* 内部留白 */
            max-width: 960px; /* 限制最大宽度 */
            margin: auto;
            position: absolute;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%); /* 绝对垂直水平居中 */
            overflow: hidden; /* 防止溢出 */
        }
        
        /* 移动端适配：取消绝对定位 */
        @media (max-width: 768px) {
            div.block-container {
                position: relative; top: 0; left: 0; transform: none;
                width: 95%; margin: 20px auto; padding: 20px !important;
            }
        }

        /* 输入框修复：去除重复边框 (Issue 1) */
        .stTextInput div[data-baseweb="input"] {
            background-color: #f8fafc !important;
            border: 1px solid #cbd5e1 !important; /* 统一边框颜色 */
            border-radius: 8px !important;
            color: #1e293b !important;
            height: 44px !important;
            box-shadow: none !important; /* 去除外发光防止重影 */
        }
        /* 去除 Streamlit 默认外层包裹的边框 */
        .stTextInput > div { border: none !important; box-shadow: none !important; }
        
        /* 焦点状态 */
        .stTextInput div[data-baseweb="input"]:focus-within {
            border-color: #3b82f6 !important;
            background-color: #ffffff !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
        }

        /* Form 样式重置：因为外层已经是卡片了，里层不需要再有卡片样式 */
        [data-testid="stForm"] {
            background: transparent !important;
            padding: 0 !important;
            border: none !important;
            box-shadow: none !important;
        }

        /* Tab 样式优化 (Issue 3) */
        .stTabs [data-baseweb="tab-list"] { 
            gap: 20px; border-bottom: 2px solid #e2e8f0; margin-bottom: 20px; 
        }
        .stTabs [data-baseweb="tab"] {
            height: 40px; 
            color: #64748b; /* 未选中状态：深灰色，更醒目 */
            font-weight: 500;
            font-size: 15px;
        }
        .stTabs [aria-selected="true"] {
            color: #2563eb !important; /* 选中状态：蓝色 */
            font-weight: 700 !important;
            border-bottom-color: #2563eb !important;
        }

        /* 左侧装饰线 */
        .hero-decoration {
            width: 60px; height: 6px; background: #3b82f6; border-radius: 3px; margin-bottom: 25px;
        }
        .hero-title { font-size: 42px; font-weight: 800; color: #0f172a; line-height: 1.2; margin-bottom: 15px; letter-spacing: -0.5px; }
        .hero-subtitle { font-size: 16px; color: #64748b; margin-bottom: 40px; line-height: 1.6; }
        
        /* 底部版权声明样式 */
        .auth-footer {
            margin-top: 40px; border-top: 1px solid #f1f5f9; padding-top: 20px;
            text-align: center; color: #94a3b8; font-size: 12px;
        }
        .auth-footer a { color: #64748b; text-decoration: none; margin: 0 10px; transition: 0.2s; }
        .auth-footer a:hover { color: #3b82f6; }
    </style>
    """
    
    # 3. 系统内页样式 (保持原样)
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
