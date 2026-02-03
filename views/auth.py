# views/auth.py
import streamlit as st
from utils import load_isolated_css
from database import login_user, register_user

def view_auth():
    load_isolated_css("auth")
    
    # --- [全 HTML 构建横屏卡片外壳] ---
    st.markdown(f"""
    <div class="auth-card-inner">
        <div class="side-brand-panel">
            <div style="font-size: 50px; margin-bottom: 20px;">💠</div>
            <h1 style="color:white; font-size: 32px; font-weight: 800; margin: 0;">抖音爆款工场</h1>
            <p style="font-size: 14px; opacity: 0.7; margin-top: 10px;">AI 驱动的一站式短视频创作中枢</p>
            <div style="margin-top: 60px; font-size: 10px; letter-spacing: 3px; opacity: 0.4;">PROFESSIONAL PRO</div>
        </div>
        <div class="form-panel" id="form-container">
    """, unsafe_allow_html=True)

    # 在右侧面板内渲染 Streamlit 组件
    # 注意：由于 CSS 中 form-panel 已设置，组件会自动排列
    tab1, tab2 = st.tabs(["🔒 安全登录", "📝 极速注册"])
    
    with tab1:
        with st.form("login_form"):
            acc = st.text_input("账号", placeholder="手机号 / 邮箱")
            pwd = st.text_input("密码", type="password")
            if st.form_submit_button("登 录"):
                if acc and pwd:
                    success, msg = login_user(acc, pwd)
                    if success:
                        st.session_state['user_phone'] = acc
                        st.rerun()
                    else: st.error(msg)
    
    with tab2:
        with st.form("register_form"):
            r_acc = st.text_input("注册账号", placeholder="常用手机/邮箱")
            # 注册内部仍可用 column 缩短输入框
            c1, c2 = st.columns(2)
            with c1: r_p1 = st.text_input("设置密码", type="password")
            with c2: r_p2 = st.text_input("确认密码", type="password")
            inv = st.text_input("邀请码", value="888888")
            if st.form_submit_button("注 册"):
                if r_p1 != r_p2: st.error("密码不一致")
                else:
                    success, msg = register_user(r_acc, r_p1, inv)
                    if success: st.success("注册成功！")
                    else: st.error(msg)

    st.markdown('</div></div>', unsafe_allow_html=True) # 闭合卡片容器

    # --- [外部免责声明] ---
    st.markdown("""
        <div class="external-disclaimer">
            使用即代表同意 用户协议 与 隐私政策<br>
            © 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.
        </div>
    """, unsafe_allow_html=True)
