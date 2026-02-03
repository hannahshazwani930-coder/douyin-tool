# views/auth.py
import streamlit as st
from database import login_user, register_user

def view_auth():
    # --- 1. 深度对齐 CSS：锁定统一字号与色彩 ---
    st.markdown("""
        <style>
            /* 【统一字体基准】 */
            :root {
                --pro-font-size: 14px;
                --pro-text-color: #475569;
                --pro-active-color: #1E3A8A;
            }

            /* 1. 顶部 Tab 样式对齐 */
            button[data-baseweb="tab"] {
                font-size: var(--pro-font-size) !important;
                color: var(--pro-text-color) !important;
                font-weight: 500 !important;
                padding: 12px 20px !important;
            }
            button[aria-selected="true"] {
                color: var(--pro-active-color) !important;
                border-bottom-color: var(--pro-active-color) !important;
            }

            /* 2. 文本框提示信息 (Placeholder) 样式对齐 */
            [data-testid="stTextInput"] input::placeholder {
                font-size: var(--pro-font-size) !important;
                color: var(--pro-text-color) !important;
                opacity: 0.8 !important; /* 稍微减淡以示区分，但大小一致 */
            }

            /* 3. 输入框本体样式统一 */
            [data-testid="stTextInput"] input {
                background-color: #F8FAFC !important;
                border: 1px solid #E2E8F0 !important;
                border-radius: 6px !important;
                font-size: var(--pro-font-size) !important;
                height: 45px !important;
                color: var(--pro-active-color) !important;
            }

            /* 4. 彻底物理屏蔽英文提示语 */
            [data-testid="stFormInstructions"] { display: none !important; }
            .stForm [data-testid="stMarkdownContainer"] p:not(:only-child) { display: none !important; }

            /* 5. 按钮文字保障 */
            button[kind="primaryFormSubmit"] [data-testid="stMarkdownContainer"] p {
                visibility: visible !important;
                display: block !important;
                color: var(--pro-active-color) !important;
                font-weight: bold !important;
                font-size: var(--pro-font-size) !important;
            }

            /* 净化顶部 */
            header, [data-testid="stHeader"] { visibility: hidden; }
        </style>
    """, unsafe_allow_html=True)

    st.write("\n" * 2)

    # --- 2. 卡片布局 ---
    _, card_container, _ = st.columns([1.1, 3.2, 1.1])

    with card_container:
        with st.container(border=True):
            col_brand, col_auth = st.columns([1, 1.5], gap="large")

            with col_brand:
                st.write("\n")
                st.markdown("<h3 style='color:#1E3A8A; margin-bottom:5px;'>💠 爆款工场</h3>", unsafe_allow_html=True)
                st.markdown("<p style='color:#94A3B8; font-size: 12px; margin-bottom: 25px;'>创作者的 AI 军师</p>", unsafe_allow_html=True)
                
                features = [("🎯", "精准选题"), ("✍️", "爆款文案"), ("⚡", "效率革命")]
                for icon, title in features:
                    st.markdown(f"<div style='font-size:13px; color:#475569; margin-bottom:12px;'>{icon} <b>{title}</b></div>", unsafe_allow_html=True)
                st.success("已助力 10k+ 出圈")

            with col_auth:
                # 使用 Tabs
                tab_l, tab_r = st.tabs(["安全登录", "快速注册"])
                
                with tab_l:
                    with st.form("login_unified", border=False):
                        acc = st.text_input("账号", placeholder="手机号 / 邮箱", label_visibility="collapsed", key="u_acc")
                        pwd = st.text_input("密码", type="password", placeholder="请输入密码", label_visibility="collapsed", key="u_pwd")
                        if st.form_submit_button("立 即 登 录", use_container_width=True):
                            if acc and pwd:
                                success, msg = login_user(acc, pwd)
                                if success:
                                    st.session_state['user_phone'] = acc
                                    st.rerun()
                                else: st.error(msg)

                with tab_r:
                    with st.form("reg_unified", border=False):
                        ru = st.text_input("账号", placeholder="手机号 / 邮箱", label_visibility="collapsed", key="r_acc")
                        rp = st.text_input("密码", type="password", placeholder="请设置登录密码", label_visibility="collapsed", key="r_pwd")
                        rp2 = st.text_input("确认", type="password", placeholder="请再次确认密码", label_visibility="collapsed", key="r_pwd2")
                        ri = st.text_input("邀请码", value="888888", label_visibility="collapsed", key="r_inv")
                        if st.form_submit_button("免 费 注 册", use_container_width=True):
                            if rp != rp2: st.error("密码不一致")
                            else:
                                success, msg = register_user(ru, rp, ri)
                                if success: st.success("成功！请登录")
    
    # --- 3. 底部剧中声明 ---
    st.write("\n" * 4)
    st.markdown("<div style='text-align: center; color: #94A3B8; font-size: 12px;'>© 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.</div>", unsafe_allow_html=True)
