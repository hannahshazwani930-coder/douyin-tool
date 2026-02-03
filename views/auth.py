# views/auth.py
import streamlit as st
from database import login_user, register_user

def view_auth():
    # --- 1. 物理级背景穿透 CSS ---
    st.markdown("""
<style>
    /* 彻底屏蔽英文提示语 */
    [data-testid="stFormInstructions"] { display: none !important; }
    
    /* 1. 样式对齐：Tab 标签和 Placeholder 统一为 14px */
    button[data-baseweb="tab"] div {
        font-size: 14px !important;
        color: #64748B !important;
    }

    /* 2. 核心：给整个文本框/密码框的外壳上色 */
    [data-testid="stTextInput"] div[data-baseweb="input"],
    [data-testid="stPasswordInput"] div[data-baseweb="input"] {
        background-color: #F9FAFB !important; /* 极淡且统一的底色 */
        border: 1px solid #F1F5F9 !important;
        border-radius: 8px !important;
    }

    /* 强制内部 input 和小眼睛按钮背景透明，确保完全透出外壳底色 */
    [data-testid="stTextInput"] input, 
    [data-testid="stPasswordInput"] input,
    [data-testid="stPasswordInput"] button {
        background-color: transparent !important;
        border: none !important;
        color: #1E3A8A !important;
        font-size: 14px !important;
        box-shadow: none !important;
    }

    /* 样式一致：Placeholder 颜色和大小 */
    [data-testid="stTextInput"] input::placeholder,
    [data-testid="stPasswordInput"] input::placeholder {
        font-size: 14px !important;
        color: #CBD5E1 !important;
    }

    /* 3. 按钮字样找回 */
    button[kind="primaryFormSubmit"] [data-testid="stMarkdownContainer"] p {
        visibility: visible !important;
        display: block !important;
        color: #1E3A8A !important;
        font-weight: bold !important;
        font-size: 14px !important;
    }

    /* 4. 界面净化 */
    header, [data-testid="stHeader"] { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

    st.write("\n" * 2)

    # --- 2. 比例控制：保持精致紧凑 ---
    _, card_container, _ = st.columns([1.4, 2.2, 1.4])

    with card_container:
        with st.container(border=True):
            col_l, col_r = st.columns([1, 1.5], gap="large")

            with col_l:
                # --- 左侧：图标+文案 ---
                st.write("\n")
                st.markdown("### 💠 爆款工场")
                st.caption("AI 驱动创作中枢")
                st.write("---")
                st.markdown("""
                🎯 **精准选题**
                ✍️ **爆款文案**
                ⚡ **效率革命**
                """)
                st.write("\n")
                st.success("已助力 10k+ 出圈")

            with col_r:
                # --- 右侧：登录/注册 ---
                t1, t2 = st.tabs(["安全登录", "快速注册"])
                
                with t1:
                    with st.form("f_login_final", border=False):
                        u = st.text_input("A", placeholder="手机号 / 邮箱", label_visibility="collapsed", key="v_u")
                        p = st.text_input("P", type="password", placeholder="请输入密码", label_visibility="collapsed", key="v_p")
                        if st.form_submit_button("立 即 登 录", use_container_width=True):
                            if u and p:
                                res, msg = login_user(u, p)
                                if res:
                                    st.session_state['user_phone'] = u
                                    st.rerun()
                                else: st.error(msg)

                with t2:
                    with st.form("f_reg_final", border=False):
                        ru = st.text_input("RA", placeholder="手机号 / 邮箱", label_visibility="collapsed", key="v_ru")
                        # 注册：垂直排版
                        rp = st.text_input("RP", type="password", placeholder="设置登录密码", label_visibility="collapsed", key="v_rp")
                        rp2 = st.text_input("RP2", type="password", placeholder="确认密码", label_visibility="collapsed", key="v_rp2")
                        ri = st.text_input("RI", value="888888", label_visibility="collapsed", key="v_ri")
                        if st.form_submit_button("免 费 注 册", use_container_width=True):
                            if rp != rp2: st.error("密码不一致")
                            else:
                                res, msg = register_user(ru, rp, ri)
                                if res: st.success("成功！请登录")

    # --- 3. 底部声明 ---
    st.write("\n" * 4)
    st.markdown("<center style='color:#CBD5E1; font-size:12px;'>© 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.</center>", unsafe_allow_html=True)
