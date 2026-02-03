# views/rewrite.py
import streamlit as st
from utils import render_copy_btn

def view_rewrite():
    st.markdown("## 📝 爆款文案改写")
    st.caption("基于深度学习模型，一键生成高质量、去重后的爆款文案。")
    
    # Requirement 6: Tab 分流
    tab_single, tab_batch = st.tabs(["⚡ 单条极速模式", "🚀 5路并行模式"])
    
    with tab_single:
        with st.container(border=True):
            content = st.text_area("输入原始文案", height=150, placeholder="请粘贴需要改写的文案...")
            if st.button("开始改写 (单条)", type="primary", use_container_width=True):
                if content:
                    with st.spinner("AI 正在深度思考中..."):
                        # 模拟生成
                        import time; time.sleep(1)
                        res = f"【改写结果】\n{content}\n(此处为模拟改写后的文案，实际请接入API)"
                        st.success("改写完成！")
                        st.text_area("结果", value=res, height=150)
                        render_copy_btn(res, "single_copy")
                else:
                    st.warning("请先输入文案")

    with tab_batch:
        st.info("💡 并行模式可同时生成 5 个不同风格的改写版本，供您择优使用。")
        with st.container(border=True):
            content_batch = st.text_area("输入原始文案 (并行)", height=150, placeholder="粘贴文案，AI将为您生成5个版本...")
            if st.button("🚀 启动5路并行改写", type="primary", use_container_width=True):
                if content_batch:
                    with st.spinner("5个AI引擎正在同时工作..."):
                        import time; time.sleep(1.5)
                        cols = st.columns(5)
                        for i, col in enumerate(cols):
                            with col:
                                res = f"版本 {i+1}:\n{content_batch[:10]}... (风格{i+1})"
                                st.text_area(f"风格 {i+1}", value=res, height=200)
                                render_copy_btn(res, f"batch_copy_{i}")
                else:
                    st.warning("请先输入文案")
