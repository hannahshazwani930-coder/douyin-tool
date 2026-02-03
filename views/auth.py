# views/auth.py
import streamlit as st
from database import login_user, register_user

def view_auth():
    # --- 1. 视觉修正补丁：解决颜色不一、标签重叠、代码外露 ---
    st.markdown("""
        <style>
            /* 【解决 Tab 乱码】强制 Tab 标签横向排列，不重叠 */
            button[data-baseweb="tab"] {
                padding: 10px 20px !important;
                margin-right: 10px !important;
            }
            div[data-baseweb="tab-list"] {
                gap: 10px !important;
            }

            /* 【统一底色】强制所有输入框背景一致，解决“两个色不统一” */
            [data-testid="stTextInput"] input {
                background-color: #F8FAFC !important; /* 统一浅灰蓝底色 */
                border: 1px solid #E2E8F0 !important;
                border-radius: 6px !important;
                color: #334155 !important;
            }

            /* 【物理抹除英文提示】彻底杀掉 Press Enter */
            [data-testid="stFormInstructions"] { display: none !important; }
            .stForm [data-testid="stMarkdownContainer"] p:not(:only-child) { display: none !important; }

            /* 【按钮文字强制显示】解决“立即登录/注册”看不见的问题 */
            button[kind="primaryFormSubmit"] [data-testid="stMarkdownContainer"] p {
                visibility: visible !important;
                display: block !important;
                color: #1E3A8A !important; /* 深蓝色文字，确保清晰 */
                font-weight: bold !important;
                font-size: 16px !important;
            }

            /* 【隐藏顶部冗余】 */
            header, [data-testid="stHeader"] { visibility: hidden; }
        </style>
    """, unsafe_allow_html=True)

    st.write("\n" * 2)

    # --- 2. 居中弹性卡片布局 ---
    _, card_container, _ = st.columns([1.1, 3.2, 1.1])

    with card_container:
        with st.container(border=True):
            col_brand, col_auth = st.columns([1, 1.5], gap="large")

            with col_brand:
                # --- 左侧：图标+精简文案 ---
                st.write("\n")
                st.markdown("<h3 style='color:#1E3A8A; margin-bottom:0;'>💠 爆款工场</h3>", unsafe_allow_html=True)
                st.markdown("<p style='color:#94A3B8; font-size: 12px; margin-bottom: 25px;'>创作者的 AI 军师</p>", unsafe_allow_html=True)
                
                features = [("🎯", "精准选题"), ("✍️", "爆款文案"), ("⚡", "效率革命")]
                for icon, title in features:
                    st.markdown(f"<div style='font-size:13px; color:#475569; margin-bottom:12px;'>{icon} <b>{title}</b></div>", unsafe_allow_html=True)
                st.success("已助力 10k+ 出圈")

            with col_auth:
                # --- 右侧：登录/注册交互 ---
                tab_l, tab_r = st.tabs(["安全登录", "快速注册"])
                
                with tab_l:
                    with st.form("login_final_fixed", border=False):
                        acc = st.text_input("账号", placeholder="手机号 / 邮箱", label_visibility="collapsed")
                        pwd = st.text_input("密码", type="password", placeholder="请输入密码", label_visibility="collapsed")
                        if st.form_submit_button("立 即 登 录", use_container_width=True):
                            if acc and pwd:
                                success, msg = login_user(acc, pwd)
                                if success:
                                    st.session_state['user_phone'] = acc
                                    st.rerun()
                                else: st.error(msg)

                with tab_r:
                    with st.form("reg_final_fixed", border=False):
                        ru = st.text_input("手机号/邮箱", placeholder="手机号/邮箱", label_visibility="collapsed")
                        rp = st.text_input("设置密码", type="password", placeholder="请设置登录密码", label_visibility="collapsed")
                        rp2 = st.text_input("确认密码", type="password", placeholder="请再次确认密码", label_visibility="collapsed")
                        ri = st.text_input("邀请码", value="888888", label_visibility="collapsed")
                        if st.form_submit_button("免 费 注 册", use_container_width=True):
                            if rp != rp2: st.error("两次密码不一致")
                            else:
                                success, msg = register_user(ru, rp, ri)
                                if success: st.success("注册成功！")

    # --- 3. 底部剧中声明 (修正代码外露问题) ---
    st.write("\n" * 4)
    st.markdown("""
        <div style="text-align: center; color: #94A3B8; font-size: 11px;">
            © 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.
        </div>
    """, unsafe_allow_html=True)
