# views/auth.py
import streamlit as st
from database import login_user, register_user

def view_auth():
    # --- 1. 工业级强效 CSS 补丁 (彻底重写，确保文字 100% 显现) ---
    st.markdown("""
        <style>
            /* 【核心物理屏蔽】锁定 Streamlit 专门存放提示语的底层容器，彻底杀掉 Press Enter */
            [data-testid="stFormInstructions"] {
                display: none !important;
            }

            /* 【精准拦截】防止点击输入框时出现的任何动态提示，但不触碰按钮 */
            .stForm [data-testid="stMarkdownContainer"] p:not(:only-child) {
                display: none !important;
            }

            /* 【强制找回文字】重点修复：锁定按钮内部的特定路径，强制文字显现 */
            /* 利用按钮的 kind 属性做唯一标识 */
            button[kind="primaryFormSubmit"] div[data-testid="stMarkdownContainer"] p {
                display: block !important;
                visibility: visible !important;
                color: white !important;
                font-size: 16px !important;
                font-weight: bold !important;
                opacity: 1 !important;
            }

            /* 【文本框精致美化】按照你的要求：背景减淡、提示文字缩小减淡 */
            [data-testid="stTextInput"] input {
                background-color: #F8FAFC !important; /* 极淡底色 */
                color: #334155 !important;
                border: 1px solid #F1F5F9 !important;
                font-size: 14px !important;
                border-radius: 8px !important;
            }
            [data-testid="stTextInput"] input::placeholder {
                color: #CBD5E1 !important; /* 提示文字减淡 */
                font-size: 12px !important; /* 提示文字缩小 */
            }

            /* 【视觉净化】隐藏 header */
            header, [data-testid="stHeader"] { visibility: hidden; }
            button[data-baseweb="tab"] { color: #94A3B8 !important; }
            button[aria-selected="true"] { color: #1E3A8A !important; border-bottom: 2px solid #1E3A8A !important; }
        </style>
    """, unsafe_allow_html=True)

    st.write("\n" * 2)

    # --- 2. 居中弹性卡片排版 ---
    _, card_container, _ = st.columns([1, 3.2, 1])

    with card_container:
        with st.container(border=True):
            col_brand, col_auth = st.columns([1, 1.4], gap="large")

            with col_brand:
                # --- 左侧：图标+精简有力文案 ---
                st.write("\n")
                st.markdown("<h2 style='color:#1E3A8A; margin-bottom:5px;'>💠 爆款工场</h2>", unsafe_allow_html=True)
                st.markdown("<p style='color:#94A3B8; font-size: 14px; margin-bottom: 25px;'>创作者的 AI 军师</p>", unsafe_allow_html=True)
                
                features = [
                    ("🎯", "精准选题", "算法锁定流量蓝海"),
                    ("✍️", "爆款文案", "AI 一键重构脚本"),
                    ("⚡", "效率革命", "创作提速 10 倍")
                ]
                for icon, title, desc in features:
                    st.markdown(f"""
                        <div style='margin-bottom: 18px;'>
                            <b style='font-size: 15px; color:#334155;'>{icon} {title}</b><br>
                            <span style='font-size: 12px; color:#64748B; margin-left: 28px;'>{desc}</span>
                        </div>
                    """, unsafe_allow_html=True)
                st.success("已助力 10k+ 出圈")

            with col_auth:
                # --- 右侧：登录/注册交互 ---
                tab_l, tab_r = st.tabs(["安全登录", "快速注册"])
                
                with tab_l:
                    with st.form("login_form_final", border=False):
                        st.write("\n")
                        acc = st.text_input("账号", placeholder="手机号 / 邮箱", label_visibility="collapsed")
                        pwd = st.text_input("密码", type="password", placeholder="请输入密码", label_visibility="collapsed")
                        # 核心：手动指定按钮显示的文字
                        if st.form_submit_button("立 即 登 录", use_container_width=True):
                            if acc and pwd:
                                success, msg = login_user(acc, pwd)
                                if success:
                                    st.session_state['user_phone'] = acc
                                    st.rerun()
                                else: st.error(msg)
                            else: st.warning("请完善信息")

                with tab_r:
                    with st.form("reg_form_final", border=False):
                        st.write("\n")
                        ru = st.text_input("账号", placeholder="手机号/邮箱", label_visibility="collapsed")
                        rp = st.text_input("密码", type="password", placeholder="设置 6-16 位密码", label_visibility="collapsed")
                        rp2 = st.text_input("确认", type="password", placeholder="再次输入密码", label_visibility="collapsed")
                        ri = st.text_input("邀请码", value="888888", label_visibility="collapsed")
                        # 核心：手动指定按钮显示的文字
                        if st.form_submit_button("注 册 账 号", use_container_width=True):
                            if rp != rp2: st.error("两次密码输入不一致")
                            elif not ru or not rp: st.warning("请填写完整")
                            else:
                                success, msg = register_user(ru, rp, ri)
                                if success: st.success("成功！请登录")
                                else: st.error(msg)

    # --- 3. 底部剧中声明 ---
    st.write("\n" * 4)
    st.markdown("<p style='text-align: center; color: #CBD5E1; font-size: 11px;'>© 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.</p>", unsafe_allow_html=True)
