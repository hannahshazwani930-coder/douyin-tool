# main.py
import streamlit as st
from config import ADMIN_ACCOUNT
from database import init_db, get_user_vip_status
from utils import inject_css, render_wechat_pill
# 导入所有视图
from views.auth import view_auth
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

# --- 主程序 ---
def main():
    if 'user_phone' not in st.session_state:
        view_auth()
    else:
        inject_css("app")
        
        # --- 侧边栏 ---
        with st.sidebar:
            current_user = st.session_state['user_phone']
            is_vip, msg = get_user_vip_status(current_user)
            
            st.markdown(f"**👤 用户：{current_user}**")
            if is_vip: st.success(f"{msg}")
            else: st.warning("普通用户")
            
            # 菜单逻辑：支持从首页卡片跳转
            if 'nav_menu_selection' in st.session_state:
                default_index = ["🏠 首页", "📝 文案改写", "💡 爆款选题", "🎨 海报生成", "🏷️ 账号起名", "👤 个人中心"].index(st.session_state['nav_menu_selection'])
                # 清除跳转状态，防止锁死
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
