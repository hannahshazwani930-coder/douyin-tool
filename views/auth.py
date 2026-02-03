# views/auth.py
import streamlit as st
from database import login_user, register_user

def view_auth():
    # --- 1. 悬浮动效 CSS 补丁：增加呼吸感与立体悬浮 ---
    st.markdown("""
        <style>
            /* 1. 彻底抹除 Streamlit 指令提示 */
            [data-testid="stFormInstructions"] { display: none !important; }

            /* 2. 核心：文本框/密码框 基础状态 */
            [data-testid="stTextInput"] div[data-baseweb="input"],
            [data-testid="stPasswordInput"] div[data-baseweb="input"] {
                background-color: white !important;
                border: 1px solid #E2E8F0 !important;
                border-radius: 8px !important;
                box-shadow: none !important;
                /* 关键：增加过渡动画，让悬浮变得丝滑 */
                transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
            }

            /* 3. 悬浮状态（Hover）：产生向上浮动和柔和阴影 */
            [data-testid="stTextInput"] div[data-baseweb="input"]:hover,
            [data-testid="stPasswordInput"] div[data-baseweb="input"]:hover {
                border-color: #1E3A8A !important; /* 悬浮时边框微深 */
                transform: translateY(-2px) !important; /* 向上轻微浮动 */
                box-shadow: 0 6px 16px rgba(30, 58, 138, 0.08) !important; /* 产生柔和的悬浮投影 */
            }

            /* 4. 聚焦状态（Focus）：点击输入时保持稳定 */
            [data-testid="stTextInput"] div[data-baseweb="input"]:focus-within,
            [data-testid="stPasswordInput"] div[data-baseweb="input"]:focus-within {
                border-color: #1E3A8A !important;
                background-color: #FFFFFF !important;
            }

            /* 5. 内部元素穿透透明化 */
            [data-testid="stTextInput"] input, 
            [data-testid="stPasswordInput"] input,
            [data-testid="stPasswordInput"] button,
            [data-baseweb="input"] > div {
                border: none !important;
                background-color: transparent !important;
                box-shadow: none !important;
                outline: none !important;
                color: #1E3A8A !important;
                font-size: 14px !important;
                height: 40px !important;
            }

            /* 6. 样式一致性：14px 锁定 */
            button[data-baseweb="tab"] div { font-size: 14px !important; color: #64748B !important; }
            [data-testid="stTextInput"] input::placeholder,
            [data-testid="stPasswordInput"] input::placeholder {
                font-size: 14px !important;
                color: #94A3B8 !important;
            }

            /* 7. 按钮文字强显 */
            button[kind="primaryFormSubmit"] [data-testid="stMarkdownContainer"] p {
                visibility: visible !important;
                display: block !important;
                color: #1E3A8A !important;
                font-weight: bold !important;
                font-size: 14px !important;
            }

            /* 净化全局 */
            header, [data-testid="stHeader"] { visibility: hidden; }
        </style>
    """, unsafe_allow_html=True)

    st.write("\n" * 2)

    # --- 2. 比例控制 ---
    _, card_container, _ = st.columns([1.3, 2.4, 1.3])

    with card_container:
        with st.container(border=True):
            col_l, col_r = st.columns([1, 1.4], gap="large")

            with col_l:
                st.write("\n")
                st.markdown("### 💠 爆款工场")
                st.caption("AI 驱动创作中枢")
                st.write("---")
                st.markdown("🎯 **精准选题**\n\n✍️ **爆款文案**\n\n⚡ **效率革命**")
                st.write("\n")
                st.success("已助力 10k+ 出圈")

            with col_r:
                t1, t2 = st.tabs(["安全登录", "快速注册"])
                
                with t1:
                    with st.form("f_login_hover_v13", border=False):
                        u = st.text_input("A", placeholder="手机号 / 邮箱", label_visibility="collapsed", key="v_log_u")
                        p = st.text_input("P", type="password", placeholder="请输入密码", label_visibility="collapsed", key="v_log_p")
                        if st.form_submit_button("立 即 登 录", use_container_width=True):
                            if u and p:
                                res, msg = login_user(u, p)
                                if res:
                                    st.session_state['user_phone'] = u
                                    st.rerun()
                                else: st.error(msg)

                with t2:
                    with st.form("f_reg_hover_v13", border=False):
                        ru = st.text_input("RA", placeholder="手机号 / 邮箱", label_visibility="collapsed", key="v_reg_ru")
                        rp = st.text_input("RP1", type="password", placeholder="设置登录密码", label_visibility="collapsed", key="v_reg_rp1")
                        rp2 = st.text_input("RP2", type="password", placeholder="再次确认密码", label_visibility="collapsed", key="v_reg_rp2")
                        ri = st.text_input("RI", value="888888", label_visibility="collapsed", key="v_reg_ri")
                        if st.form_submit_button("注 册 账 号", use_container_width=True):
                            if rp != rp2: st.error("两次密码输入不一致")
                            else:
                                res, msg = register_user(ru, rp, ri)
                                if res: st.success("成功！请登录")

    st.write("\n" * 4)
    st.markdown("<center style='color:#CBD5E1; font-size:12px;'>© 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.</center>", unsafe_allow_html=True)
