# main.py
import streamlit as st
from views.auth import view_auth
from views.home import view_home

def main():
    # --- 1. 全局配置：必须放在第一行 ---
    st.set_page_config(page_title="爆款工厂PRO", layout="wide", initial_sidebar_state="expanded")

    # --- 2. 核心 CSS 修复：精准隐藏顶部，保留侧边栏控制 ---
    st.markdown("""
<style>
    /* 仅隐藏顶部黑条和装饰，不影响侧边栏按钮 */
    [data-testid="stHeader"] { 
        background-color: rgba(0,0,0,0) !important;
        color: transparent !important;
    }
    
    /* 侧边栏大师级美化：纯白、单线、14px */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #F1F5F9 !important;
    }
    
    /* 侧边栏导航文字样式锁定 */
    [data-testid="stSidebarNav"] span {
        font-size: 14px !important;
        color: #475569 !important;
    }
</style>
""", unsafe_allow_html=True)

    # --- 3. 登录状态逻辑拦截 ---
    if 'user_phone' not in st.session_state:
        # 未登录：强制显示锁定版的登录页
        view_auth()
    else:
        # 已登录：展示侧边栏和主页面内容
        with st.sidebar:
            st.markdown("<h2 style='color: #1E3A8A; font-size: 20px; padding-left: 10px;'>爆款工厂PRO</h2>", unsafe_allow_html=True)
            st.write("\n")
            
            # 这种方式是手动侧边栏导航，更稳固
            menu = st.radio(
                "导航中心",
                ["首页大盘", "算法嗅探", "神经编辑", "系统设置"],
                label_visibility="collapsed"
            )
            
            st.write("\n" * 15)
            if st.button("安全退出", use_container_width=True):
                del st.session_state['user_phone']
                st.rerun()

        # 根据选择渲染页面
        if menu == "首页大盘":
            view_home()
        else:
            st.info(f"正在前往 {menu} 模块...")

if __name__ == "__main__":
    main()
