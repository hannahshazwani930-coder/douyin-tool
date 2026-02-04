import sys
import os

# 确保当前目录在 Python 搜索路径中
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
# ... 之后的导入语句
import streamlit as st
from views.auth import view_auth
# 导入各个独立页面模块
from views.home import view_home
from views.copywriting import view_copywriting
from views.alias import view_alias
from views.animation import view_animation
from views.profile import view_profile
from views.admin import view_admin

st.set_page_config(page_title="爆款工厂PRO", page_icon="🎯", layout="wide")

def main():
    if 'user_phone' not in st.session_state:
        st.markdown("<style>[data-testid='stSidebar'] { display:none; }</style>", unsafe_allow_html=True)
        view_auth()
        return

    user_phone = st.session_state.get('user_phone')

    # --- 顶部 Header ---
    st.markdown(f"""
    <div style="position: fixed; top: 0; left: 0; right: 0; height: 50px; background: white; border-bottom: 1px solid #F1F5F9; z-index: 99; display: flex; align-items: center; justify-content: flex-end; padding: 0 40px;">
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="text-align: right;">
                <div style="color: #1E3A8A; font-size: 13px; font-weight: 600;">{user_phone}</div>
                <div style="color: #10B981; font-size: 10px;">PRO 旗舰版</div>
            </div>
            <div style="width: 32px; height: 32px; background: #F1F5F9; border-radius: 50%; border: 1px solid #E2E8F0;"></div>
        </div>
    </div>
    <div style="height: 45px;"></div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("<h2 style='color:#1E3A8A; padding-left:10px;'>爆款工厂PRO</h2>", unsafe_allow_html=True)
        
        # 路由映射字典
        menu_map = {
            "🚀 首页控制台": view_home,
            "✍️ 文案创作": view_copywriting,
            "🏷️ 别名创作": view_alias,
            "🎬 AI动漫创作": view_animation,
            "👤 个人中心": view_profile
        }
        
        options = list(menu_map.keys())
        if user_phone == "13800138000":
            menu_map["⚙️ 后台管理"] = view_admin
            options.append("⚙️ 后台管理")

        selection = st.radio("MISSION CONTROL", options, label_visibility="collapsed")
        
        st.write("---")
        st.markdown("""<div style="padding:10px; background:#F0F4FF; border-radius:8px; border:1px dashed #3B82F6;">
            <p style="color:#1E3A8A; font-size:11px; font-weight:bold; margin:0;">🤝 技术合作</p>
            <p style="color:#3B82F6; font-size:13px; margin:4px 0 0 0;">TG: 777188</p>
        </div>""", unsafe_allow_html=True)
        
        if st.button("退出系统", use_container_width=True):
            del st.session_state['user_phone']
            st.rerun()

    # 执行选中的页面函数
    menu_map[selection]()

if __name__ == "__main__":
    main()

