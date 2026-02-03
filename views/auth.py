# views/auth.py
import streamlit as st
from database import login_user, register_user

def view_auth():
    # --- 1. 极致去色 CSS：消除背景色断层，对齐样式 ---
    st.markdown("""
        <style>
            /* 1. 彻底抹除 Streamlit 指令提示 */
            [data-testid="stFormInstructions"] { display: none !important; }

            /* 2. 核心：强制去掉所有文本框/密码框容器的背景底色 */
            /* 锁定包含 input 和小眼睛的顶层外壳 */
            [data-testid="stTextInput"] div[data-baseweb="input"],
            [data-testid="stPasswordInput"] div[data-baseweb="input"],
            [data-baseweb="input"] > div {
                background-color: white !important; /* 强制背景为纯白 */
                border: 1px solid #E2E8F0 !important; /* 极细边框 */
                border-radius: 6px !important;
                box-shadow: none !important;
            }

            /* 3. 穿透处理：让内部 input 和小眼睛按钮背景完全透明 */
            [data-testid="stTextInput"] input, 
            [data-testid="stPasswordInput"] input,
            [data-testid="stPasswordInput"] button {
                background-color: transparent !important;
                border: none !important;
                color: #1E3A8A !important;
                font-size: 14px !important;
                height: 42px !important;
            }

            /* 4. 样式对齐：Tab 标题和 Placeholder 统一 14px */
            button[data-baseweb="tab"] div {
                font-size: 14px !important;
                color: #64748B !important;
            }
            [data-testid="stTextInput"] input::placeholder,
            [data-testid="stPasswordInput"] input::placeholder {
                font-size: 14px !important;
                color: #94A3B8 !important;
            }

            /* 5. 按钮文字强制找回 */
            button[kind="primaryFormSubmit"] [data-testid="stMarkdownContainer"] p {
                visibility: visible !important;
                display: block !important;
                color: #1E3A8A !important;
                font-weight: bold !important;
                font-size: 14px !important;
            }

            /* 全局净化 */
            header, [data-testid="stHeader"] { visibility: hidden; }
        </style>
    """, unsafe_allow_html=True)

    st.write("\n" * 2)

    # --- 2. 比例控制：[1.3, 2.4, 1.3] 保持卡片精致 ---
    _, card_container, _ = st.columns([1.3, 2.4, 1.3])

    with card_container:
        with st.container(border=True):
            col_l, col_r = st.columns([1, 1.4], gap="large")

            with col_l:
                # --- 左侧：品牌文案 ---
                st.write("\n")
                st.markdown("### 💠 爆款工场")
                st.caption("AI 驱动创作中枢")
                st.write("---")
                st.markdown("🎯 **精准选题**\n\n✍️ **爆款文案**\n\n⚡ **效率革命**")
                st.write("\n")
                st.success("已助力 10k+ 出圈")

            with col_r:
                # --- 右侧：登录/注册交互 ---
                t1, t2 = st.tabs(["安全登录", "快速注册"])
                
                with t1:
                    with st.form("f_login_clean", border=False):
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
                    with st.form("f_reg_clean", border=False):
                        ru = st.text_input("RA", placeholder="手机号 / 邮箱", label_visibility="collapsed", key="v_reg_ru")
                        # 注册：遵照要求，采用上下对齐排版
                        rp = st.text_input("RP1", type="password", placeholder="请设置登录密码", label_visibility="collapsed", key="v_reg_rp1")
                        rp2 = st.text_input("RP2", type="password", placeholder="请再次确认密码", label_visibility="collapsed", key="v_reg_rp2")
                        ri = st.text_input("RI", value="888888", label_visibility="collapsed", key="v_reg_ri")
                        if st.form_submit_button("免 费 注 册", use_container_width=True):
                            if rp != rp2: st.error("两次密码输入不一致")
                            else:
                                res, msg = register_user(ru, rp, ri)
                                if res: st.success("成功！请登录")

    # --- 3. 底部声明 ---
    st.write("\n" * 4)
    st.markdown("<center style='color:#CBD5E1; font-size:12px;'>© 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.</center>", unsafe_allow_html=True)
