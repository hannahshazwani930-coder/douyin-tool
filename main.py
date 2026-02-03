# main.py
import streamlit as st
import time
from config import ADMIN_ACCOUNT
from database import init_db, get_user_vip_status, login_user, register_user
# 确保导入了 utils 中修复后的所有函数
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
# 🔐 登录 / 注册 页面
# ==========================================
def login_page():
    # 🟢 关键：注入 Auth 模式的 CSS，确保登录页样式独立
    inject_css(mode="auth")
    
    # 使用简单居中布局，配合 auth_css 实现卡片效果
    _, col_main, _ = st.columns([1, 2, 1])
    
    with col_main:
        st.markdown("<br><br>", unsafe_allow_html=True)
        # 头部标题
        st.markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: white; margin-bottom: 10px;">抖音爆款工场 Pro</h1>
            <p style="color: #cbd5e1; font-size: 16px;">全流程 AI 创作工作台 · 赋能内容生产</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 登录框容器 (白色背景由 CSS 控制)
        tab_login, tab_register = st.tabs(["账号登录", "注册新号"])
        
        with tab_login:
            with st.form("login_form"):
                st.write("") 
                username = st.text_input("账号", placeholder="手机号 / 邮箱", label_visibility="collapsed")
                st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
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
                new_user = st.text_input("注册账号", placeholder="手机号", label_visibility="collapsed")
                st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
                new_pass = st.text_input("设置密码", type="password", placeholder="密码 (≥6位)", label_visibility="collapsed")
                st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
                confirm_pass = st.text_input("确认密码", type="password", placeholder="确认密码", label_visibility="collapsed")
                st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
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
                        if success: st.balloons(); st.success("✅ 注册成功！请切换到登录页。");
                        else: st.error(f"⛔ {msg}")

# ==========================================
# 💠 主程序逻辑
# ==========================================
def main():
    if 'user_phone' not in st.session_state:
        login_page()
    else:
        # 🟢 关键：注入 App 模式的 CSS (流光效果 + 白底输入框)
        inject_css(mode="app")
        
        current_user = st.session_state['user_phone']
        is_vip, msg = get_user_vip_status(current_user)
        
        # --- 侧边栏 ---
        with st.sidebar:
            st.markdown("""<div style="display:flex; align-items:center; gap:8px; margin-bottom: 15px;"><div style="background:#2563eb; width:28px; height:28px; border-radius:6px; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold; font-size:16px;">P</div><div style="font-weight:700; font-size:16px; color:#0f172a;">爆款工场 Pro</div></div>""", unsafe_allow_html=True)
            
            render_sidebar_user_card(current_user, msg)
            
            menu_opts = ["🏠 首页", "📝 文案改写", "💡 爆款选题", "🎨 海报生成", "🏷️ 账号起名", "👤 个人中心"]
            if current_user == ADMIN_ACCOUNT: menu_opts.append("🕵️‍♂️ 管理后台")
            
            # 🟢 关键：导航跳转逻辑修复
            default_idx = 0
            if 'nav_menu_selection' in st.session_state:
                # 检查 session 中的目标页面是否在菜单列表中
                target = st.session_state['nav_menu_selection']
                if target in menu_opts:
                    default_idx = menu_opts.index(target)
                # 清除状态，防止锁定
                del st.session_state['nav_menu_selection']

            nav = st.radio("导航", menu_opts, index=default_idx, label_visibility="collapsed")
            
            st.markdown("<div style='flex-grow:1; min-height: 20px;'></div>", unsafe_allow_html=True)
            st.markdown("---")
            render_tech_support_btn("TG777188")
            
            if st.button("🚪 退出登录", use_container_width=True):
                del st.session_state['user_phone']
                st.rerun()

        # --- 路由分发 ---
        if nav == "🏠 首页": view_home()
        elif nav == "📝 文案改写": view_rewrite() # 这里会调用修复后的流光页面
        elif nav == "💡 爆款选题": view_brainstorm()
        elif nav == "🎨 海报生成": view_poster()
        elif nav == "🏷️ 账号起名": view_naming()
        elif nav == "👤 个人中心": view_account()
        elif nav == "🕵️‍♂️ 管理后台": view_admin()

if __name__ == "__main__":
    main()
