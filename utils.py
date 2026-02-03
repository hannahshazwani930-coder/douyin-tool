# utils.py
import streamlit as st
import streamlit.components.v1 as components
import hashlib
import random
import string

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_invite_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def inject_css(mode="app"):
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        html, body, [class*="css"] { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
        header[data-testid="stHeader"] { visibility: hidden; height: 0; }
        #MainMenu { visibility: hidden; }
        [data-testid="stSidebarCollapsedControl"] { display: none; }
        [data-testid="InputInstructions"] { display: none !important; }
        
        /* 全局容器调整 */
        div.block-container {
            max-width: 1400px !important;
            padding: 0 40px 40px 40px !important;
        }

        /* --- 1. 流光极光 Header (动效版) --- */
        .flowing-header {
            background: linear-gradient(-45deg, #1e3a8a, #2563eb, #3b82f6, #0ea5e9);
            background-size: 400% 400%;
            animation: gradientBG 10s ease infinite; /* 👈 流动动画 */
            border-bottom-left-radius: 40px;
            border-bottom-right-radius: 40px;
            padding: 50px 40px 100px 40px; /* 底部留白给悬浮卡片 */
            color: white; text-align: center;
            margin-bottom: -70px; /* 深度重叠 */
            margin-left: -40px; margin-right: -40px;
            box-shadow: 0 20px 50px rgba(37, 99, 235, 0.3);
            position: relative; z-index: 0;
        }
        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .header-title { font-size: 42px; font-weight: 900; letter-spacing: -1px; margin-bottom: 8px; text-shadow: 0 4px 10px rgba(0,0,0,0.2); }
        .header-sub { font-size: 15px; opacity: 0.95; background: rgba(255,255,255,0.1); padding: 5px 15px; border-radius: 30px; backdrop-filter: blur(10px); display: inline-block; border: 1px solid rgba(255,255,255,0.2); }

        /* --- 2. 一体化创作台 (解决白框问题) --- */
        .creation-console {
            background: white; border-radius: 24px; padding: 40px;
            box-shadow: 0 30px 60px -15px rgba(0,0,0,0.08); 
            border: 1px solid #e2e8f0; position: relative; z-index: 10;
            margin-top: 20px;
        }

        /* --- 3. 文本框叠影修复 (Fix Ghosting) --- */
        /* 隐藏 Streamlit 自带的外层边框 */
        .stTextArea > div { border: none !important; box-shadow: none !important; background: transparent !important; }
        .stTextArea > label { display: none !important; }
        /* 自定义内部样式 */
        .stTextArea textarea {
            background-color: #f8fafc !important; /* 淡灰底色 */
            border: 2px solid #e2e8f0 !important; /* 清晰边框 */
            border-radius: 12px; padding: 15px; font-size: 15px; line-height: 1.6; color: #334155;
            box-shadow: none !important;
        }
        .stTextArea textarea:focus { 
            background-color: #ffffff !important; 
            border-color: #3b82f6 !important; 
            box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1) !important; 
        }

        /* --- 4. 像素级对齐修复 --- */
        .custom-label { font-size: 14px; font-weight: 700; color: #1e293b; margin-bottom: 8px; display: block; }
        
        /* 强制 Selectbox 高度 */
        div[data-baseweb="select"] > div {
            height: 48px !important; border-radius: 10px !important; border-color: #e2e8f0 !important;
            display: flex; align-items: center; background-color: #f8fafc;
        }
        
        /* 强制 Primary 按钮高度与对齐 */
        div.stButton button[kind="primary"] {
            width: 100%; height: 48px !important; margin-top: 0px !important;
            background: linear-gradient(90deg, #2563eb, #3b82f6) !important;
            border: none !important; border-radius: 10px !important; 
            font-size: 16px !important; font-weight: 700 !important; letter-spacing: 1px;
            box-shadow: 0 8px 20px -5px rgba(37, 99, 235, 0.4) !important;
        }
        div.stButton button[kind="primary"]:hover {
            transform: translateY(-2px); box-shadow: 0 12px 25px -5px rgba(37, 99, 235, 0.6) !important;
        }

        /* 模式切换按钮 (Secondary) */
        div.stButton button[kind="secondary"] {
            height: 48px !important; border: 1px solid #e2e8f0 !important;
            background: white !important; color: #64748b !important; font-weight: 600 !important;
        }
        /* 选中模式的按钮样式 (通过 Primary 模拟) */
        
        /* 矩阵模式下的信息条 */
        .info-box {
            background: #eff6ff; border: 1px solid #bfdbfe; color: #1e40af;
            padding: 0 20px; border-radius: 10px; font-size: 15px;
            display: flex; align-items: center; gap: 10px; height: 48px; /* 强制高度对齐 */
        }

        /* 登录页兼容性保留 (不影响登录页) */
        .stTextInput div[data-baseweb="input"] { background-color: #f8fafc !important; border-radius: 8px !important; }
        .stTextInput div[data-baseweb="input"] > div { background-color: transparent !important; }

        .stApp { background-color: #f8fafc; }
    </style>
    """, unsafe_allow_html=True)

# --- 保持其他函数不变 ---
def call_deepseek_rewrite(content, style_prompt):
    pass

def render_copy_btn(text, key_suffix):
    safe_text = text.replace("`", "\`").replace("'", "\\'")
    html = f"""
    <script>
    function copy_{key_suffix}() {{
        navigator.clipboard.writeText(`{safe_text}`);
        document.getElementById('btn_{key_suffix}').innerHTML = '✅ 已复制';
        setTimeout(() => {{ document.getElementById('btn_{key_suffix}').innerHTML = '📋 一键复制'; }}, 2000);
    }}
    </script>
    <button id="btn_{key_suffix}" onclick="copy_{key_suffix}()" style="width:100%; height:40px; background:#0f172a; color:white; border:none; border-radius:8px; cursor:pointer; font-weight:600; font-family:'Inter'; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">📋 一键复制</button>
    """
    components.html(html, height=50)

def render_conversion_tip():
    st.markdown("""<div style="margin-top: 15px; background: #f0fdf4; border: 1px solid #bbf7d0; color: #166534; padding: 10px 15px; border-radius: 10px; font-size: 13px; display: flex; align-items: center; gap: 10px;"><span>💰</span><span><b>商业化建议：</b> 已自动植入私域钩子，预计提升 30% 导流效率。</span></div>""", unsafe_allow_html=True)
