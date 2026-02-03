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
        
        /* 隐藏 Streamlit 原生组件 */
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
    # 🏠 [LOCKED] 首页 - 绝对锁死 (这是您满意的版本)
    # ============================================================
    elif page_id == "home":
        st.markdown("""
        <style>
            .stApp { background-color: #f8fafc; }
            
            /* 1. 容器：背景透明 + 顶部去白框 */
            div[data-testid="block-container"] { 
                max-width: 1200px !important; 
                padding-top: 0px !important; /* 核心：去掉顶部padding */
                padding-left: 40px !important;
                padding-right: 40px !important;
                margin-top: 20px !important; 
                background-color: transparent !important; /* 核心：背景透明 */
            }
            div[data-testid="stAppViewContainer"] { background-color: #f8fafc !important; }

            /* 2. 悬浮岛头图 */
            .home-header-card {
                background: linear-gradient(120deg, #2563eb, #1d4ed8);
                border-radius: 20px;
                padding: 50px 40px;
                text-align: center; color: white;
                box-shadow: 0 15px 40px -10px rgba(37, 99, 235, 0.4); 
                margin-bottom: 30px;
                position: relative; overflow: hidden;
            }
            .home-header-card::before {
                content: ""; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
                background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
                animation: rotateLight 20s linear infinite;
            }
            @keyframes rotateLight { from {transform: rotate(0deg);} to {transform: rotate(360deg);} }
            .header-title { font-size: 36px; font-weight: 800; margin-bottom: 10px; position: relative; z-index: 2; }
            .header-sub { font-size: 15px; opacity: 0.95; font-weight: 400; position: relative; z-index: 2; }

            /* 3. 栏目标题 */
            .section-label { 
                font-size: 18px; font-weight: 800; color: #1e293b; 
                margin-bottom: 15px; display: flex; align-items: center; gap: 8px; 
            }
            .section-label::before { content: ""; display: block; width: 4px; height: 18px; background: #3b82f6; border-radius: 2px; }

            /* 4. 核心功能卡片 */
            .feature-card-pro {
                background: white; border: 1px solid #e2e8f0; border-radius: 16px;
                padding: 25px 20px; text-align: center; height: 160px;
                display: flex; flex-direction: column; align-items: center; justify-content: center;
                transition: all 0.3s ease; position: relative; overflow: hidden;
            }
            .feature-card-pro:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 25px -5px rgba(0,0,0,0.08);
                border-color: #bfdbfe;
            }
            .feat-icon { font-size: 32px; margin-bottom: 12px; } 
            .feat-title { font-size: 15px; font-weight: 700; color: #1e293b; margin-bottom: 6px; }
            .feat-desc { font-size: 12px; color: #64748b; line-height: 1.4; }

            /* 5. 系统公告 */
            .news-container {
                background: white; border: 1px solid #fed7aa; border-radius: 12px;
                padding: 12px 15px; display: flex; align-items: center; gap: 15px;
                box-shadow: 0 4px 10px -2px rgba(249, 115, 22, 0.1);
                margin-bottom: 30px;
            }
            .news-badge { 
                background: #fff7ed; color: #ea580c; font-size: 11px; font-weight: 800; 
                padding: 3px 8px; border-radius: 4px; border: 1px solid #ffedd5; flex-shrink: 0;
            }
            .news-content { font-size: 14px; color: #334155; font-weight: 500; }
            
            /* 隐形按钮 */
            div.stButton button { width: 100%; height: 100%; position: absolute; top: 0; left: 0; background: transparent; color: transparent; border: none; z-index: 5; }
            div.stButton button:hover { background: transparent; }
        </style>
        """, unsafe_allow_html=True)

    # ============================================================
    # 📝 [NEW] 文案改写页 (Rewrite) - 独立设计
    # ============================================================
    elif page_id == "rewrite":
        st.markdown("""
        <style>
            /* 1. 基础环境 */
            .stApp, div[data-testid="stAppViewContainer"] { 
                background-color: #f8fafc !important; 
            }
            div[data-testid="block-container"] { 
                background-color: transparent !important; 
                max-width: 1300px !important; 
                padding-top: 0px !important; /* 关键：去白框 */
                padding-left: 40px !important; 
                padding-right: 40px !important; 
                margin-top: 20px !important; 
            }

            /* 2. 顶部头图 (复刻首页) */
            .rewrite-header-card {
                background: linear-gradient(120deg, #2563eb, #1d4ed8);
                border-radius: 20px; 
                padding: 40px 30px; 
                text-align: center; color: white;
                box-shadow: 0 15px 40px -10px rgba(37, 99, 235, 0.4); 
                margin-bottom: 30px; 
                position: relative; overflow: hidden;
            }
            .rewrite-header-card::before {
                content: ""; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
                background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
                animation: rotateLight 20s linear infinite;
            }
            @keyframes rotateLight { from {transform: rotate(0deg);} to {transform: rotate(360deg);} }
            
            .rw-title { font-size: 32px; font-weight: 800; margin-bottom: 8px; position: relative; z-index: 2; }
            .rw-sub { font-size: 14px; opacity: 0.9; font-weight: 400; position: relative; z-index: 2; }

            /* 3. 工作台区域 */
            .rewrite-workstation {
                background: white;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
                padding: 30px;
                margin-bottom: 30px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            }
            
            /* 4. 输入框/输出框美化 */
            .stTextArea textarea {
                border: 1px solid #cbd5e1 !important;
                background-color: #f8fafc !important;
                border-radius: 8px !important;
                font-size: 15px !important;
                padding: 15px !important;
            }
            .stTextArea textarea:focus {
                border-color: #3b82f6 !important;
                background-color: white !important;
                box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.15) !important;
            }
            .stTextArea label { font-weight: 600; color: #334155; }
            
            /* 5. 按钮美化 */
            div.stButton button[kind="primary"] {
                width: 100%; border-radius: 8px; font-weight: 600;
                background: linear-gradient(90deg, #2563eb, #3b82f6); border: none; height: 42px;
                box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
            }
            div.stButton button[kind="primary"]:hover { transform: translateY(-2px); }
            
            div.stButton button[kind="secondary"] {
                width: 100%; border-radius: 8px; border: 1px solid #e2e8f0; color: #475569; height: 42px;
            }
        </style>
        """, unsafe_allow_html=True)

    # ----------------------------------------------------------------
    # 🔒 [LOCKED] 其他页面 (General/Admin) - 保持原样
    # ----------------------------------------------------------------
    elif page_id == "general":
        st.markdown("""<style>.stApp { background-color: #f8fafc; } div.block-container { max-width: 1200px !important; padding: 2rem 40px 50px 40px !important; } .page-banner { background: linear-gradient(120deg, #2563eb, #1d4ed8); color: white; padding: 30px; border-radius: 16px; margin-bottom: 30px; box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.4); } .banner-title { font-size: 28px; font-weight: 800; margin-bottom: 10px; } .banner-desc { font-size: 15px; opacity: 0.9; line-height: 1.5; } div[data-testid="stVerticalBlock"] > div { background: transparent; } .stButton > button { border-radius: 8px; font-weight: 600; border: none; } </style>""", unsafe_allow_html=True)
    elif page_id == "admin":
        st.markdown("""<style>.stApp { background-color: #f1f5f9; } [data-testid="stSidebar"] { background-color: #1e293b; border-right: 1px solid #334155; padding-top: 1rem; } [data-testid="stSidebar"] * { color: #e2e8f0 !important; } div[role="radiogroup"] label { padding: 10px 12px !important; border-radius: 8px !important; margin-bottom: 4px; border: 1px solid transparent; } div[role="radiogroup"] label:hover { background-color: #334155 !important; } div[role="radiogroup"] label[aria-checked="true"] { background-color: #3b82f6 !important; color: white !important; border: 1px solid #60a5fa; font-weight: 600 !important; } div[role="radiogroup"] > label > div:first-child { display: none !important; } div.block-container { max-width: 1600px !important; padding: 2rem 40px 50px 40px !important; } .page-banner { background: linear-gradient(120deg, #1e293b, #0f172a); color: white; padding: 30px; border-radius: 16px; margin-bottom: 30px; box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.4); } .banner-title { font-size: 28px; font-weight: 800; margin-bottom: 10px; } .banner-desc { font-size: 15px; opacity: 0.9; line-height: 1.5; } </style>""", unsafe_allow_html=True)

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

