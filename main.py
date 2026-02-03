# main.py 或相关入口文件
import streamlit as st

def styled_sidebar():
    # --- 1. 侧边栏专属大师级 CSS ---
    st.markdown("""
<style>
    /* 1. 彻底改造侧边栏背景与边框 */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #F1F5F9 !important;
        box-shadow: none !important;
    }

    /* 2. 侧边栏导航项 (Navigation) 样式归一化 */
    [data-testid="stSidebarNav"] {
        padding-top: 20px !important;
        background-color: transparent !important;
    }

    /* 3. 菜单文字样式：14px, 专业深灰蓝 */
    [data-testid="stSidebarNav"] span {
        font-size: 14px !important;
        color: #475569 !important;
        font-weight: 500 !important;
    }

    /* 4. 悬浮与激活态：淡蓝色呼吸感 */
    [data-testid="stSidebarNav"] a:hover {
        background-color: #F8FAFC !important;
        border-radius: 8px !important;
    }
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background-color: #F1F5F9 !important;
        border-radius: 8px !important;
    }
    [data-testid="stSidebarNav"] a[aria-current="page"] span {
        color: #1E3A8A !important; /* 激活态使用品牌深蓝 */
        font-weight: 700 !important;
    }

    /* 5. 隐藏侧边栏顶部的默认装饰线 */
    [data-testid="stSidebarNav"]::before {
        content: "爆款工厂 PRO";
        display: block;
        padding: 20px 0 10px 20px;
        font-size: 18px;
        font-weight: 800;
        color: #1E3A8A;
        letter-spacing: -0.5px;
    }

    /* 侧边栏底部信息美化 */
    .sidebar-footer {
        position: fixed;
        bottom: 20px;
        left: 20px;
        font-size: 12px;
        color: #94A3B8;
    }
</style>
""", unsafe_allow_html=True)

    # --- 2. 侧边栏内容补充 ---
    with st.sidebar:
        # 可以在这里增加一些辅助功能，比如“切换版本”或“算力状态”
        st.write("\n" * 2)
        st.caption("系统状态")
        st.success("算力引擎：极速模式")
        
        # 底部常驻用户信息（样式由 CSS 控制）
        st.markdown(f"""
            <div class="sidebar-footer">
                <div style="width: 200px; border-top: 1px solid #F1F5F9; pt-15px;">
                    当前用户: {st.session_state.get('user_phone', '访客')}
                </div>
            </div>
        """, unsafe_allow_html=True)

# 在主逻辑中调用
# styled_sidebar()
