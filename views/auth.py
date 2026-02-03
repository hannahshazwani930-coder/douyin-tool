# views/auth.py
import streamlit as st
from database import login_user, register_user

def view_auth():
    # 1. 顶部留白，让卡片在视觉上居中
    st.write("\n" * 5)
    
    # 2. 使用原生栅格系统：[左边距, 左侧内容, 中间间距, 右侧内容, 右边距]
    # 比例设定为 1:3:0.5:4:1，这是最稳固的横屏比例
    _, col_brand, col_gap, col_form, _ = st.columns([1, 3, 0.5, 4, 1])

    with col_brand:
        # 左侧品牌展示
        st.markdown("# 💠")
        st.markdown("## 抖音爆款工场")
        st.info("AI 驱动的一站式短视频创作中枢")
        st.write("---")
        st.caption("Professional Edition 2026")
        st.caption("稳定 · 高效 · 模块化")

    with col_form:
        # 右侧登录/注册切换
        # 原生 Tabs 是解决“找不到按钮”和“布局乱套”的终极方案
        tab_login, tab_reg = st.tabs(["🔒 安全登录", "📝 快速注册"])
        
        with tab_login:
            with st.form("native_login_form"):
                acc = st.text_input("手机号 / 邮箱", placeholder="请输入账号", key="l_acc")
                pwd = st.text_input("密码", type="password", placeholder="请输入密码", key="l_pwd")
                
                # 按钮自动适配宽度
                submit = st.form_submit_button("立即登录", use_container_width=True)
                
                if submit:
                    if acc and pwd:
                        success, msg = login_user(acc, pwd)
                        if success:
                            st.session_state['user_phone'] = acc
                            st.rerun()
                        else:
                            st.error(f"登录失败: {msg}")
                    else:
                        st.warning("请填写完整登录信息")

        with tab_reg:
            with st.form("native_reg_form"):
                r_acc = st.text_input("设置账号", placeholder="手机号/邮箱", key="r_acc")
                r_pwd = st.text_input("设置密码", type="password", key="r_pwd")
                r_inv = st.text_input("邀请码", value="888888", key="r_inv")
                
                r_submit = st.form_submit_button("注册新账号", use_container_width=True)
                
                if r_submit:
                    success, msg = register_user(r_acc, r_pwd, r_inv)
                    if success:
                        st.success("注册成功！请切换到登录标签进行登录")
                    else:
                        st.error(f"注册失败: {msg}")

    # 3. 页面底部版权声明
    st.write("\n" * 10)
    st.divider()
    st.caption("© 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED. 使用即代表同意用户协议与隐私政策")

if __name__ == "__main__":
    view_auth()
