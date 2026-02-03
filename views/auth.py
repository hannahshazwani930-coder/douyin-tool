# views/auth.py
import streamlit as st
from database import login_user, register_user

def view_auth():
    # 1. 页面大标题（原生布局）
    st.write("\n") # 顶部留空
    st.markdown("<h1 style='text-align: center;'>💠 爆款工场 Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>AI 驱动的一站式短视频创作辅助系统</p>", unsafe_allow_html=True)
    st.write("\n")

    # 2. 控制卡片宽度：[1份侧边, 2.5份卡片, 1份侧边] 比例让卡片适中
    _, card_col, _ = st.columns([1, 2.5, 1])

    with card_col:
        # 3. 镶嵌效果：使用原生带边框容器，这就是你的“卡片”
        with st.container(border=True):
            # 4. 左右排版：左侧品牌介绍 (2份)，右侧交互表单 (3份)
            left_side, right_side = st.columns([2, 3], gap="large")

            with left_side:
                st.write("\n")
                st.info("**专业版 v2026**")
                st.write("---")
                st.markdown("""
                🚀 **核心功能**
                - AI 文案改写
                - 智能海报生成
                - 数据趋势分析
                
                🔒 **安全保障**
                - 模块化独立存储
                """)
                st.caption("让创作更高效、更专业")

            with right_side:
                # 5. 表单切换：原生 Tabs，逻辑极其稳固
                tab_l, tab_r = st.tabs(["🔒 安全登录", "📝 快速注册"])
                
                with tab_l:
                    # 使用 st.form 确保回车键可以触发登录
                    with st.form("login_native_final"):
                        u = st.text_input("账号", placeholder="手机号 / 邮箱")
                        p = st.text_input("密码", type="password", placeholder="请输入密码")
                        submit = st.form_submit_button("立即登录", use_container_width=True)
                        
                        if submit:
                            if u and p:
                                success, msg = login_user(u, p)
                                if success:
                                    st.session_state['user_phone'] = u
                                    st.rerun()
                                else:
                                    st.error(msg)
                            else:
                                st.warning("请完善登录信息")

                with tab_r:
                    with st.form("reg_native_final"):
                        ru = st.text_input("设置账号", placeholder="手机号或邮箱")
                        rp = st.text_input("设置密码", type="password")
                        ri = st.text_input("邀请码", value="888888")
                        r_submit = st.form_submit_button("创建账号", use_container_width=True)
                        
                        if r_submit:
                            success, msg = register_user(ru, rp, ri)
                            if success:
                                st.success("注册成功！请切换到登录页")
                            else:
                                st.error(msg)

    # 6. 底部版权声明（纯净版）
    st.write("\n" * 4)
    st.divider()
    st.caption("<center>© 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.</center>", unsafe_allow_html=True)
