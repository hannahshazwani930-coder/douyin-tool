import streamlit as st
from database import login_user, register_user

def view_auth():
    # --- 1. 深度调色补丁：文本框颜色减淡，保持样式对齐 ---
    st.markdown("""
<style>
    /* 彻底隐藏英文提示 */
    [data-testid="stFormInstructions"] { display: none !important; }
    
    /* 1. 顶部 Tab 字号对齐 (14px) */
    button[data-baseweb="tab"] div {
        font-size: 14px !important;
        color: #64748B !important; /* 调淡非活动状态颜色 */
    }
    
    /* 2. 文本框深度减淡处理 */
    [data-testid="stTextInput"] input {
        background-color: #FDFDFE !important; /* 极淡底色，接近白色 */
        border: 1px solid #F1F5F9 !important; /* 极淡边框 */
        color: #1E3A8A !important;
        font-size: 14px !important;
        height: 42px !important;
    }
    
    /* 3. 框内提示文字 (Placeholder) 颜色大幅减淡 */
    [data-testid="stTextInput"] input::placeholder {
        font-size: 14px !important;
        color: #CBD5E1 !important; /* 极淡灰蓝色，看起来更轻盈 */
        font-weight: 300 !important;
    }

    /* 4. 按钮文字强制找回 */
    button[kind="primaryFormSubmit"] [data-testid="stMarkdownContainer"] p {
        visibility: visible !important;
        display: block !important;
        color: #1E3A8A !important;
        font-size: 14px !important;
        font-weight: bold !important;
    }

    /* 5. 净化界面 */
    header, [data-testid="stHeader"] { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

    st.write("\n" * 2)

    # --- 2. 布局逻辑 ---
    _, card_container, _ = st.columns([1.1, 3.2, 1.1])

    with card_container:
        with st.container(border=True):
            col_left, col_right = st.columns([1, 1.5], gap="large")

            with col_left:
                st.write("\n")
                st.markdown("### 💠 爆款工场")
                st.caption("创作者的 AI 军师")
                st.write("---")
                st.markdown("🎯 **精准选题**\n\n✍️ **爆款文案**\n\n⚡ **效率革命**")
                st.write("\n")
                st.success("已助力 10k+ 出圈")

            with col_right:
                # 顶部 Tabs
                t1, t2 = st.tabs(["安全登录", "快速注册"])
                
                with t1:
                    with st.form("f_login_pro", border=False):
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
                    with st.form("f_reg_pro", border=False):
                        ru = st.text_input("RA", placeholder="手机号 / 邮箱", label_visibility="collapsed", key="v_ru")
                        rp = st.text_input("RP", type="password", placeholder="请设置登录密码", label_visibility="collapsed", key="v_rp")
                        rp2 = st.text_input("RP2", type="password", placeholder="请再次确认密码", label_visibility="collapsed", key="v_rp2")
                        ri = st.text_input("RI", value="888888", label_visibility="collapsed", key="v_ri")
                        if st.form_submit_button("免 费 注 册", use_container_width=True):
                            if rp != rp2: st.error("密码不一致")
                            else:
                                res, msg = register_user(ru, rp, ri)
                                if res: st.success("成功！请登录")

    # --- 3. 底部剧中声明 ---
    st.write("\n" * 4)
    st.markdown("---")
    st.markdown("<center style='color:#E2E8F0; font-size:12px;'>© 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.</center>", unsafe_allow_html=True)
