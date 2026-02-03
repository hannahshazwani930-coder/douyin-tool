# views/rewrite.py
import streamlit as st
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from utils import render_copy_btn
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

# --- 局部 CSS：解锁宽幅 & 编辑器样式 ---
def load_editor_css():
    st.markdown("""
    <style>
        /* 1. 强制解锁页面最大宽度，打造沉浸式工作台 */
        div.block-container {
            max-width: 98% !important;
            padding-top: 2rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }

        /* 2. 编辑器风格的文本域 */
        .stTextArea textarea {
            font-size: 16px;
            line-height: 1.6;
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 15px;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);
            transition: all 0.3s ease;
        }
        .stTextArea textarea:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        /* 右侧结果区背景微调，以此区分输入和输出 */
        div[data-testid="column"]:nth-child(2) .stTextArea textarea {
            background-color: #f8fafc; /* 极淡的灰蓝色 */
            border-color: #cbd5e1;
        }

        /* 3. 顶部 Header 美化 */
        .rewrite-header {
            display: flex; align-items: center; justify-content: space-between;
            margin-bottom: 20px; padding-bottom: 20px;
            border-bottom: 1px solid #f1f5f9;
        }
        .rewrite-title { font-size: 24px; font-weight: 800; color: #0f172a; display: flex; align-items: center; gap: 10px; }
        .rewrite-tag { background: #eff6ff; color: #2563eb; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }

        /* 4. 风格选择器美化 */
        div[role="radiogroup"] { background: white; padding: 5px; border-radius: 10px; border: 1px solid #e2e8f0; display: inline-flex; }
        
        /* 5. 按钮增强 */
        .big-action-btn button {
            width: 100%; height: 50px; font-size: 16px !important;
            background: linear-gradient(90deg, #2563eb, #3b82f6) !important;
            color: white !important; border: none !important;
            box-shadow: 0 10px 20px -5px rgba(37, 99, 235, 0.4) !important;
        }
        .big-action-btn button:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 30px -5px rgba(37, 99, 235, 0.5) !important;
        }
    </style>
    """, unsafe_allow_html=True)

# --- DeepSeek 核心调用 ---
def call_deepseek_rewrite(content, style_prompt):
    """真实调用 DeepSeek API"""
    if not DEEPSEEK_API_KEY or "sk-" not in DEEPSEEK_API_KEY:
        return "❌ 配置错误：请在 config.py 中填入正确的 DEEPSEEK_API_KEY"

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 构建专业 Prompt
    system_prompt = f"""
    你是由抖音爆款工场开发的顶级文案专家。请对用户输入的文案进行【{style_prompt}】方向的改写。
    核心要求：
    1. 深度去重：改变句式结构，但保留核心逻辑。
    2. 情绪价值：语言要更具网感、穿透力，引发用户共鸣。
    3. 格式优化：适当分段，使用emoji增加视觉跳跃感。
    4. 直接输出：不要包含“好的”、“改写如下”等前缀。
    """
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content}
        ],
        "temperature": 1.3, # 高创造性
        "stream": False
    }

    try:
        response = requests.post(f"{DEEPSEEK_BASE_URL}/chat/completions", headers=headers, json=data, timeout=60)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"❌ API 报错: {response.status_code} - {response.text}"
    except Exception as e:
        return f"❌ 网络请求超时或错误: {str(e)}"

