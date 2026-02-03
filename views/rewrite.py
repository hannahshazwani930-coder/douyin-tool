# views/rewrite.py
import streamlit as st
import time
import requests
import json
from concurrent.futures import ThreadPoolExecutor
from utils import render_copy_btn, render_page_banner
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

# --- DeepSeek 调用函数 ---
def call_deepseek_rewrite(content, prompt_type="standard"):
    """
    调用 DeepSeek API 进行文案改写
    prompt_type: standard (标准去重) / creative (创意爆款)
    """
    if not DEEPSEEK_API_KEY or "sk-" not in DEEPSEEK_API_KEY:
        return "❌ 错误：请在 config.py 中配置正确的 DEEPSEEK_API_KEY"

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 定义提示词
    system_prompt = "你是一个拥有10年经验的爆款文案专家。请对用户提供的文案进行深度改写。要求：1.保留核心意思但重构表达；2.语言更具网感、情绪价值；3.进行全网去重处理；4.输出结果不要包含'好的'、'改写如下'等废话，直接输出文案内容。"
    
    if prompt_type == "creative":
        system_prompt += " 风格要求：幽默、反转、多巴胺情绪，适合抖音/小红书调性。"
        
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content}
        ],
        "temperature": 1.3, # 提高创造性
        "stream": False
    }

    try:
        response = requests.post(f"{DEEPSEEK_BASE_URL}/chat/completions", headers=headers, json=data, timeout=60)
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"❌ API 请求失败: {response.status_code} - {response.text}"
    except Exception as e:
        return f"❌ 网络错误: {str(e)}"

# --- 视图主逻辑 ---
def view_rewrite():
    render_page_banner("文案改写 Pro", "DeepSeek 深度赋能，支持单条精修与 5 路矩阵并行生成。")
    
    # 初始化 session_state
    if 'rewrite_single_res' not in st.session_state:
        st.session_state.rewrite_single_res = ""
    if 'rewrite_batch_res' not in st.session_state:
        st.session_state.rewrite_batch_res = [""] * 5

    tab_single, tab_batch = st.tabs(["⚡ 单条精修模式", "🚀 5路并行模式 (矩阵)"])
    
    # === 单条模式 ===
    with tab_single:
        with st.container(border=True):
            content = st.text_area("输入文案", height=150, placeholder="粘贴需要改写的文案...")
            
            # 增加风格选择
            style_mode = st.radio("改写风格", ["标准去重 (稳重)", "爆款创意 (高热度)"], horizontal=True)
            p_type = "standard" if style_mode == "标准去重 (稳重)" else "creative"

            if st.button("开始改写 (单条)", type="primary", use_container_width=True):
                if content:
                    with st.status("DeepSeek 正在思考中...", expanded=True) as status:
                        st.write("🔌 连接 API 接口...")
                        # 真实调用
                        res = call_deepseek_rewrite(content, p_type)
                        
                        if "❌" not in res:
                            st.write("✨ 生成完毕！")
                            status.update(label="✅ 改写成功", state="complete", expanded=False)
                        else:
                            status.update(label="⛔ 出错了", state="error", expanded=True)
                    
                    st.session_state.rewrite_single_res = res
                else:
                    st.warning("请先输入文案")
            
            # 显示结果
            if st.session_state.rewrite_single_res:
                st.text_area("改写结果", value=st.session_state.rewrite_single_res, height=250)
                render_copy_btn(st.session_state.rewrite_single_res, "single_copy_btn")

    # === 并行模式 (真·多线程) ===
    with tab_batch:
        st.info("💡 矩阵模式：系统将开启 5 个并发线程，同时请求 DeepSeek API，互不干扰，效率倍增。")
        
        inputs = []
        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                st.markdown(f"**任务 {i+1}**")
                val = st.text_area(f"文案 {i+1}", height=120, key=f"batch_in_{i}", label_visibility="collapsed")
                inputs.append(val)
        
        if st.button("🚀 立即并行改写", type="primary", use_container_width=True):
            valid_tasks = [(i, text) for i, text in enumerate(inputs) if text.strip()]
            
            if valid_tasks:
                status_text = st.empty()
                status_text.info(f"正在启动 {len(valid_tasks)} 个 AI 线程并行处理...")
                
                # 使用线程池并发请求
                with ThreadPoolExecutor(max_workers=5) as executor:
                    # 提交所有任务
                    future_to_index = {
                        executor.submit(call_deepseek_rewrite, text, "standard"): i 
                        for i, text in valid_tasks
                    }
                    
                    # 获取结果
                    for future in future_to_index:
                        idx = future_to_index[future]
                        try:
                            result = future.result()
                            st.session_state.rewrite_batch_res[idx] = result
                        except Exception as exc:
                            st.session_state.rewrite_batch_res[idx] = f"❌ 执行出错: {exc}"
                
                status_text.success("✅ 所有任务处理完毕！")
            else:
                st.warning("请至少输入一条文案")

        # 展示 5 路结果
        if any(st.session_state.rewrite_batch_res):
            st.markdown("---")
            st.markdown("#### 🎯 矩阵生成结果")
            res_cols = st.columns(5)
            for i, col in enumerate(res_cols):
                with col:
                    if st.session_state.rewrite_batch_res[i]:
                        # 判断是否出错，显示不同颜色
                        if "❌" in st.session_state.rewrite_batch_res[i]:
                             st.error(f"任务 {i+1} 失败")
                        else:
                             st.success(f"任务 {i+1} 完成")
                        
                        st.text_area(f"结果 {i+1}", value=st.session_state.rewrite_batch_res[i], height=200)
                        render_copy_btn(st.session_state.rewrite_batch_res[i], f"batch_res_{i}")
                    else:
                        st.caption(f"任务 {i+1} 空闲")
