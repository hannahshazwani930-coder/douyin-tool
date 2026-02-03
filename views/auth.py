# views/auth.py
import streamlit as st
from utils import load_isolated_css
from database import login_user, register_user

def view_auth():
    # 注入样式
    load_isolated_css("auth")
    
    st.write("\n" * 4)

    # 核心：通过比例锁定，让卡片宽度保持在约 600px-700px 之间
    _, main_card, _ = st.columns([1.2, 2.5, 1.2])

    with main_card:
        # 使用原生边框容器模拟卡片
        with st.container(border=True):
            # 内部左右分栏调整为对等或更紧凑的比例
            col_left, col_right = st.columns([1, 1.2], gap="medium")

            with col_left:
                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                st.subheader("💠 爆款工场")
                st.write("---")
                st.caption("AI 驱动创作中枢")
                st.markdown("""
                    <div style='font-size: 13px; color: #64748b; line-height: 1.8;'>
                    • 专业定制方案<br>
                    • 全模块化安全<br>
                    • 2026 旗舰版
                    </div>
                """, unsafe_allow_html=True)

            with col_right:
                # 镶嵌在右侧的简洁表单
                tab_l, tab_r = st.tabs(["登录", "注册"])
                
                with tab_l:
                    with st.form("l_form_compact"):
                        u = st.text_input("账号", placeholder="手机号/邮箱", label_visibility="collapsed")
                        p = st.text_input("密码", type="password", placeholder="请输入密码", label_visibility="collapsed")
                        if st.form_submit_button("立即登录", use_container_width=True):
                            if u and p:
                                success, msg = login_user(u, p)
                                if success:
                                    st.session_state['user_phone'] = u
                                    st.rerun()
                                else: st.error(msg)
                
                with tab_r:
                    with st.form("r_form_compact"):
                        ru = st.text_input("账号", placeholder="新账号")
                        rp = st.text_input("密码", type="password", placeholder="设置密码")
                        ri = st.text_input("邀请码", value="888888")
                        if st.form_submit_button("注 册", use_container_width=True):
                            success, msg = register_user(ru, rp, ri)
                            if success: st.success("成功！请登录")
                            else: st.error(msg)

    # 居中显示底部声明
    st.write("\n")
    st.markdown("<p style='text-align: center; color: rgba(255,255,255,0.3); font-size: 11px;'>© 2026 DOUYIN MASTER PRO</p>", unsafe_allow_html=True)
