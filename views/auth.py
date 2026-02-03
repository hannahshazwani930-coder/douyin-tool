# views/auth.py
import streamlit as st
from utils import load_isolated_css
from database import login_user, register_user

def view_auth():
    # 1. 注入 CSS 
    load_isolated_css("auth")
    
    # 2. 渲染左侧背景（通过 absolute 定位挂载）
    st.markdown("""
        <div class="fixed-left-brand">
            <div style="font-size: 45px;">💠</div>
            <h1 style="color:white; font-size: 30px; font-weight: 800; margin: 20px 0 10px 0;">抖音爆款工场</h1>
            <p style="font-size: 14px; opacity: 0.7; line-height: 1.6;">AI 驱动一站式创作中枢</p>
            <div style="margin-top: 80px; font-size: 10px; letter-spacing: 4px; opacity: 0.4;">EST. 2026 PRO</div>
        </div>
    """, unsafe_allow_html=True)

    # 3. 右侧表单逻辑（CSS 会自动通过 padding-left 将其推到右边）
    if 'reg_mode' not in st.session_state:
        st.session_state.reg_mode = False

    if not st.session_state.reg_mode:
        st.markdown("<h3 style='color:#0f172a;'>安全登录</h3>", unsafe_allow_html=True)
        with st.form("l_form"):
            u = st.text_input("账号", placeholder="手机号 / 邮箱")
            p = st.text_input("密码", type="password")
            if st.form_submit_button("立即登录"):
                success, msg = login_user(u, p)
                if success:
                    st.session_state['user_phone'] = u
                    st.rerun()
                else: st.error(msg)
        if st.button("新用户注册"):
            st.session_state.reg_mode = True
            st.rerun()
    else:
        st.markdown("<h3 style='color:#0f172a;'>快速注册</h3>", unsafe_allow_html=True)
        with st.form("r_form"):
            ru = st.text_input("账号", placeholder="手机号/邮箱")
            rp1 = st.text_input("密码", type="password")
            ri = st.text_input("邀请码", value="888888")
            if st.form_submit_button("创建账号"):
                success, msg = register_user(ru, rp1, ri)
                if success: st.success("注册成功！")
        if st.button("返回登录"):
            st.session_state.reg_mode = False
            st.rerun()

    # 4. 外置免责声明
    st.write("---") # 增加一个不可见的占位符确保底部空间
    st.markdown('<div class="footer-lock">© 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.</div>', unsafe_allow_html=True)
