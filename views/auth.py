# views/auth.py
import streamlit as st
from database import login_user, register_user

def view_auth():
    # 彻底隐藏所有 Streamlit 顶部冗余信息和表单提示的“黑科技”
    st.markdown("""
        <style>
            /* 隐藏表单底部的 "Press Enter to submit" 提示 */
            .stForm p { display: none !important; }
            /* 隐藏顶部工具栏 */
            header, [data-testid="stHeader"] { visibility: hidden; }
        </style>
    """, unsafe_allow_html=True)

    st.write("\n" * 2)

    # 1. 物理宽度锁定：比例 [1.2, 3.2, 1.2] 营造紧凑卡片感
    _, card_container, _ = st.columns([1.1, 3.2, 1.1])

    with card_container:
        # 2. 悬浮感卡片：使用原生边框容器
        with st.container(border=True):
            # 3. 左右排版：左侧吸粉区 (45%)，右侧交互区 (55%)
            col_left, col_right = st.columns([1.8, 2.2], gap="large")

            with col_left:
                # --- 左边：吸引眼球的文案 ---
                st.write("\n")
                st.markdown("<h2 style='color:#1E3A8A; margin-bottom:0;'>💠 爆款工场 Pro</h2>", unsafe_allow_html=True)
                st.markdown("<p style='color:#64748B; font-weight:500;'>每一秒，都在创造爆款</p>", unsafe_allow_html=True)
                st.write("---")
                
                # 核心卖点点阵
                st.markdown("""
                <div style='line-height:2.2;'>
                    <span style='font-size:18px;'>🚀 <b>AI 灵感引擎</b></span><br>
                    <span style='font-size:13px; color:#666;'>告别枯竭，一键生成百万级爆款脚本</span><br><br>
                    <span style='font-size:18px;'>📊 <b>算法深挖</b></span><br>
                    <span style='font-size:13px; color:#666;'>实时拆解抖音流量池，锁定下一个热门</span><br><br>
                    <span style='font-size:18px;'>⚡ <b>极速创作</b></span><br>
                    <span style='font-size:13px; color:#666;'>从创意到成品，效率提升 10 倍以上</span>
                </div>
                """, unsafe_allow_html=True)
                
                st.write("\n")
                st.info("💡 已有 5000+ 创作者加入")

            with col_right:
                # --- 右边：登录/注册交互 ---
                tab_login, tab_reg = st.tabs(["🔒 安全登录", "✨ 开启创作"])
                
                with tab_login:
                    with st.form("login_form", border=False):
                        acc = st.text_input("账号", placeholder="手机号 / 邮箱", label_visibility="collapsed")
                        pwd = st.text_input("密码", type="password", placeholder="请输入密码", label_visibility="collapsed")
                        
                        if st.form_submit_button("立 即 登 录", use_container_width=True):
                            if acc and pwd:
                                success, msg = login_user(acc, pwd)
                                if success:
                                    st.session_state['user_phone'] = acc
                                    st.rerun()
                                else: st.error(msg)
                            else: st.warning("请填写完整信息")

                with tab_reg:
                    with st.form("register_form", border=False):
                        r_acc = st.text_input("设置账号", placeholder="建议使用手机号", label_visibility="collapsed")
                        r_pwd = st.text_input("设置密码", type="password", placeholder="设置登录密码", label_visibility="collapsed")
                        r_pwd_confirm = st.text_input("确认密码", type="password", placeholder="请再次输入密码", label_visibility="collapsed")
                        r_inv = st.text_input("邀请码", value="888888", placeholder="请输入邀请码", label_visibility="collapsed")
                        
                        if st.form_submit_button("免 费 注 册", use_container_width=True):
                            if not r_acc or not r_pwd:
                                st.warning("请填写账号和密码")
                            elif r_pwd != r_pwd_confirm:
                                st.error("两次输入的密码不一致")
                            else:
                                success, msg = register_user(r_acc, r_pwd, r_inv)
                                if success:
                                    st.success("注册成功！请切换至登录页")
                                else:
                                    st.error(msg)

    # 4. 底部居中免责声明
    st.write("\n" * 2)
    st.markdown("""
        <div style="text-align: center; color: #BBB; font-size: 11px; font-family: sans-serif;">
            <hr style="border:0.5px solid #EEE; width:200px; margin: 10px auto;">
            使用即代表同意《用户协议》与《隐私保护政策》<br>
            © 2026 DOUYIN MASTER PRO. ALL RIGHTS RESERVED.
        </div>
    """, unsafe_allow_html=True)
