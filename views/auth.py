# views/auth.py
import streamlit as st
from utils import load_isolated_css
from database import login_user, register_user

def view_auth():
    # 加载 CSS 美化（不再包含危险的定位代码）
    load_isolated_css("auth")
    
    # 顶部空行，让卡片垂直居中
    st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

    # 第一层容器：建立一个 850px 宽的中心区域
    # 使用 [1, 4, 1] 比例让内容自动居中
    _, center_col, _ = st.columns([1, 4, 1])

    with center_col:
        # 建立左右分栏：左侧品牌，右侧表单
        # 这是 Streamlit 官方支持的排版，绝不会乱
        left_part, right_part = st.columns([1, 1.5], gap="large")

        with left_part:
            # 品牌视觉区
            st.markdown("""
                <div class="brand-box">
                    <div style="font-size: 40px;">💠</div>
                    <h2 style="color: white; font-weight: 800; margin-top: 10px;">抖音爆款工场</h2>
                    <p style="color: rgba(255,255,255,0.7); font-size: 14px;">专业短视频创作辅助系统</p>
                    <div style="margin-top: 50px; font-size: 10px; opacity: 0.3; letter-spacing: 2px;">PRO EDITION</div>
                </div>
            """, unsafe_allow_html=True)

        with right_part:
            # 登录与注册切换
            tab_login, tab_reg = st.tabs(["🔑 安全登录", "📝 快速注册"])
            
            with tab_login:
                with st.form("login_final"):
                    acc = st.text_input("账号", placeholder="手机号 / 邮箱")
                    pwd = st.text_input("密码", type="password")
                    if st.form_submit_button("登 录", use_container_width=True):
                        if acc and pwd:
                            success, msg = login_user(acc, pwd)
                            if success:
                                st.session_state['user_phone'] = acc
                                st.rerun()
                            else: st.error(msg)
            
            with tab_reg:
                with st.form("reg_final"):
                    r_acc = st.text_input("设置账号")
                    r_pwd = st.text_input("设置密码", type="password")
                    r_inv = st.text_input("邀请码", value="888888")
                    if st.form_submit_button("注 册", use_container_width=True):
                        success, msg = register_user(r_acc, r_pwd, r_inv)
                        if success: st.success("注册成功！请登录")
                        else: st.error(msg)

    # 底部免责声明
    st.markdown("""
        <div style="position: fixed; bottom: 20px; width: 100%; text-align: center; color: rgba(255,255,255,0.3); font-size: 11px;">
            © 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.
        </div>
    """, unsafe_allow_html=True)
