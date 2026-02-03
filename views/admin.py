# views/admin.py
import streamlit as st
import pandas as pd
from database import get_stats, get_all_feedbacks_admin, reply_feedback, create_announcement, delete_announcement, get_active_announcements, get_conn

def view_admin():
    st.markdown("## 🕵️‍♂️ 管理员后台")
    
    # 1. 核心数据 (Requirement 11: 注册统计)
    uc, vc = get_stats()
    c1, c2, c3 = st.columns(3)
    c1.metric("总注册用户", uc)
    c2.metric("有效VIP用户", vc)
    c3.metric("今日新增", "+2") # 模拟数据
    
    tab_stats, tab_ann, tab_feed, tab_code = st.tabs(["📊 数据概览", "📢 公告管理", "💬 反馈回复", "🔑 卡密管理"])
    
    with tab_stats:
        st.write("用户增长趋势 (模拟数据)")
        st.line_chart({"date": ["10-01", "10-02", "10-03"], "users": [10, 25, 42]})
        
    with tab_ann:
        st.markdown("#### 发布新公告")
        new_ann = st.text_input("公告内容")
        if st.button("发布公告"):
            if new_ann:
                create_announcement(new_ann)
                st.success("发布成功！")
                st.rerun()
        
        st.markdown("#### 正在展示的公告")
        anns = get_active_announcements()
        for ann_content, ann_time in anns:
            c_a, c_b = st.columns([4, 1])
            c_a.info(f"[{str(ann_time)[:10]}] {ann_content}")
            if c_b.button("删除", key=f"del_{ann_content}"):
                delete_announcement(ann_content)
                st.rerun()
                
    with tab_feed:
        st.markdown("#### 用户反馈列表")
        feeds = get_all_feedbacks_admin()
        df = pd.DataFrame(feeds, columns=["ID", "用户", "内容", "回复", "时间", "状态"])
        
        # 简单的回复界面
        for index, row in df.iterrows():
            with st.expander(f"【{row['状态']}】{row['用户']}: {row['内容'][:10]}..."):
                st.write(f"**完整内容：** {row['内容']}")
                if row['回复']:
                    st.success(f"已回复: {row['回复']}")
                    new_reply = st.text_input("修改回复", key=f"re_input_{row['ID']}")
                else:
                    new_reply = st.text_input("输入回复", key=f"re_input_{row['ID']}")
                
                if st.button("发送回复", key=f"btn_re_{row['ID']}"):
                    reply_feedback(row['ID'], new_reply)
                    st.success("已发送")
                    st.rerun()

    with tab_code:
        st.markdown("#### 卡密使用情况")
        conn = get_conn()
        df_codes = pd.read_sql("SELECT code, duration_days, status, bind_user, activated_at FROM access_codes ORDER BY create_time DESC LIMIT 50", conn)
        conn.close()
        st.dataframe(df_codes, use_container_width=True)
