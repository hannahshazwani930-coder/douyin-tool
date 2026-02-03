# views/auth.py
import streamlit as st
from utils import load_isolated_css
from database import login_user, register_user

def view_auth():
    # 1. 注入 CSS 锁定样式
    load_isolated_css("auth")
    
    # 2. 渲染横屏大卡片外壳 (HTML)
    st.markdown("""
    <div class="auth-wrapper">
        <div class="side-panel">
            <div style="font-size: 50px; margin-bottom: 20px;">💠</div>
            <h1 style="color:white; font-size: 30px; font-weight: 800; margin: 0;">抖音爆款工场</h1>
            <p style="font-size: 14px; opacity: 0.7; margin-top: 15px; line-height: 1.6;">
                专业短视频创作辅助系统<br>AI 驱动 · 模块化安全版
            </p>
            <div style="margin-top: 60px; font-size: 10px; letter-spacing: 4px; opacity: 0.3;">PRO EDITION 2026</div>
        </div>
        <div class="form-panel">
    """, unsafe_allow_html=True)

    # 3. 在表单区渲染 Streamlit 原生逻辑
    # 使用独立的容器避免内容溢出
    with st.container():
        if 'reg_mode' not in st.session_state:
            st.session_state.reg_mode = False

        if not st.session_state.reg_mode:
            st.markdown("<h3 style='margin-bottom:20px; color:#0f172a;'>安全登录</h3>", unsafe_allow_html=True)
            with st.form("l_form", clear_on_submit=False):
                u = st.text_input("手机号 / 邮箱", placeholder="请输入账号")
                p = st.text_input("密码", type="password", placeholder="请输入密码")
                if st.form_submit_button("立即登录"):
                    if u and p:
                        success, msg = login_user(u, p)
                        if success:
                            st.session_state['user_phone'] = u
                            st.rerun()
                        else: st.error(msg)
            if st.button("新用户注册", key="go_reg"):
                st.session_state.reg_mode = True
                st.rerun()
        else:
            st.markdown("<h3 style='margin-bottom:20px; color:#0f172a;'>快速注册</h3>", unsafe_allow_html=True)
            with st.form("r_form"):
                ru = st.text_input("注册账号", placeholder="手机号或邮箱")
                rp1 = st.text_input("设置密码", type="password")
                rp2 = st.text_input("确认密码", type="password")
                ri = st.text_input("邀请码", value="888888")
                if st.form_submit_button("创建账号"):
                    if rp1 != rp2: st.error("两次密码不一致")
                    else:
                        success, msg = register_user(ru, rp1, ri)
                        if success: st.success("注册成功！请返回登录")
            if st.button("已有账号登录", key="go_log"):
                st.session_state.reg_mode = False
                st.rerun()

    # 4. 闭合标签
    st.markdown('</div></div>', unsafe_allow_html=True)

    # 5. 外部声明
    st.markdown("""
        <div class="footer-disclaimer">
            使用即代表同意 <span style="color:rgba(255,255,255,0.6)">用户协议</span> 与 <span style="color:rgba(255,255,255,0.6)">隐私政策</span><br>
            © 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.
        </div>
    """, unsafe_allow_html=True)
