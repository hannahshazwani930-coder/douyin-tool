# views/auth.py
import streamlit as st
from database import login_user, register_user

def view_auth():
    # 1. 页面大背景与标题 (使用原生 markdown，简洁大气)
    st.markdown("<h1 style='text-align: center;'>💠 爆款工场 Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>AI 驱动的一站式短视频创作辅助系统</p>", unsafe_allow_html=True)
    
    # 顶部留空
    st.write("\n")

    # 2. 物理级对齐：通过 columns [1, 2, 1] 锁定中间卡片的宽度
    # 这里的 2 就是卡片的宽度，数值越小卡片越窄
    empty_l, card_area, empty_r = st.columns([1, 2, 1])

    with card_area:
        # 3. 核心：使用原生带边框的容器，这就是“卡片”本身
        with st.container(border=True):
            # 4. 内部左右排版
            col_brand, col_form = st.columns([1, 1.2], gap="medium")

            with col_brand:
                # 左侧品牌视觉
                st.write("\n")
                st.info("**专业版 2026**")
                st.write("---")
                st.write("🚀 **全模块化设计**")
                st.write("🔒 **独立安全存储**")
                st.write("📈 **抖音深度算法**")
                st.caption("让创作更有生命力")

            with col_form:
                # 右侧登录/注册逻辑切换
                tab_login, tab_reg = st.tabs(["安全登录", "快速注册"])
                
                with tab_login:
                    # 使用原生 form 确保回车自动提交
                    with st.form("login_native"):
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
                                st.warning("请填写完整")

                with tab_reg:
                    with st.form("reg_native"):
                        ru = st.text_input("设置账号", placeholder="建议用手机号")
                        rp = st.text_input("设置密码", type="password")
                        ri = st.text_input("邀请码", value="888888")
                        r_submit = st.form_submit_button("注 册", use_container_width=True)
                        
                        if r_submit:
                            success, msg = register_user(ru, rp, ri)
                            if success:
                                st.success("注册成功！请切换到登录页")
                            else:
                                st.error(msg)

    # 5. 底部版权声明
    st.write("\n" * 3)
    st.divider()
    st.caption("<center>© 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.</center>", unsafe_allow_html=True)
