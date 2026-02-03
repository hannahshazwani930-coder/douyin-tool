# main.py
import streamlit as st
import time
from config import ADMIN_ACCOUNT
from database import init_db, get_user_vip_status, login_user, register_user
from utils import inject_css, render_wechat_pill

# --- 导入视图 ---
from views.home import view_home
from views.rewrite import view_rewrite
from views.brainstorm import view_brainstorm
from views.poster import view_poster
from views.naming import view_naming
from views.account import view_account
from views.admin import view_admin

# --- 页面配置 ---
st.set_page_config(
    page_title="抖音爆款工场 Pro", 
    layout="wide",
    page_icon="💠",
    initial_sidebar_state="expanded"
)

# --- 初始化 ---
init_db()

# ==========================================
# 💎 终极美化版：登录 / 注册 页面
# ==========================================
def login_page():
    inject_css(mode="auth")
    
    # 垂直对齐调整：在顶部加一点点空白，让整体视觉垂直居中
    st.markdown("<div style='height: 5vh;'></div>", unsafe_allow_html=True)
    
    # 布局：左侧 (文案) 60% - 右侧 (登录框) 40%
    # 通过 gap="large" 增加间距
    col_left, col_right = st.columns([1.5, 1], gap="large")
    
    # --- 左侧：大气展示区 ---
    with col_left:
        # 增加一点左侧边距，使其不贴边
        st.markdown("<div style='margin-left: 20px; margin-top: 40px;'>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="hero-title">
            智能创作<br>
            <span style="color: #60a5fa;">触手可及</span>
        </div>
        <div class="hero-subtitle">
            专为创作者打造的 AI 工作台。<br>
            从灵感爆发到爆款落地，只需这一套系统。
        </div>
        """, unsafe_allow_html=True)
        
        # 极简功能列表
        st.markdown("""
        <div class="feature-item"><div class="feature-icon">✨</div> 深度学习爆款逻辑，一键改写</div>
        <div class="feature-item"><div class="feature-icon">🎨</div> 智能排版设计，秒出专业海报</div>
        <div class="feature-item"><div class="feature-icon">🔒</div> 企业级数据加密，安全无忧</div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    # --- 右侧：精致登录框 ---
    with col_right:
        # 这里的 Tab 标签文案精简
        tab_login, tab_register = st.tabs(["登录", "注册新号"])
        
        # === 登录模块 ===
        with tab_login:
            with st.form("login_form"):
                st.write("") # 顶部微小间距
                
                # 输入框：去除繁琐的 label，只保留核心提示
                username = st.text_input("账号", placeholder="手机号 / 邮箱", label_visibility="collapsed")
                st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True) # 手动间距
                password = st.text_input("密码", type="password", placeholder="请输入密码", label_visibility="collapsed")
                
                st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
                submit_login = st.form_submit_button("登 录", use_container_width=True)
                
                if submit_login:
                    if not username or not password:
                        st.warning("⚠️ 请输入账号和密码")
                    else:
                        success, msg = login_user(username, password)
                        if success:
                            st.success("✅ 欢迎回来")
                            st.session_state['user_phone'] = username
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error(f"⛔ {msg}")

        # === 注册模块 ===
        with tab_register:
            with st.form("register_form"):
                st.write("")
                
                # 1. 账号
                new_user = st.text_input("注册账号", placeholder="请输入手机号或邮箱", label_visibility="collapsed")
                st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
                
                # 2. 密码
                new_pass = st.text_input("设置密码", type="password", placeholder="设置密码 (≥6位)", label_visibility="collapsed")
                st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
                confirm_pass = st.text_input("确认密码", type="password", placeholder="再次确认密码", label_visibility="collapsed")
                st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
                
                # 3. 邀请码 (核心修改：默认显示提示词，逻辑自动处理)
                invite_input = st.text_input("邀请码", placeholder="邀请码 (选填，默认888888)", label_visibility="collapsed")
                
                st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
                submit_reg = st.form_submit_button("立即注册", use_container_width=True)
                
                if submit_reg:
                    # 逻辑：如果用户没填，就用 '888888'
                    final_invite_code = invite_input.strip() if invite_input.strip() else "888888"
                    
                    if not new_user:
                        st.warning("⚠️ 请输入账号")
                    elif not new_pass or len(new_pass) < 6:
                        st.warning("⚠️ 密码太短")
                    elif new_pass != confirm_pass:
                        st.error("⛔ 密码不一致")
                    else:
                        success, msg = register_user(new_user, new_pass, final_invite_code)
                        if success:
                            st.balloons()
                            st.success("✅ 注册成功！请切换登录")
                        else:
                            st.error(f"⛔ {msg}")

# --- 主程序逻辑 ---
def main():
    if 'user_phone' not in st.session_state:
        login_page()
    else:
        inject_css("app")
        with st.sidebar:
            current_user = st.session_state['user_phone']
            is_vip, msg = get_user_vip_status(current_user)
            
            st.markdown(f"**👤 {current_user}**")
            st.info(f"{msg}") if is_vip else st.warning("普通用户")
            
            # 导航菜单
            menu_opts = ["🏠 首页", "📝 文案改写", "💡 爆款选题", "🎨 海报生成", "🏷️ 账号起名", "👤 个人中心"]
            if current_user == ADMIN_ACCOUNT: menu_opts.append("🕵️‍♂️ 管理后台")
            
            # 处理跳转逻辑
            default_idx = 0
            if 'nav_menu_selection' in st.session_state:
                if st.session_state['nav_menu_selection'] in menu_opts:
                    default_idx = menu_opts.index(st.session_state['nav_menu_selection'])
                del st.session_state['nav_menu_selection']

            nav = st.radio("系统导航", menu_opts, index=default_idx, label_visibility="collapsed")
            
            st.markdown("---")
            if st.button("🚪 退出", use_container_width=True):
                del st.session_state['user_phone']
                st.rerun()

        # 路由分发
        if nav == "🏠 首页": view_home()
        elif nav == "📝 文案改写": view_rewrite()
        elif nav == "💡 爆款选题": view_brainstorm()
        elif nav == "🎨 海报生成": view_poster()
        elif nav == "🏷️ 账号起名": view_naming()
        elif nav == "👤 个人中心": view_account()
        elif nav == "🕵️‍♂️ 管理后台": view_admin()

if __name__ == "__main__":
    main()
