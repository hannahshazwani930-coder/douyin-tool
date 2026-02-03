# views/auth.py
import streamlit as st
from utils import load_isolated_css
from database import login_user, register_user

def view_auth():
    # 🔒 锁定加载：强制应用独立视觉规范
    load_isolated_css("auth")
    
    # --- [核心卡片：左右对等分栏布局] ---
    st.markdown('<div class="auth-card-inner">', unsafe_allow_html=True)
    
    # 采用 4:6 比例，让左侧品牌更有视觉张力
    left, right = st.columns([0.4, 0.6], gap="small")
    
    with left:
        # 左侧：极简品牌墙
        st.markdown("""
            <div class="side-brand-panel">
                <div class="logo-circle">💠</div>
                <h1 class="brand-title">抖音爆款工场</h1>
                <p class="brand-tagline">AI 驱动的一站式短视频创作中枢</p>
                <div class="brand-footer">PROFESSIONAL PRO</div>
            </div>
        """, unsafe_allow_html=True)

    with right:
        # 右侧：精细化操作区
        st.markdown('<div class="form-panel">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🔒 安全登录", "📝 极速注册"])
        
        with tab1:
            with st.form("login_form", clear_on_submit=False):
                acc = st.text_input("账号", placeholder="手机号 / 邮箱")
                pwd = st.text_input("密码", type="password")
                if st.form_submit_button("登 录"):
                    if acc and pwd:
                        success, msg = login_user(acc, pwd)
                        if success:
                            st.session_state['user_phone'] = acc
                            st.rerun()
                        else: st.error(msg)
                    else: st.warning("请完善信息")
        
        with tab2:
            with st.form("register_form"):
                r_acc = st.text_input("注册账号", placeholder="常用手机/邮箱")
                cp1, cp2 = st.columns(2)
                with cp1: r_p1 = st.text_input("设置密码", type="password")
                with cp2: r_p2 = st.text_input("确认密码", type="password")
                inv = st.text_input("邀请码", value="888888")
                if st.form_submit_button("注 册"):
                    if r_p1 != r_p2: st.error("密码不一致")
                    else:
                        success, msg = register_user(r_acc, r_p1, inv)
                        if success: st.success("注册成功！")
                        else: st.error(msg)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True) # 结束 auth-card-inner

    # --- [声明外置：位于极光背景下方] ---
    st.markdown("""
        <div class="external-disclaimer">
            使用即代表同意 <a href='#'>用户协议</a> 与 <a href='#'>隐私政策</a><br>
            © 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.
        </div>
    """, unsafe_allow_html=True)
