# main.py
import streamlit as st
import time
from config import ADMIN_ACCOUNT
from database import init_db, get_user_vip_status, login_user, register_user
from utils import inject_css, render_wechat_pill, render_sidebar_user_card, render_tech_support_btn

# --- 导入视图 ---
from views.home import view_home
from views.rewrite import view_rewrite
from views.brainstorm import view_brainstorm
from views.poster import view_poster
from views.naming import view_naming
from views.account import view_account
from views.admin import view_admin

st.set_page_config(page_title="抖音爆款工场 Pro", layout="wide", page_icon="💠", initial_sidebar_state="expanded")
init_db()

# ==========================================
# 🔐 登录页
# ==========================================
def login_page():
    inject_css(page_id="auth")
    
    col_left, col_right = st.columns([1.2, 1], gap="large")
    with col_left:
        st.markdown('<div class="auth-left-decor">', unsafe_allow_html=True)
        st.markdown("""
        <div class="hero-title">打造爆款<br><span style="color:#2563eb">从未如此简单</span></div>
        <div class="hero-sub">抖音爆款工场 Pro 是一站式 AI 创作工作台。<br>集成了文案改写、海报设计、选题挖掘等核心功能。</div>
        <div class="hero-tags"><span class="tag-pill">🚀 极速生成</span><span class="tag-pill">💡 爆款逻辑</span></div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown("<div style='padding-top:10px'></div>", unsafe_allow_html=True)
        tab_login, tab_register = st.tabs(["账号登录", "注册新号"])
        with tab_login:
            st.write("")
            with st.form("login_form"):
                username = st.text_input("账号", placeholder="手机号 / 邮箱")
                password = st.text_input("密码", type="password", placeholder="请输入密码")
                st.markdown("<div style='height:25px'></div>", unsafe_allow_html=True)
                submit_login = st.form_submit_button("立即登录", use_container_width=True)
                if submit_login:
                    if not username or not password: st.warning("⚠️ 请输入账号和密码")
                    else:
                        success, msg = login_user(username, password)
                        if success: st.success("✅ 登录成功"); st.session_state['user_phone'] = username; time.sleep(0.5); st.rerun()
                        else: st.error(f"⛔ {msg}")
        with tab_register:
            st.write("")
            with st.form("register_form"):
                new_user = st.text_input("注册账号", placeholder="手机号")
                new_pass = st.text_input("设置密码", type="password", placeholder="密码 (≥6位)")
                confirm_pass = st.text_input("确认密码", type="password", placeholder="再次确认")
                invite_input = st.text_input("邀请码", placeholder="邀请码 (默认888888)")
                st.markdown("<div style='height:25px'></div>", unsafe_allow_html=True)
                submit_reg = st.form_submit_button("创建账号", use_container_width=True)
                if submit_reg:
                    final_invite_code = invite_input.strip() if invite_input.strip() else "888888"
                    if not new_user: st.warning("⚠️ 请输入账号")
                    elif len(new_pass) < 6: st.warning("⚠️ 密码太短")
                    elif new_pass != confirm_pass: st.error("⛔ 密码不一致")
                    else:
                        success, msg = register_user(new_user, new_pass, final_invite_code)
                        if success: st.balloons(); st.success("✅ 注册成功！请切换登录");
                        else: st.error(f"⛔ {msg}")

# ==========================================
# 主程序
# ==========================================
def main():
    if 'user_phone' not in st.session_state:
        login_page()
    else:
        current_user = st.session_state['user_phone']
        is_vip, msg = get_user_vip_status(current_user)
        
        with st.sidebar:
            st.markdown("""<div style="display:flex; align-items:center; gap:8px; margin-bottom: 15px;"><div style="background:#2563eb; width:28px; height:28px; border-radius:6px; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold; font-size:16px;">P</div><div style="font-weight:700; font-size:16px; color:#0f172a;">爆款工场 Pro</div></div>""", unsafe_allow_html=True)
            render_sidebar_user_card(current_user, msg)
            
            menu_opts = ["🏠 首页", "📝 文案改写", "💡 爆款选题", "🎨 海报生成", "🏷️ 账号起名", "👤 个人中心"]
            if current_user == ADMIN_ACCOUNT: menu_opts.append("🕵️‍♂️ 管理后台")
            
            default_idx = 0
            if 'nav_menu_selection' in st.session_state:
                target = st.session_state['nav_menu_selection']
                if target in menu_opts: default_idx = menu_opts.index(target)
                del st.session_state['nav_menu_selection']

            nav = st.radio("导航", menu_opts, index=default_idx, label_visibility="collapsed")
            
            st.markdown("<div style='flex-grow:1; min-height: 20px;'></div>", unsafe_allow_html=True)
            st.markdown("---")
            render_tech_support_btn("TG777188")
            if st.button("🚪 退出登录", use_container_width=True):
                del st.session_state['user_phone']
                st.rerun()

        # 🔴 每一个页面都拥有独立的 CSS ID
        if nav == "🏠 首页":
            inject_css("home")
            view_home()
        elif nav == "📝 文案改写":
            inject_css("rewrite")
            view_rewrite()
        elif nav == "💡 爆款选题":
            inject_css("brainstorm") # 独立 ID
            view_brainstorm()
        elif nav == "🎨 海报生成":
            inject_css("poster") # 独立 ID
            view_poster()
        elif nav == "🏷️ 账号起名":
            inject_css("naming") # 独立 ID
            view_naming()
        elif nav == "👤 个人中心":
            inject_css("account") # 独立 ID
            view_account()
        elif nav == "🕵️‍♂️ 管理后台":
            inject_css("admin") # 独立 ID
            view_admin()

if __name__ == "__main__":
    main()
