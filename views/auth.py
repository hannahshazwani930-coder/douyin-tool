# views/auth.py
import streamlit as st
from database import login_user, register_user

def view_auth():
    # --- 1. 深度精致化 CSS (仅针对表单提示和基础美化) ---
    st.markdown("""
        <style>
            /* 仅隐藏表单底部的 Press Enter 提示，不影响按钮 */
            [data-testid="stForm"] p { display: none !important; }
            /* 隐藏顶部冗余 */
            header, [data-testid="stHeader"] { visibility: hidden; }
            /* 调优 Tab 字体 */
            button[data-baseweb="tab"] { font-size: 16px !important; font-weight: 600 !important; }
        </style>
    """, unsafe_allow_html=True)

    st.write("\n" * 2)

    # --- 2. 比例控制：[1.1, 3.0, 1.1] 营造呼吸感 ---
    _, card_container, _ = st.columns([1.1, 3.0, 1.1])

    with card_container:
        with st.container(border=True):
            # 左右分栏：左侧精致卖点 (42%)，右侧交互表单 (58%)
            col_left, col_right = st.columns([1, 1.4], gap="large")

            with col_left:
                # --- 左边：紧凑精致的文案排版 ---
                st.write("\n")
                st.markdown("<h2 style='color:#1E3A8A; margin-bottom:5px; font-size: 28px;'>💠 爆款工场</h2>", unsafe_allow_html=True)
                st.markdown("<p style='color:#94A3B8; font-size: 14px; margin-bottom: 25px;'>抖音创作者的 AI 军师</p>", unsafe_allow_html=True)
                
                # 精致点阵图标排版
                features = [
                    ("🎯", "精准选题", "通过算法捕捉流量蓝海"),
                    ("✍️", "爆款文案", "AI 一键重构高转化脚本"),
                    ("⚡", "效率革命", "创作成本降低 90% 以上")
                ]
                
                for icon, title, desc in features:
                    st.markdown(f"""
                        <div style='margin-bottom: 20px;'>
                            <div style='display: flex; align-items: center; gap: 10px;'>
                                <span style='font-size: 20px;'>{icon}</span>
                                <b style='font-size: 16px; color: #334155;'>{title}</b>
                            </div>
                            <div style='font-size: 12px; color: #64748B; margin-left: 32px;'>{desc}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.write("\n")
                st.success("已助力 10k+ 内容出圈")

            with col_right:
                # --- 右边：登录/注册交互 ---
                tab_login, tab_reg = st.tabs(["安全登录", "开启创作"])
                
                with tab_login:
                    # 使用原生 form，并确保按钮逻辑正确
                    with st.form("login_form_final", border=False):
                        st.write("\n")
                        acc = st.text_input("账号", placeholder="手机号 / 邮箱", label_visibility="collapsed")
                        pwd = st.text_input("密码", type="password", placeholder="请输入密码", label_visibility="collapsed")
                        
                        # 核心：确保按钮在表单内
                        submit = st.form_submit_button("登 录", use_container_width=True)
                        if submit:
                            if acc and pwd:
                                success, msg = login_user(acc, pwd)
                                if success:
                                    st.session_state['user_phone'] = acc
                                    st.rerun()
                                else: st.error(msg)
                            else: st.warning("请完善信息")

                with tab_reg:
                    with st.form("reg_form_final", border=False):
                        st.write("\n")
                        r_acc = st.text_input("账号", placeholder="建议使用手机号", label_visibility="collapsed")
                        r_pwd = st.text_input("密码", type="password", placeholder="设置 6-16 位密码", label_visibility="collapsed")
                        r_pwd_2 = st.text_input("确认密码", type="password", placeholder="再次确认密码", label_visibility="collapsed")
                        r_inv = st.text_input("邀请码", value="888888", label_visibility="collapsed")
                        
                        # 按钮逻辑
                        reg_submit = st.form_submit_button("注 册", use_container_width=True)
                        if reg_submit:
                            if r_pwd != r_pwd_2:
                                st.error("两次密码输入不一致")
                            elif not r_acc or not r_pwd:
                                st.warning("信息不完整")
                            else:
                                success, msg = register_user(r_acc, r_pwd, r_inv)
                                if success: st.success("注册成功！请登录")
                                else: st.error(msg)

    # --- 3. 底部剧中声明 ---
    st.write("\n" * 4)
    st.markdown("""
        <div style="text-align: center; color: #94A3B8; font-size: 11px;">
            <p>© 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.</p>
            <p style="opacity: 0.6;">使用即代表同意用户服务协议与隐私政策</p>
        </div>
    """, unsafe_allow_html=True)
