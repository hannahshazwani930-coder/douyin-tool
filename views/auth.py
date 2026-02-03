# views/auth.py
import streamlit as st
from utils import load_isolated_css
from database import login_user, register_user

def view_auth():
    # 注入纯净版 CSS (只管颜色，不管排版)
    load_isolated_css("auth")
    
    # 顶部空行，实现视觉垂直居中
    st.write("\n" * 4)

    # 核心容器：使用原生列建立一个 80% 宽度的居中卡片区域
    _, main_card, _ = st.columns([1, 8, 1])

    with main_card:
        # 模拟卡片背景：通过容器美化
        with st.container(border=True):
            # 内部左右分栏：左侧品牌 (40%)，右侧表单 (60%)
            col_left, col_right = st.columns([2, 3], gap="large")

            with col_left:
                st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
                st.markdown("### 💠 爆款工场 Pro")
                st.write("---")
                st.info("AI 驱动的一站式创作辅助系统")
                st.markdown("""
                    - **高效**：全模块化设计
                    - **安全**：独立数据存储
                    - **专业**：抖音深度定制
                """)
                st.caption("Version 2026.1")

            with col_right:
                # 镶嵌在卡片右侧的登录/注册
                tab_l, tab_r = st.tabs(["🔑 安全登录", "📝 快速注册"])
                
                with tab_l:
                    with st.form("l_form_card"):
                        u = st.text_input("账号", placeholder="手机号 / 邮箱")
                        p = st.text_input("密码", type="password")
                        if st.form_submit_button("立即登录", use_container_width=True):
                            if u and p:
                                success, msg = login_user(u, p)
                                if success:
                                    st.session_state['user_phone'] = u
                                    st.rerun()
                                else: st.error(msg)
                            else: st.warning("请填写完整")

                with tab_r:
                    with st.form("r_form_card"):
                        ru = st.text_input("设置账号")
                        rp = st.text_input("设置密码", type="password")
                        ri = st.text_input("邀请码", value="888888")
                        if st.form_submit_button("注 册", use_container_width=True):
                            success, msg = register_user(ru, rp, ri)
                            if success: st.success("注册成功！请登录")
                            else: st.error(msg)

    # 底部声明
    st.write("\n" * 2)
    st.caption("<center>© 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.</center>", unsafe_allow_html=True)
