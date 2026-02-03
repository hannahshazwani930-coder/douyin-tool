# views/auth.py
import streamlit as st
from utils import load_isolated_css
from database import login_user

def view_auth():
    # 1. 注入 CSS 
    load_isolated_css("auth")
    
    # 2. 建立原生分栏：左侧 4 份放文字，中间 1 份空格，右侧 5 份放表单
    col_left, col_space, col_right = st.columns([4, 1, 5])
    
    with col_left:
        # 纯净的品牌展示
        st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
        st.markdown("<h1 style='color:white; font-size:48px; margin-bottom:0;'>💠</h1>", unsafe_allow_html=True)
        st.markdown("<h1 style='color:white; font-size:42px; font-weight:800; margin-top:10px;'>抖音爆款工场</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:rgba(255,255,255,0.7); font-size:18px; line-height:1.6;'>AI 驱动的一站式短视频创作中枢<br>专业 · 高效 · 模块化</p>", unsafe_allow_html=True)
        st.markdown("<div style='margin-top:100px; color:rgba(255,255,255,0.3); letter-spacing:4px;'>EST. 2026 PRO EDITION</div>", unsafe_allow_html=True)

    with col_right:
        # 右侧原生登录表单
        st.markdown("<h2 style='color:white; margin-bottom:30px;'>安全登录</h2>", unsafe_allow_html=True)
        
        with st.form("login_pro_form"):
            acc = st.text_input("账号", placeholder="手机号 / 邮箱", key="l_acc")
            pwd = st.text_input("密码", type="password", placeholder="请输入登录密码", key="l_pwd")
            
            submit = st.form_submit_button("登 录")
            if submit:
                if acc and pwd:
                    success, msg = login_user(acc, pwd)
                    if success:
                        st.session_state['user_phone'] = acc
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")
                else:
                    st.warning("⚠️ 请输入账号和密码")

        # 注册引导
        st.markdown("<p style='text-align:center; color:rgba(255,255,255,0.5); margin-top:20px;'>新用户请联系管理员获取邀请码</p>", unsafe_allow_html=True)

    # 3. 底部版权
    st.markdown("""
        <div class="footer-text">
            使用即代表同意《用户协议》与《隐私政策》<br>
            © 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.
        </div>
    """, unsafe_allow_html=True)
