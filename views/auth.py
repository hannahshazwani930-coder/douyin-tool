# views/auth.py
import streamlit as st
from database import login_user, register_user

def view_auth():
    # --- 1. 终极视觉补丁：强制底色撑满、净化 UI ---
    st.markdown("""
        <style>
            /* 【彻底抹除提示语】物理屏蔽 Streamlit 官方提示容器 */
            [data-testid="stFormInstructions"] { display: none !important; }
            .stForm [data-testid="stMarkdownContainer"] p:not(:only-child) { display: none !important; }

            /* 【文本框底色撑满】解决底色不到边、缩进的问题 */
            [data-testid="stTextInput"] input {
                background-color: #F8FAFC !important; /* 浅灰色背景 */
                color: #334155 !important;
                border: 1px solid #E2E8F0 !important;
                border-radius: 6px !important;
                width: 100% !important;        /* 强制宽度撑满 */
                box-sizing: border-box !important; /* 确保内边距不影响背景填充 */
                padding: 10px 15px !important;
                font-size: 13px !important;
                height: 42px !important;
            }
            
            /* 移除聚焦时的厚重边框 */
            [data-testid="stTextInput"] input:focus {
                border-color: #1E3A8A !important;
                box-shadow: none !important;
            }

            /* 【按钮文字 100% 显现】最高优先级保障 */
            button[kind="primaryFormSubmit"] div[data-testid="stMarkdownContainer"] p {
                display: block !important;
                visibility: visible !important;
                color: #1E3A8A !important;
                font-size: 15px !important;
                font-weight: bold !important;
                margin: 0 !important;
            }

            /* 隐藏顶部工具栏 */
            header, [data-testid="stHeader"] { visibility: hidden; }
            
            /* 调整表单内部组件的垂直间距，让上下排列更紧凑 */
            [data-testid="stVerticalBlock"] { gap: 0.8rem !important; }
        </style>
    """, unsafe_allow_html=True)

    st.write("\n" * 3)

    # --- 2. 宽度比例锁定：保持精致的窄卡片视觉 ---
    _, card_container, _ = st.columns([1.3, 2.4, 1.3])

    with card_container:
        with st.container(border=True):
            # 内部左右分栏
            col_brand, col_auth = st.columns([1, 1.5], gap="large")

            with col_brand:
                # --- 左侧：图标+精简文案 ---
                st.write("\n")
                st.markdown("<h3 style='color:#1E3A8A; margin-bottom:0;'>💠 爆款工场</h3>", unsafe_allow_html=True)
                st.markdown("<p style='color:#94A3B8; font-size: 12px; margin-bottom: 20px;'>AI 驱动创作中枢</p>", unsafe_allow_html=True)
                
                features = [("🎯", "精准选题"), ("✍️", "爆款文案"), ("⚡", "效率革命")]
                for icon, title in features:
                    st.markdown(f"<div style='font-size:13px; color:#475569; margin-bottom:12px;'>{icon} <b>{title}</b></div>", unsafe_allow_html=True)
                st.success("10k+ 创作者首选")

            with col_auth:
                # --- 右侧：登录/注册交互 ---
                tab_l, tab_r = st.tabs(["安全登录", "快速注册"])
                
                with tab_l:
                    with st.form("login_final_v7", border=False):
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

                with tab_r:
                    with st.form("reg_final_v7", border=False):
                        st.write("\n")
                        # 注册部分：全部回归上下排列，确保流程清晰专业
                        ru = st.text_input("账号", placeholder="请输入手机号或邮箱", label_visibility="collapsed")
                        rp = st.text_input("密码", type="password", placeholder="请设置登录密码", label_visibility="collapsed")
                        rp2 = st.text_input("确认密码", type="password", placeholder="请再次输入密码确认", label_visibility="collapsed")
                        ri = st.text_input("邀请码", value="888888", label_visibility="collapsed")
                        
                        if st.form_submit_button("注 册 账 号", use_container_width=True):
                            if not ru or not rp:
                                st.warning("请填写账号和密码")
                            elif rp != rp2:
                                st.error("两次密码输入不一致")
                            else:
                                success, msg = register_user(ru, rp, ri)
                                if success: st.success("注册成功！请登录")
                                else: st.error(msg)

    # --- 3. 底部剧中声明 ---
    st.write("\n" * 4)
    st.markdown("<p style='text-align: center; color: #CBD5E1; font-size: 10px;'>© 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.</p>", unsafe_allow_html=True)
