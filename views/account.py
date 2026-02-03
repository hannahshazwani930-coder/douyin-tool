import streamlit as st
import sqlite3
import datetime
import time
from database import get_user_invite_info, get_user_vip_status, add_vip_days, get_conn, REWARD_DAYS_REFERRER
from utils import load_isolated_css

def view_account():
    user = st.session_state.get('user_phone')
    if not user: 
        st.error("登录状态失效")
        return

    st.markdown("### 👤 个人中心")
    
    t1, t2 = st.tabs(["🎁 邀请有礼", "💳 账户状态"])
    
    with t1:
        code, count = get_user_invite_info(user)
        st.success(f"🎉 您的邀请码：{code}")
        st.markdown(f"**已邀请人数：{count} 人**（每邀请1人，双方各得 {REWARD_DAYS_REFERRER} 天 VIP）")
        render_copy_btn(code, "invite_code")
        
    with t2:
        is_vip, msg = get_user_vip_status(user)
        col1, col2 = st.columns(2)
        col1.metric("当前账号", user)
        col2.metric("会员状态", "VIP" if is_vip else "普通用户", delta=msg)
        
        st.markdown("---")
        st.write("#### 激活卡密")
        c_code = st.text_input("输入卡密", placeholder="VIP-XXXXXX")
        if st.button("立即激活"):
            conn = get_conn(); cur = conn.cursor()
            cur.execute("SELECT * FROM access_codes WHERE code=?", (c_code,))
            row = cur.fetchone()
            cur.close()
            
            if row and row[4] == 'unused':
                add_vip_days(user, row[1], "CDKEY")
                conn = get_conn(); cur = conn.cursor()
                cur.execute("UPDATE access_codes SET status='active', activated_at=?, bind_user=? WHERE code=?", (datetime.datetime.now(), user, c_code))
                conn.commit(); conn.close()
                st.success(f"✅ 激活成功！增加 {row[1]} 天")
                time.sleep(1); st.rerun()
            else:
                st.error("❌ 卡密无效或已使用")