# views/auth.py
import streamlit as st
from database import login_user, register_user

def view_auth():
    # --- 1. 工业级强效 CSS 补丁 (彻底重写选择器逻辑) ---
    st.markdown("""
        <style>
            /* 【1. 物理抹除提示语】直接锁定 Streamlit 专门渲染提示文字的 div 容器 */
            [data-testid="stFormInstructions"] {
                display: none !important;
                height: 0 !important;
            }

            /* 【2. 深度拦截】通过属性选择器，隐藏表单中所有非按钮类的 Markdown 文本 */
            /* 这能精准杀掉点击输入框时出现的 Press Enter 提示 */
            [data-testid="stForm"] [data-testid="stMarkdownContainer"] p {
                visibility: hidden !important;
                height: 0 !important;
                margin: 0 !important;
            }

            /* 【3. 强力找回文字】利用按钮的唯一标识符，强制将文字恢复为可见 */
            /* 重点：通过 kind="primaryFormSubmit" 定位，它是提交按钮的灵魂 */
            button[kind="primaryFormSubmit"] [data-testid="stMarkdownContainer"] p {
                visibility: visible !important;
                display: block !important;
                color: white !important;
                font-size: 16px !important;
                font-weight: 800 !important;
                line-height: 1.5 !important;
                text-align: center !important;
            }

            /* 【4. 输入框美化】减淡背景与提示文字 */
            [data-testid="stTextInput"] input {
                background-color: #f9fafb !important;
                color: #1f2937 !important;
                border: 1px solid #f3f4f6 !important;
                font-size: 14px !important;
            }
            [data-testid="stTextInput"] input::placeholder {
                color: #d1d5db !important;
                font-size: 12px !important;
            }

            /* 【5. 界面净化】隐藏 header 和顶部空白 */
            header, [data-testid="stHeader"] { visibility: hidden; }
        </style>
    """, unsafe_allow_html=True)

    st.write("\n" * 2)

    # --- 2. 居中卡片布局 (物理锁定宽度) ---
    _, card_container, _ = st.columns([1.1, 3.2, 1.1])

    with card_container:
        with st.container(border=True):
            # 内部左右分栏
            col_left, col_right = st.columns([1, 1.35], gap="large")

            with col_left:
                # --- 左侧：精致精简文案 ---
                st.write("\n")
                st.markdown("<h2 style='color:#1e3a8a; margin-bottom:0;'>💠 爆款工场</h2>", unsafe_allow_html=True)
                st.markdown("<p style='color:#94a3b8; font-size: 13px;'>创作者的 AI 军师</p>", unsafe_allow_html=True)
                
                # 磁贴式卖点
                features = [
                    ("🎯", "精准选题", "算法锁定流量蓝海"),
                    ("✍️", "爆款文案", "AI 重构高转化脚本"),
                    ("⚡", "效率革命", "创作成本降低 90%")
                ]
                
                for icon, title, desc in features:
                    st.markdown(f"""
                        <div style='margin-bottom: 18px;'>
                            <div style='display: flex; align-items: center; gap: 8px;'>
                                <span style='font-size: 18px;'>{icon}</span>
                                <b style='font-size: 15px; color: #334155;'>{title}</b>
                            </div>
                            <div style='font-size: 11px; color: #64748b; margin-left: 28px;'>{desc}</div>
                        </div>
                    """, unsafe_allow_html=True)
                st.success("10k+ 创作者的首选")

            with col_right:
                # --- 右侧：登录/注册 ---
                tab_l, tab_r = st.tabs(["安全登录", "开启创作"])
                
                with tab_l:
                    with st.form("login_final_fixed"):
                        u = st.text_input("账号", placeholder="手机号 / 邮箱", label_visibility="collapsed")
                        p = st.text_input("密码", type="password", placeholder="请输入密码", label_visibility="collapsed")
                        # 按钮：显式写明文字
                        if st.form_submit_button("立即登录", use_container_width=True):
                            if u and p:
                                success, msg = login_user(u, p)
                                if success:
                                    st.session_state['user_phone'] = u
                                    st.rerun()
                                else: st.error(msg)

                with tab_r:
                    with st.form("reg_final_fixed"):
                        ru = st.text_input("账号", placeholder="手机号/邮箱", label_visibility="collapsed")
                        rp = st.text_input("密码", type="password", placeholder="设置密码", label_visibility="collapsed")
                        rp2 = st.text_input("确认密码", type="password", placeholder="再次确认密码", label_visibility="collapsed")
                        ri = st.text_input("邀请码", value="888888", label_visibility="collapsed")
                        if st.form_submit_button("免费注册", use_container_width=True):
                            if rp != rp2: st.error("两次密码不一致")
                            else:
                                success, msg = register_user(ru, rp, ri)
                                if success: st.success("注册成功！")

    # --- 3. 底部居中免责声明 ---
    st.write("\n" * 4)
    st.markdown("<p style='text-align: center; color: #d1d5db; font-size: 11px;'>© 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.</p>", unsafe_allow_html=True)
