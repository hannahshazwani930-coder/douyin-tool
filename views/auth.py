# views/auth.py
import streamlit as st
from database import login_user, register_user

def view_auth():
    # --- 1. 像素级 CSS 补丁：强制并排对齐、文字显现、屏蔽提示 ---
    st.markdown("""
        <style>
            /* 【彻底抹除提示语】物理屏蔽 Streamlit 官方提示容器 */
            [data-testid="stFormInstructions"] { display: none !important; }
            .stForm [data-testid="stMarkdownContainer"] p:not(:only-child) { display: none !important; }

            /* 【强制找回按钮文字】最高权重保障文字可见 */
            button[kind="primaryFormSubmit"] div[data-testid="stMarkdownContainer"] p {
                display: block !important;
                visibility: visible !important;
                color: #1E3A8A !important; /* 调整为深蓝色增强对比度 */
                font-size: 15px !important;
                font-weight: bold !important;
                margin: 0 !important;
            }

            /* 【文本框精致化】浅色底、极细边框、小字号 Placeholder */
            [data-testid="stTextInput"] input {
                background-color: #F8FAFC !important;
                color: #334155 !important;
                border: 1px solid #E2E8F0 !important;
                font-size: 13px !important;
                height: 38px !important;
                border-radius: 6px !important;
            }
            [data-testid="stTextInput"] input::placeholder {
                color: #94A3B8 !important;
                font-size: 11px !important;
            }

            /* 【核心修复：并排撑满】消除列间距，让组件“不到边”的问题彻底消失 */
            [data-testid="stHorizontalBlock"] {
                gap: 0.5rem !important; /* 缩小间距，确保撑满 */
            }
            [data-testid="stHorizontalBlock"] > div {
                width: 100% !important;
            }

            /* 净化顶部 */
            header, [data-testid="stHeader"] { visibility: hidden; }
        </style>
    """, unsafe_allow_html=True)

    st.write("\n" * 3)

    # --- 2. 宽度锁定：[1.4, 2.2, 1.4] 营造高度聚焦的紧凑感 ---
    _, card_container, _ = st.columns([1.4, 2.2, 1.4])

    with card_container:
        with st.container(border=True):
            # 内部左右分栏：左侧品牌 (38%)，右侧交互 (62%)
            col_brand, col_auth = st.columns([1, 1.6], gap="large")

            with col_brand:
                # --- 左侧：精致精简文案 ---
                st.write("\n")
                st.markdown("<h3 style='color:#1E3A8A; margin-bottom:0;'>💠 爆款工场</h3>", unsafe_allow_html=True)
                st.markdown("<p style='color:#94A3B8; font-size: 12px; margin-bottom: 20px;'>创作者的 AI 军师</p>", unsafe_allow_html=True)
                
                features = [
                    ("🎯", "精准选题"),
                    ("✍️", "爆款文案"),
                    ("⚡", "效率革命")
                ]
                for icon, title in features:
                    st.markdown(f"<div style='font-size:13px; color:#475569; margin-bottom:12px;'>{icon} <b>{title}</b></div>", unsafe_allow_html=True)
                
                st.write("\n")
                st.success("10k+ 创作者首选")

            with col_auth:
                # --- 右侧：登录/注册交互 ---
                tab_l, tab_r = st.tabs(["安全登录", "快速注册"])
                
                with tab_l:
                    with st.form("login_final_compact", border=False):
                        st.write("\n")
                        acc = st.text_input("账号", placeholder="手机号 / 邮箱", label_visibility="collapsed")
                        pwd = st.text_input("密码", type="password", placeholder="请输入密码", label_visibility="collapsed")
                        
                        if st.form_submit_button("立 即 登 录", use_container_width=True):
                            if acc and pwd:
                                success, msg = login_user(acc, pwd)
                                if success:
                                    st.session_state['user_phone'] = acc
                                    st.rerun()
                                else: st.error(msg)
                            else: st.warning("请完善信息")

                with tab_r:
                    with st.form("reg_final_compact", border=False):
                        st.write("\n")
                        ru = st.text_input("账号", placeholder="手机号/邮箱", label_visibility="collapsed")
                        
                        # --- 核心改进：密码框水平并排且撑满 ---
                        p_col1, p_col2 = st.columns(2)
                        with p_col1:
                            rp = st.text_input("设置密码", type="password", placeholder="设置密码", label_visibility="collapsed")
                        with p_col2:
                            rp2 = st.text_input("确认密码", type="password", placeholder="确认密码", label_visibility="collapsed")
                        
                        ri = st.text_input("邀请码", value="888888", label_visibility="collapsed")
                        
                        if st.form_submit_button("注 册 账 号", use_container_width=True):
                            if rp != rp2: st.error("两次密码不一致")
                            elif not ru or not rp: st.warning("请填写完整")
                            else:
                                success, msg = register_user(ru, rp, ri)
                                if success: st.success("成功！请登录")
                                else: st.error(msg)

    # --- 3. 底部剧中声明 ---
    st.write("\n" * 4)
    st.markdown("<p style='text-align: center; color: #CBD5E1; font-size: 10px;'>© 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.</p>", unsafe_allow_html=True)
