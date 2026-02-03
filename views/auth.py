# views/auth.py
import streamlit as st
from database import login_user, register_user

def view_auth():
    # --- 1. 深度穿透 CSS：消除色差，统一视觉基准 ---
    st.markdown("""
<style>
    /* 彻底屏蔽英文提示语 */
    [data-testid="stFormInstructions"] { display: none !important; }
    
    /* 1. 样式高度对齐：Tab 标签和 Placeholder 统一为 14px */
    button[data-baseweb="tab"] div {
        font-size: 14px !important;
        color: #64748B !important;
    }

    /* 2. 核心：给整个输入框外壳上色，解决“小眼睛”背景断层问题 */
    /* 我们锁定包含 input 和 按钮的共同父容器 */
    [data-testid="stTextInput"] div[data-baseweb="input"],
    [data-testid="stPasswordInput"] div[data-baseweb="input"] {
        background-color: #F9FAFB !important; /* 统一的极淡底色 */
        border: 1px solid #F1F5F9 !important; /* 极淡边框线 */
        border-radius: 8px !important;
        transition: all 0.2s;
    }

    /* 3. 穿透处理：让内部所有组件背景透明，透出父容器底色 */
    [data-testid="stTextInput"] input, 
    [data-testid="stPasswordInput"] input,
    [data-testid="stPasswordInput"] button {
        background-color: transparent !important;
        border: none !important;
        color: #1E3A8A !important;
        font-size: 14px !important;
        box-shadow: none !important;
    }

    /* Placeholder 颜色与字号保持 100% 一致 */
    [data-testid="stTextInput"] input::placeholder,
    [data-testid="stPasswordInput"] input::placeholder {
        font-size: 14px !important;
        color: #CBD5E1 !important;
    }

    /* 4. 提交按钮文字强制找回 */
    button[kind="primaryFormSubmit"] [data-testid="stMarkdownContainer"] p {
        visibility: visible !important;
        display: block !important;
        color: #1E3A8A !important;
        font-weight: bold !important;
        font-size: 14px !important;
    }

    /* 5. 净化全局界面 */
    header, [data-testid="stHeader"] { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

    st.write("\n" * 2)

    # --- 2. 布局逻辑：[1.4, 2.2, 1.4] 紧凑精致布局 ---
    _, card_container, _ = st.columns([1.4, 2.2, 1.4])

    with card_container:
        with st.container(border=True):
            col_left, col_right = st.columns([1, 1.5], gap="large")

            with col_left:
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
                st.write("\n")
                st.success("已助力 10k+ 出圈")

            with col_right:
                # --- 右侧：登录/注册交互 ---
                t1, t2 = st.tabs(["安全登录", "快速注册"])
                
                with t1:
                    with st.form("f_login_pro_v9", border=False):
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
                    with st.form("f_reg_pro_v9", border=False):
                        ru = st.text_input("RA", placeholder="手机号 / 邮箱", label_visibility="collapsed", key="v_ru")
                        # 注册部分：遵照要求，采用上下对齐排版
                        rp = st.text_input("RP1", type="password", placeholder="请设置登录密码", label_visibility="collapsed", key="v_rp1")
                        rp2 = st.text_input("RP2", type="password", placeholder="请再次确认密码", label_visibility="collapsed", key="v_rp2")
                        ri = st.text_input("RI", value="888888", label_visibility="collapsed", key="v_ri")
                        if st.form_submit_button("免 费 注 册", use_container_width=True):
                            if rp != rp2: st.error("两次密码输入不一致")
                            else:
                                res, msg = register_user(ru, rp, ri)
                                if res: st.success("注册成功！请切换登录")

    # --- 3. 底部剧中声明 ---
    st.write("\n" * 4)
    st.markdown("<center style='color:#CBD5E1; font-size:12px;'>© 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.</center>", unsafe_allow_html=True)
