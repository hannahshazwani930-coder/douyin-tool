# views/auth.py
import streamlit as st
from utils import load_isolated_css
from database import login_user, register_user

def view_auth():
    # 🔒 [LOCKED] 强制加载独立样式隔离系统，确保格式不被改动
    load_isolated_css("auth")
    
    # 页面大标题
    st.markdown("<h1 style='text-align:center; color:#0f172a; margin-bottom:10px;'>💠 抖音爆款工场 Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#64748b; margin-bottom:30px;'>专业短视频创作辅助系统 · 模块化安全版</p>", unsafe_allow_html=True)

    # 创建登录与注册选项卡
    tab1, tab2 = st.tabs(["🔒 账号登录", "📝 快速注册"])
    
    # --- 登录模块 ---
    with tab1:
        # 5. 回车登录：使用 st.form 封装，在输入框按回车即可触发提交按钮
        with st.form("login_form", clear_on_submit=False):
            st.markdown("<div style='padding:10px 0;'>", unsafe_allow_html=True)
            
            # 1. 账号支持手机或邮箱（逻辑层处理）
            account = st.text_input("手机号 / 邮箱", placeholder="请输入您的注册账号")
            password = st.text_input("登录密码", type="password", placeholder="请输入密码")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # 6. 按钮悬浮效果已在 auth.css 中定义
            submit_login = st.form_submit_button("立即进入系统")
            
            if submit_login:
                if account and password:
                    success, msg = login_user(account, password)
                    if success:
                        st.session_state['user_phone'] = account
                        st.success("登录成功，正在跳转...")
                        st.rerun()
                    else:
                        st.error(msg)
                else:
                    st.warning("请填写完整的账号和密码")

    # --- 注册模块 ---
    with tab2:
        # 使用 form 封装以支持回车并规范布局
        with st.form("register_form"):
            st.markdown("<div style='padding:10px 0;'>", unsafe_allow_html=True)
            
            # 1. 注册账号支持手机/邮箱
            reg_account = st.text_input("注册账号", placeholder="手机号或常用邮箱")
            
            # 2. 设置密码需要输入 2 次，且利用 800px 宽度进行双列排版
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                reg_pwd1 = st.text_input("设置密码", type="password", placeholder="不少于6位")
            with col_p2:
                reg_pwd2 = st.text_input("确认密码", type="password", placeholder="请再次输入密码")
            
            # 3. 邀请码默认 888888
            invite_code = st.text_input("邀请码", value="888888", help="若无邀请码请联系客服")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            submit_reg = st.form_submit_button("创建新账号")
            
            if submit_reg:
                # 校验二次密码
                if reg_pwd1 != reg_pwd2:
                    st.error("❌ 两次输入的密码不一致，请检查！")
                elif len(reg_pwd1) < 6:
                    st.error("❌ 密码安全强度不足，请至少设置 6 位密码")
                elif not reg_account:
                    st.error("❌ 账号名不能为空")
                else:
                    success, msg = register_user(reg_account, reg_pwd1, invite_code)
                    if success:
                        st.success("✅ 注册成功！请切换至“账号登录”选项卡进入系统。")
                    else:
                        st.error(f"❌ {msg}")

    # 4. 底部添加相关免责声明
    st.markdown("""
        <div class="disclaimer">
            <hr style="border:0; border-top:1px solid #eee; margin:30px 0 20px 0;">
            <b>免责声明：</b><br>
            本系统生成的文案、选题及图片内容仅供创作参考，用户需自行审核并承担发布后果。<br>
            登录即代表您已阅读并同意《用户协议》与《隐私政策》。版权所有 © 2026 抖音爆款工场。
        </div>
    """, unsafe_allow_html=True)

# 确保 views 文件夹下的脚本能正常工作
if __name__ == "__main__":
    view_auth()
