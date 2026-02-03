# main.py
import streamlit as st
from config import ADMIN_ACCOUNT
from database import init_db, get_user_vip_status
from utils import load_isolated_css, render_wechat_pill
from views.auth import view_auth

# --- 1. 基础配置 (必须是第一行代码) ---
st.set_page_config(
    page_title="抖音爆款工场 Pro", 
    layout="wide",
    page_icon="💠",
    initial_sidebar_state="expanded"
)

# 初始化数据库
init_db()

def main():
    # 检查登录状态
    if 'user_phone' not in st.session_state:
        # 🔒 锁定：仅加载登录页独立样式
        load_isolated_css("auth")
        view_auth()
    else:
        # --- 2. 侧边栏导航与锁定 ---
        with st.sidebar:
            current_user = st.session_state['user_phone']
            is_vip, msg = get_user_vip_status(current_user)
            
            st.markdown(f"👤 用户：{current_user}")
            if is_vip:
                st.success(f"{msg}")
            else:
                st.warning("普通用户")
            
            # 导航菜单
            ops = ["🏠 首页", "📝 文案改写", "💡 爆款选题", "🎨 海报生成", "🏷️ 账号起名", "👤 个人中心"]
            if current_user == ADMIN_ACCOUNT:
                ops.append("🕵️‍♂️ 管理后台")
            
            nav = st.radio("导航", ops, label_visibility="collapsed")
            
            st.markdown("---")
            render_wechat_pill("🎁 领取资料", "W7774X")
            
            if st.button("🚪 退出登录", use_container_width=True):
                del st.session_state['user_phone']
                st.rerun()

        # --- 3. 页面路由与样式隔离 (重点) ---
        if nav == "🏠 首页":
            load_isolated_css("home")
            from views.home import view_home
            view_home()
            
        elif nav == "📝 文案改写":
            load_isolated_css("rewrite")
            from views.rewrite import view_rewrite
            view_rewrite()
            
        elif nav == "💡 爆款选题":
            load_isolated_css("brainstorm")
            from views.brainstorm import view_brainstorm
            view_brainstorm()
         
        elif nav == "🎨 海报生成":
            load_isolated_css("poster")
            from views.poster import view_poster
            view_poster()   
            
        # ... 其他页面按此逻辑添加 ...

if __name__ == "__main__":
    main()

