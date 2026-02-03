# main.py
import streamlit as st
import time
from config import ADMIN_ACCOUNT
from database import init_db, get_user_vip_status, login_user, register_user
from utils import inject_css, render_wechat_pill, render_sidebar_user_card

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
# 💎 登录 / 注册 页面
# ==========================================
def login_page():
    inject_css(mode="auth")
    
    col_left, col_right = st.columns([1.2, 1], gap="large")
    
    with col_left:
        st.markdown("<div style='padding-right: 20px; padding-top: 20px;'>", unsafe_allow_html=True)
        st.markdown('<div class="hero-decoration"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="hero-title">
            打造爆款<br>
            <span style="color: #3b82f6;">从未如此简单</span>
        </div>
        <div class="hero-subtitle">
            抖音爆款工场 Pro 是一站式 AI 创作工作台。<br>
            集成了文案改写、海报设计、选题挖掘等核心功能，<br>
            帮助企业和创作者高效产出优质内容。
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="display:flex; gap:15px; margin-top:30px;">
            <span style="background:#eff6ff; color:#3b82f6; padding:6px 12px; border-radius:20px; font-size:12px; font-weight:600;">🚀 极速生成</span>
            <span style="background:#eff6ff; color:#3b82f6; padding:6px 12px; border-radius:20px; font-size:12px; font-weight:600;">🔒 数据安全</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        
        tab_login, tab_register = st.tabs(["账号登录", "注册新号"])
        
        with tab_login:
            with st.form("login_form"):
                st.write("") 
                username = st.text_input("账号", placeholder="手机号 / 邮箱", label_visibility="collapsed")
                st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
                password = st.text_input("密码", type="password", placeholder="请输入密码", label_visibility="collapsed")
                
                st.markdown("<div style='height:25px'></div>", unsafe_allow_html=True)
                submit_login = st.form_submit_button("立即登录", use_container_width=True)
                
                if submit_login:
                    if not username or not password:
                        st.warning("⚠️ 请输入账号和密码")
                    else:
                        success, msg = login_user(username, password)
                        if success:
                            st.success("✅ 登录成功")
                            st.session_state['user_phone'] = username
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error(f"⛔ {msg}")

        with tab_register:
            with st.form("register_form"):
                st.write("")
                new_user = st.text_input("注册账号", placeholder="请输入手机号或邮箱", label_visibility="collapsed")
                st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
                new_pass = st.text_input("设置密码", type="password", placeholder="设置密码 (≥6位)", label_visibility="collapsed")
                st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
                confirm_pass = st.text_input("确认密码", type="password", placeholder="再次确认密码", label_visibility="collapsed")
                st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
                invite_input = st.text_input("邀请码", placeholder="邀请码 (默认888888)", label_visibility="collapsed")
                
                st.markdown("<div style='height:25px'></div>", unsafe_allow_html=True)
                submit_reg = st.form_submit_button("创建账号", use_container_width=True)
                
                if submit_reg:
                    final_invite_code = invite_input.strip() if invite_input.strip() else "888888"
                    if not new_user: st.warning("⚠️ 请输入账号")
                    elif len(new_pass) < 6: st.warning("⚠️ 密码太短")
                    elif new_pass != confirm_pass: st.error("⛔ 密码不一致")
                    else:
                        success, msg = register_user(new_user, new_pass, final_invite_code)
                        if success:
                            st.balloons()
                            st.success("✅ 注册成功！请切换登录")
                        else:
                            st.error(f"⛔ {msg}")
    
    st.markdown("""
    <div class="auth-footer">
        © 2026 抖音爆款工场 Pro System. All Rights Reserved.<br>
        <div style="margin-top: 8px;">
            <a href="#">用户协议</a> • <a href="#">隐私政策</a> • <a href="#">免责声明</a> • <a href="#">联系客服</a>
        </div>
        <div style="margin-top: 8px; color: #cbd5e1; font-size: 11px;">
            本系统仅供辅助创作使用，请遵守相关法律法规。
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 主程序逻辑 (侧边栏终极美化版) ---
def main():
    if 'user_phone' not in st.session_state:
        login_page()
    else:
        # 1. 首先注入系统 CSS (解决样式乱码的关键)
        inject_css("app")
        
        current_user = st.session_state['user_phone']
        is_vip, msg = get_user_vip_status(current_user)
        
        # 2. 侧边栏构建
        with st.sidebar:
            # 顶部 Logo 区域
            st.markdown("""
            <div style="display:flex; align-items:center; gap:10px; padding-bottom: 20px; border-bottom: 1px solid #f1f5f9; margin-bottom: 20px;">
                <div style="background:#2563eb; width:32px; height:32px; border-radius:8px; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold;">P</div>
                <div style="font-weight:700; font-size:18px; color:#0f172a;">爆款工场 Pro</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 用户信息卡片 (使用 utils 里的美化函数)
            render_sidebar_user_card(current_user, msg)
            
            # 导航菜单
            st.markdown("<div style='font-size:12px; font-weight:600; color:#94a3b8; margin-bottom:10px; margin-top:10px;'>功能导航</div>", unsafe_allow_html=True)
            
            menu_opts = ["🏠 首页", "📝 文案改写", "💡 爆款选题", "🎨 海报生成", "🏷️ 账号起名", "👤 个人中心"]
            if current_user == ADMIN_ACCOUNT: menu_opts.append("🕵️‍♂️ 管理后台")
            
            default_idx = 0
            if 'nav_menu_selection' in st.session_state:
                if st.session_state['nav_menu_selection'] in menu_opts:
                    default_idx = menu_opts.index(st.session_state['nav_menu_selection'])
                del st.session_state['nav_menu_selection']

            # 导航 Radio (已被 CSS 美化为按钮)
            nav = st.radio("导航", menu_opts, index=default_idx, label_visibility="collapsed")
            
            # 底部区域
            st.markdown("<div style='flex-grow:1;'></div>", unsafe_allow_html=True) # 占位撑开
            st.markdown("---")
            render_wechat_pill("🎁 客服支持", "W7774X")
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            if st.button("🚪 退出登录", use_container_width=True):
                del st.session_state['user_phone']
                st.rerun()

        # 3. 路由分发
        if nav == "🏠 首页": view_home()
        elif nav == "📝 文案改写": view_rewrite()
        elif nav == "💡 爆款选题": view_brainstorm()
        elif nav == "🎨 海报生成": view_poster()
        elif nav == "🏷️ 账号起名": view_naming()
        elif nav == "👤 个人中心": view_account()
        elif nav == "🕵️‍♂️ 管理后台": view_admin()

if __name__ == "__main__":
    main()
