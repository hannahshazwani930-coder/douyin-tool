# views/auth.py
import streamlit as st
from utils import load_isolated_css
from database import login_user, register_user

def view_auth():
    # 1. 注入 CSS 
    load_isolated_css("auth")
    
    # 2. 渲染左侧品牌内容 (其背景已由 CSS ::before 伪元素锁死)
    st.markdown("""
        <div class="brand-fixed-content">
            <div style="font-size: 50px; margin-bottom: 20px;">💠</div>
            <h1 style="color:white; font-size: 32px; font-weight: 800; margin: 0;">抖音爆款工场</h1>
            <p style="font-size: 14px; opacity: 0.7; margin-top: 15px; line-height: 1.6;">
                专业短视频创作辅助系统<br>AI 驱动 · 模块化安全版
            </p>
            <div style="margin-top: 80px; font-size: 10px; letter-spacing: 4px; opacity: 0.3;">EST. 2026 PRO</div>
        </div>
    """, unsafe_allow_html=True)

    # 3. 右侧逻辑区 (CSS 会自动给这里的组件加上 margin-left: 360px)
    # 顶部留白，模拟纵向居中
    st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#0f172a; margin-bottom:20px;'>安全登录</h3>", unsafe_allow_html=True)
    
    with st.form("auth_main_form"):
        acc = st.text_input("账号", placeholder="手机号 / 邮箱", key="l_acc")
        pwd = st.text_input("密码", type="password", placeholder="请输入登录密码", key="l_pwd")
        
        # 按钮由 CSS 锁定样式
        if st.form_submit_button("登 录"):
            if acc and pwd:
                success, msg = login_user(acc, pwd)
                if success:
                    st.session_state['user_phone'] = acc
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.warning("请填写完整信息")

    # 底部注册跳转
    if st.button("新用户注册 / 申请试用", use_container_width=True):
        st.info("系统维护中，请联系客服获取激活码")

    # 4. 独立渲染外部下方声明
    st.markdown("""
        <div class="footer-disclaimer-fixed">
            使用即代表同意《用户协议》与《隐私政策》<br>
            © 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    view_auth()
