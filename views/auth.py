# views/auth.py
import streamlit as st
from database import login_user, register_user

def view_auth():
    # --- 1. 工业级 CSS 补丁：实现底色全覆盖与样式对齐 ---
    st.markdown("""
<style>
    /* 彻底屏蔽英文提示语 */
    [data-testid="stFormInstructions"] { display: none !important; }
    
    /* 1. 统一字号基准 (14px) */
    button[data-baseweb="tab"] div {
        font-size: 14px !important;
        color: #475569 !important;
    }

    /* 2. 核心修复：文本框与密码框容器底色绝对统一，实现“覆盖小眼睛背景” */
    /* 锁定 input 的外层包裹 div */
    [data-testid="stTextInput"] div[data-baseweb="input"],
    [data-testid="stPasswordInput"] div[data-baseweb="input"] {
        background-color: #F8FAFC !important; /* 统一极淡灰蓝色底色 */
        border: 1px solid #E2E8F0 !important;
        border-radius: 6px !important;
    }

    /* 强制让输入框本体透明，透出容器的底色 */
    [data-testid="stTextInput"] input, 
    [data-testid="stPasswordInput"] input {
        background-color: transparent !important;
        color: #1E3A8A !important;
        font-size: 14px !important;
        height: 40px !important;
        border: none !important;
    }

    /* 【关键】让小眼睛按钮透明，使其完美融入容器背景色 */
    [data-testid="stPasswordInput"] button {
        background-color: transparent !important;
        border: none !important;
        margin-right: 5px !important;
    }

    /* 提示文字 (Placeholder) 样式完全对齐 */
    [data-testid="stTextInput"] input::placeholder,
    [data-testid="stPasswordInput"] input::placeholder {
        font-size: 14px !important;
        color: #94A3B8 !important;
    }

    /* 3. 按钮文字强制找回 */
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

    # --- 2. 比例控制：[1.4, 2, 1.4] 保持卡片精致紧凑 ---
    _, card_container, _ = st.columns([1.4, 2, 1.4])

    with card_container:
        with st.container(border=True):
            col_l, col_r = st.columns([1, 1.4], gap="large")

            with col_l:
                # --- 左侧：品牌展示 ---
                st.write("\n")
                st.markdown("### 💠 爆款工场")
                st.caption("AI 驱动创作中枢")
                st.write("---")
                st.markdown("""
                🎯 **精准选题**
                ✍️ **爆款文案**
                ⚡ **效率革命**
                """)
                st.success("已助力 10k+ 出圈")

            with col_r:
                # --- 右侧：登录/注册交互 ---
                t1, t2 = st.tabs(["安全登录", "快速注册"])
                
                with t1:
                    with st.form("login_final_fixed", border=False):
                        u = st.text_input("A", placeholder="手机号 / 邮箱", label_visibility="collapsed", key="log_u")
                        p = st.text_input("P", type="password", placeholder="请输入密码", label_visibility="collapsed", key="log_p")
                        if st.form_submit_button("立 即 登 录", use_container_width=True):
                            if u and p:
                                res, msg = login_user(u, p)
                                if res:
                                    st.session_state['user_phone'] = u
                                    st.rerun()
                                else: st.error(msg)

                with t2:
                    with st.form("reg_final_fixed", border=False):
                        ru = st.text_input("RA", placeholder="手机号 / 邮箱", label_visibility="collapsed", key="reg_u")
                        # 注册区域：密码框垂直排列，彰显专业稳重
                        rp = st.text_input("RP1", type="password", placeholder="请设置登录密码", label_visibility="collapsed", key="reg_p1")
                        rp2 = st.text_input("RP2", type="password", placeholder="请再次确认密码", label_visibility="collapsed", key="reg_p2")
                        ri = st.text_input("RI", value="888888", label_visibility="collapsed", key="reg_i")
                        if st.form_submit_button("免 费 注 册", use_container_width=True):
                            if rp != rp2: st.error("两次密码输入不一致")
                            else:
                                res, msg = register_user(ru, rp, ri)
                                if res: st.success("成功！请登录")

    # --- 3. 底部剧中声明 ---
    st.write("\n" * 4)
    st.markdown("<center style='color:#94A3B8; font-size:12px;'>© 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.</center>", unsafe_allow_html=True)
