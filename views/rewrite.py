# views/rewrite.py
import streamlit as st
from utils import render_copy_btn, render_page_banner

def view_rewrite():
    render_page_banner("文案改写 Pro", "支持单条精修与批量矩阵生成，深度学习爆款逻辑，全网去重。")
    
    tab_single, tab_batch = st.tabs(["⚡ 单条精修模式", "🚀 5路并行模式 (矩阵)"])
    
    with tab_single:
        with st.container(border=True):
            content = st.text_area("输入文案", height=150, placeholder="粘贴需要改写的文案...")
            if st.button("开始改写 (单条)", type="primary", use_container_width=True):
                if content:
                    with st.spinner("AI 正在重构文案逻辑..."):
                        import time; time.sleep(1)
                        res = f"【改写结果】\n{content}\n(此处为模拟结果，请接入大模型API)"
                        st.success("改写完成！")
                        st.text_area("结果", value=res, height=150)
                        render_copy_btn(res, "single_copy")
                else:
                    st.warning("请输入文案")

    with tab_batch:
        st.info("💡 在下方同时输入 5 条不同的文案，AI 将并行处理，互不干扰。")
        
        # 创建5个输入框
        inputs = []
        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                st.markdown(f"**文案 {i+1}**")
                val = st.text_area(f"输入 {i+1}", height=150, key=f"in_{i}", label_visibility="collapsed")
                inputs.append(val)
        
        if st.button("🚀 立即并行改写", type="primary", use_container_width=True):
            if any(inputs):
                with st.spinner("正在启动 5 个 AI 线程并行处理..."):
                    import time; time.sleep(2)
                    res_cols = st.columns(5)
                    for i, col in enumerate(res_cols):
                        with col:
                            if inputs[i]:
                                res = f"改写版 {i+1}:\n{inputs[i][:10]}... (已去重)"
                                st.success(f"任务 {i+1} 完成")
                                st.text_area(f"结果 {i+1}", value=res, height=150)
                                render_copy_btn(res, f"batch_res_{i}")
                            else:
                                st.caption("无输入")
            else:
                st.warning("请至少输入一条文案")
