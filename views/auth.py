# views/auth.py
import streamlit as st
from utils import load_isolated_css
from database import login_user, register_user

def view_auth():
    # 加载样式
    load_isolated_css("auth")
    
    # 顶部空行，实现垂直居中
    st.markdown("<div style='height: 120px;'></div>", unsafe_allow_html=True)

    # 建立主排版容器：[侧边占位, 中心内容(10份), 侧边占位]
    _, main_col, _ = st.columns([1, 10, 1])

    with main_col:
        # 在中心区域建立左右分栏：[左侧品牌(4.5), 中间空隙(1), 右侧表单(4.5)]
        left_p, gap_p, right_p = st.columns([4.5, 1, 4.5])

        with left_p:
            # 品牌视觉区：100% 稳固，绝不偏移
            st.markdown("""
                <div class="brand-box-pro">
                    <div style="font-size: 50px; margin-bottom: 20px;">💠</div>
                    <h1 style="color:white; font-size: 36px; font-weight: 800; margin:0;">抖音爆款工场</h1>
                    <p style="color:rgba(255,255,255,0.7); font-size: 16px; margin-top:15px; line-height:1.6;">
                        专业短视频创作辅助系统<br>AI 驱动 · 模块化安全版
                    </p>
                    <div style="margin-top: 60px; font-size: 10px; letter-spacing: 4px; opacity: 0.4;">EST. 2026 PRO EDITION</div>
                </div>
            """, unsafe_allow_html=True)

        with right_p:
            # 这里的 Tab 是原生组件，会自动在白色卡片上方对齐
            tab_login, tab_reg = st.tabs(["🔒 安全登录", "📝 快速注册"])
            
            with tab_login:
                with st.form("final_login_form"):
                    acc = st.text_input("账号", placeholder="手机号 / 邮箱")
                    pwd = st.text_input("密码", type="password", placeholder="请输入登录密码")
                    if st.form_submit_button("登 录", use_container_width=True):
                        if acc and pwd:
                            success, msg = login_user(acc, pwd)
                            if success:
                                st.session_state['user_phone'] = acc
                                st.rerun()
                            else: st.error(msg)
                        else: st.warning("请完善登录信息")
            
            with tab_reg:
                with st.form("final_reg_form"):
                    r_acc = st.text_input("注册账号", placeholder="手机号/邮箱")
                    r_p1 = st.text_input("设置密码", type="password")
                    r_inv = st.text_input("邀请码", value="888888")
                    if st.form_submit_button("立即注 册", use_container_width=True):
                        success, msg = register_user(r_acc, r_p1, r_inv)
                        if success: st.success("注册成功！请切换到登录页")
                        else: st.error(msg)

    # 底部版权
    st.markdown("""
        <div style="position: fixed; bottom: 30px; width: 100%; text-align: center; color: rgba(255,255,255,0.3); font-size: 12px;">
            © 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.
        </div>
    """, unsafe_allow_html=True)
