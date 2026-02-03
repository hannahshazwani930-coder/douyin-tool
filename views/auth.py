# views/auth.py
import streamlit as st
from utils import load_isolated_css
from database import login_user, register_user

def view_auth():
    # 🔒 锁定加载：确保 CSS 路由正确
    load_isolated_css("auth")
    
    # --- [第一层：卡片主容器] ---
    # 使用 HTML 注入确保左右分栏在同一个层级
    st.markdown('<div class="auth-card-inner">', unsafe_allow_html=True)
    
    # 划分左右比例 3.5 : 6.5
    left, right = st.columns([0.35, 0.65], gap="none")
    
    with left:
        # 左侧蓝色品牌区
        st.markdown("""
            <div style="background: linear-gradient(135deg, #2563eb, #1d4ed8); height: 500px; padding: 40px; color: white; display: flex; flex-direction: column; justify-content: center; border-top-left-radius: 24px; border-bottom-left-radius: 24px;">
                <h1 style='color:white; margin:0;'>💠</h1>
                <h2 style='color:white; margin:20px 0 10px 0; font-size:26px;'>爆款工场 Pro</h2>
                <p style='font-size:14px; opacity:0.8; line-height:1.6;'>
                    专业短视频创作辅助系统<br>
                    AI 驱动 · 模块化安全版
                </p>
            </div>
        """, unsafe_allow_html=True)

    with right:
        # 右侧白色表单区
        # 注意：这里我们使用 Streamlit 原生组件，它们会被 CSS 自动渲染到右侧
        st.markdown('<div style="padding: 20px 30px;">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🔑 登录", "📝 注册"])
        
        with tab1:
            with st.form("login_form", clear_on_submit=False):
                acc = st.text_input("手机号 / 邮箱", placeholder="请输入账号", key="login_acc")
                pwd = st.text_input("密码", type="password", placeholder="请输入密码", key="login_pwd")
                if st.form_submit_button("立即登录"):
                    if acc and pwd:
                        success, msg = login_user(acc, pwd)
                        if success:
                            st.session_state['user_phone'] = acc
                            st.rerun()
                        else: st.error(msg)
                    else: st.warning("请填写信息")
        
        with tab2:
            with st.form("register_form"):
                r_acc = st.text_input("注册账号", placeholder="手机号/邮箱", key="reg_acc")
                c1, c2 = st.columns(2)
                with c1: r_p1 = st.text_input("设置密码", type="password", key="reg_p1")
                with c2: r_p2 = st.text_input("确认密码", type="password", key="reg_p2")
                inv = st.text_input("邀请码", value="888888", key="reg_inv")
                
                if st.form_submit_button("创建新账号"):
                    if r_p1 != r_p2: st.error("两次密码不一致")
                    else:
                        success, msg = register_user(r_acc, r_p1, inv)
                        if success: st.success("注册成功！")
                        else: st.error(msg)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 关闭卡片主容器标签
    st.markdown('</div>', unsafe_allow_html=True)

    # --- [第二层：外部下方免责声明] ---
    st.markdown("""
        <div class="external-disclaimer">
            <p>登录即代表您同意《用户协议》及《隐私政策》</p>
            <p style="opacity:0.6; font-size:12px;">本系统仅供参考，请遵守平台规范。版权所有 © 2026</p>
        </div>
    """, unsafe_allow_html=True)
