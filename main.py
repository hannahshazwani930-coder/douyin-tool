# main.py
import streamlit as st
from views.auth import view_auth

# 1. 全局配置：锁定横屏宽版与侧边栏
st.set_page_config(page_title="爆款工厂PRO", page_icon="🎯", layout="wide", initial_sidebar_state="expanded")

def main():
    # --- 登录拦截判定 ---
    if 'user_phone' not in st.session_state:
        st.markdown("<style>[data-testid='stSidebar'] { display:none; }</style>", unsafe_allow_html=True)
        view_auth()
        return

    # --- 2. [锁定] 大厂级全局 Header (顶部会员登录信息) ---
    # 模拟飞书/阿里云的顶部通条
    st.markdown(f"""
    <div style="position: fixed; top: 0; left: 0; right: 0; height: 50px; background: white; border-bottom: 1px solid #F1F5F9; z-index: 99; display: flex; align-items: center; justify-content: flex-end; padding: 0 40px;">
        <div style="display: flex; align-items: center; gap: 20px;">
            <div style="text-align: right;">
                <div style="color: #1E3A8A; font-size: 13px; font-weight: 600;">{st.session_state.get('user_phone', '用户')}</div>
                <div style="color: #10B981; font-size: 10px;">钻石会员 · 算力无限</div>
            </div>
            <div style="width: 32px; height: 32px; background: #E0E7FF; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #1E3A8A; font-weight: bold; font-size: 12px;">
                ID
            </div>
        </div>
    </div>
    <div style="height: 40px;"></div>
    """, unsafe_allow_html=True)

    # --- 3. [锁定] 侧边栏：业务指挥中心 ---
    with st.sidebar:
        # A. 品牌区
        st.markdown("""
        <div style="padding: 10px 0 25px 5px;">
            <div style="background: #1E3A8A; color: white; width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; float: left; margin-right: 12px; font-weight: 900; font-size: 20px;">V</div>
            <div style="float: left;">
                <div style="color: #1E3A8A; font-weight: 800; font-size: 18px; line-height: 1.2;">爆款工厂</div>
                <div style="color: #94A3B8; font-size: 11px; letter-spacing: 1px;">PRODUCTION PRO</div>
            </div>
            <div style="clear: both;"></div>
        </div>
        """, unsafe_allow_html=True)

        # B. 核心业务目录
        st.markdown("<p style='color: #94A3B8; font-size: 11px; font-weight: 600; margin-top:10px;'>PRODUCTION / 生产链路</p>", unsafe_allow_html=True)
        menu = st.radio(
            "业务导航",
            ["首页控制台", "DeepSeek 改文", "小说短剧拉新", "动漫全链路制作", "会员个人中心", "后台管理"],
            label_visibility="collapsed"
        )

        # C. 底部算力监控
        st.write("\n" * 2)
        st.markdown("""
        <div style="background: #F8FAFC; border-radius: 10px; padding: 12px; border: 1px solid #F1F5F9; margin-bottom: 20px;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <span style="color: #64748B; font-size: 11px;">算力负载</span>
                <span style="color: #10B981; font-size: 11px;">1.2ms</span>
            </div>
            <div style="width: 100%; background: #E2E8F0; height: 3px; border-radius: 2px; margin-top: 8px;">
                <div style="width: 25%; background: #1E3A8A; height: 3px; border-radius: 2px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("退出系统", use_container_width=True):
            del st.session_state['user_phone']
            st.rerun()

    # --- 4. 页面路由分发 ---
    if menu == "首页控制台":
        st.subheader("🚀 实时创作指挥大盘")
        # 这里放置首页指标
    elif menu == "会员个人中心":
        show_member_center()
    elif menu == "后台管理":
        show_admin_panel()
    else:
        st.info(f"正在载入 {menu} 核心模块...")

# --- 5. 功能模块组件化设计 ---

def show_member_center():
    st.markdown("### 👤 会员个人中心")
    col1, col2 = st.columns([1, 2])
    with col1:
        with st.container(border=True):
            st.write("📷 **账号头像**")
            st.image("https://via.placeholder.com/150", width=100)
            st.button("修改资料")
    with col2:
        with st.container(border=True):
            st.write("💳 **订阅状态**")
            st.success("旗舰版会员（永久有效）")
            st.write("已节省算力费用：¥12,400")

def show_admin_panel():
    st.markdown("### ⚙️ 管理员后台")
    t1, t2, t3 = st.tabs(["用户管理", "算力监控", "分销统计"])
    with t1:
        st.table([{"ID": 1, "手机号": "13800138000", "等级": "管理员"}, {"ID": 2, "手机号": "13911112222", "等级": "普通用户"}])

if __name__ == "__main__":
    main()
