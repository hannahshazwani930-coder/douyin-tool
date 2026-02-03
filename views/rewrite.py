# views/rewrite.py
import streamlit as st
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from utils import render_copy_btn
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

# --- 🎨 注入灵魂 CSS (SaaS 3.0 风格) ---
def load_immersive_css():
    st.markdown("""
    <style>
        /* 1. 布局重置：打破容器，释放空间 */
        div.block-container {
            max-width: 100% !important;
            padding-top: 0 !important; /* 顶满 */
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
        
        /* 2. 通栏极光顶栏 (Hero Header) */
        .immersive-header {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #3b82f6 100%);
            padding: 60px 40px 80px 40px; /* 底部留出空间给 Tab */
            color: white;
            text-align: center;
            margin-bottom: -40px; /* 让下面的卡片往上叠 */
            clip-path: polygon(0 0, 100% 0, 100% 85%, 0 100%); /* 底部斜切造型 */
        }
        .header-title { 
            font-size: 36px; font-weight: 800; letter-spacing: -1px; margin-bottom: 10px; 
            text-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }
        .header-sub { 
            font-size: 16px; opacity: 0.9; font-weight: 400; max-width: 600px; margin: 0 auto; line-height: 1.6;
            background: rgba(255,255,255,0.1); padding: 8px 20px; border-radius: 30px; backdrop-filter: blur(5px);
        }

        /* 3. 核心工作区容器 */
        .workspace-container {
            max-width: 1200px; margin: 0 auto; padding: 0 20px;
        }

        /* 4. 魔改 Streamlit Tabs -> 悬浮胶囊 */
        .stTabs { margin-top: -20px; } /* 往上提，叠在 Header 上 */
        
        div[data-baseweb="tab-list"] {
            justify-content: center; gap: 15px; border: none !important; margin-bottom: 30px;
        }
        div[data-baseweb="tab"] {
            background-color: rgba(255,255,255,0.9) !important;
            backdrop-filter: blur(10px);
            border-radius: 12px !important;
            padding: 12px 30px !important;
            border: 1px solid rgba(255,255,255,0.5) !important;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;
            color: #64748b !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        /* 选中状态 */
        div[data-baseweb="tab"][aria-selected="true"] {
            background: #2563eb !important;
            color: white !important;
            transform: translateY(-2px);
            box-shadow: 0 15px 30px rgba(37, 99, 235, 0.4) !important;
        }

        /* 5. 悬浮白卡 (替代原本的 border=True) */
        .glass-card {
            background: white; border-radius: 20px; padding: 30px;
            box-shadow: 0 20px 40px -10px rgba(0,0,0,0.05);
            border: 1px solid #f1f5f9;
        }
        
        /* 6. 输入框极简风 */
        .stTextArea textarea {
            background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px;
            padding: 15px; font-size: 15px; line-height: 1.6; transition: 0.3s;
        }
        .stTextArea textarea:focus {
            background: white; border-color: #3b82f6; box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
        }
        
        /* 7. 按钮特效 */
        .action-btn button {
            background: linear-gradient(90deg, #2563eb, #3b82f6); color: white; border: none;
            height: 45px; border-radius: 8px; font-weight: 600; font-size: 15px;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3); transition: 0.3s;
        }
        .action-btn button:hover {
            transform: translateY(-2px); box-shadow: 0 8px 25px rgba(37, 99, 235, 0.5);
        }
        
        /* 去除 Streamlit 默认顶部空白 */
        .stApp { background-color: #f8fafc; }
    </style>
    """, unsafe_allow_html=True)

# --- DeepSeek 调用逻辑 (保持不变，稳健核心) ---
def call_deepseek_rewrite(content, style_prompt):
    if not DEEPSEEK_API_KEY or "sk-" not in DEEPSEEK_API_KEY:
        return "❌ 配置错误：请在 config.py 中填入正确的 DEEPSEEK_API_KEY"

    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    system_prompt = f"""
    你是由抖音爆款工场开发的顶级文案专家。请对用户输入的文案进行【{style_prompt}】方向的改写。
    核心要求：1.深度去重；2.语言更有网感和穿透力；3.适当使用emoji；4.直接输出结果，不要废话。
    """
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": content}],
        "temperature": 1.3, "stream": False
    }
    try:
        response = requests.post(f"{DEEPSEEK_BASE_URL}/chat/completions", headers=headers, json=data, timeout=60)
        if response.status_code == 200: return response.json()['choices'][0]['message']['content']
        else: return f"❌ API 报错: {response.status_code} - {response.text}"
    except Exception as e: return f"❌ 网络错误: {str(e)}"

