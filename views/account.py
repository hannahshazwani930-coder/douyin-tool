# views/account.py
import streamlit as st
from utils import render_copy_btn
from database import get_user_invite_info, get_user_vip_status, add_feedback, get_user_feedbacks

def view_account():
    st.markdown("## 👤 个人中心")
    
    user = st.session_state['user_phone']
    vip_status, msg = get_user_vip_status(user)
    my_code, invite_count = get_user_invite_info(user)
    
    # 1. 顶部状态卡
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.metric("会员状态", msg, delta="已激活" if vip_status else "去续费")
    with col2:
        with st.container(border=True):
            st.metric("邀请人数", f"{invite_count} 人", delta="推广赚钱")
            
    # 2. 推广功能 (Requirement 10)
    with st.container(border=True):
        st.markdown("#### 💸 推广赚钱")
        st.write(f"您的专属邀请码：**{my_code}**")
        invite_link = f"http://app-link.com/?invite={my_code}" # 模拟链接
        st.text_input("专属推广链接", value=invite_link, disabled=True)
        render_copy_btn(invite_link, "invite_link_copy")
        
    # 3. 反馈系统 (Requirement 10)
    st.markdown("### 📬 意见反馈")
    tab_write, tab_history = st.tabs(["✍️ 提交反馈", "📜 历史记录"])
    
    with tab_write:
        with st.form("feedback_form"):
            content = st.text_area("请输入您遇到的问题或建议", height=100)
            if st.form_submit_button("提交反馈", type="primary"):
                if content:
                    add_feedback(user, content)
                    st.success("提交成功！管理员回复后将在此处显示。")
                else:
                    st.warning("内容不能为空")
                    
    with tab_history:
        feeds = get_user_feedbacks(user)
        if feeds:
            for f_content, f_reply, f_time, f_status in feeds:
                with st.expander(f"[{str(f_time)[:10]}] {f_content[:20]}...", expanded=True):
                    st.write(f"**我的反馈：** {f_content}")
                    if f_reply:
                        st.success(f"**管理员回复：** {f_reply}")
                    else:
                        st.info("⏳ 等待管理员回复...")
        else:
            st.caption("暂无反馈记录")
