# views/auth.py
import streamlit as st
from utils import load_isolated_css
from database import login_user, register_user

def view_auth():
    # 🔒 锁定：加载横屏版隔离样式
    load_isolated_css("auth")
    
    # --- 1. 核心卡片容器 (左右横屏分布) ---
    # 利用 Streamlit columns 模拟分栏
    with st.container():
        # 整体卡片开始渲染
        st.markdown('<div class="auth-card-inner">', unsafe_allow_html=True)
        
        # 布局分栏：3.5 (左蓝) : 6.5 (右白)
        left, right = st.columns([0.35, 0.65], gap="none")
        
        with left:
            # 左侧品牌展示区
            st.markdown("""
                <div style="background: linear-gradient(135deg, #2563eb, #1d4ed8); height: 500px; padding: 40px; color: white; display: flex; flex-direction: column; justify-content: center;">
                    <h1 style='color:white; margin:0;'>💠</h1>
                    <h2 style='color:white; margin:20px 0 10px 0; font-size:28px;'>爆款工场 Pro</h2>
                    <p style='font-size:14px; opacity:0.8; line-height:1.6;'>
                        专业短视频创作辅助系统<br>
                        AI 驱动 · 模块化安全版
                    </p>
                </div>
            """, unsafe_allow_html=True)

        with right:
            # 右侧操作区
            st.markdown('<div style="padding: 30px 40px;">', unsafe_allow_html=True)
            tab1, tab2 = st.tabs(["🔑 账号登录", "📝 快速注册"])
            
            with tab1:
                with st.form("login_form", clear_on_submit=False):
                    account = st.text_input("手机号 / 邮箱", placeholder="请输入您的账号")
                    password = st.text_input("登录密码", type="password", placeholder="请输入密码")
                    if st.form_submit_button("立即登录"):
                        if account and password:
                            success, msg = login_user(account, password)
                            if success:
                                st.session_state['user_phone'] = account
                                st.rerun()
                            else: st.error(msg)
                        else: st.warning("请完善登录信息")
            
            with tab2:
                with st.form("register_form"):
                    reg_acc = st.text_input("注册账号", placeholder="手机号或常用邮箱")
                    cp1, cp2 = st.columns(2)
                    with cp1: reg_p1 = st.text_input("设置密码", type="password")
                    with cp2: reg_p2 = st.text_input("确认密码", type="password")
                    invite = st.text_input("邀请码", value="888888")
                    
                    if st.form_submit_button("创建新账号"):
                        if reg_p1 != reg_p2: st.error("两次密码输入不一致")
                        else:
                            success, msg = register_user(reg_acc, reg_p1, invite)
                            if success: st.success("注册成功！请登录")
                            else: st.error(msg)
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True) # 结束 auth-card-inner

    # --- 2. 卡片外部下方：免责声明 ---
    st.markdown("""
        <div class="external-disclaimer">
            <p>登录即代表您同意《用户协议》及《隐私政策》</p>
            <p style="opacity:0.7;">本系统内容仅供创作参考，请遵守各平台运营规范。版权所有 © 2026 抖音爆款工场</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    view_auth()