# --- 主视图 ---
def view_rewrite():
    load_immersive_css()
    
    # 1. 极光通栏 Header (SaaS 级视觉)
    st.markdown("""
    <div class="immersive-header">
        <div class="header-title">✨ 文案改写 Pro</div>
        <div class="header-sub">DeepSeek V3 深度驱动 · 全网去重 · 爆款逻辑重构</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. 状态管理
    if 'rw_single_res' not in st.session_state: st.session_state.rw_single_res = ""
    if 'rw_batch_res' not in st.session_state: st.session_state.rw_batch_res = [""] * 5

    # 3. 工作区容器 (限制宽度，防止在大屏太散)
    st.markdown('<div class="workspace-container">', unsafe_allow_html=True)
    
    # 4. 胶囊式 Tab 切换 (悬浮在 Header 之上)
    tab_single, tab_batch = st.tabs(["⚡ 单条精修模式", "🚀 5路矩阵模式"])
    
    # === 单条模式 (沉浸式双屏) ===
    with tab_single:
        # 使用自定义 class 代替 st.container(border=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        c_in, c_mid, c_out = st.columns([10, 1, 10])
        
        with c_in:
            st.markdown("##### 📝 原始内容")
            content = st.text_area("in", height=400, placeholder="在此粘贴文案...", label_visibility="collapsed")
            
            # 底部操作栏
            st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
            cc1, cc2 = st.columns([2, 1])
            with cc1:
                style = st.selectbox("风格偏好", ["标准去重", "爆款悬疑", "情感共鸣", "硬核干货", "幽默反转"], label_visibility="collapsed")
            with cc2:
                st.markdown('<div class="action-btn">', unsafe_allow_html=True)
                if st.button("✨ 立即改写", use_container_width=True):
                    if content:
                        with st.spinner("DeepSeek 正在重构..."):
                            st.session_state.rw_single_res = call_deepseek_rewrite(content, style)
                    else:
                        st.toast("⚠️ 内容不能为空")
                st.markdown('</div>', unsafe_allow_html=True)

        # 中间分割线 (视觉引导)
        with c_mid:
            st.markdown("""
            <div style="height:400px; display:flex; align-items:center; justify-content:center; color:#cbd5e1;">
                <span style="font-size:24px;">➔</span>
            </div>
            """, unsafe_allow_html=True)

        with c_out:
            st.markdown("##### 🎯 改写结果")
            if st.session_state.rw_single_res:
                st.text_area("out", value=st.session_state.rw_single_res, height=400, label_visibility="collapsed")
                st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
                render_copy_btn(st.session_state.rw_single_res, "copy_single_new")
            else:
                # 空状态占位符
                st.markdown("""
                <div style="height:400px; background:#f8fafc; border-radius:12px; border:2px dashed #e2e8f0; display:flex; flex-direction:column; align-items:center; justify-content:center; color:#94a3b8;">
                    <div style="font-size:40px; margin-bottom:10px; opacity:0.5;">🤖</div>
                    <div style="font-size:14px;">AI 智能改写结果将展示在此处</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True) # close glass-card

    # === 5路矩阵模式 (宽幅平铺) ===
    with tab_batch:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        # 顶部控制栏
        top_c1, top_c2 = st.columns([4, 1])
        with top_c1:
            st.info("💡 **矩阵效率提升 500%**：系统将开启 5 个并发线程，独立处理 5 条不同的文案。")
        with top_c2:
            st.markdown('<div class="action-btn">', unsafe_allow_html=True)
            run_batch = st.button("🚀 并行启动", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        
        # 5列布局
        cols = st.columns(5, gap="small")
        inputs = []
        
        # 渲染输入
        for i, col in enumerate(cols):
            with col:
                st.markdown(f"<div style='text-align:center; font-weight:700; color:#64748b; margin-bottom:10px;'>通道 {i+1}</div>", unsafe_allow_html=True)
                val = st.text_area(f"in_{i}", height=150, key=f"bi_{i}", placeholder="输入文案...", label_visibility="collapsed")
                inputs.append(val)
        
        st.markdown("---")
        
        # 渲染输出
        res_cols = st.columns(5, gap="small")
        
        # 逻辑处理
        if run_batch:
            valid = [(i, t) for i, t in enumerate(inputs) if t.strip()]
            if valid:
                status = st.status(f"正在并行处理 {len(valid)} 个任务...", expanded=True)
                with ThreadPoolExecutor(max_workers=5) as ex:
                    f_map = {ex.submit(call_deepseek_rewrite, t, "标准去重"): i for i, t in valid}
                    for f in f_map:
                        try:
                            st.session_state.rw_batch_res[f_map[f]] = f.result()
                        except:
                            st.session_state.rw_batch_res[f_map[f]] = "Error"
                status.update(label="✅ 完成", state="complete", expanded=False)
        
        # 显示结果
        for i, col in enumerate(res_cols):
            with col:
                res = st.session_state.rw_batch_res[i]
                if res:
                    st.text_area(f"out_{i}", value=res, height=200, label_visibility="collapsed")
                    render_copy_btn(res, f"cp_b_{i}")
                else:
                    st.markdown("<div style='height:200px; background:#f8fafc; border-radius:12px; border:1px dashed #e2e8f0;'></div>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True) # close glass-card

    st.markdown('</div>', unsafe_allow_html=True) # close workspace-container