# --- 主视图 ---
def view_rewrite():
    # 1. 注入宽幅 CSS
    load_editor_css()
    
    # 2. 顶部导航栏
    st.markdown("""
    <div class="rewrite-header">
        <div class="rewrite-title">
            <span>📝 文案改写 Pro</span>
            <span class="rewrite-tag">DeepSeek V3 驱动</span>
        </div>
        <div style="color: #64748b; font-size: 14px;">
            🚀 你的全能 AI 创作助手
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 3. 初始化状态
    if 'rw_single_input' not in st.session_state: st.session_state.rw_single_input = ""
    if 'rw_single_res' not in st.session_state: st.session_state.rw_single_res = ""
    if 'rw_batch_res' not in st.session_state: st.session_state.rw_batch_res = [""] * 5

    # 4. 模式切换 Tab
    mode = st.radio("工作模式", ["⚡ 单条精修 (双屏对照)", "🚀 5路并行 (矩阵生成)"], horizontal=True, label_visibility="collapsed")
    
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    # ==========================================
    # 模式 A: 单条精修 (左右分栏，超级编辑器体验)
    # ==========================================
    if "单条" in mode:
        # 布局：左侧输入(45%) - 中间操作(10%) - 右侧输出(45%)
        c_input, c_btn, c_output = st.columns([4, 1, 4], gap="medium")
        
        with c_input:
            st.markdown("#### 📄 原始内容")
            input_text = st.text_area("Source", height=500, placeholder="在此粘贴文案，支持长文本...", key="single_in_area", label_visibility="collapsed")
        
        with c_btn:
            # 垂直居中的操作区
            st.markdown("<div style='height: 150px;'></div>", unsafe_allow_html=True)
            
            st.markdown("##### 🎨 风格")
            style = st.selectbox("Style", ["标准去重", "爆款悬疑", "情感共鸣", "硬核干货", "幽默反转"], label_visibility="collapsed")
            
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            
            # 大按钮
            st.markdown('<div class="big-action-btn">', unsafe_allow_html=True)
            if st.button("开始\n改写", use_container_width=True):
                if input_text:
                    st.session_state.rw_single_res = "" # 清空旧结果
                    with c_output:
                        with st.status("DeepSeek 深度思考中...", expanded=True) as status:
                            st.write("🧠 语义解构...")
                            time.sleep(0.5)
                            st.write("🌪️ 风格重塑...")
                            res = call_deepseek_rewrite(input_text, style)
                            status.update(label="✅ 完成", state="complete", expanded=False)
                        st.session_state.rw_single_res = res
                else:
                    st.toast("⚠️ 请先输入文案内容")
            st.markdown('</div>', unsafe_allow_html=True)

        with c_output:
            st.markdown("#### ✨ 改写结果")
            if st.session_state.rw_single_res:
                st.text_area("Result", value=st.session_state.rw_single_res, height=500, key="single_out_area", label_visibility="collapsed")
                # 底部工具栏
                col_copy, col_space = st.columns([1, 3])
                with col_copy:
                    render_copy_btn(st.session_state.rw_single_res, "copy_single_final")
            else:
                st.markdown("""
                <div style="height:500px; background:#f8fafc; border:2px dashed #e2e8f0; border-radius:12px; display:flex; align-items:center; justify-content:center; color:#94a3b8; flex-direction:column;">
                    <div style="font-size:40px; margin-bottom:10px;">🤖</div>
                    <div>AI 改写结果将显示在这里</div>
                </div>
                """, unsafe_allow_html=True)

    # ==========================================
    # 模式 B: 5路并行 (矩阵生成，宽幅平铺)
    # ==========================================
    else:
        st.info("💡 矩阵模式：5 个 AI 线程将同时工作，适合批量生产短视频脚本、小红书文案。")
        
        # 顶部操作栏
        c_opt_1, c_opt_2 = st.columns([4, 1])
        with c_opt_1:
            pass 
        with c_opt_2:
            st.markdown('<div class="big-action-btn">', unsafe_allow_html=True)
            start_batch = st.button("🚀 并行启动", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # 5列布局
        cols = st.columns(5, gap="small")
        inputs = []
        
        # 渲染输入区
        for i, col in enumerate(cols):
            with col:
                st.markdown(f"**任务通道 {i+1}**")
                val = st.text_area(f"文案 {i+1}", height=200, key=f"b_in_{i}", placeholder="输入文案...", label_visibility="collapsed")
                inputs.append(val)
        
        # 执行逻辑
        if start_batch:
            valid_tasks = [(i, text) for i, text in enumerate(inputs) if text.strip()]
            if valid_tasks:
                status_bar = st.status(f"正在并行处理 {len(valid_tasks)} 个任务...", expanded=True)
                
                with ThreadPoolExecutor(max_workers=5) as executor:
                    future_to_idx = {
                        executor.submit(call_deepseek_rewrite, text, "标准去重"): i 
                        for i, text in valid_tasks
                    }
                    
                    completed = 0
                    for future in future_to_idx:
                        idx = future_to_idx[future]
                        try:
                            res = future.result()
                            st.session_state.rw_batch_res[idx] = res
                            completed += 1
                        except Exception as e:
                            st.session_state.rw_batch_res[idx] = f"❌ Error: {str(e)}"
                
                status_bar.update(label="✅ 所有通道处理完毕", state="complete", expanded=False)
            else:
                st.warning("请至少在任意一个通道输入文案")

        st.markdown("---")
        
        # 渲染结果区 (对应上面的5列)
        res_cols = st.columns(5, gap="small")
        for i, col in enumerate(res_cols):
            with col:
                if st.session_state.rw_batch_res[i]:
                    if "❌" in st.session_state.rw_batch_res[i]:
                        st.error("生成失败")
                    else:
                        st.success("✅ 完成")
                    
                    st.text_area(f"结果 {i+1}", value=st.session_state.rw_batch_res[i], height=300, label_visibility="collapsed")
                    render_copy_btn(st.session_state.rw_batch_res[i], f"copy_b_{i}")
                else:
                    st.markdown("""
                    <div style="height:300px; background:#f1f5f9; border-radius:8px; border:1px dashed #cbd5e1;"></div>
                    """, unsafe_allow_html=True)
