# views/poster.py
import streamlit as st

def view_poster():
    st.markdown("## 🎨 智能海报生成")
    st.caption("无需设计基础，3步生成专业级小红书/抖音封面。")
    
    # Requirement 8: 流程化
    step = st.radio("流程", ["1. 输入内容", "2. 选择风格", "3. 生成结果"], horizontal=True, label_visibility="collapsed")
    
    col_l, col_r = st.columns([1, 1.5])
    
    with col_l:
        with st.container(border=True):
            st.markdown("#### 🛠️ 配置参数")
            main_text = st.text_input("主标题", placeholder="例如：3天精通Python")
            sub_text = st.text_input("副标题", placeholder="新手必看保姆级教程")
            style = st.selectbox("设计风格", ["极简风 (Notion)", "高饱和 (多巴胺)", "商务风 (深蓝金)", "二次元 (插画)"])
            
            if st.button("✨ 立即生成海报", type="primary", use_container_width=True):
                st.session_state['poster_generating'] = True
    
    with col_r:
        with st.container(border=True):
            st.markdown("#### 🖼️ 预览画布")
            if st.session_state.get('poster_generating'):
                with st.spinner("正在排版渲染中..."):
                    import time; time.sleep(1.5)
                    # 模拟生成图片
                    st.image("https://via.placeholder.com/600x800.png?text=AI+Poster+Generated", caption=f"风格：{style}")
                    st.success("生成完毕！右键另存为即可。")
                    del st.session_state['poster_generating']
            else:
                st.info("👈 请在左侧配置内容并点击生成")
                st.markdown("""
                <div style="height:300px; background:#f1f5f9; border-radius:8px; display:flex; align-items:center; justify-content:center; color:#94a3b8;">
                    此处将显示生成的海报预览
                </div>
                """, unsafe_allow_html=True)
