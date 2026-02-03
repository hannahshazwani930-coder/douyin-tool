# views/auth.py
import streamlit as st
from database import login_user, register_user

def view_auth():
    # --- 1. 核心样式补丁：彻底清理干扰，锁定精致 UI ---
    st.markdown("""
        <style>
            /* 【彻底抹除提示语】直接锁定 Streamlit 渲染提示文字的官方容器 ID */
            [data-testid="stFormInstructions"] {
                display: none !important;
            }

            /* 【物理级拦截】隐藏表单中点击输入框时出现的动态提示 */
            .stForm [data-testid="stMarkdownContainer"] p:not(:empty) {
                visibility: hidden !important;
                height: 0 !important;
                margin: 0 !important;
            }

            /* 【强制找回文字】通过提交按钮的专属属性锁定，确保文字可见 */
            button[kind="primaryFormSubmit"] [data-testid="stMarkdownContainer"] p {
                visibility: visible !important;
                display: block !important;
                color: white !important;
                font-size: 16px !important;
                font-weight: 700 !important;
                margin: 0 !important;
            }

            /* 【输入框精致化】减淡底色、缩小提示、颜色柔和 */
            [data-testid="stTextInput"] input {
                background-color: #F8FAFC !important;
                color: #334155 !important;
                border: 1px solid #F1F5F9 !important;
                font-size: 14px !important;
                border-radius: 8px !important;
            }
            [data-testid="stTextInput"] input::placeholder {
                color: #CBD5E1 !important;
                font-size: 12px !important;
            }

            /* 【全局净化】 */
            header, [data-testid="stHeader"] { visibility: hidden; }
            button[data-baseweb="tab"] { color: #94A3B8 !important; }
            button[aria-selected="true"] { color: #1E3A8A !important; border-bottom: 2px solid #1E3A8A !important; }
        </style>
    """, unsafe_allow_html=True)

    st.write("\n" * 2)

    # --- 2. 居中弹性卡片排版 ---
    _, card_container, _ = st.columns([1, 2.8, 1])

    with card_container:
        # 使用原生带边框容器，确保 100% 兼容性
        with st.container(border=True):
            # 内部左右分栏：左侧品牌 (42%)，右侧交互 (58%)
            col_brand, col_auth = st.columns([1, 1.4], gap="large")

            with col_brand:
                # --- 左侧：精致精简文案 ---
                st.write("\n")
                st.markdown("<h2 style='color:#1E3A8A; margin-bottom:0;'>💠 爆款工场</h2>", unsafe_allow_html=True)
                st.markdown("<p style='color:#94A3B8; font-size: 13px;'>创作者的 AI 军师</p>", unsafe_allow_html=True)
                st.write("---")
                
                features = [
                    ("🎯", "精准选题", "锁定流量蓝海"),
                    ("✍️", "爆款文案", "一键重构脚本"),
                    ("⚡", "效率革命", "创作提速 10 倍")
                ]
                for icon, title, desc in features:
                    st.markdown(f"""
                        <div style='margin-bottom: 18px;'>
                            <b style='font-size: 15px; color:#334155;'>{icon} {title}</b><br>
                            <span style='font-size: 12px; color:#64748B; margin-left: 26px;'>{desc}</span>
                        </div>
                    """, unsafe_allow_html=True)
                st.success("已助力 10k+ 出圈")

            with col_auth:
                # --- 右侧：登录/注册交互 ---
                tab_l, tab_r = st.tabs(["安全登录", "快速注册"])
                
                with tab_l:
                    with st.form("login_final", border=False):
                        st.write("\n")
                        u = st.text_input("账号", placeholder="手机号 / 邮箱", label_visibility="collapsed")
                        p = st.text_input("密码", type="password", placeholder="请输入密码", label_visibility="collapsed")
                        # 按钮：显式文字
                        if st.form_submit_button("登 录", use_container_width=True):
                            if u and p:
                                success, msg = login_user(u, p)
                                if success:
                                    st.session_state['user_phone'] = u
                                    st.rerun()
                                else: st.error(msg)
                            else: st.warning("请完善信息")

                with tab_r:
                    with st.form("reg_final", border=False):
                        st.write("\n")
                        ru = st.text_input("账号", placeholder="手机号/邮箱", label_visibility="collapsed")
                        rp = st.text_input("密码", type="password", placeholder="设置 6-16 位密码", label_visibility="collapsed")
                        rp2 = st.text_input("确认", type="password", placeholder="请再次输入密码", label_visibility="collapsed")
                        ri = st.text_input("邀请码", value="888888", label_visibility="collapsed")
                        
                        if st.form_submit_button("注 册", use_container_width=True):
                            if rp != rp2: st.error("两次密码不一致")
                            elif not ru or not rp: st.warning("请填写完整")
                            else:
                                success, msg = register_user(ru, rp, ri)
                                if success: st.success("成功！请切换至登录")
                                else: st.error(msg)

    # --- 3. 底部剧中声明 ---
    st.write("\n" * 4)
    st.markdown("<p style='text-align: center; color: #CBD5E1; font-size: 11px;'>© 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.</p>", unsafe_allow_html=True)
