# views/auth.py
import streamlit as st
from utils import load_isolated_css
from database import login_user, register_user

def view_auth():
    # 1. 注入 CSS 
    load_isolated_css("auth")
    
    # 2. 渲染左侧品牌展示区 (绝对定位挂载)
    st.markdown("""
        <div class="brand-panel-fixed">
            <div style="font-size: 45px;">💠</div>
            <h1 style="color:white; font-size: 32px; font-weight: 800; margin: 20px 0 10px 0; letter-spacing:-1px;">抖音爆款工场</h1>
            <p style="font-size: 14px; opacity: 0.7; line-height: 1.6;">
                专业短视频创作辅助系统<br>AI 驱动 · 模块化安全版
            </p>
            <div style="margin-top: 80px; font-size: 10px; letter-spacing: 4px; opacity: 0.3;">EST. 2026 PRO EDITION</div>
        </div>
    """, unsafe_allow_html=True)

    # 3. 右侧表单逻辑 (CSS 已通过 margin-left 将内容强行推至卡片右半部)
    st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#0f172a; margin-bottom:20px;'>安全登录</h3>", unsafe_allow_html=True)
    
    with st.form("auth_final_lock"):
        acc = st.text_input("手机号 / 邮箱", placeholder="请输入账号", key="login_u")
        pwd = st.text_input("密码", type="password", placeholder="请输入密码", key="login_p")
        
        if st.form_submit_button("登 录"):
            if acc and pwd:
                success, msg = login_user(acc, pwd)
                if success:
                    st.session_state['user_phone'] = acc
                    st.rerun()
                else: st.error(msg)
            else: st.warning("请填写信息")

    # 为了保证布局稳固，将注册引导做成简单按钮
    if st.button("新用户注册 / 申请试用", use_container_width=True):
        st.info("请联系客服获取邀请码：888888")

    # 4. 底部外部声明
    st.markdown("""
        <div class="footer-lock-pro">
            使用即代表同意《用户协议》与《隐私政策》<br>
            © 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.
        </div>
    """, unsafe_allow_html=True)
