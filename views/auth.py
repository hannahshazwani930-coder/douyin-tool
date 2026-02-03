# views/auth.py
import streamlit as st
from utils import load_isolated_css
from database import login_user, register_user

def view_auth():
    # 🔒 锁定：强制加载 auth 专用独立样式
    load_isolated_css("auth")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<h1 style="color:#0f172a;">抖音爆款工场</h1>', unsafe_allow_html=True)
        st.write("专业短视频创作辅助系统 - 模块化安全版")
        st.image("https://img.icons8.com/fluency/200/rocket.png") # 示例配图

    with col2:
        tab1, tab2 = st.tabs(["🔑 登录", "📝 注册"])
        
        with tab1:
            phone = st.text_input("手机号", key="login_phone")
            pwd = st.text_input("密码", type="password", key="login_pwd")
            if st.button("立即进入系统", key="login_btn"):
                success, msg = login_user(phone, pwd)
                if success:
                    st.session_state['user_phone'] = phone
                    st.rerun()
                else:
                    st.error(msg)
                    
        with tab2:
            reg_phone = st.text_input("手机号", key="reg_phone")
            reg_pwd = st.text_input("设置密码", type="password", key="reg_pwd")
            invite_code = st.text_input("邀请码", key="reg_invite")
            if st.button("创建账号", key="reg_btn"):
                success, msg = register_user(reg_phone, reg_pwd, invite_code)
                if success: st.success(msg)
                else: st.error(msg)