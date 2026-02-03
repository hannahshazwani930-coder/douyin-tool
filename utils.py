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

# ==============================================================================
# 🎨 页面级样式隔离系统 (CSS Router)
# ==============================================================================

def inject_css(page_id="auth"):
    # 1. 全局基础
    base_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        html, body, [class*="css"] { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
        
        /* 隐藏原生头部 */
        header[data-testid="stHeader"] { display: none !important; height: 0 !important; visibility: hidden !important; }
        [data-testid="stToolbar"] { display: none !important; }
        [data-testid="stDecoration"] { display: none !important; }
        #MainMenu { display: none !important; }
        
        /* 侧边栏 */
        [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; padding-top: 1rem; }
        div[role="radiogroup"] label { padding: 10px 12px !important; border-radius: 8px !important; margin-bottom: 4px; border: 1px solid transparent; }
        div[role="radiogroup"] label:hover { background-color: #f1f5f9 !important; }
        div[role="radiogroup"] label[aria-checked="true"] { background-color: #eff6ff !important; color: #2563eb !important; border: 1px solid #bfdbfe; font-weight: 600 !important; }
        div[role="radiogroup"] > label > div:first-child { display: none !important; }
    </style>
    """
    st.markdown(base_css, unsafe_allow_html=True)

    # ----------------------------------------------------------------
    # 🔒 [LOCKED] 登录页
    # ----------------------------------------------------------------
    if page_id == "auth":
        st.markdown("""
        <style>
            .stApp { background: linear-gradient(-45deg, #020617, #0f172a, #1e3a8a, #172554); background-size: 400% 400%; animation: authGradient 15s ease infinite; }
            @keyframes authGradient { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
            div.block-container { background-color: rgba(255, 255, 255, 0.98); border-radius: 24px; box-shadow: 0 30px 80px rgba(0,0,0,0.6); padding: 60px 50px !important; max-width: 1100px !important; margin: auto; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); overflow: hidden; }
            .auth-left-decor { border-right: 1px solid #f1f5f9; padding-right: 40px; height: 100%; display: flex; flex-direction: column; justify-content: center; }
            .hero-title { font-size: 42px; font-weight: 800; color: #0f172a; line-height: 1.2; margin-bottom: 20px; letter-spacing: -1px; }
            .hero-sub { font-size: 16px; color: #64748b; line-height: 1.6; margin-bottom: 30px; }
            .hero-tags { display: flex; gap: 10px; }
            .tag-pill { background: #eff6ff; color: #2563eb; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }
            .stTextInput div[data-baseweb="input"] { background-color: #f8fafc !important; border: 1px solid #cbd5e1 !important; border-radius: 8px !important; height: 48px !important; padding: 0 !important; }
            .stTextInput input { background-color: transparent !important; border: none !important; color: #1e293b !important; height: 48px !important; padding: 0 15px !important; }
            .stTextInput div[data-baseweb="input"]:focus-within { border-color: #3b82f6 !important; background-color: #ffffff !important; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important; }
            .stTextInput div[data-baseweb="input"] > div { background-color: transparent !important; }
            div.stButton > button { width: 100%; height: 48px; background: linear-gradient(90deg, #2563eb, #3b82f6); color: white; border: none; border-radius: 8px; font-weight: 600; }
            div.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(37,99,235,0.3); }
            .stTabs [data-baseweb="tab-list"] { gap: 20px; border-bottom: 1px solid #f1f5f9 !important; margin-bottom: 25px; }
            .stTabs [data-baseweb="tab"] { height: 45px; color: #64748b; font-weight: 600; }
            .stTabs [aria-selected="true"] { color: #2563eb !important; border-bottom: 3px solid #2563eb !important; }
            [data-testid="stSidebar"] { display: none; }
        </style>
        """, unsafe_allow_html=True)

    # ============================================================
    # 🏠 [NEW] 首页 - 垂直压缩修复版
    # ============================================================
    elif page_id == "home":
        st.markdown("""
        <style>
            .stApp { background-color: #f8fafc; }
            
            /* 1. 容器清零 */
            div[data-testid="block-container"] { 
                max-width: 1200px !important; 
                padding-top: 0px !important;
                padding-left: 40px !important;
                padding-right: 40px !important;
                margin-top: 0px !important;
            }
            
            /* 🔴 2. 消除组件垂直间距 (关键修复) */
            /* 这行代码会强制让头图和下方的白色面板紧紧贴在一起，消灭缝隙 */
            div[data-testid="stVerticalBlock"] { gap: 0 !important; }
            
            /* 3. 悬浮岛头图 */
            .home-header-card {
                background: linear-gradient(120deg, #2563eb, #1d4ed8);
                border-radius: 20px; padding: 50px 40px; text-align: center; color: white;
                box-shadow: 0 15px 40px -10px rgba(37, 99, 235, 0.4); 
                margin-top: 20px;
                /* 🔴 增加底部负边距，让下面的元素被吸上来 */
                margin-bottom: -30px; 
                position: relative; overflow: hidden; z-index: 1;
            }
            .home-header-card::before {
                content: ""; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
                background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
                animation: rotateLight 20s linear infinite;
            }
            @keyframes rotateLight { from {transform: rotate(0deg);} to {transform: rotate(360deg);} }
            .header-title-v3 { font-size: 36px; font-weight: 800; margin-bottom: 10px; position: relative; z-index: 2; }
            .header-sub-v3 { font-size: 15px; opacity: 0.95; font-weight: 400; position: relative; z-index: 2; }

            /* 4. 白色控制台 (核心功能区容器) */
            .creation-console {
                background: white; border-radius: 24px; 
                padding: 40px; 
                /* 🔴 向上提拉，覆盖可能存在的白条，并制造层级感 */
                margin-top: 0px; 
                position: relative; z-index: 2; /* 层级高于头图，确保盖住 */
                box-shadow: 0 -10px 40px -10px rgba(0,0,0,0.05); /* 顶部阴影 */
            }

            /* 核心功能 */
            .feature-box-v3 {
                background: white; border: 1px solid #e2e8f0; border-radius: 16px;
                padding: 25px 20px; text-align: center; height: 160px;
                display: flex; flex-direction: column; align-items: center; justify-content: center;
                transition: all 0.3s ease; position: relative; overflow: hidden;
            }
            .feature-box-v3:hover { transform: translateY(-5px); box-shadow: 0 10px 25px -5px rgba(0,0,0,0.08); border-color: #bfdbfe; }
            .feat-icon-v3 { font-size: 32px; margin-bottom: 12px; } 
            .feat-title-v3 { font-size: 15px; font-weight: 700; color: #1e293b; margin-bottom: 6px; }
            .feat-desc-v3 { font-size: 12px; color: #64748b; line-height: 1.4; }

            /* 公告 */
            .news-box-v3 {
                background: white; border: 1px solid #fed7aa; border-radius: 12px;
                padding: 12px 15px; display: flex; align-items: center; gap: 15px;
                box-shadow: 0 4px 10px -2px rgba(249, 115, 22, 0.1); margin-bottom: 30px;
            }
            .news-tag-v3 { background: #fff7ed; color: #ea580c; font-size: 11px; font-weight: 800; padding: 3px 8px; border-radius: 4px; border: 1px solid #ffedd5; flex-shrink: 0; }
            .news-text-v3 { font-size: 14px; color: #334155; font-weight: 500; }

            /* 标题 */
            .section-title-v3 { font-size: 18px; font-weight: 800; color: #1e293b; margin-bottom: 15px; display: flex; align-items: center; gap: 8px; }
            .section-title-v3::before { content: ""; display: block; width: 4px; height: 18px; background: #3b82f6; border-radius: 2px; }
            div.stButton button { width: 100%; height: 100%; position: absolute; top: 0; left: 0; background: transparent; color: transparent; border: none; z-index: 10; }
            div.stButton button:hover { background: transparent; }

            /* 变现项目 V7 (无乱码纯净版) */
            .proj-card-v7 {
                background: white; border-radius: 16px; border: 1px solid #e2e8f0;
                padding: 24px; height: 100%; display: flex; flex-direction: column;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }
            .proj-card-v7:hover { transform: translateY(-5px); box-shadow: 0 15px 30px -5px rgba(0,0,0,0.08); border-color: #3b82f6; }
            .pure-head { display: flex; align-items: center; gap: 12px; margin-bottom: 15px; }
            .pure-icon { font-size: 24px; }
            .pure-title { font-size: 16px; font-weight: 700; color: #0f172a; }
            .pure-desc { font-size: 13px; color: #64748b; line-height: 1.6; flex-grow: 1; margin-bottom: 20px; }
            .pure-footer {
                margin-top: auto; padding-top: 15px; border-top: 1px dashed #e2e8f0;
                color: #64748b; font-size: 12px; display: flex; align-items: center; gap: 6px; font-family: monospace;
            }
            .footer-icon { font-size: 14px; }
        </style>
        """, unsafe_allow_html=True)

    # ----------------------------------------------------------------
    # 🔒 [LOCKED] 文案改写页
    # ----------------------------------------------------------------
    elif page_id == "rewrite":
        st.markdown("""
        <style>
            .stApp { background-color: #f8fafc; }
            div.block-container { max-width: 1400px !important; padding: 0 40px 50px 40px !important; margin-top: 0 !important; }
            .flowing-header {
                background: linear-gradient(-45deg, #1e3a8a, #2563eb, #3b82f6, #0ea5e9); background-size: 400% 400%; animation: gradientBG 10s ease infinite;
                border-bottom-left-radius: 40px; border-bottom-right-radius: 40px;
                padding: 60px 40px 180px 40px; color: white; text-align: center;
                margin: -60px -40px -100px -40px; box-shadow: 0 20px 50px rgba(37, 99, 235, 0.3); position: relative; z-index: 0;
            }
            @keyframes gradientBG { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
            .header-title { font-size: 42px; font-weight: 900; letter-spacing: -1px; margin-bottom: 8px; text-shadow: 0 4px 10px rgba(0,0,0,0.2); }
            .header-sub { font-size: 15px; opacity: 0.95; background: rgba(255,255,255,0.1); padding: 5px 15px; border-radius: 30px; backdrop-filter: blur(10px); display: inline-block; border: 1px solid rgba(255,255,255,0.2); }
            div.stButton button[kind="primary"], div.stButton button[kind="secondary"] { position: relative; z-index: 20; }
            .creation-console {
                background: white; border-radius: 24px; padding: 10px 40px 40px 40px;
                box-shadow: 0 30px 60px -15px rgba(0,0,0,0.08); border: 1px solid #e2e8f0; 
                position: relative; z-index: 10; margin-top: -50px; 
            }
            .stTextArea > div { border: none !important; box-shadow: none !important; background: transparent !important; }
            .stTextArea > label { display: none !important; }
            .stTextArea textarea { background-color: #ffffff !important; border: 2px solid #e2e8f0 !important; border-radius: 12px; padding: 15px; font-size: 15px; line-height: 1.6; color: #334155; }
            .stTextArea textarea:focus { border-color: #3b82f6 !important; box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1) !important; }
            .custom-label { font-size: 14px; font-weight: 700; color: #1e293b; margin-bottom: 8px; display: block; }
            div[data-baseweb="select"] > div { height: 48px !important; border-radius: 10px !important; background-color: #f8fafc; }
            div.stButton button[kind="primary"] { width: 100%; height: 48px !important; border: none !important; background: linear-gradient(90deg, #2563eb, #3b82f6) !important; color: white !important; border-radius: 10px !important; font-size: 16px !important; box-shadow: 0 8px 20px -5px rgba(37, 99, 235, 0.4) !important; }
            div.stButton button[kind="primary"]:hover { transform: translateY(-2px); }
            div.stButton button[kind="secondary"] { height: 48px !important; border: 1px solid #e2e8f0 !important; background: white !important; color: #64748b !important; font-weight: 600 !important; }
            .info-box { background: #eff6ff; border: 1px solid #bfdbfe; color: #1e40af; padding: 0 20px; border-radius: 10px; font-size: 15px; display: flex; align-items: center; gap: 10px; height: 48px; }
            .conversion-tip { margin-top: 15px; background: #f0fdf4; border: 1px solid #bbf7d0; color: #166534; padding: 10px 15px; border-radius: 10px; font-size: 13px; display: flex; align-items: center; gap: 10px; }
        </style>
        """, unsafe_allow_html=True)

    # ----------------------------------------------------------------
    # 🔒 [LOCKED] 其他页面
    # ----------------------------------------------------------------
    elif page_id == "general":
        st.markdown("""
        <style>
            .stApp { background-color: #f8fafc; }
            div.block-container { max-width: 1200px !important; padding: 2rem 40px 50px 40px !important; }
            .page-banner { background: linear-gradient(120deg, #2563eb, #1d4ed8); color: white; padding: 30px; border-radius: 16px; margin-bottom: 30px; box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.4); }
            .banner-title { font-size: 28px; font-weight: 800; margin-bottom: 10px; }
            .banner-desc { font-size: 15px; opacity: 0.9; line-height: 1.5; }
            div[data-testid="stVerticalBlock"] > div { background: transparent; }
            .stButton > button { border-radius: 8px; font-weight: 600; border: none; }
        </style>
        """, unsafe_allow_html=True)

    # ----------------------------------------------------------------
    # 🔒 [LOCKED] 管理后台
    # ----------------------------------------------------------------
    elif page_id == "admin":
        st.markdown("""
        <style>
            .stApp { background-color: #f1f5f9; }
            [data-testid="stSidebar"] { background-color: #1e293b; border-right: 1px solid #334155; padding-top: 1rem; }
            [data-testid="stSidebar"] * { color: #e2e8f0 !important; }
            div[role="radiogroup"] label { padding: 10px 12px !important; border-radius: 8px !important; margin-bottom: 4px; border: 1px solid transparent; }
            div[role="radiogroup"] label:hover { background-color: #334155 !important; }
            div[role="radiogroup"] label[aria-checked="true"] { background-color: #3b82f6 !important; color: white !important; border: 1px solid #60a5fa; font-weight: 600 !important; }
            div[role="radiogroup"] > label > div:first-child { display: none !important; }
            div.block-container { max-width: 1600px !important; padding: 2rem 40px 50px 40px !important; }
            .page-banner { background: linear-gradient(120deg, #1e293b, #0f172a); color: white; padding: 30px; border-radius: 16px; margin-bottom: 30px; box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.4); }
            .banner-title { font-size: 28px; font-weight: 800; margin-bottom: 10px; }
            .banner-desc { font-size: 15px; opacity: 0.9; line-height: 1.5; }
        </style>
        """, unsafe_allow_html=True)

# --- 组件函数 ---
def render_sidebar_user_card(username, vip_info):
    status_bg = "#eff6ff" if "VIP" in vip_info or "管理员" in vip_info else "#f1f5f9"
    st.sidebar.markdown(f"""<div style="background: {status_bg}; border: 1px solid #e2e8f0; border-radius: 12px; padding: 15px; margin-bottom: 20px;"><div style="display:flex; align-items:center; margin-bottom: 8px;"><div style="width: 32px; height: 32px; background: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 16px; margin-right: 10px; border: 1px solid #e2e8f0;">👤</div><div style="font-weight: 700; color: #0f172a; font-size: 14px; overflow: hidden; text-overflow: ellipsis;">{username}</div></div><div style="background: white; padding: 6px 10px; border-radius: 6px; font-size: 12px; color: #2563eb; font-weight: 600; border: 1px solid #e2e8f0; text-align: center;">{vip_info}</div></div>""", unsafe_allow_html=True)

def render_tech_support_btn(wx_id):
    st.sidebar.markdown(f"""<div onclick="navigator.clipboard.writeText('{wx_id}');alert('已复制')" style="width: 100%; text-align: center; background: white; border: 1px solid #e2e8f0; color: #334155; font-weight: 600; padding: 10px 0; border-radius: 8px; cursor: pointer; font-size: 14px; margin-bottom: 10px;">🤝 技术合作: {wx_id}</div>""", unsafe_allow_html=True)

def render_copy_btn(text, key_suffix):
    safe_text = text.replace("`", "\`").replace("'", "\\'")
    html = f"""<script>function copy_{key_suffix}(){{navigator.clipboard.writeText(`{safe_text}`);}}</script><button onclick="copy_{key_suffix}();this.innerText='✅ 已复制';setTimeout(()=>this.innerText='📋 一键复制',2000)" style="width:100%; height:40px; background:#0f172a; color:white; border:none; border-radius:8px; cursor:pointer; font-weight:600; font-family:'Inter'; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">📋 一键复制</button>"""
    components.html(html, height=50)

def render_wechat_pill(label, wx_id):
    components.html(f"""<div style="display:flex;justify-content:space-between;align-items:center;background:white;border:1px solid #e2e8f0;border-radius:6px;padding:0 10px;height:34px;cursor:pointer;font-family:'Inter',sans-serif;font-size:12px;color:#334155;" onclick="navigator.clipboard.writeText('{wx_id}')"><span style="font-weight:600">{label}</span><span style="color:#059669;font-family:monospace;background:#ecfdf5;padding:2px 6px;border-radius:4px;">📋 {wx_id}</span></div>""", height=40)

def render_cta_wechat(wx_id):
    html = f"""<div style="padding:10px;"><div style="background:linear-gradient(90deg,#059669,#10b981);color:white;border-radius:12px;padding:15px 25px;display:flex;align-items:center;justify-content:space-between;cursor:pointer;box-shadow:0 5px 15px rgba(16,185,129,0.4);font-family:'Inter',sans-serif;" onclick="navigator.clipboard.writeText('{wx_id}');alert('微信号 {wx_id} 已复制！')"><div style="display:flex;align-items:center;"><div style="font-size:24px;margin-right:15px;">🎁</div><div><span style="font-size:16px;font-weight:700;display:block;">领取内部资料 & 项目白皮书</span><span style="font-size:13px;opacity:0.9;">添加微信，备注【资料】</span></div></div><div style="background:rgba(255,255,255,0.2);padding:5px 12px;border-radius:20px;font-size:13px;font-weight:600;font-family:monospace;">📋 {wx_id}</div></div></div>"""
    components.html(html, height=100)

def render_home_project_card(icon, title, desc, tag): return ""
def render_page_banner(title, desc): st.markdown(f"""<div class="page-banner"><div class="banner-title">{title}</div><div class="banner-desc">{desc}</div></div>""", unsafe_allow_html=True)
def render_conversion_tip(): st.markdown("""<div class="conversion-tip"><span>💰</span><span><b>商业化建议：</b> 已自动植入私域钩子，预计提升 30% 导流效率。</span></div>""", unsafe_allow_html=True)
def render_feature_card_home(icon, title, desc): return ""

# 🔴 纯 HTML 渲染卡片 (无乱码，无交互，纯展示)
def render_pure_html_card(icon, title, desc, wx_id):
    html = f"""
    <div class="proj-card-v7">
        <div class="pure-head">
            <span class="pure-icon">{icon}</span>
            <span class="pure-title">{title}</span>
        </div>
        <div class="pure-desc">{desc}</div>
        <div class="pure-footer">
            <span class="footer-icon">📋</span>
            <span>资料领取: {wx_id}</span>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