# 🔴 [CRITICAL FIX] 确保函数名为 render_project_card，避免首页报错
# 同时保持无乱码、高度压缩的 190px 设计
def render_project_card(icon, title, desc, wx_id):
    safe_text = wx_id.replace("'", "\\'")
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        body {{
            margin: 0; padding: 0;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI Emoji", "Apple Color Emoji", sans-serif;
            overflow: hidden;
            box-sizing: border-box;
        }}
        .card-container {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            display: flex; flex-direction: column; justify-content: space-between;
            height: 190px;
            transition: all 0.3s ease;
            cursor: pointer; position: relative; overflow: hidden;
        }}
        .card-container:hover {{ border-color: #bfdbfe; box-shadow: 0 15px 30px -5px rgba(59, 130, 246, 0.1); transform: translateY(-4px); }}
        .card-content {{ padding: 18px 18px 10px 18px; }}
        .header {{ display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }}
        .icon {{ font-size: 22px; }}
        .title {{ font-size: 15px; font-weight: 700; color: #0f172a; margin: 0; }}
        .desc {{ font-size: 12px; color: #64748b; line-height: 1.4; margin: 0; }}
        
        .action-btn {{
            background-color: #ecfdf5; color: #059669; width: 100%; padding: 10px 0;
            text-align: center; font-size: 12px; font-weight: 600; border-top: 1px solid #e2e8f0;
            transition: all 0.2s; display: flex; align-items: center; justify-content: center; gap: 6px;
        }}
        .card-container:hover .action-btn {{ background-color: #10b981; color: white; border-color: #10b981; }}
        .action-btn:active {{ background-color: #059669; }}
    </style>
    </head>
    <body>
        <div class="card-container" onclick="copyAction()">
            <div class="card-content">
                <div class="header">
                    <span class="icon">{icon}</span>
                    <span class="title">{title}</span>
                </div>
                <div class="desc">{desc}</div>
            </div>
            <div class="action-btn" id="btn-text">
                <span>📋</span> 复制微信领取资料 ({wx_id})
            </div>
        </div>
        <script>
            function copyAction() {{
                const text = "{safe_text}";
                navigator.clipboard.writeText(text).then(() => {{
                    const btn = document.getElementById('btn-text');
                    const originalHTML = btn.innerHTML;
                    btn.innerHTML = '✅ 已复制！请去微信添加';
                    btn.style.backgroundColor = '#10b981'; btn.style.color = 'white';
                    setTimeout(() => {{ btn.innerHTML = originalHTML; btn.style.backgroundColor = ''; btn.style.color = ''; }}, 2000);
                }}).catch(err => {{ alert('复制失败: ' + text); }});
            }}
        </script>
    </body>
    </html>
    """
    components.html(html, height=200)
