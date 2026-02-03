# views/admin.py
import streamlit as st
import pandas as pd
from database import get_stats, get_all_feedbacks_admin, reply_feedback, create_announcement, delete_announcement, get_active_announcements, generate_bulk_cards, update_setting, get_setting, get_conn
from utils import load_isolated_css

def view_admin():
    render_page_banner("管理后台", "系统监控、用户管理、卡密分发中心。")
    
    uc, vc = get_stats()
    c1, c2 = st.columns(2)
    c1.metric("总注册用户", uc)
    c2.metric("激活VIP用户", vc)
    
    tab_card, tab_set, tab_ann, tab_feed = st.tabs(["🔑 卡密管理", "⚙️ 系统设置", "📢 公告", "💬 反馈"])
    
    # 1. 卡密管理 (Requirement 9)
    with tab_card:
        st.markdown("#### 批量生成卡密")
        with st.form("gen_card"):
            days = st.selectbox("时长 (天)", [1, 7, 30, 90, 365])
            amount = st.number_input("数量", min_value=1, max_value=100, value=10)
            if st.form_submit_button("生成"):
                codes = generate_bulk_cards(amount, days)
                st.success(f"成功生成 {amount} 个 {days}天卡密")
                st.code("\n".join(codes))
        
        st.markdown("#### 卡密状态")
        conn = get_conn()
        df = pd.read_sql("SELECT code, duration_days, status, bind_user, activated_at FROM access_codes ORDER BY create_time DESC LIMIT 50", conn)
        conn.close()
        st.dataframe(df, use_container_width=True)

    # 2. 系统设置 (Requirement 9)
    with tab_set:
        st.markdown("#### 购买链接设置")
        curr_url = get_setting("buy_card_url")
        new_url = st.text_input("卡密购买网址 (发卡网)", value=curr_url)
        if st.button("保存设置"):
            update_setting("buy_card_url", new_url)
            st.success("已保存")

    # 3. 公告
    with tab_ann:
        n_ann = st.text_input("新公告内容")
        if st.button("发布"):
            create_announcement(n_ann)
            st.rerun()
        anns = get_active_announcements()
        for c, t in anns:
            c1, c2 = st.columns([4,1])
            c1.info(f"{t}: {c}")
            if c2.button("删除", key=c):
                delete_announcement(c)
                st.rerun()

    # 4. 反馈
    with tab_feed:
        feeds = get_all_feedbacks_admin()
        for fid, phone, content, reply, time, status in feeds:
            with st.expander(f"{phone}: {content[:10]}..."):
                st.write(content)
                if reply: st.success(f"已回: {reply}")
                else:
                    r_txt = st.text_input("回复", key=f"r_{fid}")
                    if st.button("发送", key=f"b_{fid}"):
                        reply_feedback(fid, r_txt)
                        st.rerun()

