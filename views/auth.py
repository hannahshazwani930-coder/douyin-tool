# views/auth.py
import streamlit as st
import time
import sqlite3
from database import login_user, register_user, get_conn, GLOBAL_INVITE_CODE
from utils import inject_css
from config import REWARD_DAYS_NEW_USER

def view_auth():
    # 注入登录页专用样式
    inject_css("auth")
    
    st.markdown("<div style='height: 10vh;'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 10, 1])
    
    with c2:
        col_text, col_form = st.columns([1.2, 1], gap="large")
        
        # 左侧文案区
        with col_text:
            st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
            st.markdown("<div class='lp-header'>抖音爆款工场 Pro</div>", unsafe_allow_html=True)
            st.markdown("<div class='lp-sub'>全网首个 AI + KOC 商业变现操作系统<br>让流量不再是玄学</div>", unsafe_allow_html=True)
            features = [
                ("🚀", "5路并发 · 极速文案清洗改写"),
                ("💡", "爆款选题 · 击穿流量焦虑"),
                ("🎨", "海报生成 · 影视级光影质感"),
                ("💰", "裂变系统 · 邀请好友免费续杯")
            ]
            for icon, text in features:
                st.markdown(f"<div class='lp-item'><div class='lp-icon'>{icon}</div>{text}</div>", unsafe_allow_html=True)
        
        # 右侧表单区
        with col_form:
            t1, t2 = st.tabs(["🔐 登录账号", "📝 注册新号"])
            
            # --- 登录 Tab ---
            with t1:
                with st.form("login"):
                    st.text_input("账号", placeholder="手机号", key="l_u")
                    st.text_input("密码", placeholder="密码", type="password", key="l_p")
                    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
                    if st.form_submit_button("立即进入系统", type="primary", use_container_width=True):
                        if not st.session_state.l_u or not st.session_state.l_p:
                            st.error("请输入账号和密码")
                        else:
                            s, m = login_user(st.session_state.l_u, st.session_state.l_p)
                            if s: 
                                st.session_state['user_phone'] = st.session_state.l_u
                                st.rerun()
                            else: st.error(m)
            
            # --- 注册 Tab ---
            with t2:
                with st.form("register"):
                    st.info(f"🎁 新用户立送 {REWARD_DAYS_NEW_USER} 天 VIP")
                    r_u = st.text_input("手机号", placeholder="作为登录账号")
                    r_p = st.text_input("设置密码", type="password")
                    r_c = st.text_input("邀请码", placeholder="必填，无码请联系客服")
                    if st.form_submit_button("立即注册", use_container_width=True):
                        if not r_u or not r_p or not r_c:
                            st.warning("请填写完整信息")
                        else:
                            # 验证邀请码
                            valid = False
                            if r_c == GLOBAL_INVITE_CODE: valid = True
                            else:
                                conn = get_conn(); cu = conn.cursor()
                                cu.execute("SELECT phone FROM users WHERE own_invite_code=?", (r_c,))
                                if cu.fetchone(): valid = True
                                conn.close()
                            
                            if valid:
                                s, m = register_user(r_u, r_p, r_c)
                                if s: 
                                    st.success(m)
                                    st.session_state['user_phone'] = r_u
                                    time.sleep(1)
                                    st.rerun()
                                else: st.error(m)
                            else: st.error("❌ 邀请码无效，请联系客服获取")

    st.markdown("<div style='position:fixed; bottom:20px; width:100%; text-align:center; color:rgba(255,255,255,0.4); font-size:12px;'>© 2026 抖音爆款工场 Pro | 鄂ICP备2024XXXXXX号-1</div>", unsafe_allow_html=True)
