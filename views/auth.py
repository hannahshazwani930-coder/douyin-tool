# views/auth.py
import streamlit as st
from utils import load_isolated_css
from database import login_user, register_user

def view_auth():
    # 🔒 加载独立样式
    load_isolated_css("auth")
    
    st.markdown("<h2 style='text-align:center; color:#0f172a;'>抖音爆款工场 Pro</h2>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 账号登录", "📝 快速注册"])
    
    with tab1:
        # 5. 回车登录：Streamlit 的 st.form 配合 clear_on_submit=False 可实现回车提交
        with st.form("login_form"):
            account = st.text_input("手机号 / 邮箱")
            password = st.text_input("密码", type="password")
            submit = st.form_submit_button("立即登录")
            
            if submit:
                if account and password:
                    success, msg = login_user(account, password)
                    if success:
                        st.session_state['user_phone'] = account
                        st.rerun()
                    else:
                        st.error(msg)
                else:
                    st.warning("请完善登录信息")

    with tab2:
        with st.form("register_form"):
            # 1. 邮箱或手机注册
            reg_account = st.text_input("注册账号", placeholder="请输入手机号或邮箱")
            
            # 2. 密码输入两次
            reg_pwd1 = st.text_input("设置密码", type="password")
            reg_pwd2 = st.text_input("确认密码", type="password")
            
            # 3. 邀请码默认 888888
            invite_code = st.text_input("邀请码", value="888888")
            
            reg_submit = st.form_submit_button("确认注册")
            
            if reg_submit:
                if reg_pwd1 != reg_pwd2:
                    st.error("两次输入的密码不一致！")
                elif len(reg_pwd1) < 6:
                    st.error("密码长度至少需要6位")
                elif not reg_account:
                    st.error("账号不能为空")
                else:
                    success, msg = register_user(reg_account, reg_pwd1, invite_code)
                    if success:
                        st.success("注册成功！请切换到登录页进入。")
                    else:
                        st.error(msg)

    # 4. 底部免责声明
    st.markdown("""
        <div class="disclaimer">
            登录即代表您同意《用户协议》及《隐私政策》<br>
            本系统仅供短视频创作参考，请遵守各平台运营规范。
        </div>
    """, unsafe_allow_html=True)
