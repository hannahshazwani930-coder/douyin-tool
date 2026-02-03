# views/auth.py
import streamlit as st
from utils import load_isolated_css
from database import login_user, register_user

def view_auth():
    # 1. 注入 CSS 锁定样式
    load_isolated_css("auth")
    
    # 2. 渲染左侧文字（背景由 CSS 伪元素绘制，确保不偏移）
    st.markdown("""
        <div class="brand-overlay">
            <div style="font-size: 50px; margin-bottom: 20px;">💠</div>
            <h1 style="color:white; font-size: 32px; font-weight: 800; margin: 0;">抖音爆款工场</h1>
            <p style="font-size: 14px; opacity: 0.7; margin-top: 15px; line-height: 1.6;">
                专业短视频创作辅助系统<br>AI 驱动 · 模块化安全版
            </p>
            <div style="margin-top: 80px; font-size: 10px; letter-spacing: 4px; opacity: 0.3;">EST. 2026 PRO</div>
        </div>
    """, unsafe_allow_html=True)

    # 3. 右侧原生组件逻辑
    # 注意：CSS 会自动拦截这里的组件并强制 margin-left: 360px
    st.write("") # 增加顶部间距
    st.markdown("<h3 style='color:#0f172a;'>安全登录</h3>", unsafe_allow_html=True)
    
    with st.form("login_p"):
        acc = st.text_input("手机号 / 邮箱", key="l_acc")
        pwd = st.text_input("密码", type="password", key="l_pwd")
        if st.form_submit_button("登 录"):
            if acc and pwd:
                success, msg = login_user(acc, pwd)
                if success:
                    st.session_state['user_phone'] = acc
                    st.rerun()
                else: st.error(msg)
    
    if st.button("新用户注册"):
        st.info("请联系管理员获取邀请码")

    # 4. 底部声明
    st.markdown('<div class="footer-fix">© 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.</div>', unsafe_allow_html=True)
