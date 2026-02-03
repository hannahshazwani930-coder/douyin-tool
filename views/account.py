# views/account.py
import streamlit as st
from utils import load_isolated_css
from database import get_user_invite_info, get_user_vip_status, add_feedback, get_user_feedbacks, redeem_card, get_setting

def view_account():
    render_page_banner("个人中心", "管理您的会员权益、推广收益及系统反馈。")
    
    user = st.session_state['user_phone']
    vip_status, msg = get_user_vip_status(user)
    my_code, invite_count = get_user_invite_info(user)
    
    # 状态卡片
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.metric("当前状态", msg)
            if not vip_status:
                buy_url = get_setting("buy_card_url")
                if buy_url:
                    st.markdown(f"[💳 去购买卡密]({buy_url})")
                else:
                    st.caption("请联系管理员获取卡密")
                    
    with c2:
        with st.container(border=True):
            st.metric("已邀请好友", f"{invite_count} 人")

    # 卡密激活 (Requirement 8)
    with st.container(border=True):
        st.markdown("#### 🔑 会员续费 / 激活")
        c_code, c_btn = st.columns([3, 1])
        with c_code:
            card_key = st.text_input("输入卡密", placeholder="VIP-30D-XXXXXX", label_visibility="collapsed")
        with c_btn:
            if st.button("立即激活", type="primary", use_container_width=True):
                if card_key:
                    success, res_msg = redeem_card(user, card_key.strip())
                    if success:
                        st.balloons()
                        st.success(res_msg)
                        st.rerun()
                    else:
                        st.error(res_msg)
                else:
                    st.warning("请输入卡密")

    # 推广链接
    with st.container(border=True):
        st.markdown("#### 💸 推广赚钱")
        invite_link = f"http://app-link.com/?invite={my_code}" 
        st.text_input("专属链接", value=invite_link, disabled=True)
        render_copy_btn(invite_link, "invite_link_copy")

    # 反馈
    st.markdown("### 📬 意见反馈")
    tab_w, tab_h = st.tabs(["提交反馈", "历史记录"])
    with tab_w:
        with st.form("fb"):
            txt = st.text_area("内容", height=100)
            if st.form_submit_button("提交"):
                add_feedback(user, txt)
                st.success("已提交")
    with tab_h:
        feeds = get_user_feedbacks(user)
        for c, r, t, s in feeds:
            with st.expander(f"{str(t)[:10]} - {s}", expanded=True):
                st.write(f"问: {c}")
                if r: st.success(f"答: {r}")

