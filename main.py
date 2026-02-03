# main.py
import streamlit as st
from database import init_db
from views.auth import view_auth
from views.home import view_home
from config import APP_NAME, APP_ICON

# 设置页面属性
st.set_page_config(page_title=APP_NAME, page_icon=APP_ICON, layout="wide")

# 初始化数据库
init_db()

def main():
    # 检查登录状态
    if 'user_phone' not in st.session_state:
        # 未登录：显示登录页
        view_auth()
    else:
        # 已登录：显示首页或功能页
        # 这里你可以根据侧边栏 st.sidebar.selectbox 来切换不同的 view_xxx()
        view_home()

if __name__ == "__main__":
    main()
