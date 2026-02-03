# views/auth.py
import streamlit as st
from utils import load_isolated_css
from database import login_user, register_user

def view_auth():
    # 🔒 锁定加载：确保 CSS 路由正确并应用
    load_isolated_css("auth")
    
    # --- [第一层：卡片主容器] ---
    # 使用自定义 div 包装，配合 CSS 实现 800px 横屏对齐
    st.markdown('<div class="auth-card-inner">', unsafe_allow_html=True)
    
    # 使用 columns 但通过 CSS 强制消除间隙
    left, right = st.columns([0.35, 0.65], gap="small")
    
    with left:
        # 左侧蓝色品牌展示区 (高度固定 500px，圆角贴合)
        st.markdown("""
            <div style="background: linear-gradient(135deg, #2563eb, #1d4ed8); 
                        height: 500px; padding: 40px; color: white; 
                        display: flex; flex-direction: column; justify-content: center; 
                        border-top-left-radius: 24px; border-bottom-left-radius: 24px;">
                <h1 style='color:white; margin:0; font-size:40px;'>💠</h1>
                <h2 style='color:white; margin:20px 0 10px 0; font-size:26px;'>爆款工场 Pro</h2>
                <p style='font-size:14px; opacity:0.8; line-height:1.6;'>
                    专业短视频创作辅助系统<br>
                    AI 驱动 · 模块化安全版
                </p>
            </div>
        """, unsafe_allow_html=True)

    with right:
        # 右侧白色交互表单区
        st.markdown('<div style="padding: 30px 40px; background: white; height: 500px; border-top-right-radius: 24px; border-bottom-right-radius: 24px;">', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔑 账号登录", "📝 快速注册"])
        
        with tab1:
            with st.form("login_form", clear_on_submit=False):
                acc = st.text_input("手机号 / 邮箱", placeholder="请输入账号", key="login_acc")
                pwd = st.text_input("登录密码", type="password", placeholder="请输入密码", key="login_pwd")
                
                # 按钮触发回车登录
                if st.form_submit_button("立即登录"):
                    if acc and pwd:
                        success, msg = login_user(acc, pwd)
                        if success:
                            st.session_state['user_phone'] = acc
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.warning("请完善登录信息")
        
        with tab2:
            with st.form("register_form"):
                reg_acc = st.text_input("注册账号", placeholder="手机号或邮箱", key="reg_acc")
                
                col_pwd1, col_pwd2 = st.columns(2)
                with col_pwd1:
                    reg_pwd1 = st.text_input("设置密码", type="password", key="reg_p1")
                with col_pwd2:
                    reg_pwd2 = st.text_input("确认密码", type="password", key="reg_p2")
                
                invite = st.text_input("邀请码", value="888888", key="reg_inv")
                
                if st.form_submit_button("创建新账号"):
                    if reg_pwd1 != reg_pwd2:
                        st.error("❌ 两次输入的密码不一致")
                    elif len(reg_pwd1) < 6:
                        st.error("❌ 密码长度至少需要6位")
                    else:
                        success, msg = register_user(reg_acc, reg_pwd1, invite)
                        if success:
                            st.success("✅ 注册成功！请切换到登录页。")
                        else:
                            st.error(msg)
                            
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 关闭卡片主容器 div
    st.markdown('</div>', unsafe_allow_html=True)

    # --- [第二层：外部下方免责声明] ---
    st.markdown("""
        <div class="external-disclaimer">
            <p>登录即代表您同意《用户协议》及《隐私政策》</p>
            <p style="opacity:0.6; font-size:12px; margin-top:5px;">
                本系统生成的文案及建议仅供参考。版权所有 © 2026 抖音爆款工场
            </p>
        </div>
    """, unsafe_allow_html=True)
