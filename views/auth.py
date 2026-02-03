# views/auth.py
import streamlit as st
from database import login_user, register_user

def view_auth():
    # --- 1. 顶级 CSS 修复：找回消失的按钮文字 ---
    st.markdown("""
        <style>
            /* 隐藏表单底部的提示文字 (Press Enter...) */
            [data-testid="stForm"] div[data-testid="stVerticalBlock"] > div:last-child p {
                visibility: hidden !important;
                height: 0 !important;
                margin: 0 !important;
            }
            
            /* 强制找回按钮文字：确保登录/注册字样显示 */
            .stButton button p {
                visibility: visible !important;
                display: block !important;
                color: white !important;
                font-weight: 700 !important;
                font-size: 16px !important;
            }
            
            /* 隐藏顶部工具栏 */
            header, [data-testid="stHeader"] { visibility: hidden; }
            
            /* 调整 Tab 标签选中的颜色，更有高级感 */
            button[data-baseweb="tab"] { color: #94A3B8 !important; }
            button[aria-selected="true"] { color: #1E3A8A !important; border-bottom-color: #1E3A8A !important; }
        </style>
    """, unsafe_allow_html=True)

    st.write("\n" * 2)

    # --- 2. 比例控制：[1.1, 3.2, 1.1] 营造精致卡片感 ---
    _, card_container, _ = st.columns([1.1, 3.2, 1.1])

    with card_container:
        with st.container(border=True):
            # 左右分栏：左侧精致卖点 (45%)，右侧交互表单 (55%)
            col_left, col_right = st.columns([1.8, 2.2], gap="large")

            with col_left:
                # --- 左边：紧凑精致的文案排版 ---
                st.write("\n")
                st.markdown("<h2 style='color:#1E3A8A; margin-bottom:5px; font-size: 28px;'>💠 爆款工场</h2>", unsafe_allow_html=True)
                st.markdown("<p style='color:#94A3B8; font-size: 14px; margin-bottom: 25px;'>抖音创作者的 AI 军师</p>", unsafe_allow_html=True)
                
                # 精致图标列表
                features = [
                    ("🎯", "精准选题", "算法锁定流量蓝海"),
                    ("✍️", "爆款文案", "AI 重构高转化脚本"),
                    ("⚡", "效率革命", "创作成本降低 90%")
                ]
                
                for icon, title, desc in features:
                    st.markdown(f"""
                        <div style='margin-bottom: 22px;'>
                            <div style='display: flex; align-items: center; gap: 12px;'>
                                <span style='font-size: 20px;'>{icon}</span>
                                <b style='font-size: 16px; color: #334155;'>{title}</b>
                            </div>
                            <div style='font-size: 12px; color: #64748B; margin-left: 32px;'>{desc}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.write("\n")
                st.success("已助力 10k+ 创作者出圈")

            with col_right:
                # --- 右边：登录/注册交互 ---
                tab_login, tab_reg = st.tabs(["安全登录", "开启创作"])
                
                with tab_login:
                    with st.form("login_final_pro", border=False):
                        st.write("\n")
                        acc = st.text_input("账号", placeholder="手机号 / 邮箱", label_visibility="collapsed")
                        pwd = st.text_input("密码", type="password", placeholder="请输入密码", label_visibility="collapsed")
                        
                        # 指定显示文字为“立即登录”
                        if st.form_submit_button("立 即 登 录", use_container_width=True):
                            if acc and pwd:
                                success, msg = login_user(acc, pwd)
                                if success:
                                    st.session_state['user_phone'] = acc
                                    st.rerun()
                                else: st.error(msg)
                            else: st.warning("请完善登录信息")

                with tab_reg:
                    with st.form("reg_final_pro", border=False):
                        st.write("\n")
                        r_acc = st.text_input("账号", placeholder="手机号/邮箱", label_visibility="collapsed")
                        r_pwd = st.text_input("密码", type="password", placeholder="设置登录密码", label_visibility="collapsed")
                        r_pwd_2 = st.text_input("确认密码", type="password", placeholder="再次输入密码", label_visibility="collapsed")
                        r_inv = st.text_input("邀请码", value="888888", label_visibility="collapsed")
                        
                        # 指定显示文字为“免 费 注 册”
                        if st.form_submit_button("免 费 注 册", use_container_width=True):
                            if r_pwd != r_pwd_2:
                                st.error("两次密码输入不一致")
                            elif not r_acc or not r_pwd:
                                st.warning("请填写完整信息")
                            else:
                                success, msg = register_user(r_acc, r_pwd, r_inv)
                                if success: st.success("注册成功！请登录")
                                else: st.error(msg)

    # --- 3. 底部剧中声明 ---
    st.write("\n" * 4)
    st.markdown("""
        <div style="text-align: center; color: #94A3B8; font-size: 11px; font-family: sans-serif;">
            © 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.<br>
            <span style="opacity: 0.6;">使用即代表同意用户服务协议与隐私政策</span>
        </div>
    """, unsafe_allow_html=True)
