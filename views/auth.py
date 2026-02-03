# views/auth.py
import streamlit as st
from database import login_user, register_user

def view_auth():
    # --- 1. [已锁定] 核心 CSS：右侧样式与悬浮动效 ---
    st.markdown("""
        <style>
            [data-testid="stFormInstructions"] { display: none !important; }
            [data-testid="stTextInput"] div[data-baseweb="input"],
            [data-testid="stPasswordInput"] div[data-baseweb="input"] {
                background-color: white !important;
                border: 1px solid #E2E8F0 !important;
                border-radius: 8px !important;
                box-shadow: none !important;
                transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
            }
            [data-testid="stTextInput"] div[data-baseweb="input"]:hover,
            [data-testid="stPasswordInput"] div[data-baseweb="input"]:hover {
                border-color: #1E3A8A !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 6px 16px rgba(30, 58, 138, 0.08) !important;
            }
            [data-testid="stTextInput"] input, [data-testid="stPasswordInput"] input,
            [data-testid="stPasswordInput"] button, [data-baseweb="input"] > div {
                border: none !important; background-color: transparent !important;
                box-shadow: none !important; color: #1E3A8A !important;
                font-size: 14px !important; height: 40px !important;
            }
            button[data-baseweb="tab"] div { font-size: 14px !important; color: #64748B !important; }
            [data-testid="stTextInput"] input::placeholder,
            [data-testid="stPasswordInput"] input::placeholder {
                font-size: 14px !important; color: #94A3B8 !important;
            }
            button[kind="primaryFormSubmit"] [data-testid="stMarkdownContainer"] p {
                visibility: visible !important; display: block !important;
                color: #1E3A8A !important; font-weight: bold !important; font-size: 14px !important;
            }
            header, [data-testid="stHeader"] { visibility: hidden; }
        </style>
    """, unsafe_allow_html=True)

    st.write("\n" * 3)

    # --- 2. 布局 ---
    _, card_container, _ = st.columns([1.2, 3, 1.2])

    with card_container:
        with st.container(border=True):
            col_l, col_r = st.columns([1, 1.4], gap="large")

            # --- 左侧：爆款工厂PRO 极简文案 ---
            with col_l:
                st.write("\n" * 2)
                # 品牌升级
                st.markdown("""
                    <h1 style='color: #1E3A8A; font-size: 32px; margin-bottom: 5px;'>爆款工厂<span style='font-size: 18px; vertical-align: super; margin-left: 4px; color: #3B82F6;'>PRO</span></h1>
                    <p style='color: #94A3B8; font-size: 14px; margin-bottom: 40px;'>AI 驱动的创作决策系统</p>
                """, unsafe_allow_html=True)
                
                # 极简核心工具
                features = [
                    ("💠", "算法嗅探", "锁定蓝海流量"),
                    ("🧠", "神经编辑器", "重构爆款脚本"),
                    ("⚗️", "数据炼金", "驱动高转化率")
                ]
                
                for icon, title, desc in features:
                    st.markdown(f"""
                        <div style='margin-bottom: 30px;'>
                            <b style='color: #334155; font-size: 16px;'>{icon} {title}</b>
                            <p style='color: #64748B; font-size: 13px; margin: 4px 0 0 26px;'>{desc}</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.write("\n")
                # 极简背书
                st.markdown("""
                    <p style='color: #1E3A8A; font-weight: 500; font-size: 13px; border-top: 1px solid #F1F5F9; padding-top: 20px;'>
                        ✓ 已助力 12k+ 创作者出圈
                    </p>
                """, unsafe_allow_html=True)

            # --- 右侧：[锁定] 登录/注册逻辑 ---
            with col_r:
                t1, t2 = st.tabs(["安全登录", "快速注册"])
                
                with t1:
                    with st.form("f_login_pro_final", border=False):
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
                    with st.form("f_reg_pro_final", border=False):
                        ru = st.text_input("RA", placeholder="手机号 / 邮箱", label_visibility="collapsed", key="v_reg_ru")
                        rp = st.text_input("RP1", type="password", placeholder="设置登录密码", label_visibility="collapsed", key="v_reg_rp1")
                        rp2 = st.text_input("RP2", type="password", placeholder="再次确认密码", label_visibility="collapsed", key="v_reg_rp2")
                        ri = st.text_input("RI", value="888888", label_visibility="collapsed", key="v_reg_ri")
                        if st.form_submit_button("注 册 账 号", use_container_width=True):
                            if rp != rp2: st.error("两次密码输入不一致")
                            else:
                                res, msg = register_user(ru, rp, ri)
                                if res: st.success("成功！请登录")

    # --- 3. 底部剧中声明 ---
    st.write("\n" * 4)
    st.markdown("<center style='color:#CBD5E1; font-size:11px; letter-spacing: 2px;'>© 2026 VIRAL FACTORY PRO. ALL RIGHTS RESERVED.</center>", unsafe_allow_html=True)
