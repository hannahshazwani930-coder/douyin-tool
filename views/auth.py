# views/auth.py
import streamlit as st
from database import login_user, register_user

def view_auth():
    # --- 1. 物理级 CSS 穿透：强制去除底色，消除小眼睛断层 ---
    st.markdown("""
<style>
    /* 彻底屏蔽 Streamlit 默认提示语 */
    [data-testid="stFormInstructions"] { display: none !important; }
    
    /* 【核心对齐】统一 Tab 和 Placeholder 的字号 (14px) */
    button[data-baseweb="tab"] div {
        font-size: 14px !important;
        color: #475569 !important;
    }

    /* 【核心修复】强制去掉所有输入框容器的背景色（改用纯白） */
    /* 覆盖范围：外壳、输入区、小眼睛按钮容器 */
    [data-testid="stTextInput"] div[data-baseweb="input"],
    [data-testid="stPasswordInput"] div[data-baseweb="input"],
    [data-testid="stPasswordInput"] [data-baseweb="input"] > div {
        background-color: #FFFFFF !important; /* 强制纯白，消除断层 */
        border: 1px solid #E2E8F0 !important; /* 统一浅色边框 */
        border-radius: 6px !important;
    }

    /* 内部输入区透明化，确保不产生二次背景覆盖 */
    [data-testid="stTextInput"] input, 
    [data-testid="stPasswordInput"] input {
        background-color: transparent !important;
        color: #1E3A8A !important;
        font-size: 14px !important;
        height: 40px !important;
        border: none !important;
    }

    /* 【彻底杀掉小眼睛背景】强制小眼睛按钮背景透明 */
    [data-testid="stPasswordInput"] button {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Placeholder 样式对齐 */
    [data-testid="stTextInput"] input::placeholder,
    [data-testid="stPasswordInput"] input::placeholder {
        font-size: 14px !important;
        color: #94A3B8 !important;
    }

    /* 强制找回按钮文字 */
    button[kind="primaryFormSubmit"] [data-testid="stMarkdownContainer"] p {
        visibility: visible !important;
        display: block !important;
        color: #1E3A8A !important;
        font-weight: bold !important;
        font-size: 14px !important;
    }

    /* 隐藏顶部冗余 */
    header, [data-testid="stHeader"] { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

    st.write("\n" * 2)

    # --- 2. 比例锁定：保持大气紧凑感 ---
    _, card_container, _ = st.columns([1.3, 2.5, 1.3])

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
                # --- 右侧：登录/注册 ---
                t1, t2 = st.tabs(["安全登录", "快速注册"])
                
                with t1:
                    # 使用新的 key 来强制强制刷新组件渲染
                    with st.form("f_log_final_v11", border=False):
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
                    with st.form("f_reg_final_v11", border=False):
                        ru = st.text_input("RA", placeholder="手机号 / 邮箱", label_visibility="collapsed", key="v_reg_ru")
                        # 注册部分：垂直排版，样式统一
                        rp = st.text_input("RP1", type="password", placeholder="设置登录密码", label_visibility="collapsed", key="v_reg_rp1")
                        rp2 = st.text_input("RP2", type="password", placeholder="再次确认密码", label_visibility="collapsed", key="v_reg_rp2")
                        ri = st.text_input("RI", value="888888", label_visibility="collapsed", key="v_reg_ri")
                        if st.form_submit_button("免 费 注 册", use_container_width=True):
                            if rp != rp2: st.error("两次密码输入不一致")
                            else:
                                res, msg = register_user(ru, rp, ri)
                                if res: st.success("成功！请登录")

    # --- 3. 底部剧中声明 ---
    st.write("\n" * 4)
    st.markdown("<center style='color:#CBD5E1; font-size:12px;'>© 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.</center>", unsafe_allow_html=True)
