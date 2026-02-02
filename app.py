import streamlit as st
from openai import OpenAI
import time

# ==========================================
# 🔐 第一部分：24小时 IP 记忆锁 (核心代码)
# ==========================================

# 设置你的密码
PASSWORD = "taoge888"

# 使用 cache_resource 创建一个全局字典，存在服务器内存里
# 这个字典会记录：{ "IP地址": 上次登录的时间戳 }
@st.cache_resource
def get_login_cache():
    return {}

def get_remote_ip():
    """尝试获取用户的真实IP"""
    try:
        from streamlit.web.server.websocket_headers import _get_websocket_headers
        headers = _get_websocket_headers()
        # 优先获取 X-Forwarded-For (云服务器常用)，其次是 Remote-Addr
        return headers.get("X-Forwarded-For", headers.get("Remote-Addr", "unknown_ip"))
    except:
        return "unknown_ip"

def check_login():
    """检查是否需要登录"""
    # 1. 获取当前用户 IP
    user_ip = get_remote_ip()
    current_time = time.time()
    
    # 2. 获取服务器上的登录记录
    login_cache = get_login_cache()
    
    # 3. 判断：如果 IP 在记录里，且距离上次登录没超过 24小时 (86400秒)
    if user_ip in login_cache and (current_time - login_cache[user_ip] < 86400):
        return True # 通过验证，无需输入密码
        
    # 4. 如果没通过，显示登录界面
    st.set_page_config(page_title="🔒 请先登录", layout="centered")
    st.title("🔒 访问受限")
    st.markdown("### 请输入会员密码解锁工具")
    
    pwd = st.text_input("密码", type="password", key="login_pwd")
    
    if st.button("解锁进入"):
        if pwd == PASSWORD:
            # 密码正确，记录 IP 和时间到服务器内存
            login_cache[user_ip] = current_time
            st.success("✅ 验证成功！")
            time.sleep(0.5)
            st.rerun() # 刷新页面进入主程序
        else:
            st.error("❌ 密码错误")
            
    return False

# 🛑 程序入口：如果没登录，直接停止运行后面的代码
if not check_login():
    st.stop()

# ==========================================
# 🛠️ 第二部分：五路改写机 (原功能区)
# ==========================================

# --- 1. 密钥配置 ---
try:
    api_key = st.secrets["DEEPSEEK_API_KEY"]
except:
    st.error("⚠️ 请先在 Settings -> Secrets 里配置 DEEPSEEK_API_KEY")
    st.stop()

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# --- 2. 核心：爆款改写逻辑 ---
def rewrite_viral_script(content):
    prompt = f"""
    你是一个抖音千万粉的口播博主。
    
    【原始素材】：
    {content}
    
    【你的任务】：
    1. **清洗数据**：自动去除时间轴、乱码、表情等杂质，提取核心语义。
    2. **暴力改写**：将核心语义改写为“原创爆款口播文案”。
    
    【爆款公式】：
    - **开头（黄金3秒）**：必须用一句反直觉、引发焦虑或极度好奇的话。（例如：“千万别再...”、“我这辈子最后悔的...”）。
    - **中间**：大白话，短句，情绪饱满（像跟闺蜜/兄弟吐槽）。
    - **结尾**：强引导互动（“如果是你，你会怎么做？”）。
    
    【输出格式】：
    不要任何解释，直接输出改写后的文案。字数200字左右。
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

# --- 3. 初始化记忆功能 ---
if 'results' not in st.session_state:
    st.session_state['results'] = {}

# --- 4. 页面布局 ---
# 注意：set_page_config 只能调用一次，所以如果上面登录页调用了，这里用 layout="wide" 可能会有小警告，但不影响使用
# 这里的 title 会覆盖登录页的 title
st.title("⚡️ 抖音爆款 · 5窗口独立作战版 (已加密)")
st.caption("✅ 已验证身份 | 5个窗口独立工作 | 自动清洗杂乱文案")

# 循环生成 5 个独立的工作区
for i in range(1, 6):
    with st.expander(f"🎬 **工作台 #{i}** (点击展开/收起)", expanded=True):
        col1, col2 = st.columns([1, 1])
        
        # --- 左边：输入区 ---
        with col1:
            st.markdown(f"**📥 输入素材 #{i}**")
            input_text = st.text_area(f"粘贴第 {i} 个视频的文案", height=200, key=f"input_{i}")
            
            if st.button(f"🚀 改写第 {i} 条", key=f"btn_{i}", use_container_width=True):
                if input_text:
                    with st.spinner(f"正在改写第 {i} 条..."):
                        result = rewrite_viral_script(input_text)
                        st.session_state['results'][i] = result
                        st.rerun()
                else:
                    st.warning("⚠️ 请先粘贴内容！")

        # --- 右边：输出区 ---
        with col2:
            st.markdown(f"**📤 爆款文案 #{i}**")
            if i in st.session_state['results']:
                st.text_area(f"结果 #{i}", value=st.session_state['results'][i], height=285, key=f"output_{i}")
            else:
                st.info("等待生成...")
