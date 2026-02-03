# views/auth.py
import streamlit as st
from database import login_user, register_user

def view_auth():
    # --- 1. 深度清理与样式锁定 (解决图片中的颜色不一和文字消失) ---
    st.markdown("""
        <style>
            /* 强制抹除所有表单自带的提示语 */
            [data-testid="stFormInstructions"] { display: none !important; }

            /* 统一输入框底色：解决图片中“两个色不统一”的问题 */
            [data-testid="stTextInput"] input {
                background-color: #F8FAFC !important;
                border: 1px solid #E2E8F0 !important;
                color: #334155 !important;
                border-radius: 6px !important;
            }

            /* 修复 Tab 标签重叠乱码 */
            button[data-baseweb="tab"] {
                padding: 10px 15px !important;
            }

            /* 按钮文字强制找回：使用最强路径锁定 */
            button[kind="primaryFormSubmit"] div[data-testid="stMarkdownContainer"] p {
                visibility: visible !important;
                display: block !important;
                color: #1E3A8A !important;
                font-weight: bold !important;
                font-size: 16px !important;
            }

            /* 隐藏顶部冗余 */
            header, [data-testid="stHeader"] { visibility: hidden; }
        </style>
    """, unsafe_allow_html=True)

    st.write("\n" * 2)

    # --- 2. 居中弹性卡片布局 (锁定比例防止重叠) ---
    _, card_container, _ = st.columns([1.1, 3.2, 1.1])

    with card_container:
        with st.container(border=True):
            col_brand, col_auth = st.columns([1, 1.5], gap="large")

            with col_brand:
                # --- 左侧：图标+精简文案 ---
                st.write("\n")
                st.markdown("<h3 style='color:#1E3A8A; margin-bottom:5px;'>💠 爆款工场</h3>", unsafe_allow_html=True)
                st.markdown("<p style='color:#94A3B8; font-size: 12px; margin-bottom: 25px;'>创作者的 AI 军师</p>", unsafe_allow_html=True)
                
                # 功能磁贴
                features = [("🎯", "精准选题"), ("✍️", "爆款文案"), ("⚡", "效率革命")]
                for icon, title in features:
                    st.markdown(f"<div style='font-size:13px; color:#475569; margin-bottom:12px;'>{icon} <b>{title}</b></div>", unsafe_allow_html=True)
                
                st.success("已助力 10k+ 出圈")

            with col_auth:
                # --- 右侧：登录/注册交互 ---
                tab_l, tab_r = st.tabs(["安全登录", "快速注册"])
                
                with tab_l:
                    # 使用唯一的 form key 防止冲突
                    with st.form("login_stable_v1", border=False):
                        st.write("\n")
                        acc = st.text_input("账号", placeholder="手机号 / 邮箱", label_visibility="collapsed", key="login_acc")
                        pwd = st.text_input("密码", type="password", placeholder="请输入密码", label_visibility="collapsed", key="login_pwd")
                        
                        if st.form_submit_button("立即登录", use_container_width=True):
                            if acc and pwd:
                                success, msg = login_user(acc, pwd)
                                if success:
                                    st.session_state['user_phone'] = acc
                                    st.rerun()
                                else:
                                    st.error(msg)

                with tab_r:
                    with st.form("reg_stable_v1", border=False):
                        st.write("\n")
                        ru = st.text_input("手机号/邮箱", placeholder="手机号/邮箱", label_visibility="collapsed", key="reg_acc")
                        rp = st.text_input("设置密码", type="password", placeholder="设置登录密码", label_visibility="collapsed", key="reg_pwd1")
                        rp2 = st.text_input("确认密码", type="password", placeholder="确认密码", label_visibility="collapsed", key="reg_pwd2")
                        ri = st.text_input("邀请码", value="888888", label_visibility="collapsed", key="reg_inv")
                        
                        if st.form_submit_button("快速注册", use_container_width=True):
                            if rp != rp2:
                                st.error("密码不一致")
                            else:
                                success, msg = register_user(ru, rp, ri)
                                if success:
                                    st.success("注册成功！")

    # --- 3. 底部声明 (彻底修复代码外露问题) ---
    st.write("\n" * 4)
    st.markdown("""
        <div style="text-align: center; color: #94A3B8; font-size: 11px; width: 100%;">
            © 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.
        </div>
    """, unsafe_allow_html=True)
