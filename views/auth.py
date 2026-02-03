# views/auth.py
import streamlit as st
from database import login_user, register_user

def view_auth():
    # --- 1. 深度对齐与净化 CSS ---
    st.markdown("""
<style>
    /* 【1. 物理抹除提示语】彻底干掉 Press Enter */
    [data-testid="stFormInstructions"] { display: none !important; }
    
    /* 【2. 统一颜色与字号】解决图示中颜色不一、样式不齐的问题 */
    [data-testid="stTextInput"] input, 
    [data-testid="stPasswordInput"] input {
        background-color: #F8FAFC !important; /* 统一极淡灰蓝色 */
        border: 1px solid #E2E8F0 !important;
        color: #1E3A8A !important;
        font-size: 14px !important;
        height: 40px !important;
        border-radius: 6px !important;
    }
    
    /* 统一 Placeholder 样式 */
    [data-testid="stTextInput"] input::placeholder,
    [data-testid="stPasswordInput"] input::placeholder {
        font-size: 14px !important;
        color: #94A3B8 !important;
    }

    /* 【3. 按钮文字强制找回】解决按钮无字的问题 */
    button[kind="primaryFormSubmit"] [data-testid="stMarkdownContainer"] p {
        visibility: visible !important;
        display: block !important;
        color: #1E3A8A !important; /* 调整为与主题一致的深蓝色 */
        font-weight: bold !important;
        font-size: 14px !important;
    }

    /* 【4. Tab 标签美化】防止重叠乱码 */
    button[data-baseweb="tab"] div {
        font-size: 14px !important;
        color: #475569 !important;
    }

    /* 净化顶部 */
    header, [data-testid="stHeader"] { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

    st.write("\n" * 2)

    # --- 2. 比例锁定：[1.4, 2, 1.4] 让卡片更紧凑，解决文本框太宽的问题 ---
    _, card_container, _ = st.columns([1.4, 2, 1.4])

    with card_container:
        with st.container(border=True):
            col_left, col_right = st.columns([1, 1.4], gap="large")

            with col_left:
                st.write("\n")
                st.markdown("### 💠 爆款工场")
                st.caption("创作者的 AI 军师")
                st.write("---")
                st.markdown("""
                🎯 **精准选题**
                ✍️ **爆款文案**
                ⚡ **效率革命**
                """)
                st.write("\n")
                st.success("已助力 10k+ 出圈")

            with col_right:
                # 顶部 Tabs
                t1, t2 = st.tabs(["安全登录", "快速注册"])
                
                with t1:
                    with st.form("f_login_aligned", border=False):
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
                    with st.form("f_reg_aligned", border=False):
                        ru = st.text_input("RA", placeholder="手机号 / 邮箱", label_visibility="collapsed", key="reg_u")
                        # 注册部分：垂直排列更专业
                        rp = st.text_input("RP", type="password", placeholder="请设置登录密码", label_visibility="collapsed", key="reg_p1")
                        rp2 = st.text_input("RP2", type="password", placeholder="请再次确认密码", label_visibility="collapsed", key="reg_p2")
                        ri = st.text_input("RI", value="888888", label_visibility="collapsed", key="reg_i")
                        if st.form_submit_button("免 费 注 册", use_container_width=True):
                            if rp != rp2: st.error("密码不一致")
                            else:
                                res, msg = register_user(ru, rp, ri)
                                if res: st.success("成功！请登录")

    # --- 3. 底部剧中声明 ---
    st.write("\n" * 4)
    st.markdown("<center style='color:#94A3B8; font-size:12px;'>© 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.</center>", unsafe_allow_html=True)
