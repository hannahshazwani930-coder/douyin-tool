import streamlit as st
import pandas as pd
import uuid
import datetime
from database import get_conn
from config import ADMIN_ACCOUNT

def view_admin():
    if st.session_state.get('user_phone') != ADMIN_ACCOUNT:
        st.error("无权访问")
        return
        
    st.markdown("### 🕵️‍♂️ 管理后台")
    
    t1, t2 = st.tabs(["用户管理", "卡密生成"])
    with t1:
        conn = get_conn()
        # 简单查询前50个用户
        df = pd.read_sql("SELECT phone, invite_count, register_time FROM users ORDER BY register_time DESC LIMIT 50", conn)
        st.dataframe(df, use_container_width=True)
        conn.close()
        
    with t2:
        days = st.number_input("天数", value=30)
        count = st.number_input("数量", value=10)
        if st.button("生成卡密"):
            conn = get_conn(); c = conn.cursor()
            new_codes = []
            for _ in range(count):
                code = f"VIP-{uuid.uuid4().hex[:8].upper()}"
                c.execute("INSERT INTO access_codes (code, duration_days, status, create_time) VALUES (?, ?, ?, ?)", (code, days, 'unused', datetime.datetime.now()))
                new_codes.append([code, days])
            conn.commit(); conn.close()
            st.success(f"已生成 {count} 个卡密")
            st.dataframe(pd.DataFrame(new_codes, columns=["卡密", "天数"]))