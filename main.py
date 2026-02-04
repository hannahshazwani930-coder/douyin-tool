# main.py
import streamlit as st
from views.auth import view_auth

# 1. 全局配置锁定
st.set_page_config(page_title="爆款工厂PRO", page_icon="🎯", layout="wide", initial_sidebar_state="expanded")

def main():
    # --- 登录拦截判定 ---
    if 'user_phone' not in st.session_state:
        st.markdown("<style>[data-testid='stSidebar'] { display:none; }</style>", unsafe_allow_html=True)
        view_auth()
        return

    user_phone = st.session_state.get('user_phone')

    # --- 2. [锁定] 大厂级全局 Header ---
    st.markdown(f"""
    <div style="position: fixed; top: 0; left: 0; right: 0; height: 50px; background: white; border-bottom: 1px solid #F1F5F9; z-index: 99; display: flex; align-items: center; justify-content: flex-end; padding: 0 40px;">
        <div style="display: flex; align-items: center; gap: 20px;">
            <div style="text-align: right;">
                <div style="color: #1E3A8A; font-size: 13px; font-weight: 600;">{user_phone}</div>
                <div style="color: #10B981; font-size: 10px;">PRO 旗舰版 · 已授权</div>
            </div>
            <div style="width: 32px; height: 32px; background: #E0E7FF; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #1E3A8A; font-weight: bold; font-size: 12px;">ID</div>
        </div>
    </div>
    <div style="height: 40px;"></div>
    """, unsafe_allow_html=True)

    # --- 3. 侧边栏：业务指挥中心 ---
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

        # B. 功能目录设计
        st.markdown("<p style='color: #94A3B8; font-size: 11px; font-weight: 600;'>PRODUCTION / 生产链路</p>", unsafe_allow_html=True)
        
        # 基础功能列表
        menu_options = ["首页控制台", "文案创作", "别名创作", "AI动漫创作", "个人中心"]
        
        # 【关键：总管理员权限检查】
        if user_phone == "13800138000":
            menu_options.append("后台管理")

        menu = st.radio("业务导航", menu_options, label_visibility="collapsed")

        # C. 算力监控 (锁定)
        st.write("\n" * 2)
        st.markdown("""
        <div style="background: #F8FAFC; border-radius: 10px; padding: 12px; border: 1px solid #F1F5F9; margin-bottom: 20px;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <span style="color: #64748B; font-size: 11px;">算力负载</span>
                <span style="color: #10B981; font-size: 11px;">极速</span>
            </div>
            <div style="width: 100%; background: #E2E8F0; height: 3px; border-radius: 2px; margin-top: 8px;">
                <div style="width: 28%; background: #1E3A8A; height: 3px; border-radius: 2px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # D. 技术合作：TG信息强制注入
        st.markdown("""
        <div style="padding: 10px; border-radius: 8px; background: #F0F4FF; border: 1px dashed #3B82F6; margin-bottom: 20px;">
            <p style="color: #1E3A8A; font-size: 11px; margin: 0; font-weight: bold;">🤝 技术合作</p>
            <p style="color: #3B82F6; font-size: 13px; margin: 4px 0 0 0; font-family: monospace;">TG: 777188</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("退出系统", use_container_width=True):
            del st.session_state['user_phone']
            st.rerun()

    # --- 4. 路由渲染 ---
    if menu == "首页控制台":
        st.subheader("🚀 实时创作指挥大盘")
        # 首页大盘逻辑...
    elif menu == "个人中心":
        show_user_profile()
    elif menu == "后台管理" and user_phone == "13800138000":
        show_admin_panel()
    else:
        st.info(f"正在调取 {menu} 核心引擎...")

def show_user_profile():
    st.markdown("### 👤 个人中心")
    with st.container(border=True):
        st.write("会员等级：钻石会员")
        st.write(f"当前账号：{st.session_state.get('user_phone')}")

def show_admin_panel():
    st.markdown("### ⚙️ 总管理员后台")
    st.warning("当前处于最高权限模式")
    # 管理员数据统计逻辑...

if __name__ == "__main__":
    main()
