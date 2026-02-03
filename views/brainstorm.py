# views/brainstorm.py
import streamlit as st
from utils import render_copy_btn

def view_brainstorm():
    st.markdown("## 💡 爆款选题挖掘")
    st.caption("输入赛道或关键词，AI 自动挖掘全网最热选题方向。")
    
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            topic = st.text_input("输入赛道/关键词", placeholder="例如：美妆、职场、AI工具")
        with col2:
            st.markdown("<div style='height: 28px'></div>", unsafe_allow_html=True)
            btn = st.button("开始挖掘", type="primary", use_container_width=True)
            
    if btn and topic:
        with st.spinner(f"正在分析【{topic}】赛道的大盘数据..."):
            import time; time.sleep(1)
            st.success("挖掘成功！为您推荐以下 3 个爆款方向：")
            
            c1, c2, c3 = st.columns(3)
            data = [
                ("🔥 痛点反差类", "小白如何3天精通...", "利用用户急于求成的心态，结合强烈的反差数据。"),
                ("📚 干货盘点类", "2026年必用的10个...", "高收藏价值，利于长尾流量获取。"),
                ("⚡ 认知颠覆类", "别再....，其实...", "打破固有认知，引发评论区激烈讨论。")
            ]
            
            for i, (title, ex, desc) in enumerate(data):
                with [c1, c2, c3][i]:
                    with st.container(border=True):
                        st.markdown(f"#### {title}")
                        st.markdown(f"**示例标题：**\n{ex} {topic}")
                        st.caption(desc)
                        render_copy_btn(f"{ex} {topic}", f"topic_{i}")
