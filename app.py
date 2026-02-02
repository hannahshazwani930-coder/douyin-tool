import streamlit as st
from openai import OpenAI
import time
from concurrent.futures import ThreadPoolExecutor 

# ==========================================
# 🎨 0. 全局 UI 与 CSS 配置
# ==========================================
st.set_page_config(page_title="抖音爆款工场 Pro", layout="wide", page_icon="💠")

# 注入 CSS：美化侧边栏、按钮和字体
st.markdown("""
<style>
    /* 全局字体 */
    .stApp { font-family: 'PingFang SC', 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    
    /* 侧边栏美化 */
    [data-testid="stSidebar"] {
        background-color: #f0f2f6;
        border-right: 1px solid #e0e0e0;
    }
    
    /* 标题样式 */
    h1, h2, h3 { color: #2C3E50; font-weight: 700 !important; }
    
    /* 按钮美化 */
    div.stButton > button { 
        border-radius: 8px; 
        font-weight: 600; 
        transition: all 0.3s;
    }
    
    /* 结果框代码块样式优化 */
    .stCode { font-size: 1.1em; }
    
    /* 卡片容器样式 */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        background-color: white;
        padding: 20px;
    }
    
    /* 暗黑模式适配 */
    @media (prefers-color-scheme: dark) {
        [data-testid="stVerticalBlockBorderWrapper"] { background-color: #262730; }
        [data-testid="stSidebar"] { background-color: #1e1e1e; border-right: 1px solid #333; }
        h1, h2, h3 { color: #eee; }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🔐 1. 登录与安全系统
# ==========================================

PASSWORD = "taoge888"

def clear_text_callback(key):
    st.session_state[key] = ""

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
    if st.session_state.get('is_logged_in', False):
        return True

    user_ip = get_remote_ip()
    current_time = time.time()
    login_cache = get_login_cache()
    
    if user_ip in login_cache and (current_time - login_cache[user_ip] < 172800):
        st.session_state['is_logged_in'] = True 
        return True 
        
    # --- 登录界面 ---
    st.markdown("<br><br><br>", unsafe_allow_html=True) 
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center;'>💠 爆款工场 Pro</h2>", unsafe_allow_html=True)
            st.info("🔑 获取密码请联系微信：TG777188", icon="💬")
            
            with st.form("login_form"):
                pwd = st.text_input("请输入会员密码", type="password")
                submitted = st.form_submit_button("🚀 立即解锁", type="primary", use_container_width=True)
                
                if submitted:
                    if pwd == PASSWORD:
                        login_cache[user_ip] = current_time 
                        st.session_state['is_logged_in'] = True 
                        st.toast("验证成功！欢迎回来", icon="✅")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("❌ 密码错误")
    return False

if not check_login():
    st.stop()

# ==========================================
# ⚙️ 2. API 配置
# ==========================================

try:
    api_key = st.secrets["DEEPSEEK_API_KEY"]
except:
    st.error("⚠️ 请先在 Settings -> Secrets 里配置 DEEPSEEK_API_KEY")
    st.stop()

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# ==========================================
# 🧩 3. 功能模块函数化
# ==========================================

# --- 功能 A: 文案改写 (五路并发) ---
def page_rewrite():
    st.markdown("## ⚡ 爆款文案改写中台")
    st.caption("五路并发架构 | 自动清洗杂质 | 40秒黄金完播率模型")
    
    if 'results' not in st.session_state:
        st.session_state['results'] = {}
        
    def rewrite_logic(content):
        if not content or len(content.strip()) < 5: return "⚠️ 内容太短"
        prompt = f"""
        你是一个抖音千万粉的口播博主。
        【原始素材】：{content}
        【任务】：清洗数据，暴力改写为原创爆款文案。
        【公式】：黄金3秒开头（反直觉/焦虑）+ 中间说人话（情绪饱满）+ 结尾强引导。
        【输出】：直接输出文案，200字左右。
        """
        try:
            res = client.chat.completions.create(
                model="deepseek-chat", messages=[{"role": "user", "content": prompt}], temperature=1.3
            )
            return res.choices[0].message.content
        except Exception as e: return f"Error: {e}"

    with st.container(border=True):
        col_main, col_tips = st.columns([1, 3])
        with col_main:
            if st.button("🚀 一键并发执行 (提速500%)", type="primary", use_container_width=True):
                tasks, indices = [], []
                for i in range(1, 6):
                    text = st.session_state.get(f"input_{i}", "")
                    if text.strip():
                        tasks.append(text)
                        indices.append(i)
                
                if not tasks:
                    st.toast("请先在下方输入素材", icon="⚠️")
                else:
                    with st.status("正在进行云端计算...", expanded=True) as status:
                        with ThreadPoolExecutor(max_workers=5) as executor:
                            results_list = list(executor.map(rewrite_logic, tasks))
                        for idx, res in zip(indices, results_list):
                            st.session_state['results'][idx] = res
                        status.update(label="✅ 生成完毕", state="complete", expanded=False)
                        st.rerun()
        with col_tips:
            st.markdown("*💡 提示：将不同视频的提取文案粘贴到下方窗口，点击左侧按钮同时生成。*")

    st.markdown("<br>", unsafe_allow_html=True)
    for i in range(1, 6):
        with st.container(border=True):
            st.markdown(f"**🎬 工作台 #{i}**")
            c1, c2 = st.columns([1, 1], gap="large")
            with c1:
                input_key = f"input_{i}"
                st.text_area("输入", height=150, key=input_key, label_visibility="collapsed", placeholder="按 Ctrl+V 粘贴...")
                b1, b2 = st.columns([1, 3])
                b1.button("🗑️", key=f"clr_{i}", on_click=clear_text_callback, args=(input_key,), use_container_width=True, help="清空")
                if b2.button(f"⚡ 仅生成 #{i}", key=f"btn_{i}", use_container_width=True):
                    val = st.session_state.get(input_key, "")
                    if val:
                        with st.spinner("生成中..."):
                            st.session_state['results'][i] = rewrite_logic(val)
                            st.rerun()
            with c2:
                res_val = st.session_state['results'].get(i, "")
                if res_val:
                    st.code(res_val, language='text')
