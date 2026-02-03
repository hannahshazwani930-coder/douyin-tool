# main.py
import streamlit as st
from config import ADMIN_ACCOUNT
from database import init_db, get_user_vip_status
from utils import inject_css, render_wechat_pill
from views.auth import view_auth

# --- 页面配置 (必须是第一行) ---
st.set_page_config(
    page_title=抖音爆款工场 Pro, 
    layout=wide,
    page_icon=💠,
    initial_sidebar_state=expanded
)

# --- 初始化数据库 ---
init_db()

# --- 主程序逻辑 ---
def main()
    if 'user_phone' not in st.session_state
        # 未登录 - 显示登录页
        view_auth()
    else
        # 已登录 - 显示主界面
        inject_css(app) # 注入系统样式
        
        # --- 侧边栏导航 ---
        with st.sidebar
            current_user = st.session_state['user_phone']
            is_vip, msg = get_user_vip_status(current_user)
            
            st.markdown(f👤 用户：{current_user})
            if is_vip st.success(f{msg})
            else st.warning(普通用户)
            
            # 菜单选项
            ops = [🏠 首页, 📝 文案改写, 💡 爆款选题, 🎨 海报生成, 🏷️ 账号起名, 👤 个人中心]
            if current_user == ADMIN_ACCOUNT
                ops.append(🕵️‍♂️ 管理后台)
                
            nav = st.radio(导航, ops, index=0, label_visibility=collapsed)
            
            st.markdown(---)
            render_wechat_pill(🎁 领取资料, W7774X)
            st.markdown(div style='height10px'div, unsafe_allow_html=True)
            if st.button(🚪 退出登录, use_container_width=True)
                del st.session_state['user_phone']
                st.rerun()

        # --- 页面路由 (占位符) ---
        if nav == 🏠 首页
            st.info(🚧 首页功能正在迁移中...) # 暂时占位
        elif nav == 📝 文案改写
            st.info(🚧 文案功能正在迁移中...)
        elif nav == 💡 爆款选题
            st.info(🚧 选题功能正在迁移中...)
        elif nav == 🎨 海报生成
            st.info(🚧 海报功能正在迁移中...)
        elif nav == 🏷️ 账号起名
            st.info(🚧 起名功能正在迁移中...)
        elif nav == 👤 个人中心
            st.info(🚧 个人中心正在迁移中...)
        elif nav == 🕵️‍♂️ 管理后台
            st.info(🚧 后台功能正在迁移中...)
        
        # 底部 Footer
        st.markdown(div style='margin-top50px; text-aligncenter; color#cbd5e1; font-size12px;'© 2026 抖音爆款工场 Pro System (Modular Ver.)div, unsafe_allow_html=True)

if __name__ == __main__
    main()
