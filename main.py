# main.py
import streamlit as st
import time
from config import ADMIN_ACCOUNT
# 👇 修改点1：从 database 导入 login_user 和 register_user
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

# --- 初始化数据库 ---
init_db()

# ==========================================
# 登录 / 注册 页面逻辑
# ==========================================
def login_page():
    # 注入登录页专用 CSS
    inject_css(mode="auth")
    
    # 创建左右分栏布局
    col_left, col_right = st.columns([1.3, 1], gap="large")
    
    # --- 左侧：品牌展示 ---
    with col_left:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="hero-title">
            抖音爆款工场<br>
            <span style="color: #3b82f6;">Pro System</span>
        </div>
        <div class="hero-subtitle">
            全流程AI赋能，从选题到海报，打造您的流量引擎。
            高效、安全、稳定的企业级创作工作台。
        </div>
        """, unsafe_allow_html=True)
        
        # 悬停特效卡片
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🚀</div>
            <div class="feature-text">
                <h4>爆款改写</h4>
                <p>深度学习爆款逻辑，一键生成高质量文案。</p>
            </div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🎨</div>
            <div class="feature-text">
                <h4>海报生成</h4>
                <p>自动排版设计，无需PS即可产出专业封面。</p>
            </div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-text">
                <h4>数据驱动</h4>
                <p>基于全网热点数据，辅助选题决策。</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- 右侧：登录/注册 表单 ---
    with col_right:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Tabs 切换
        tab_login, tab_register = st.tabs(["🔐 账号登录", "✨ 注册新号"])
        
        # === 登录模块 ===
        with tab_login:
            with st.form("login_form"):
                st.write("")
                username = st.text_input("账号 / 手机号 / 邮箱", placeholder="请输入登录账号")
                password = st.text_input("密码", type="password", placeholder="请输入密码")
                
                submit_login = st.form_submit_button("立即登录", use_container_width=True)
                
                if submit_login:
                    if not username or not password:
                        st.warning("⚠️ 请输入账号和密码")
                    else:
                        # 👇 修改点2：调用数据库真实登录接口
                        success, msg = login_user(username, password)
                        
                        if success:
                            st.success(f"✅ {msg}，正在跳转...")
                            st.session_state['user_phone'] = username # 记录登录状态
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error(f"⛔ {msg}")

        # === 注册模块 ===
        with tab_register:
            with st.form("register_form"):
                st.write("")
                # 1. 注册方式
                new_user = st.text_input("手机号 或 邮箱", placeholder="作为您的唯一登录凭证")
                
                # 2. 密码
                new_pass = st.text_input("设置密码", type="password", placeholder="不少于6位")
                confirm_pass = st.text_input("确认密码", type="password", placeholder="请再次输入密码")
                
                # 3. 邀请码 (默认888888)
                invite_code = st.text_input("邀请码", value="888888", help="默认为管理员邀请码")
                
                submit_reg = st.form_submit_button("创建账号", use_container_width=True)
                
                if submit_reg:
                    if not new_user:
                        st.warning("⚠️ 请输入手机号或邮箱")
                    elif not new_pass or len(new_pass) < 6:
                        st.warning("⚠️ 密码长度不能少于6位")
                    elif new_pass != confirm_pass:
                        st.error("⛔ 两次输入的密码不一致")
                    else:
                        # 👇 修改点3：调用数据库真实注册接口
                        # 注意：database.py 会自动处理密码加密和生成新邀请码
                        success, msg = register_user(new_user, new_pass, invite_code)
                        
                        if success:
                            st.balloons()
                            st.success(f"✅ {msg}！请点击左侧【账号登录】标签页进行登录。")
                        else:
                            st.error(f"⛔ {msg}")


# --- 主程序入口 ---
def main():
    # 检查登录状态
    if 'user_phone' not in st.session_state:
        login_page() # 未登录显示登录页
    else:
        # 已登录显示主系统
        inject_css("app")
        
        # --- 侧边栏 ---
        with st.sidebar:
            current_user = st.session_state['user_phone']
            is_vip, msg = get_user_vip_status(current_user)
            
            st.markdown(f"**👤 用户：{current_user}**")
            if is_vip: st.success(f"{msg}")
            else: st.warning("普通用户")
            
            # 菜单逻辑
            if 'nav_menu_selection' in st.session_state:
                try:
                    default_index = ["🏠 首页", "📝 文案改写", "💡 爆款选题", "🎨 海报生成", "🏷️ 账号起名", "👤 个人中心"].index(st.session_state['nav_menu_selection'])
                except ValueError:
                    default_index = 0
                del st.session_state['nav_menu_selection']
            else:
                default_index = 0
            
            ops = ["🏠 首页", "📝 文案改写", "💡 爆款选题", "🎨 海报生成", "🏷️ 账号起名", "👤 个人中心"]
            if current_user == ADMIN_ACCOUNT:
                ops.append("🕵️‍♂️ 管理后台")
                
            nav = st.radio("导航", ops, index=default_index, label_visibility="collapsed")
            
            st.markdown("---")
            render_wechat_pill("🎁 领取资料", "W7774X")
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            if st.button("🚪 退出登录", use_container_width=True):
                del st.session_state['user_phone']
                st.rerun()

        # --- 路由分发 ---
        if nav == "🏠 首页": view_home()
        elif nav == "📝 文案改写": view_rewrite()
        elif nav == "💡 爆款选题": view_brainstorm()
        elif nav == "🎨 海报生成": view_poster()
        elif nav == "🏷️ 账号起名": view_naming()
        elif nav == "👤 个人中心": view_account()
        elif nav == "🕵️‍♂️ 管理后台": view_admin()
        
        st.markdown("<div style='margin-top:50px; text-align:center; color:#cbd5e1; font-size:12px;'>© 2026 抖音爆款工场 Pro System (V3.0 Modular)</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
