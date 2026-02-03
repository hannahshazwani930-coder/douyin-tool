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
    
    base_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        html, body, [class*="css"] { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
        header[data-testid="stHeader"] { visibility: hidden; height: 0; }
        #MainMenu { visibility: hidden; }
        [data-testid="stSidebarCollapsedControl"] { display: none; }
        [data-testid="InputInstructions"] { display: none !important; }

        div.stButton > button {
            border-radius: 6px; font-weight: 600; border: none;
            padding: 0.4rem 0.8rem; font-size: 14px;
            transition: all 0.2s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        div.stButton > button:hover { transform: translateY(-1px); box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
    </style>
    """
    
    auth_css = """
    <style>
        .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%); background-attachment: fixed; }
        div.block-container {
            background-color: rgba(255, 255, 255, 0.98); border-radius: 24px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            padding: 60px 50px !important; max-width: 960px;
            margin: auto; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); overflow: hidden;
        }
        @media (max-width: 768px) {
            div.block-container { position: relative; top: 0; left: 0; transform: none; width: 95%; margin: 20px auto; padding: 20px !important; }
        }
        .stTextInput div[data-baseweb="input"] { background-color: #f8fafc !important; border: 1px solid #cbd5e1 !important; border-radius: 8px !important; color: #1e293b !important; height: 44px !important; box-shadow: none !important; overflow: hidden; }
        .stTextInput div[data-baseweb="input"] > div { background-color: transparent !important; }
        .stTextInput div[data-baseweb="input"]:focus-within { border-color: #3b82f6 !important; background-color: #ffffff !important; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important; }
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
    
    app_css = """
    <style>
        .stApp { background-color: #f8fafc; }
        [data-testid="stSidebar"] {
            background-color: #ffffff; border-right: 1px solid #e2e8f0;
            box-shadow: 4px 0 15px rgba(0,0,0,0.02);
            padding-top: 1rem;
        }
        
        /* 侧边栏紧凑优化 */
        div[role="radiogroup"] > label > div:first-child { display: none !important; }
        div[role="radiogroup"] { gap: 4px; }
        div[role="radiogroup"] label {
            padding: 8px 12px !important;
            border-radius: 6px !important;
            transition: all 0.2s ease;
            margin-bottom: 2px;
            border: 1px solid transparent;
            font-size: 14px;
        }
        div[role="radiogroup"] label:hover { background-color: #f1f5f9 !important; color: #1e293b !important; }
        div[role="radiogroup"] label[data-baseweb="radio"] > div:nth-child(2) { margin-left: 0 !important; }
        div[role="radiogroup"] label[aria-checked="true"] {
            background-color: #eff6ff !important; color: #2563eb !important;
            font-weight: 600 !important; border: 1px solid #bfdbfe;
        }

        section[data-testid="stSidebar"] > div { padding-top: 20px; }
        div.block-container { padding-top: 2rem; max-width: 1100px; }
        
        /* 首页项目卡片样式 */
        .project-card {
            background: white; border-radius: 12px; padding: 20px;
            border: 1px solid #e2e8f0; transition: all 0.3s ease;
            height: 100%; display: flex; flex-direction: column;
        }
        .project-card:hover {
            transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.08); border-color: #bfdbfe;
        }
        .proj-title { font-size: 18px; font-weight: 700; color: #1e293b; margin-bottom: 8px; display: flex; align-items: center; }
        .proj-desc { font-size: 13px; color: #64748b; line-height: 1.5; flex-grow: 1; }
        .proj-tag { 
            font-size: 11px; padding: 3px 8px; border-radius: 10px; 
            background: #f1f5f9; color: #475569; margin-top: 15px; width: fit-content; 
        }
    </style>
    """
    
    st.markdown(base_css, unsafe_allow_html=True)
    if mode == "auth": st.markdown(auth_css, unsafe_allow_html=True)
    else: st.markdown(app_css, unsafe_allow_html=True)

def render_sidebar_user_card(username, vip_info):
    """侧边栏用户卡片：支持显示剩余天数"""
    if "VIP" in vip_info or "管理员" in vip_info:
        status_color = "#2563eb"
        bg_color = "#eff6ff"
    else:
        status_color = "#64748b"
        bg_color = "#f8fafc"

    html = f"""
    <div style="
        background: {bg_color}; border: 1px solid #e2e8f0; border-radius: 10px;
        padding: 12px; margin-bottom: 15px; display: flex; align-items: center;
    ">
        <div style="
            width: 36px; height: 36px; background: white; border-radius: 50%; 
            display: flex; align-items: center; justify-content: center;
            font-size: 18px; border: 1px solid #e2e8f0; margin-right: 10px;
        ">👤</div>
        <div style="flex-grow: 1; overflow: hidden;">
            <div style="font-size: 14px; font-weight: 700; color: #0f172a; margin-bottom: 2px;">{username}</div>
            <div style="font-size: 12px; color: {status_color}; font-weight: 500;">{vip_info}</div>
        </div>
    </div>
    """
    st.sidebar.markdown(html, unsafe_allow_html=True)

# 👇👇👇 [这里补回了 render_copy_btn 函数] 👇👇👇
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
    """简单的微信复制胶囊 (侧边栏用)"""
    components.html(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;background:white;border:1px solid #e2e8f0;border-radius:6px;padding:0 10px;height:34px;cursor:pointer;font-family:'Inter',sans-serif;font-size:12px;color:#334155;" onclick="navigator.clipboard.writeText('{wx_id}')">
        <span style="font-weight:600">{label}</span>
        <span style="color:#059669;font-family:monospace;background:#ecfdf5;padding:2px 6px;border-radius:4px;">📋 {wx_id}</span>
    </div>
    """, height=40)

def render_cta_wechat(wx_id):
    """首页专用：带悬浮特效的微信资料领取按钮"""
    html = f"""
    <style>
    .cta-box {{
        background: linear-gradient(90deg, #059669, #10b981);
        color: white; border-radius: 12px; padding: 15px 25px;
        display: flex; align-items: center; justify-content: space-between;
        cursor: pointer; transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
        margin-top: 30px; font-family: 'Inter', sans-serif;
    }}
    .cta-box:hover {{ transform: translateY(-3px); box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4); }}
    .cta-icon {{ font-size: 24px; margin-right: 15px; }}
    .cta-text {{ flex-grow: 1; }}
    .cta-title {{ font-size: 16px; font-weight: 700; display: block; }}
    .cta-sub {{ font-size: 13px; opacity: 0.9; }}
    .cta-copy {{ background: rgba(255,255,255,0.2); padding: 5px 12px; border-radius: 20px; font-size: 13px; font-weight: 600; font-family: monospace; }}
    </style>
    
    <div class="cta-box" onclick="copyToClip('{wx_id}')" id="cta-btn">
        <div style="display:flex; align-items:center;">
            <div class="cta-icon">🎁</div>
            <div class="cta-text">
                <span class="cta-title">领取内部资料 & 项目白皮书</span>
                <span class="cta-sub">添加微信，备注【资料】</span>
            </div>
        </div>
        <div class="cta-copy" id="cta-code">📋 {wx_id}</div>
    </div>

    <script>
    function copyToClip(text) {{
        navigator.clipboard.writeText(text).then(function() {{
            const codeElem = document.getElementById('cta-code');
            const original = codeElem.innerHTML;
            codeElem.innerHTML = '✅ 已复制';
            codeElem.style.background = 'white';
            codeElem.style.color = '#059669';
            setTimeout(() => {{ 
                codeElem.innerHTML = original; 
                codeElem.style.background = 'rgba(255,255,255,0.2)';
                codeElem.style.color = 'white';
            }}, 2000);
        }}, function(err) {{
            console.error('Async: Could not copy text: ', err);
        }});
    }}
    </script>
    """
    components.html(html, height=90)

def render_home_project_card(icon, title, desc, tag):
    """渲染首页的项目切片"""
    return f"""
    <div class="project-card">
        <div class="proj-title"><span style="margin-right:8px;">{icon}</span>{title}</div>
        <div class="proj-desc">{desc}</div>
        <div class="proj-tag">{tag}</div>
    </div>
    """
