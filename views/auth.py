# views/auth.py
import streamlit as st
from utils import load_isolated_css
from database import login_user, register_user

def view_auth():
    # 1. 注入 CSS 锁定样式
    load_isolated_css("auth")
    
    # 2. 渲染左侧文字内容 (背景已由 CSS 伪元素固定，不占组件位)
    st.markdown("""
        <div class="brand-overlay-content">
            <div style="font-size: 45px;">💠</div>
            <h1 style="color:white; font-size: 30px; font-weight: 800; margin: 20px 0 10px 0;">抖音爆款工场</h1>
            <p style="font-size: 14px; opacity: 0.7; line-height: 1.6;">
                专业短视频创作辅助系统<br>AI 驱动 · 模块化安全版
            </p>
            <div style="margin-top: 80px; font-size: 10px; letter-spacing: 4px; opacity: 0.3;">EST. 2026 PRO</div>
        </div>
    """, unsafe_allow_html=True)

    # 3. 右侧原生组件逻辑区
    # CSS 已强制此区域所有组件 margin-left: 360px
    st.markdown("<h3 style='color:#0f172a; margin-top:20px;'>安全登录</h3>", unsafe_allow_html=True)
    
    with st.form("login_form_lock"):
        acc = st.text_input("手机号 / 邮箱", placeholder="请输入账号", key="l_acc")
        pwd = st.text_input("密码", type="password", placeholder="请输入密码", key="l_pwd")
        
        # 按钮悬浮与定位已由 CSS 统一控制
        if st.form_submit_button("立即登录"):
            if acc and pwd:
                success, msg = login_user(acc, pwd)
                if success:
                    st.session_state['user_phone'] = acc
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.warning("请完善信息")

    # 注册逻辑切换（简单模式防止布局崩溃）
    if st.button("新用户注册 / 忘记密码"):
        st.info("系统维护中，请联系管理员获取邀请码")

    # 4. 外部声明 (独立于主卡片)
    st.markdown("""
        <div class="fixed-footer">
            © 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.
        </div>
    """, unsafe_allow_html=True)
