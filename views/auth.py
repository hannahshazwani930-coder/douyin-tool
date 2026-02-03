# views/auth.py
import streamlit as st
from utils import load_isolated_css
from database import login_user, register_user

def view_auth():
    # 注入精简版 CSS（见下方）
    load_isolated_css("auth")
    
    # 顶部品牌区
    st.markdown("""
        <div style="text-align: center; padding: 40px 0;">
            <h1 style="color: white; font-size: 48px; margin-bottom: 0;">💠</h1>
            <h1 style="color: white; font-weight: 800; margin-top: 10px;">抖音爆款工场 Pro</h1>
            <p style="color: rgba(255,255,255,0.6);">AI 驱动的一站式短视频创作辅助系统</p>
        </div>
    """, unsafe_allow_html=True)

    # 居中表单容器
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # 使用原生 Tabs，这是 Streamlit 最稳固的组件
        tab_login, tab_reg = st.tabs(["🔒 安全登录", "📝 账号注册"])
        
        with tab_login:
            with st.form("login_form_final"):
                acc = st.text_input("账号", placeholder="请输入手机号/邮箱")
                pwd = st.text_input("密码", type="password", placeholder="请输入密码")
                submit = st.form_submit_button("立即登录", use_container_width=True)
                
                if submit:
                    if acc and pwd:
                        success, msg = login_user(acc, pwd)
                        if success:
                            st.session_state['user_phone'] = acc
                            st.rerun()
                        else: st.error(msg)
                    else: st.warning("请填写完整")

        with tab_reg:
            with st.form("reg_form_final"):
                r_acc = st.text_input("设置账号", placeholder="建议使用手机号")
                r_pwd = st.text_input("设置密码", type="password")
                r_inv = st.text_input("邀请码", value="888888")
                r_submit = st.form_submit_button("创建账号", use_container_width=True)
                
                if r_submit:
                    success, msg = register_user(r_acc, r_pwd, r_inv)
                    if success: st.success("注册成功！请切换到登录页")
                    else: st.error(msg)

    # 底部版权
    st.markdown("""
        <div style="position: fixed; bottom: 20px; width: 100%; text-align: center; color: rgba(255,255,255,0.3); font-size: 12px;">
            © 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.
        </div>
    """, unsafe_allow_html=True)
