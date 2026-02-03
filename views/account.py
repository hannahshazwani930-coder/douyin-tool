# views/account.py
import streamlit as st
from utils import load_isolated_css
from database import get_user_vip_status, get_user_invite_info

def view_account():
    load_isolated_css("account") # 🔒 锁定样式
    
    st.markdown("### 👤 个人中心")
    
    current_user = st.session_state.get('user_phone', '未知用户')
    is_vip, vip_msg = get_user_vip_status(current_user)
    invite_code, invite_count = get_user_invite_info(current_user)
    
    with st.container():
        st.markdown('<div class="account-container">', unsafe_allow_html=True)
        st.markdown(f"""
            <div class="profile-header">
                <div style="font-size: 40px;">👤</div>
                <div>
                    <div style="font-weight:700; font-size:18px;">{current_user}</div>
                    <span class="vip-badge">{vip_msg}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="info-row"><span>我的邀请码</span><b>{invite_code}</b></div>
            <div class="info-row"><span>累计邀请人数</span><b>{invite_count} 人</b></div>
            <div class="info-row"><span>账号状态</span><b style="color:green;">正常运行</b></div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
