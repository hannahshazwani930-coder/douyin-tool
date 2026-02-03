# views/auth.py
import streamlit as st
from database import login_user, register_user

def view_auth():
    # --- 1. 极致纯净 CSS：去掉背景色，对齐样式 ---
    st.markdown("""
<style>
    /* 彻底屏蔽英文提示语 */
    [data-testid="stFormInstructions"] { display: none !important; }
    
    /* 1. 样式对齐：Tab 标签字号锁定 14px */
    button[data-baseweb="tab"] div {
        font-size: 14px !important;
        color: #64748B !important;
    }

    /* 2. 核心：去掉所有背景色，统一使用纯白底色 */
    /* 锁定输入框外壳，解决“小眼睛”背景断层 */
    [data-testid="stTextInput"] div[data-baseweb="input"],
    [data-testid="stPasswordInput"] div[data-baseweb="input"] {
        background-color: #FFFFFF !important; /* 纯白底色，去掉之前的浅灰色 */
        border: 1px solid #E2E8F0 !important; /* 极细浅色边框 */
        border-radius: 6px !important;
        box-shadow: none !important;
    }

    /* 3. 内部透传：确保输入区和按钮都是透明的，直接透出底层的纯白 */
    [data-testid="stTextInput"] input, 
    [data-testid="stPasswordInput"] input,
    [data-testid="stPasswordInput"] button {
        background-color: transparent !important;
        border: none !important;
        color: #1E3A8A !important;
        font-size: 14px !important;
        height: 40px !important;
    }

    /* Placeholder 字号颜色 100% 对齐 */
    [data-testid="stTextInput"] input::placeholder,
    [data-testid="stPasswordInput"] input::placeholder {
        font-size: 14px !important;
        color: #94A3B8 !important;
    }

    /* 4. 按钮文字保障 */
    button[kind="primaryFormSubmit"] [data-testid="stMarkdownContainer"] p {
        visibility: visible !important;
        display: block !important;
        color: #1E3A8A !important;
        font-weight: bold !important;
        font-size: 14px !important;
    }

    /* 净化顶部 */
    header, [data-testid="stHeader"] { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

    st.write("\n" * 2)

    # --- 2. 比例控制：保持紧凑 ---
    _, card_container, _ = st.columns([1.4, 2.2, 1.4])

    with card_container:
        with st.container(border=True):
            col_l, col_r = st.columns([1, 1.5], gap="large")

            with col_l:
                # --- 左侧：品牌文案 ---
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
                # --- 右侧：登录/注册交互 ---
                t1, t2 = st.tabs(["安全登录", "快速注册"])
                
                with t1:
                    with st.form("f_login_clean_v10", border=False):
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
                    with st.form("f_reg_clean_v10", border=False):
                        ru = st.text_input("RA", placeholder="手机号 / 邮箱", label_visibility="collapsed", key="v_ru")
                        # 注册：保持稳重的垂直排版
                        rp = st.text_input("RP", type="password", placeholder="请设置登录密码", label_visibility="collapsed", key="v_rp")
                        rp2 = st.text_input("RP2", type="password", placeholder="确认密码", label_visibility="collapsed", key="v_rp2")
                        ri = st.text_input("RI", value="888888", label_visibility="collapsed", key="v_ri")
                        if st.form_submit_button("注 册 账 号", use_container_width=True):
                            if rp != rp2: st.error("两次密码输入不一致")
                            else:
                                res, msg = register_user(ru, rp, ri)
                                if res: st.success("成功！请登录")

    # --- 3. 底部剧中声明 ---
    st.write("\n" * 4)
    st.markdown("<center style='color:#CBD5E1; font-size:12px;'>© 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.</center>", unsafe_allow_html=True)
