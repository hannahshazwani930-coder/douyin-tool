# views/auth.py
import streamlit as st
from utils import load_isolated_css
from database import login_user, register_user

def view_auth():
    # 1. 注入 CSS 
    load_isolated_css("auth")
    
    # 2. 渲染左侧品牌信息
    st.markdown("""
        <div class="brand-fixed-lock">
            <div style="font-size: 50px; margin-bottom: 20px;">💠</div>
            <h1 style="color:white; font-size: 32px; font-weight: 800; margin: 0;">抖音爆款工场</h1>
            <p style="font-size: 14px; opacity: 0.7; margin-top: 15px; line-height: 1.6;">
                专业短视频创作辅助系统<br>AI 驱动 · 模块化安全版
            </p>
            <div style="margin-top: 80px; font-size: 10px; letter-spacing: 4px; opacity: 0.3;">EST. 2026 PRO</div>
        </div>
    """, unsafe_allow_html=True)

    # 3. 右侧原生组件（CSS 会自动强制将其 margin-left 设置为 360px）
    st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#0f172a; margin-bottom:20px;'>安全登录</h3>", unsafe_allow_html=True)
    
    with st.form("auth_pro_form"):
        acc = st.text_input("账号", placeholder="手机号 / 邮箱", key="l_acc")
        pwd = st.text_input("密码", type="password", placeholder="请输入密码", key="l_pwd")
        
        if st.form_submit_button("立即登录"):
            if acc and pwd:
                success, msg = login_user(acc, pwd)
                if success:
                    st.session_state['user_phone'] = acc
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.warning("请填写完整信息")

    if st.button("新用户注册", use_container_width=True):
        st.info("请联系客服获取邀请码")

    # 4. 底部声明
    st.markdown("""
        <div class="footer-disclaimer-pro">
            © 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.
        </div>
    """, unsafe_allow_html=True)
