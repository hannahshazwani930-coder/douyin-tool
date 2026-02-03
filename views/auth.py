# views/auth.py
import streamlit as st
from database import login_user, register_user

def view_auth():
    # --- 1. [物理锁定] 核心 CSS ---
    st.markdown("""
<style>
    [data-testid="stFormInstructions"] { display: none !important; }
    button[data-baseweb="tab"] div { font-size: 14px !important; color: #475569 !important; }

    /* 2. 背景纯白锁定，消除重叠 */
    [data-testid="stTextInput"] div[data-baseweb="input"],
    [data-testid="stPasswordInput"] div[data-baseweb="input"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        box-shadow: none !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    }

    /* 3. 悬浮动效锁定 */
    [data-testid="stTextInput"] div[data-baseweb="input"]:hover,
    [data-testid="stPasswordInput"] div[data-baseweb="input"]:hover {
        border-color: #1E3A8A !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(30, 58, 138, 0.08) !important;
    }

    /* 4. 消除边框重叠锁定 */
    [data-testid="stTextInput"] input, 
    [data-testid="stPasswordInput"] input,
    [data-testid="stPasswordInput"] button,
    [data-baseweb="input"] > div {
        background-color: transparent !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        color: #1E3A8A !important;
        font-size: 14px !important;
        height: 40px !important;
    }

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
            col_l, col_r = st.columns([1.1, 1.4], gap="large")

            # --- 左侧：爆款工厂PRO [原子化防乱码版] ---
            with col_l:
                # 采用标准 HTML，移除所有特殊 Unicode 符号
                brand_content = """
                <div style="padding-left: 35px; padding-top: 32px; font-family: sans-serif;">
                    <div style="margin-bottom: 22px;">
                        <h1 style="color: #1E3A8A; font-size: 28px; margin: 0; font-weight: 800; line-height: 1.2;">
                            爆款工厂<span style="color: #3B82F6; font-size: 16px; font-weight: 400; margin-left: 5px;">PRO</span>
                        </h1>
                        <div style="width: 24px; height: 3px; background: #1E3A8A; margin: 12px 0;"></div>
                        <p style="color: #64748B; font-size: 13px; margin: 0; line-height: 1.5;">AI 驱动的全链路创作决策系统</p>
                    </div>
                    
                    <div style="margin-bottom: 15px;">
                        <b style="color: #334155; font-size: 14px; display: block; margin-bottom: 2px;">算法嗅探</b>
                        <span style="color: #94A3B8; font-size: 12px;">毫秒级监控全网流量趋势</span>
                    </div>
                    
                    <div style="margin-bottom: 15px;">
                        <b style="color: #334155; font-size: 14px; display: block; margin-bottom: 2px;">神经编辑器</b>
                        <span style="color: #94A3B8; font-size: 12px;">重构爆款视频的底层逻辑</span>
                    </div>

                    <div style="margin-top: 28px; padding-top: 15px; border-top: 1px solid #F1F5F9;">
                        <span style="color: #10B981; font-weight: 700; font-size: 13px; margin-right: 5px;">LIVE</span>
                        <span style="color: #94A3B8; font-size: 12px;">12.8k+ 创作者的共同选择</span>
                    </div>
                </div>
                """
                st.markdown(brand_content, unsafe_allow_html=True)

            # --- 右侧：[锁定不动] ---
            with col_r:
                t1, t2 = st.tabs(["安全登录", "快速注册"])
                with t1:
                    with st.form("f_login_v16", border=False):
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
                    with st.form("f_reg_v16", border=False):
                        ru = st.text_input("RA", placeholder="手机号 / 邮箱", label_visibility="collapsed", key="v_reg_ru")
                        rp = st.text_input("RP1", type="password", placeholder="设置密码", label_visibility="collapsed", key="v_reg_rp1")
                        rp2 = st.text_input("RP2", type="password", placeholder="确认密码", label_visibility="collapsed", key="v_reg_rp2")
                        ri = st.text_input("RI", value="888888", label_visibility="collapsed", key="v_reg_ri")
                        if st.form_submit_button("注 册 账 号", use_container_width=True):
                            if rp != rp2: st.error("密码不一致")
                            else:
                                res, msg = register_user(ru, rp, ri)
                                if res: st.success("成功！请登录")

    st.write("\n" * 4)
    st.markdown("<center style='color:#CBD5E1; font-size:11px; letter-spacing: 2px;'>© 2026 VIRAL FACTORY PRO. ALL RIGHTS RESERVED.</center>", unsafe_allow_html=True)
