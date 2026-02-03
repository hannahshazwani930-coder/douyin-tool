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

# --- CSS 样式配置 (拆分变量以防语法错误) ---

def inject_css(mode="app"):
    # 1. 基础样式
    base_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        html, body, [class*="css"] { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
        header[data-testid="stHeader"] { visibility: hidden; height: 0; }
        #MainMenu { visibility: hidden; }
        [data-testid="stSidebarCollapsedControl"] { display: none; }
        [data-testid="InputInstructions"] { display: none !important; }
    </style>
    """
    st.markdown(base_css, unsafe_allow_html=True)

    # 2. 登录页样式 (左右排版 + 极光)
    if mode == "auth":
        st.markdown("""
        <style>
            /* 极光背景动画 */
            .stApp {
                background: linear-gradient(-45deg, #020617, #0f172a, #1e3a8a, #172554);
                background-size: 400% 400%;
                animation: authGradient 15s ease infinite;
            }
            @keyframes authGradient { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }

            /* 布局容器：允许左右排版 */
            div.block-container {
                max-width: 1200px !important;
                padding-top: 8vh !important;
            }

            /* 左侧文案 */
            .hero-title { font-size: 48px; font-weight: 800; color: white; line-height: 1.2; margin-bottom: 20px; text-shadow: 0 4px 10px rgba(0,0,0,0.5); }
            .hero-sub { font-size: 18px; color: #cbd5e1; line-height: 1.6; margin-bottom: 40px; font-weight: 300; }
            .hero-tag { display:inline-block; background:rgba(37,99,235,0.2); color:#60a5fa; border:1px solid rgba(59,130,246,0.3); padding:5px 15px; border-radius:20px; font-size:12px; margin-right:10px; }

            /* 右侧登录卡片 (玻璃拟态) */
            .login-card-container {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 24px;
                padding: 40px;
                box-shadow: 0 25px 60px rgba(0,0,0,0.5);
                backdrop-filter: blur(20px);
            }

            /* 输入框 (标准样式，白底) */
            .stTextInput input {
                background-color: #f8fafc !important;
                color: #0f172a !important;
                border: 1px solid #cbd5e1 !important;
                border-radius: 8px !important;
                height: 45px !important;
            }
            .stTextInput input:focus { border-color: #3b82f6 !important; background: white !important; }
            
            /* 按钮 */
            div.stButton > button {
                width: 100%; height: 45px;
                background: linear-gradient(90deg, #2563eb, #3b82f6);
                color: white; border: none; border-radius: 8px; font-weight: 600;
            }
            div.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(37,99,235,0.4); }

            /* Tab 样式 */
            .stTabs [data-baseweb="tab-list"] { gap: 20px; border-bottom: 1px solid #e2e8f0 !important; margin-bottom: 20px; }
            .stTabs [data-baseweb="tab"] { height: 45px; color: #64748b; font-weight: 600; font-size: 15px; }
            .stTabs [aria-selected="true"] { color: #2563eb !important; border-bottom: 2px solid #2563eb !important; }

            [data-testid="stSidebar"] { display: none; }
        </style>
        """, unsafe_allow_html=True)

    # 3. 系统内页样式 (浅色 + 悬浮控制台)
    elif mode == "app":
        st.markdown("""
        <style>
            .stApp { background-color: #f8fafc; }
            [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; padding-top: 1rem; }
            div.block-container { max-width: 1400px !important; padding: 0 40px 50px 40px !important; }

            /* 文案改写页专用：浅色悬浮极光 Banner */
            .flowing-header {
                background: linear-gradient(-45deg, #1e3a8a, #2563eb, #3b82f6, #0ea5e9);
                background-size: 400% 400%; animation: gradientBG 10s ease infinite;
                border-bottom-left-radius: 40px; border-bottom-right-radius: 40px;
                padding: 50px 40px 100px 40px; color: white; text-align: center;
                margin-bottom: -70px; margin-left: -40px; margin-right: -40px;
                box-shadow: 0 20px 50px rgba(37, 99, 235, 0.3); position: relative; z-index: 0;
            }
            @keyframes gradientBG { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }

            /* 纯白一体化控制台 */
            .creation-console {
                background: white; border-radius: 24px; padding: 40px;
                box-shadow: 0 30px 60px -15px rgba(0,0,0,0.08); 
                border: 1px solid #e2e8f0; position: relative; z-index: 10; margin-top: 20px;
            }

            /* 内页输入框 (无叠影，白底) */
            .stTextArea > div { border: none !important; box-shadow: none !important; background: transparent !important; }
            .stTextArea > label { display: none !important; }
            .stTextArea textarea {
                background-color: #ffffff !important; border: 2px solid #e2e8f0 !important;
                border-radius: 12px; padding: 15px; font-size: 15px; line-height: 1.6; color: #334155;
            }
            .stTextArea textarea:focus { border-color: #3b82f6 !important; box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1) !important; }

            /* 按钮与标签 */
            .custom-label { font-size: 14px; font-weight: 700; color: #1e293b; margin-bottom: 8px; display: block; }
            div.stButton button[kind="primary"] {
                width: 100%; height: 48px !important; border: none !important;
                background: linear-gradient(90deg, #2563eb, #3b82f6) !important;
                color: white !important; border-radius: 10px !important; font-size: 16px !important;
                box-shadow: 0 8px 20px -5px rgba(37, 99, 235, 0.4) !important;
            }
            div.stButton button[kind="primary"]:hover { transform: translateY(-2px); }
            div.stButton button[kind="secondary"] { height: 48px !important; border: 1px solid #e2e8f0 !important; background: white !important; color: #64748b !important; font-weight: 600 !important; }
            
            /* 矩阵模式对齐 Info Box */
            .info-box { background: #eff6ff; border: 1px solid #bfdbfe; color: #1e40af; padding: 0 20px; border-radius: 10px; font-size: 15px; display: flex; align-items: center; gap: 10px; height: 48px; }
            
            /* 通用 Banner */
            .page-banner { background: linear-gradient(120deg, #2563eb, #1d4ed8); color: white; padding: 30px; border-radius: 16px; margin-bottom: 30px; box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.4); }
            .banner-title { font-size: 28px; font-weight: 800; margin-bottom: 10px; }
            .banner-desc { font-size: 15px; opacity: 0.9; line-height: 1.5; }
            
            /* 侧边栏菜单 */
            div[role="radiogroup"] label { padding: 10px 12px !important; border-radius: 8px !important; margin-bottom: 4px; border: 1px solid transparent; }
            div[role="radiogroup"] label:hover { background-color: #f1f5f9 !important; }
            div[role="radiogroup"] label[aria-checked="true"] { background-color: #eff6ff !important; color: #2563eb !important; border: 1px solid #bfdbfe; font-weight: 600 !important; }
            div[role="radiogroup"] > label > div:first-child { display: none !important; }
            
            /* 公告卡片 */
            .ann-card { background: #fff7ed; border: 1px solid #fed7aa; border-radius: 8px; padding: 12px 15px; margin-bottom: 10px; display: flex; align-items: start; gap: 10px; font-size: 14px; color: #9a3412; }
            
            /* 转化提示 */
            .conversion-tip { margin-top: 15px; background: #f0fdf4; border: 1px solid #bbf7d0; color: #166534; padding: 10px 15px; border-radius: 10px; font-size: 13px; display: flex; align-items: center; gap: 10px; }
        </style>
        """, unsafe_allow_html=True)

# --- 组件函数 (全部找回) ---

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

def render_home_project_card(icon, title, desc, tag):
    return f"""<div style="background:white;border-radius:12px;padding:20px;border:1px solid #e2e8f0;height:100%;display:flex;flex-direction:column;"><div style="font-size:16px;font-weight:700;color:#1e293b;margin-bottom:8px;"><span style="margin-right:8px;">{icon}</span>{title}</div><div style="font-size:12px;color:#64748b;line-height:1.5;flex-grow:1;">{desc}</div><div style="font-size:11px;padding:3px 8px;border-radius:10px;background:#f8fafc;color:#475569;margin-top:15px;width:fit-content;border:1px solid #e2e8f0;">{tag}</div></div>"""

def render_page_banner(title, desc):
    st.markdown(f"""<div class="page-banner"><div class="banner-title">{title}</div><div class="banner-desc">{desc}</div></div>""", unsafe_allow_html=True)

def render_conversion_tip():
    st.markdown("""<div class="conversion-tip"><span>💰</span><span><b>商业化建议：</b> 已自动植入私域钩子，预计提升 30% 导流效率。</span></div>""", unsafe_allow_html=True)

def render_feature_card_home(icon, title, desc):
    return f"""<div style="background:white;border:1px solid #e2e8f0;border-radius:12px;padding:15px;text-align:center;height:100px;display:flex;flex-direction:column;justify-content:center;align-items:center;"><div style="font-size:24px;margin-bottom:5px;">{icon}</div><div style="font-weight:700;color:#0f172a;">{title}</div></div>"""
