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
    base_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        html, body, [class*="css"] { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
        header[data-testid="stHeader"] { visibility: hidden; height: 0; }
        #MainMenu { visibility: hidden; }
        [data-testid="stSidebarCollapsedControl"] { display: none; }
        [data-testid="InputInstructions"] { display: none !important; }
        div.stButton > button {
            border-radius: 8px; font-weight: 600; border: none;
            padding: 0.5rem 1rem; font-size: 14px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: all 0.2s ease;
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
            box-shadow: 4px 0 15px rgba(0,0,0,0.02); padding-top: 1rem;
        }
        div[role="radiogroup"] > label > div:first-child { display: none !important; }
        div[role="radiogroup"] { gap: 4px; }
        div[role="radiogroup"] label {
            padding: 10px 12px !important; border-radius: 8px !important;
            transition: all 0.2s ease; margin-bottom: 4px; border: 1px solid transparent; font-size: 14px;
        }
        div[role="radiogroup"] label:hover { background-color: #f1f5f9 !important; color: #1e293b !important; }
        div[role="radiogroup"] label[data-baseweb="radio"] > div:nth-child(2) { margin-left: 0 !important; }
        div[role="radiogroup"] label[aria-checked="true"] {
            background-color: #eff6ff !important; color: #2563eb !important;
            font-weight: 600 !important; border: 1px solid #bfdbfe;
        }
        section[data-testid="stSidebar"] > div { padding-top: 20px; }
        div.block-container { padding-top: 2rem; max-width: 1150px; padding-bottom: 5rem; }
        
        /* Banner Styles */
        .page-banner {
            background: linear-gradient(120deg, #2563eb, #1d4ed8);
            color: white; padding: 30px; border-radius: 16px; margin-bottom: 30px;
            box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.4);
        }
        .banner-title { font-size: 28px; font-weight: 800; margin-bottom: 10px; }
        .banner-desc { font-size: 15px; opacity: 0.9; line-height: 1.5; max-width: 800px; }

        /* Section Header */
        .section-header { font-size: 18px; font-weight: 700; color: #1e293b; margin: 30px 0 15px 0; border-left: 5px solid #3b82f6; padding-left: 12px; }

        /* Project Card */
        .project-card {
            background: white; border-radius: 12px; padding: 20px;
            border: 1px solid #e2e8f0; transition: all 0.3s ease; height: 100%; display: flex; flex-direction: column;
        }
        .project-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.08); border-color: #93c5fd; }
        .proj-title { font-size: 16px; font-weight: 700; color: #1e293b; margin-bottom: 8px; display: flex; align-items: center; }
        .proj-desc { font-size: 12px; color: #64748b; line-height: 1.5; flex-grow: 1; }
        .proj-tag { font-size: 11px; padding: 3px 8px; border-radius: 10px; background: #f1f5f9; color: #475569; margin-top: 15px; width: fit-content; }
        
        /* Feature Nav Card (New) */
        .feature-card-home {
            background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 20px;
            text-align: center; height: 100%; transition: 0.2s; display: flex; flex-direction: column; align-items: center;
        }
        .feature-card-home:hover { border-color: #bfdbfe; box-shadow: 0 10px 20px rgba(0,0,0,0.05); }
        .fc-icon { width: 48px; height: 48px; background: #eff6ff; color: #2563eb; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px; margin-bottom: 15px; }
        .fc-title { font-size: 16px; font-weight: 700; color: #0f172a; margin-bottom: 5px; }
        .fc-desc { font-size: 12px; color: #64748b; margin-bottom: 15px; line-height: 1.4; flex-grow: 1; }
        
        /* Announcements */
        .ann-card { background: #fff7ed; border: 1px solid #fed7aa; border-radius: 8px; padding: 12px 15px; margin-bottom: 10px; display: flex; align-items: start; gap: 10px; font-size: 14px; color: #9a3412; }
    </style>
    """
    
    st.markdown(base_css, unsafe_allow_html=True)
    if mode == "auth": st.markdown(auth_css, unsafe_allow_html=True)
    else: st.markdown(app_css, unsafe_allow_html=True)

def render_page_banner(title, desc):
    """通用页面顶部大气切片"""
    st.markdown(f"""
    <div class="page-banner">
        <div class="banner-title">{title}</div>
        <div class="banner-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar_user_card(username, vip_info):
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
    """侧边栏：技术合作按钮 (点击复制修复)"""
    # 增加 unique ID 防止冲突
    btn_id = f"tech_btn_{random.randint(1000,9999)}"
    html = f"""
    <script>
    function copyTech_{btn_id}() {{
        navigator.clipboard.writeText('{wx_id}');
        const el = document.getElementById('{btn_id}');
        el.innerText = '✅ 已复制';
        el.style.color = '#059669';
        el.style.borderColor = '#059669';
        setTimeout(() => {{ 
            el.innerText = '🤝 技术合作: {wx_id}'; 
            el.style.color = '#334155';
            el.style.borderColor = '#e2e8f0';
        }}, 2000);
    }}
    </script>
    <div id="{btn_id}" onclick="copyTech_{btn_id}()" 
         style="width: 100%; text-align: center; background: white; border: 1px solid #e2e8f0; color: #334155; font-weight: 600; padding: 10px 0; border-radius: 8px; cursor: pointer; font-size: 14px; margin-bottom: 10px; transition: 0.2s;">
        🤝 技术合作: {wx_id}
    </div>
    """
    st.sidebar.markdown(html, unsafe_allow_html=True)

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
    <button id="btn_{key_suffix}" onclick="copy_{key_suffix}()" style="width:100%; height:40px; background:#0f172a; color:white; border:none; border-radius:8px; cursor:pointer; font-weight:600; font-family:'Inter';">📋 一键复制</button>
    """
    components.html(html, height=50)

def render_wechat_pill(label, wx_id):
    components.html(f"""<div style="display:flex;justify-content:space-between;align-items:center;background:white;border:1px solid #e2e8f0;border-radius:6px;padding:0 10px;height:34px;cursor:pointer;font-family:'Inter',sans-serif;font-size:12px;color:#334155;" onclick="navigator.clipboard.writeText('{wx_id}')"><span style="font-weight:600">{label}</span><span style="color:#059669;font-family:monospace;background:#ecfdf5;padding:2px 6px;border-radius:4px;">📋 {wx_id}</span></div>""", height=40)

def render_cta_wechat(wx_id):
    """首页：领取资料 (修复阴影被切)"""
    html = f"""
    <style>
    .cta-container {{ padding: 10px; }} /* Container padding prevents shadow clip */
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
    return f"""<div class="project-card"><div class="proj-title"><span style="margin-right:8px;">{icon}</span>{title}</div><div class="proj-desc">{desc}</div><div class="proj-tag">{tag}</div></div>"""

def render_feature_card_home(icon, title, desc):
    """首页功能卡片 HTML 结构 (配合 Streamlit 按钮使用)"""
    return f"""
    <div class="feature-card-home">
        <div class="fc-icon">{icon}</div>
        <div class="fc-title">{title}</div>
        <div class="fc-desc">{desc}</div>
    </div>
    """
