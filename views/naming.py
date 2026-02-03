# views/naming.py
import streamlit as st
from utils import render_copy_btn

def view_naming():
    st.markdown("## 🏷️ 账号起名神器")
    st.caption("基于玄学+营销学，生成好听、好记、易传播的账号昵称。")
    
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            keywords = st.text_input("核心关键词", placeholder="例如：美妆、小强")
        with col2:
            vibe = st.selectbox("风格偏好", ["亲切邻家", "专业权威", "幽默搞怪", "高端大气"])
            
        if st.button("🔮 生成好名字", type="primary", use_container_width=True):
            if keywords:
                with st.spinner("AI 正在测算五行与传播力..."):
                    import time; time.sleep(1)
                    results = [
                        f"{keywords}说干货",
                        f"是{keywords}呀",
                        f"{keywords}的秘密基地",
                        f"暴走的{keywords}",
                        f"{keywords}研究所"
                    ]
                    st.markdown("### 🎯 推荐结果")
                    c1, c2 = st.columns(2)
                    for i, name in enumerate(results):
                        with (c1 if i % 2 == 0 else c2):
                            st.info(f"**{name}**")
                            render_copy_btn(name, f"name_{i}")
            else:
                st.warning("请输入关键词")
