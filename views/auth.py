# views/auth.py
import streamlit as st
from utils import load_isolated_css
from database import login_user, register_user

def view_auth():
    # 1. 注入 CSS 
    load_isolated_css("auth")
    
    # 2. 渲染品牌层 (绝对定位，不影响组件流)
    st.markdown("""
        <div class="brand-overlay-lock">
            <div style="font-size: 50px; margin-bottom: 20px;">💠</div>
            <h1 style="color:white; font-size: 32px; font-weight: 800; margin: 0; letter-spacing:-1px;">抖音爆款工场</h1>
            <p style="font-size: 14px; opacity: 0.7; margin-top: 15px; line-height: 1.6;">
                专业短视频创作辅助系统<br>AI 驱动 · 模块化安全版
            </p>
            <div style="margin-top: 80px; font-size: 10px; letter-spacing: 4px; opacity: 0.3;">EST. 2026 PRO</div>
        </div>
    """, unsafe_allow_html=True)

    # 3. 右侧原生组件 (CSS 会自动强制 margin-left: 350px)
    st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True) # 顶部留白
    st.markdown("<h3 style='color:#0f172a;'>安全登录</h3>", unsafe_allow_html=True)
    
    # 使用表单锁定回车逻辑
    with st.form("auth_login_form"):
        acc = st.text_input("手机号 / 邮箱", placeholder="请输入您的账号", key="l_acc")
        pwd = st.text_input("密码", type="password", placeholder="请输入密码", key="l_pwd")
        
        if st.form_submit_button("登 录"):
            if acc and pwd:
                success, msg = login_user(acc, pwd)
                if success:
                    st.session_state['user_phone'] = acc
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.warning("请填写完整信息")

    # 底部注册引导 (简单按钮，防止布局偏移)
    if st.button("新用户注册 / 申请试用", use_container_width=True):
        st.info("请联系客服获取邀请码：888888")

    # 4. 渲染免责声明
    st.markdown("""
        <div class="footer-disclaimer-fixed">
            使用即代表同意《用户协议》与《隐私政策》<br>
            © 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.
        </div>
    """, unsafe_allow_html=True)
