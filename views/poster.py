import streamlit as st
import streamlit.components.v1 as components

def view_poster():
    st.markdown("### 🎨 海报生成 (专业版)")
    st.info("💡 因算力需求较大，海报生成功能已迁移至独立 GPU 集群。")
    
    st.markdown("""
    <div style="background:linear-gradient(135deg, #4f46e5, #7c3aed); padding:30px; border-radius:16px; color:white; display:flex; justify-content:space-between; align-items:center;">
        <div>
            <h2 style="margin:0; color:white;">前往「小提大作」工作站</h2>
            <p style="opacity:0.9; margin-top:5px;">请复制下方的专用邀请码，可获得额外的算力点数。</p>
        </div>
        <div style="font-size:40px;">🚀</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 第一步：复制邀请码")
        st.code("5yzMbpxn", language="text")
    with c2:
        st.markdown("#### 第二步：点击跳转")
        st.link_button("👉 前往海报生成工作站", "https://aixtdz.com/", type="primary", use_container_width=True)