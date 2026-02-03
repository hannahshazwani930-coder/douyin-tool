# views/auth.py
import streamlit as st
from utils import load_isolated_css
from database import login_user, register_user

def view_auth():
    # 1. 注入 CSS 
    load_isolated_css("auth")
    
    # 2. 渲染品牌展示层（它会浮在 CSS 生成的蓝色区上方）
    st.markdown("""
        <div class="brand-fixed-layer">
            <div style="font-size: 45px;">💠</div>
            <h1 style="color:white; font-size: 30px; font-weight: 800; margin: 20px 0 10px 0;">抖音爆款工场</h1>
            <p style="font-size: 14px; opacity: 0.7; line-height: 1.6;">
                专业短视频创作辅助系统<br>AI 驱动 · 模块化安全版
            </p>
            <div style="margin-top: 80px; font-size: 10px; letter-spacing: 4px; opacity: 0.3;">EST. 2026 PRO</div>
        </div>
    """, unsafe_allow_html=True)

    # 3. 原生表单组件（CSS 会强行将其向右推 360 像素）
    # 顶部适当留白模拟垂直居中
    st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#0f172a;'>安全登录</h3>", unsafe_allow_html=True)
    
    with st.form("main_auth_form"):
        acc = st.text_input("手机号 / 邮箱", placeholder="请输入账号", key="l_acc")
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
                st.warning("请完善信息")

    # 为了防止布局崩溃，将注册按钮做成简单链接样式
    if st.button("新用户注册 / 申请试用", use_container_width=True):
        st.info("请联系客服获取邀请码：888888")

    # 4. 底部声明
    st.markdown("""
        <div class="footer-text-lock">
            © 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.
        </div>
    """, unsafe_allow_html=True)
