import streamlit as st
from views.auth import view_auth

st.set_page_config(page_title="爆款工厂PRO", page_icon="🎯", layout="wide")

def main():
    if 'user_phone' not in st.session_state:
        st.markdown("<style>[data-testid='stSidebar'] { display:none; }</style>", unsafe_allow_html=True)
        view_auth()
        return

    with st.sidebar:
        # A. 品牌标识区 (锁定)
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

        # B. 指挥中心功能目录 (SaaS 级重编)
        
        # 模块 1：内容实验室 (核心文本加工)
        st.markdown("<p style='color: #94A3B8; font-size: 11px; font-weight: 600; margin-top:20px;'>CONTENT LAB / 内容实验</p>", unsafe_allow_html=True)
        st.markdown("""
        <div style="padding-left: 10px;">
            <div style="color: #475569; font-size: 14px; margin-bottom: 12px; cursor: pointer;">🧠 DeepSeek 深度改文</div>
            <div style="color: #475569; font-size: 14px; margin-bottom: 12px; cursor: pointer;">🖋️ 小说/短剧拉新策略</div>
            <div style="color: #475569; font-size: 14px; margin-bottom: 12px; cursor: pointer;">🏷️ 剧本/小说别名矩阵</div>
        </div>
        """, unsafe_allow_html=True)

        # 模块 2：视觉引擎 (生图与海报)
        st.markdown("<p style='color: #94A3B8; font-size: 11px; font-weight: 600; margin-top:20px;'>VISUAL ENGINE / 视觉引擎</p>", unsafe_allow_html=True)
        st.markdown("""
        <div style="padding-left: 10px;">
            <div style="color: #475569; font-size: 14px; margin-bottom: 12px; cursor: pointer;">🖼️ 小题大作 · 封面海报</div>
            <div style="color: #475569; font-size: 14px; margin-bottom: 12px; cursor: pointer;">🎨 智能生图与改名</div>
        </div>
        """, unsafe_allow_html=True)

        # 模块 3：动漫全链路 (重度创作流)
        st.markdown("<p style='color: #94A3B8; font-size: 11px; font-weight: 600; margin-top:20px;'>ANIMATION FLOW / 动漫创作</p>", unsafe_allow_html=True)
        st.markdown("""
        <div style="padding-left: 10px;">
            <div style="color: #475569; font-size: 14px; margin-bottom: 12px; cursor: pointer;">🤝 御灵AI · 人机协同</div>
            <div style="color: #475569; font-size: 14px; margin-bottom: 12px; cursor: pointer;">🎬 小说转剧本/分镜</div>
            <div style="color: #475569; font-size: 14px; margin-bottom: 12px; cursor: pointer;">🎥 AI 动漫全流程制作</div>
        </div>
        """, unsafe_allow_html=True)

        # C. 底部系统状态
        st.write("\n" * 2)
        st.markdown("""
        <div style="background: #F8FAFC; border-radius: 10px; padding: 12px; border: 1px solid #F1F5F9;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <span style="color: #64748B; font-size: 11px;">算力负载</span>
                <span style="color: #10B981; font-size: 11px;">极速</span>
            </div>
            <div style="width: 100%; background: #E2E8F0; height: 3px; border-radius: 2px; margin-top: 8px;">
                <div style="width: 35%; background: #1E3A8A; height: 3px; border-radius: 2px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.write("\n" * 2)
        if st.button("退出系统", use_container_width=True):
            del st.session_state['user_phone']
            st.rerun()

if __name__ == "__main__":
    main()
