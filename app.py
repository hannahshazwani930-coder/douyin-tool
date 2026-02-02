import streamlit as st
from openai import OpenAI
import time
from concurrent.futures import ThreadPoolExecutor # 引入多线程工具

# ==========================================
# ⚙️ 全局配置 (解决网页宽度问题)
# ==========================================
# 这一行必须放在代码的最最最前面，甚至在 import 之后的第一行
st.set_page_config(page_title="🔥 抖音爆款改写机", layout="wide")

# ==========================================
# 🔐 第一部分：24小时 IP 记忆锁
# ==========================================

PASSWORD = "taoge888"

@st.cache_resource
def get_login_cache():
    return {}

def get_remote_ip():
    try:
        from streamlit.web.server.websocket_headers import _get_websocket_headers
        headers = _get_websocket_headers()
        return headers.get("X-Forwarded-For", headers.get("Remote-Addr", "unknown_ip"))
    except:
        return "unknown_ip"

def check_login():
    user_ip = get_remote_ip()
    current_time = time.time()
    login_cache = get_login_cache()
    
    # 检查IP记忆
    if user_ip in login_cache and (current_time - login_cache[user_ip] < 86400):
        return True 
        
    # 登录界面 (使用 columns 居中显示，因为 layout 已经是 wide 了)
    st.markdown("<br><br><br>", unsafe_allow_html=True) # 稍微空几行
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🔒 访问受限")
        st.markdown("### 请输入会员密码解锁工具")
        pwd = st.text_input("密码", type="password", key="login_pwd")
        if st.button("解锁进入", use_container_width=True):
            if pwd == PASSWORD:
                login_cache[user_ip] = current_time
                st.success("✅ 验证成功！")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("❌ 密码错误")
    return False

if not check_login():
    st.stop()

# ==========================================
# 🛠️ 第二部分：五路并发改写机
# ==========================================

# --- 1. 密钥配置 ---
try:
    api_key = st.secrets["DEEPSEEK_API_KEY"]
except:
    st.error("⚠️ 请先在 Settings -> Secrets 里配置 DEEPSEEK_API_KEY")
    st.stop()

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# --- 2. 核心改写逻辑 ---
def rewrite_viral_script(content):
    if not content or len(content.strip()) < 5:
        return "⚠️ 内容太短，无法改写"
        
    prompt = f"""
    你是一个抖音千万粉的口播博主。
    【原始素材】：{content}
    【任务】：清洗数据，去除乱码时间轴，暴力改写为原创爆款文案。
    【公式】：
    1. 黄金3秒开头（反直觉/焦虑/好奇）。
    2. 中间说人话（情绪饱满，像跟朋友吐槽）。
    3. 结尾强引导。
    【输出】：直接输出文案，200字左右。
    """
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=1.3, 
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"生成出错：{e}"

# --- 3. 初始化记忆 ---
if 'results' not in st.session_state:
    st.session_state['results'] = {}

# --- 4. 页面布局 ---
st.title("⚡️ 抖音爆款 · 5窗口并发版 (已加速)")
st.caption("✅ 网页已自适应宽度 | ✅ 支持 5 窗口并发执行 (提速500%)")

# --- 🔥 新增：总控操作区 ---
st.markdown("### 🚀 总控台")
col_main_btn, col_tips = st.columns([1, 4])
with col_main_btn:
    # 这是一个超级按钮，点击后会同时处理所有填了字的窗口
    start_all = st.button("🚀 一键改写所有已填窗口", type="primary", use_container_width=True)

if start_all:
    # 1. 收集所有需要处理的任务
    tasks = []   # 存文案
    indices = [] # 存窗口编号(1-5)
    
    for i in range(1, 6):
        # 从 session_state 获取输入框的值
        text = st.session_state.get(f"input_{i}", "")
        if text.strip():
            tasks.append(text)
            indices.append(i)
    
    if not tasks:
        st.warning("⚠️ 所有窗口都是空的，请先粘贴文案！")
    else:
        # 2. 并发执行 (Magic happens here)
        with st.spinner(f"正在同时处理 {len(tasks)} 个任务，请稍候..."):
            # 使用线程池，同时派出 5 个工人干活
            with ThreadPoolExecutor(max_workers=5) as executor:
                # map 会把 rewrite_viral_script 函数应用到 tasks 里的每一个文本上
                results_list = list(executor.map(rewrite_viral_script, tasks))
            
            # 3. 将结果存回 Session State
            for idx, res in zip(indices, results_list):
                st.session_state['results'][idx] = res
            
            st.success("🎉 全部完成！")
            time.sleep(1)
            st.rerun()

st.markdown("---")

# --- 5. 独立窗口展示区 ---
# 使用 columns 来布局，更紧凑
# 这里我们用 5 个独立的 expander，默认全部展开

for i in range(1, 6):
    # 使用 expander 包装，看着整齐
    with st.expander(f"🎬 **工作台 #{i}**", expanded=True):
        c1, c2 = st.columns([1, 1])
        
        # 左侧输入
        with c1:
            st.markdown(f"**📥 输入 #{i}**")
            # 注意：key=f"input_{i}" 非常重要，总控台靠这个取值
            input_text = st.text_area(f"文案 #{i}", height=150, key=f"input_{i}", label_visibility="collapsed", placeholder="粘贴杂乱文案...")
            
            # 保留单独执行按钮，万一只想改这一个
            if st.button(f"⚡️ 仅改写 #{i}", key=f"btn_{i}"):
                if input_text:
                    with st.spinner("生成中..."):
                        res = rewrite_viral_script(input_text)
                        st.session_state['results'][i] = res
                        st.rerun()
        
        # 右侧输出
        with c2:
            st.markdown(f"**📤 结果 #{i}**")
            val = st.session_state['results'].get(i, "")
            st.text_area(f"结果 #{i}", value=val, height=205, key=f"output_{i}", label_visibility="collapsed", placeholder="等待生成...")
