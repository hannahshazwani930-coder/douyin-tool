import streamlit as st
from views.auth import view_auth

# 1. 全局配置锁定
st.set_page_config(
    page_title="爆款工厂PRO",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # --- 登录拦截判定 ---
    if 'user_phone' not in st.session_state:
        # 未登录状态强制渲染已锁定的登录页
        st.markdown("<style>[data-testid='stSidebar'] { display:none; }</style>", unsafe_allow_html=True)
        view_auth()
        return

    # --- 2. 侧边栏：大厂 SaaS 指挥中心重塑 ---
    with st.sidebar:
        # A. 品牌标识区
        st.markdown("""
        <div style="padding: 10px 0 30px 5px;">
            <div style="background: #1E3A8A; color: white; width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; float: left; margin-right: 12px; font-weight: 900; font-size: 20px;">V</div>
            <div style="float: left;">
                <div style="color: #1E3A8A; font-weight: 800; font-size: 18px; line-height: 1.2;">爆款工厂</div>
                <div style="color: #94A3B8; font-size: 11px; letter-spacing: 1px;">MANAGEMENT PRO</div>
            </div>
            <div style="clear: both;"></div>
        </div>
        """, unsafe_allow_html=True)

        # B. 算力监控区 (彰显 SaaS 含金量)
        st.markdown("""
        <div style="background: #F8FAFC; border: 1px solid #F1F5F9; border-radius: 12px; padding: 15px; margin-bottom: 25px;">
            <div style="color: #64748B; font-size: 11px; margin-bottom: 8px; font-weight: 600;">AI ENGINE STATUS</div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #1E3A8A; font-size: 13px; font-weight: 700;">Neural v3.5</span>
                <span style="color: #10B981; font-size: 11px; font-weight: 700;">● 运行中</span>
            </div>
            <div style="width: 100%; background: #E2E8F0; height: 4px; border-radius: 2px; margin-top: 10px;">
                <div style="width: 78%; background: #1E3A8A; height: 4px; border-radius: 2px;"></div>
            </div>
            <div style="color: #94A3B8; font-size: 10px; margin-top: 6px;">当前负载: 78% (高速)</div>
        </div>
        """, unsafe_allow_html=True)

        # C. 业务功能区 (原生 pages/ 菜单会自动渲染在此处)
        st.markdown("<p style='color: #94A3B8; font-size: 11px; padding-left: 5px; margin-bottom: 15px; font-weight: 600;'>MISSION CONTROL</p>", unsafe_allow_html=True)
        
        # D. 底部管理区
        st.write("\n" * 5)
        with st.container():
            st.markdown("---")
            col_u1, col_u2 = st.columns([1, 3])
            with col_u1:
                st.write("👤")
            with col_u2:
                st.markdown(f"<p style='color: #475569; font-size: 13px; margin: 0;'>{st.session_state.get('user_phone', 'Admin')}</p>", unsafe_allow_html=True)
            
            if st.button("安全登出指挥系统", use_container_width=True):
                del st.session_state['user_phone']
                st.rerun()

    # --- 3. 页面渲染逻辑 ---
    # 这里保持为空，Streamlit 会自动根据 pages/ 下的文件渲染当前选中的功能页内容

if __name__ == "__main__":
    main()
