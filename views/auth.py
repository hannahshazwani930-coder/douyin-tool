# views/auth.py
import streamlit as st
from utils import load_isolated_css
from database import login_user, register_user

def view_auth():
    load_isolated_css("auth")
    
    # 用一个大的外层 div 包裹
    st.markdown('<div class="auth-wrapper">', unsafe_allow_html=True)
    
    # 建立左右两栏
    left, right = st.columns([0.4, 0.6], gap="small")
    
    with left:
        # 纯 HTML 渲染左侧，高度由 CSS 锁定
        st.markdown("""
            <div class="side-brand">
                <div style="font-size: 50px;">💠</div>
                <h1 style="color:white; font-size: 32px; font-weight: 800; margin: 20px 0 10px 0;">抖音爆款工场</h1>
                <p style="font-size: 14px; opacity: 0.7; line-height: 1.6;">AI 驱动的一站式创作中枢</p>
                <div style="margin-top: 50px; font-size: 10px; letter-spacing: 3px; opacity: 0.4;">EST. 2026 PRO</div>
            </div>
        """, unsafe_allow_html=True)

    with right:
        # 右侧直接承载 Streamlit 原生表单
        st.markdown('<div class="form-area">', unsafe_allow_html=True)
        
        # 简化交互：去掉 Tabs（Tabs 容易引起布局崩溃），直接显示登录
        # 如果需要注册，点击下方的按钮切换
        if 'show_reg' not in st.session_state:
            st.session_state.show_reg = False

        if not st.session_state.show_reg:
            st.subheader("安全登录")
            with st.form("login_p"):
                acc = st.text_input("手机号 / 邮箱", key="l_acc")
                pwd = st.text_input("密码", type="password", key="l_pwd")
                if st.form_submit_button("登 录"):
                    success, msg = login_user(acc, pwd)
                    if success:
                        st.session_state['user_phone'] = acc
                        st.rerun()
                    else: st.error(msg)
            if st.button("没有账号？去注册"):
                st.session_state.show_reg = True
                st.rerun()
        else:
            st.subheader("快速注册")
            with st.form("reg_p"):
                r_acc = st.text_input("注册账号", key="r_acc")
                r_pwd = st.text_input("设置密码", type="password")
                r_inv = st.text_input("邀请码", value="888888")
                if st.form_submit_button("注 册"):
                    success, msg = register_user(r_acc, r_pwd, r_inv)
                    if success: st.success("注册成功！")
            if st.button("已有账号？回登录"):
                st.session_state.show_reg = False
                st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True) # 闭合 auth-wrapper

    # 外部下方声明
    st.markdown("""
        <div class="footer-text">
            登录即代表同意 用户协议 与 隐私政策<br>
            © 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.
        </div>
    """, unsafe_allow_html=True)
