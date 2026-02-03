# views/auth.py
import streamlit as st
from database import login_user, register_user

def view_auth():
    # --- 1. [物理锁定] 核心 CSS：右侧样式、悬浮动效、14px 对齐 ---
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

    # --- 2. 布局布局：锁定比例 ---
    _, card_container, _ = st.columns([1.2, 3, 1.2])

    with card_container:
        with st.container(border=True):
            col_l, col_r = st.columns([1.1, 1.4], gap="large")

            # --- 左侧：爆款工厂PRO [向右位移美化版] ---
            with col_l:
                # 使用 div 包装并增加 padding-left 实现整体右移，避免靠边
                st.markdown("""
                    <div style='padding-left: 35px; padding-top: 15px;'>
                        <div style='margin-bottom: 25px;'>
                            <h1 style='color: #1E3A8A; font-size: 30px; margin: 0; font-weight: 800; letter-spacing: -0.5px;'>
                                爆款工厂<span style='color: #3B82F6; font-size: 18px; font-weight: 400; margin-left: 5px;'>PRO</span>
                            </h1>
                            <div style='width: 30px; height: 3px; background: #1E3A8A; margin: 12px 0;'></div>
                            <p style='color: #64748B; font-size: 14px; line-height: 1.4; letter-spacing: 0.5px;'>
                                深度神经网络驱动的<br>短视频全链路创作指挥系统
                            </p>
                        </div>
                        
                        <div style='margin-bottom: 16px; display: flex; align-items: flex-start; gap: 10px;'>
                            <div style='font-size: 18px; margin-top: 2px;'>💠</div>
                            <div>
                                <b style='color: #334155; font-size: 15px; display: block;'>算法嗅探</b>
                                <span style='color: #94A3B8; font-size: 12px; line-height: 1.2;'>全网流量趋势毫秒级监控</span>
                            </div>
                        </div>
                        <div style='margin-bottom: 16px; display: flex; align-items: flex-start; gap: 10px;'>
                            <div style='font-size: 18px; margin-top: 2px;'>🧠</div>
                            <div>
                                <b style='color: #334155; font-size: 15px; display: block;'>神经编辑器</b>
                                <span style='color: #94A3B8; font-size: 12px; line-height: 1.2;'>基于爆款底层逻辑的剧本重构</span>
                            </div>
                        </div>
                        <div style='margin-bottom: 16px; display: flex; align-items: flex-start; gap: 10px;'>
                            <div style='font-size: 18px; margin-top: 2px;'>⚗️</div>
                            <div>
                                <b style='color: #334155; font-size: 15px; display: block;'>数据炼金</b>
                                <span style='color: #94A3B8; font-size: 12px; line-height: 1.2;'>精准定位每一秒的转化拐点</span>
                            </div>
                        </div>
                        
                        <div style='margin-top: 25px; padding-top: 15px; border-top: 1px solid #F1F5F9;'>
                            <div style='display: flex; align-items: center; gap: 8px;'>
                                <div style='width: 8px; height: 8px; background: #10B981; border-radius: 50%;'></div>
                                <span style='color: #334155; font-weight: 600; font-size: 13px;'>12,840+</span>
                                <span style='color: #94A3B8; font-size: 12px;'>位创作者的共同选择</span>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            # --- 右侧：[绝对锁定] 登录/注册交互 ---
            with col_r:
                t1, t2 = st.tabs(["安全登录", "快速注册"])
                
                with t1:
                    with st.form("f_login_pro_final_move", border=False):
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
                    with st.form("f_reg_pro_final_move", border=False):
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
