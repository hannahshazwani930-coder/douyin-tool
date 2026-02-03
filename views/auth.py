# views/auth.py
import streamlit as st
from database import login_user, register_user

def view_auth():
    # --- 1. 精简防御性 CSS ---
    st.markdown("""
        <style>
            /* 1. 彻底杀掉 Press Enter 提示 */
            [data-testid="stFormInstructions"] { display: none !important; }
            [data-testid="stForm"] p:not(:only-child) { display: none !important; }

            /* 2. 文本框美化：去掉多余边框，防止重叠 */
            [data-testid="stTextInput"] input {
                background-color: #F8FAFC !important;
                border: 1px solid #E2E8F0 !important;
                color: #334155 !important;
                border-radius: 8px !important;
                font-size: 14px !important;
            }

            /* 3. 强制确保按钮文字可见 */
            button[kind="primaryFormSubmit"] div[data-testid="stMarkdownContainer"] p {
                display: block !important;
                visibility: visible !important;
                color: white !important;
                font-weight: bold !important;
            }

            /* 4. 隐藏 header */
            header, [data-testid="stHeader"] { visibility: hidden; }
        </style>
    """, unsafe_allow_html=True)

    st.write("\n" * 3)

    # --- 2. 比例锁定：保持大气卡片感 ---
    _, card_container, _ = st.columns([1.2, 3, 1.2])

    with card_container:
        with st.container(border=True):
            # 左右分栏：左侧品牌，右侧交互
            col_brand, col_auth = st.columns([1, 1.4], gap="large")

            with col_brand:
                st.write("\n")
                st.markdown("<h2 style='color:#1E3A8A; margin-bottom:5px;'>💠 爆款工场</h2>", unsafe_allow_html=True)
                st.markdown("<p style='color:#94A3B8; font-size: 14px; margin-bottom: 25px;'>创作者的 AI 军师</p>", unsafe_allow_html=True)
                
                features = [("🎯", "精准选题"), ("✍️", "爆款文案"), ("⚡", "效率革命")]
                for icon, title in features:
                    st.markdown(f"<div style='font-size:14px; color:#475569; margin-bottom:15px;'>{icon} <b>{title}</b></div>", unsafe_allow_html=True)
                st.success("已助力 10k+ 出圈")

            with col_auth:
                tab_l, tab_r = st.tabs(["安全登录", "快速注册"])
                
                with tab_l:
                    # 使用原生 form，不要加任何多余的 CSS margin
                    with st.form("login_clean_v8", border=False):
                        st.write("\n")
                        acc = st.text_input("账号", placeholder="手机号 / 邮箱", label_visibility="collapsed")
                        pwd = st.text_input("密码", type="password", placeholder="请输入密码", label_visibility="collapsed")
                        if st.form_submit_button("立即登录", use_container_width=True):
                            if acc and pwd:
                                success, msg = login_user(acc, pwd)
                                if success:
                                    st.session_state['user_phone'] = acc
                                    st.rerun()
                                else: st.error(msg)

                with tab_r:
                    with st.form("reg_clean_v8", border=False):
                        st.write("\n")
                        # 注册部分：垂直排列，严丝合缝
                        ru = st.text_input("账号", placeholder="手机号/邮箱", label_visibility="collapsed")
                        rp = st.text_input("密码", type="password", placeholder="请设置登录密码", label_visibility="collapsed")
                        rp2 = st.text_input("确认", type="password", placeholder="请再次输入密码", label_visibility="collapsed")
                        ri = st.text_input("邀请码", value="888888", label_visibility="collapsed")
                        
                        if st.form_submit_button("免费注册", use_container_width=True):
                            if not ru or not rp: st.warning("请完善信息")
                            elif rp != rp2: st.error("两次密码输入不一致")
                            else:
                                success, msg = register_user(ru, rp, ri)
                                if success: st.success("注册成功！请登录")
                                else: st.error(msg)

    st.write("\n" * 4)
    st.markdown("<p style='text-align: center; color: #CBD5E1; font-size: 10px;'>© 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.</p>", unsafe_allow_html=True)
