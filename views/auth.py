# views/auth.py
import streamlit as st
from database import login_user, register_user

def view_auth():
    # 1. 顶部视觉留白 (让卡片看起来是在屏幕中上部悬浮)
    st.write("\n" * 3)

    # 2. 物理宽度锁定：[1.2份边距, 3份卡片内容, 1.2份边距]
    # 这里的 3 决定了卡片的紧凑度，比例越大卡片越宽
    _, card_container, _ = st.columns([1.2, 3, 1.2])

    with card_container:
        # 3. 悬浮感卡片：使用原生边框容器
        with st.container(border=True):
            # 4. 内部左右分栏：左侧品牌 (40%)，右侧表单 (60%)
            col_left, col_right = st.columns([1.5, 2], gap="large")

            with col_left:
                # --- 左边：专业文字内容 ---
                st.write("\n")
                st.markdown("### 💠 爆款工场 Pro")
                st.write("---")
                st.markdown("""
                **AI 驱动创作中枢**
                
                🚀 **全模块化架构**
                每一秒创作都经过精密算法优化
                
                🔒 **独立安全存储**
                企业级数据隔离，保护原创灵感
                
                📈 **趋势深度洞察**
                实时抓取抖音爆款逻辑
                """)
                st.write("\n")
                st.caption("Professional Edition 2026")

            with col_right:
                # --- 右边：登录/注册交互内容 ---
                tab_login, tab_reg = st.tabs(["🔒 安全登录", "📝 快速注册"])
                
                with tab_login:
                    with st.form("pro_login_form"):
                        acc = st.text_input("账号", placeholder="手机号 / 邮箱", label_visibility="collapsed")
                        pwd = st.text_input("密码", type="password", placeholder="请输入密码", label_visibility="collapsed")
                        
                        # 登录按钮
                        if st.form_submit_button("立 即 登 录", use_container_width=True):
                            if acc and pwd:
                                success, msg = login_user(acc, pwd)
                                if success:
                                    st.session_state['user_phone'] = acc
                                    st.rerun()
                                else:
                                    st.error(f"登录失败: {msg}")
                            else:
                                st.warning("请填写账号和密码")

                with tab_reg:
                    with st.form("pro_reg_form"):
                        r_acc = st.text_input("设置账号", placeholder="手机号/邮箱")
                        r_pwd = st.text_input("设置密码", type="password")
                        r_inv = st.text_input("邀请码", value="888888")
                        
                        if st.form_submit_button("注 册 账 号", use_container_width=True):
                            success, msg = register_user(r_acc, r_pwd, r_inv)
                            if success:
                                st.success("注册成功！请切换到登录页")
                            else:
                                st.error(f"注册失败: {msg}")

    # 5. 底部免责声明 (独立于卡片，强制居中)
    st.write("\n" * 4)
    st.divider()
    st.markdown("""
        <div style="text-align: center; color: #888; font-size: 12px;">
            <p>使用即代表您同意《用户服务协议》与《隐私保护政策》</p>
            <p>© 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.</p>
        </div>
    """, unsafe_allow_html=True)
