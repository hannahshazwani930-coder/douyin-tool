# utils.py
import streamlit as st
import streamlit.components.v1 as components
import hashlib
import random
import string

# --- 基础工具 ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_invite_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# --- 全局样式注入 (包含最新的流光效果 + 修复叠影) ---
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
            animation: gradientBG 10s ease infinite;
            border-bottom-left-radius: 40px;
            border-bottom-right-radius: 40px;
            padding: 50px 40px 100px 40px;
            color: white; text-align: center;
            margin-bottom: -70px;
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

        /* --- 2. 一体化创作台 --- */
        .creation-console {
            background: white; border-radius: 24px; padding: 40px;
            box-shadow: 0 30px 60px -15px rgba(0,0,0,0.08); 
            border: 1px solid #e2e8f0; position: relative; z-index: 10;
            margin-top: 20px;
        }

        /* --- 3. 文本框叠影修复 --- */
        .stTextArea > div { border: none !important; box-shadow: none !important; background: transparent !important; }
        .stTextArea > label { display: none !important; }
        .stTextArea textarea {
            background-color: #f8fafc !important;
            border: 2px solid #e2e8f0 !important;
            border-radius: 12px; padding: 15px; font-size: 15px; line-height: 1.6; color: #334155;
            box-shadow: none !important;
        }
        .stTextArea textarea:focus { 
            background-color: #ffffff !important; 
            border-color: #3b82f6 !important; 
            box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1) !important; 
        }

        /* --- 4. 像素级对齐与组件美化 --- */
        .custom-label { font-size: 14px; font-weight: 700; color: #1e293b; margin-bottom: 8px; display: block; }
        
        div[data-baseweb="select"] > div {
            height: 48px !important; border-radius: 10px !important; border-color: #e2e8f0 !important;
            display: flex; align-items: center; background-color: #f8fafc;
        }
        
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
        div.stButton button[kind="secondary"] {
            height: 48px !important; border: 1px solid #e2e8f0 !important;
            background: white !important; color: #64748b !important; font-weight: 600 !important;
        }

        .info-box {
            background: #eff6ff; border: 1px solid #bfdbfe; color: #1e40af;
            padding: 0 20px; border-radius: 10px; font-size: 15px;
            display: flex; align-items: center; gap: 10px; height: 48px;
        }

        /* --- 5. 登录页/全局通用兼容 --- */
        .stTextInput div[data-baseweb="input"] { background-color: #f8fafc !important; border-radius: 8px !important; }
        .stTextInput div[data-baseweb="input"] > div { background-color: transparent !important; }
        .stApp { background-color: #f8fafc; }
        [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
        
        /* 公告卡片 */
        .ann-card { background: #fff7ed; border: 1px solid #fed7aa; border-radius: 8px; padding: 12px 15px; margin-bottom: 10px; display: flex; align-items: start; gap: 10px; font-size: 14px; color: #9a3412; }
        
        /* 转化提示 */
        .conversion-tip { margin-top: 15px; background: #f0fdf4; border: 1px solid #bbf7d0; color: #166534; padding: 10px 15px; border-radius: 10px; font-size: 13px; display: flex; align-items: center; gap: 10px; }
        
        /* 通用 Banner (后台/其他页面用) */
        .page-banner {
            background: linear-gradient(120deg, #2563eb, #1d4ed8);
            color: white; padding: 30px; border-radius: 16px; margin-bottom: 30px;
            box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.4);
        }
        .banner-title { font-size: 28px; font-weight: 800; margin-bottom: 10px; }
        .banner-desc { font-size: 15px; opacity: 0.9; line-height: 1.5; }
        
        /* 首页项目卡片 */
        .project-card {
            background: white; border-radius: 12px; padding: 20px;
            border: 1px solid #e2e8f0; transition: all 0.3s ease; height: 100%; display: flex; flex-direction: column;
        }
        .project-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.08); border-color: #93c5fd; }
        .proj-title { font-size: 16px; font-weight: 700; color: #1e293b; margin-bottom: 8px; display: flex; align-items: center; }
        .proj-desc { font-size: 12px; color: #64748b; line-height: 1.5; flex-grow: 1; }
        .proj-tag { font-size: 11px; padding: 3px 8px; border-radius: 10px; background: #f1f5f9; color: #475569; margin-top: 15px; width: fit-content; }
        
        /* 侧边栏菜单按钮 */
        div[role="radiogroup"] label { padding: 10px 12px !important; border-radius: 8px !important; margin-bottom: 4px; border: 1px solid transparent; }
        div[role="radiogroup"] label:hover { background-color: #f1f5f9 !important; }
        div[role="radiogroup"] label[aria-checked="true"] { background-color: #eff6ff !important; color: #2563eb !important; border: 1px solid #bfdbfe; font-weight: 600 !important; }
        div[role="radiogroup"] > label > div:first-child { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 补全所有丢失的组件函数 ---

def render_sidebar_user_card(username, vip_info):
    """侧边栏用户卡片"""
    status_bg = "#eff6ff" if "VIP" in vip_info or "管理员" in vip_info else "#f1f5f9"
    status_color = "#2563eb" if "VIP" in vip_info or "管理员" in vip_info else "#64748b"
    html = f"""
    <div style="background: {status_bg}; border: 1px solid #e2e8f0; border-radius: 12px; padding: 15px; margin-bottom: 20px;">
        <div style="display:flex; align-items:center; margin-bottom: 8px;">
            <div style="width: 32px; height: 32px; background: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 16px; margin-right: 10px; border: 1px solid #e2e8f0;">👤</div>
            <div style="font-weight: 700; color: #0f172a; font-size: 14px; overflow: hidden; text-overflow: ellipsis;">{username}</div>
        </div>
        <div style="background: white; padding: 6px 10px; border-radius: 6px; font-size: 12px; color: {status_color}; font-weight: 600; border: 1px solid #e2e8f0; text-align: center;">{vip_info}</div>
    </div>
    """
    st.sidebar.markdown(html, unsafe_allow_html=True)

def render_tech_support_btn(wx_id):
    """技术支持按钮 (带复制)"""
    btn_id = f"tech_btn_{random.randint(1000,9999)}"
    html = f"""
    <script>
    function copyTech_{btn_id}() {{
        navigator.clipboard.writeText('{wx_id}');
        const el = document.getElementById('{btn_id}');
        el.innerText = '✅ 已复制'; el.style.color = '#059669'; el.style.borderColor = '#059669';
        setTimeout(() => {{ el.innerText = '🤝 技术合作: {wx_id}'; el.style.color = '#334155'; el.style.borderColor = '#e2e8f0'; }}, 2000);
    }}
    </script>
    <div id="{btn_id}" onclick="copyTech_{btn_id}()" 
         style="width: 100%; text-align: center; background: white; border: 1px solid #e2e8f0; color: #334155; font-weight: 600; padding: 10px 0; border-radius: 8px; cursor: pointer; font-size: 14px; margin-bottom: 10px; transition: 0.2s;">
        🤝 技术合作: {wx_id}
    </div>
    """
    st.sidebar.markdown(html, unsafe_allow_html=True)

def render_copy_btn(text, key_suffix):
    """一键复制按钮"""
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

def render_wechat_pill(label, wx_id):
    """微信胶囊"""
    components.html(f"""<div style="display:flex;justify-content:space-between;align-items:center;background:white;border:1px solid #e2e8f0;border-radius:6px;padding:0 10px;height:34px;cursor:pointer;font-family:'Inter',sans-serif;font-size:12px;color:#334155;" onclick="navigator.clipboard.writeText('{wx_id}')"><span style="font-weight:600">{label}</span><span style="color:#059669;font-family:monospace;background:#ecfdf5;padding:2px 6px;border-radius:4px;">📋 {wx_id}</span></div>""", height=40)

def render_cta_wechat(wx_id):
    """首页领取资料"""
    html = f"""
    <style>
    .cta-container {{ padding: 10px; }}
    .cta-box {{
        background: linear-gradient(90deg, #059669, #10b981);
        color: white; border-radius: 12px; padding: 15px 25px;
        display: flex; align-items: center; justify-content: space-between;
        cursor: pointer; transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(16, 185, 129, 0.4);
        font-family: 'Inter', sans-serif;
    }}
    .cta-box:hover {{ transform: translateY(-3px); box-shadow: 0 10px 25px rgba(16, 185, 129, 0.5); }}
    .cta-copy {{ background: rgba(255,255,255,0.2); padding: 5px 12px; border-radius: 20px; font-size: 13px; font-weight: 600; font-family: monospace; }}
    </style>
    <div class="cta-container">
        <div class="cta-box" onclick="navigator.clipboard.writeText('{wx_id}');alert('微信号 {wx_id} 已复制！')">
            <div style="display:flex; align-items:center;">
                <div style="font-size: 24px; margin-right: 15px;">🎁</div>
                <div>
                    <span class="cta-title" style="font-size:16px;font-weight:700;display:block;">领取内部资料 & 项目白皮书</span>
                    <span class="cta-sub" style="font-size:13px;opacity:0.9;">添加微信，备注【资料】</span>
                </div>
            </div>
            <div class="cta-copy">📋 {wx_id}</div>
        </div>
    </div>
    """
    components.html(html, height=100)

def render_home_project_card(icon, title, desc, tag):
    """首页项目卡片"""
    return f"""<div class="project-card"><div class="proj-title"><span style="margin-right:8px;">{icon}</span>{title}</div><div class="proj-desc">{desc}</div><div class="proj-tag">{tag}</div></div>"""

def render_page_banner(title, desc):
    """通用页面 Banner"""
    st.markdown(f"""<div class="page-banner"><div class="banner-title">{title}</div><div class="banner-desc">{desc}</div></div>""", unsafe_allow_html=True)

def render_conversion_tip():
    """转化提示条"""
    st.markdown("""<div class="conversion-tip"><span>💰</span><span><b>商业化建议：</b> 已自动植入私域钩子，预计提升 30% 导流效率。</span></div>""", unsafe_allow_html=True)

def render_feature_card_home(icon, title, desc):
    """首页功能卡片 (配合 Button)"""
    return f"""
    <div style="background:white; border:1px solid #e2e8f0; border-radius:12px; padding:15px; text-align:center; height:100px; display:flex; flex-direction:column; justify-content:center; align-items:center;">
        <div style="font-size:24px; margin-bottom:5px;">{icon}</div>
        <div style="font-weight:700; color:#0f172a;">{title}</div>
    </div>
    """
