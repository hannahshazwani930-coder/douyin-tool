import streamlit as st
from openai import OpenAI
import time
from concurrent.futures import ThreadPoolExecutor
import io
import os
import requests # 用于调用外部 API
import base64

# ==========================================
# 0. 核心配置
# ==========================================
st.set_page_config(
    page_title="抖音爆款工场 Pro", 
    layout="wide",
    page_icon="💠",
    initial_sidebar_state="expanded"
)

# 注入 CSS：修复按钮文字颜色 + 极致 UI + 商业化引导
st.markdown("""
<style>
    /* 1. 全局字体与背景 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .stApp { 
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; 
        background-color: #f8fafc; 
    }
    
    /* 2. 布局容器 */
    div.block-container {
        max-width: 90% !important;
        min-width: 90% !important;
        background-color: #ffffff;
        padding: 3rem !important;
        margin: 2rem auto !important;
        border-radius: 16px;
        box-shadow: 0 10px 40px -10px rgba(0,0,0,0.05); 
    }

    /* 3. 侧边栏 */
    [data-testid="stSidebar"] { 
        background-color: #ffffff; 
        border-right: 1px solid #f1f5f9; 
    }
    
    /* 4. 工作台卡片 */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 24px;
        position: relative;
        transition: all 0.3s ease;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #cbd5e1;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
    
    /* 5. 标题与文字颜色控制 */
    h1 { color: #0f172a !important; font-weight: 800 !important; margin-bottom: 1.5rem !important; }
    h2, h3, h4, h5 { color: #334155 !important; font-weight: 700 !important; }
    
    /* 普通文本颜色 */
    .stMarkdown p, label { color: #475569 !important; }
    
    /* 6. 按钮极致美化 */
    div.stButton > button {
        border-radius: 8px; font-weight: 600; height: 40px; transition: all 0.2s;
    }
    
    /* (A) 次级按钮 */
    div.stButton > button:not([kind="primary"]) {
        background-color: #f1f5f9; 
        color: #475569 !important;
        border: 1px solid transparent;
    }
    div.stButton > button:not([kind="primary"]):hover {
        background-color: #e0f2fe; 
        color: #0284c7 !important;
        border-color: #bae6fd;
    }
    
    /* (B) 主按钮 - 强制白字 */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        border: none;
    }
    div.stButton > button[kind="primary"] * {
        color: #ffffff !important; 
    }
    div.stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4); 
        transform: translateY(-1px);
    }
    
    /* (C) 充值链接按钮 (显眼的渐变红/橙色，促进点击) */
    a.recharge-btn {
        display: block;
        width: 100%;
        text-align: center;
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); /* 橙色系吸引点击 */
        color: white !important;
        padding: 12px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 700;
        margin-top: 10px;
        box-shadow: 0 4px 10px rgba(245, 158, 11, 0.3);
        transition: transform 0.2s;
        border: 1px solid #d97706;
    }
    a.recharge-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 14px rgba(245, 158, 11, 0.4);
    }

    /* 7. 输入框修复 */
    .stTextArea textarea, .stTextInput input {
        border-radius: 8px;
        border: 1px solid #cbd5e1;
        background-color: #f8fafc !important; 
        color: #1e293b !important;            
        caret-color: #2563eb;                 
        font-weight: 500;
        -webkit-text-fill-color: #1e293b !important;
        transition: border 0.2s, box-shadow 0.2s;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        background-color: #ffffff !important;
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
    }
    ::placeholder { color: #94a3b8 !important; opacity: 1; }

    /* 8. 空状态占位符 */
    .empty-state-box { height: 200px; background-image: repeating-linear-gradient(45deg, #f8fafc 25%, transparent 25%, transparent 75%, #f8fafc 75%, #f8fafc), repeating-linear-gradient(45deg, #f8fafc 25%, #ffffff 25%, #ffffff 75%, #f8fafc 75%, #f8fafc); background-size: 20px 20px; border: 2px dashed #e2e8f0; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #94a3b8; font-weight: 500; flex-direction: column; gap: 10px; }
    .idea-card { background-color: #f0f9ff; border-left: 4px solid #0ea5e9; padding: 15px; margin-bottom: 10px; border-radius: 4px; color: #334155; }
    .login-spacer { height: 10vh; }
    
    /* 海报预览图圆角 */
    [data-testid="stImage"] img { border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. 登录与安全系统
# ==========================================

PASSWORD = "taoge888"

def clear_text_callback(key):
    if key in st.session_state:
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
        
    login_placeholder = st.empty()
    with login_placeholder.container():
        st.markdown("<div class='login-spacer'></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 1.5, 1])
        with c2:
            st.markdown("<h2 style='text-align: center; margin-bottom: 20px;'>💠 爆款工场 Pro</h2>", unsafe_allow_html=True)
            st.info("🔒 系统已加密，获取密码请联系微信：TG777188", icon="🔑")
            
            with st.form("login_form"):
                pwd = st.text_input("请输入会员密码", type="password", placeholder="******")
                st.markdown("<br>", unsafe_allow_html=True)
                submitted = st.form_submit_button("🚀 立即解锁", type="primary", use_container_width=True)
            
            if submitted:
                if pwd == PASSWORD:
                    login_cache[user_ip] = current_time 
                    st.session_state['is_logged_in'] = True 
                    st.success("✅ 验证成功！")
                    time.sleep(0.5)
                    login_placeholder.empty()
                    st.rerun()
                else:
                    st.error("❌ 密码错误")
    return False

if not check_login():
    st.stop()

# ==========================================
# 2. API 配置 (DeepSeek - 文本用)
# ==========================================

try:
    api_key = st.secrets["DEEPSEEK_API_KEY"]
except:
    st.error("❌ 未检测到 DEEPSEEK_API_KEY，请在后台 Secrets 中配置。")
    st.stop()

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# ==========================================
# 3. 功能模块
# ==========================================

# --- A. 文案改写 ---
def page_rewrite():
    st.markdown("## ⚡ 爆款文案改写中台")
    st.caption("AI 驱动的五路并发架构 | 40秒黄金完播率模型")
    st.markdown("---")

    if 'results' not in st.session_state:
        st.session_state['results'] = {}
        
    def rewrite_logic(content):
        if not content or len(content.strip()) < 5: return "⚠️ 内容过短"
        prompt = f"""
        你是一个抖音千万粉的口播博主。
        【原始素材】：{content}
        【任务】：清洗数据，改写为原创爆款文案。
        【公式】：黄金3秒开头 + 中间情绪饱满说人话 + 结尾强引导。
        【输出】：直接输出文案，200字左右。
        """
        try:
            res = client.chat.completions.create(
                model="deepseek-chat", messages=[{"role": "user", "content": prompt}], temperature=1.3
            )
            return res.choices[0].message.content
        except Exception as e: return f"Error: {e}"

    col_main, col_tips = st.columns([1, 2])
    with col_main:
        if st.button("🚀 一键并发执行 (5路全开)", type="primary", use_container_width=True):
            tasks, indices = [], []
            for i in range(1, 6):
                text = st.session_state.get(f"input_{i}", "")
                if text.strip():
                    tasks.append(text)
                    indices.append(i)
            
            if not tasks:
                st.toast("⚠️ 请先输入文案", icon="🛑")
            else:
                with st.status("☁️ 云端计算中...", expanded=True) as status:
                    with ThreadPoolExecutor(max_workers=5) as executor:
                        results_list = list(executor.map(rewrite_logic, tasks))
                    for idx, res in zip(indices, results_list):
                        st.session_state['results'][idx] = res
                    status.update(label="✅ 完成！", state="complete", expanded=False)
                    st.rerun()
    with col_tips:
        st.info("💡 指南：粘贴文案到下方窗口，点击左侧 **【蓝色按钮】** 同时处理。", icon="📝")

    st.markdown("<br>", unsafe_allow_html=True)
    
    for i in range(1, 6):
        with st.container(border=True):
            st.markdown(f"#### 🎬 工作台 #{i}")
            c1, c2 = st.columns([1, 1], gap="large")
            with c1:
                input_key = f"input_{i}"
                st.text_area("原始文案", height=200, key=input_key, label_visibility="collapsed", placeholder="💡在此按 Ctrl+V 粘贴提取的文案...")
                b1, b2 = st.columns([1, 2.5])
                b1.button("🗑️ 清空", key=f"clr_{i}", on_click=clear_text_callback, args=(input_key,), use_container_width=True)
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
                    st.toast(f"#{i} 已生成，可复制", icon="🎉")
                else:
                    st.markdown("""
                    <div class="empty-state-box">
                        <div style="font-size: 24px;">⏳</div>
                        <div>等待指令...</div>
                        <div style="font-size: 12px; color: #94a3b8;">Input content to generate</div>
                    </div>
                    """, unsafe_allow_html=True)

# --- B. 别名创建 ---
def page_alias_creation():
    st.markdown("## 🎭 剧名别名生成")
    st.caption("防屏蔽 | 矩阵分发专用")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        original_name = st.text_input("🎬 原剧名/原书名", placeholder="例如：霸道总裁爱上我")
    with col2:
        count = st.slider("生成数量", 5, 20, 10)
    
    tags = st.multiselect("🏷️ 强化元素", ["高甜", "复仇", "逆袭", "悬疑", "虐恋", "豪门"], default=["逆袭", "高甜"])
    
    if st.button("🚀 生成别名", type="primary", use_container_width=True):
        if not original_name:
            st.toast("请输入原名", icon="🛑")
        else:
            prompt = f"""
            请将《{original_name}》改写为{count}个推广别名。
            策略：加入“{'、'.join(tags)}”元素，去原名化，直击痛点。
            输出：只输出别名列表，一行一个。
            """
            try:
                with st.spinner("生成中..."):
                    res = client.chat.completions.create(
                        model="deepseek-chat", messages=[{"role": "user", "content": prompt}], temperature=1.4
                    )
                    st.session_state['alias_result'] = res.choices[0].message.content
            except Exception as e: st.error(f"Error: {e}")

    if 'alias_result' in st.session_state:
        st.info("💡 点击右上角图标复制", icon="📋")
        st.code(st.session_state['alias_result'], language='text')

# --- C. 账号起名 ---
def page_naming():
    st.markdown("## 🏷️ 账号/IP 起名大师")
    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        niche = st.selectbox("🎯 赛道", ["短剧", "小说", "口播", "情感", "带货"])
    with c2:
        style = st.selectbox("🎨 风格", ["高冷", "搞笑", "文艺", "粗暴", "反差"])
    keywords = st.text_input("🔑 关键词 (选填)")
    
    if st.button("🎲 生成名字", type="primary", use_container_width=True):
        prompt = f"为【{niche}】赛道生成10个{style}风格账号名，含关键词：{keywords}。格式：名字+解释。"
        try:
            with st.spinner("生成中..."):
                res = client.chat.completions.create(
                    model="deepseek-chat", messages=[{"role": "user", "content": prompt}], temperature=1.5
                )
                st.session_state['naming_result'] = res.choices[0].message.content
        except Exception as e: st.error(str(e))

    if 'naming_result' in st.session_state:
        st.code(st.session_state['naming_result'], language='text')

# --- D. 选题灵感库 ---
def page_brainstorm():
    st.markdown("## 💡 爆款选题灵感库")
    st.caption("文案枯竭？输入关键词，AI 帮你生成 10 个“必火”的选题方向。")
    st.markdown("---")

    with st.container(border=True):
        c1, c2 = st.columns([3, 1])
        with c1:
            topic = st.text_input("🔍 输入你的赛道/关键词", placeholder="例如：职场、美妆、减肥、副业...")
        with c2:
            st.write("") 
            st.write("") 
            generate_btn = st.button("🧠 帮我想选题", type="primary", use_container_width=True)

    if generate_btn and topic:
        prompt = f"""
        我是做【{topic}】领域的。现在文案枯竭，请帮我生成 10 个绝对会火的爆款选题。
        
        【要求】：
        1. 必须反直觉，打破认知。
        2. 必须直击痛点，引发焦虑或强烈好奇。
        3. 格式：
        1. 标题：xxxx | 钩子：xxxx
        2. 标题：xxxx | 钩子：xxxx
        """
        try:
            with st.spinner("AI 正在疯狂头脑风暴..."):
                res = client.chat.completions.create(
                    model="deepseek-chat", messages=[{"role": "user", "content": prompt}], temperature=1.5
                )
                st.session_state['brainstorm_result'] = res.choices[0].message.content
        except Exception as e: st.error(str(e))

    if 'brainstorm_result' in st.session_state:
        st.markdown("### ✨ 推荐选题")
        ideas = st.session_state['brainstorm_result'].split('\n')
        for idea in ideas:
            if idea.strip():
                st.markdown(f"<div class='idea-card'>{idea}</div>", unsafe_allow_html=True)


# --- E. 海报生成 (调用 bj.nfai.lol - Nano Banana Pro) ---
def page_poster_gen():
    st.markdown("## 🎨 剧名海报生成 (Banana Pro)")
    st.caption("基于 Nano Banana Pro 模型，智能替换海报文字。")
    st.markdown("---")

    # 1. 检查 Key 是否配置
    user_api_key = st.session_state.get('baojian_api_key', '')
    
    if not user_api_key:
        st.warning("⚠️ 需配置 **豹剪 API Key** 方可使用商业版模型。")
        st.info("👇 请查看左侧侧边栏底部，获取或填入 Key。")
        return

    with st.container(border=True):
        c1, c2 = st.columns([1, 1], gap="large")
        with c1:
            uploaded_file = st.file_uploader("📤 上传原海报 (支持 JPG/PNG)", type=["jpg", "png", "jpeg"])
        with c2:
            new_title = st.text_input("🎬 输入新剧名", placeholder="例如：重生之我在豪门当保姆")
            st.caption("提示：将调用 `Nano Banana Pro` 模型进行智能重绘。")
            
            generate_btn = st.button("✨ 立即生成新海报", type="primary", use_container_width=True, disabled=(not uploaded_file or not new_title))

    if generate_btn and uploaded_file and new_title:
        try:
            with st.spinner("🍌 正在呼叫 Nano Banana Pro 模型进行绘图..."):
                
                # 1. 图片转 Base64
                image_bytes = uploaded_file.getvalue()
                base64_image = base64.b64encode(image_bytes).decode('utf-8')
                
                # 2. 构建请求
                # 目标：bj.nfai.lol
                # 模型：Nano Banana Pro
                api_url = "https://bj.nfai.lol/v1/chat/completions" 
                
                headers = {
                    "Authorization": f"Bearer {user_api_key}",
                    "Content-Type": "application/json"
                }
                
                # 构造多模态 Payload (Vision 格式)
                data = {
                    "model": "Nano Banana Pro", # 强制指定模型
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text", 
                                    "text": f"将海报上的剧名文字修改为：{new_title}。保持海报原有设计风格，字体大气，无痕替换。"
                                },
                                {
                                    "type": "image_url", 
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ],
                    "stream": False
                }
                
                # 3. 发送请求
                response = requests.post(api_url, headers=headers, json=data, timeout=60)
                
                if response.status_code == 200:
                    res_json = response.json()
                    # 假设返回格式为 OpenAI 兼容格式，内容在 content 中
                    # 对于生图/改图模型，通常 URL 会在 content 里，或者是以 markdown 图片格式返回
                    try:
                        content = res_json['choices'][0]['message']['content']
                        
                        st.success("🎉 生成成功！")
                        st.markdown("### ✨ 生成结果")
                        
                        # 解析返回内容，如果是 URL 直接显示，如果是 Markdown 图片提取显示
                        # 这里简单处理：直接把 content 渲染出来，通常模型会返回 ![](url)
                        st.markdown(content) 
                        
                        # 如果 API 返回的是纯 URL 文本，尝试自动提取并显示图片组件以便下载
                        if content.startswith("http"):
                             st.image(content)
                             
                    except Exception as parse_err:
                        st.error(f"解析响应失败: {parse_err} | 原始返回: {res_json}")
                else:
                    st.error(f"API 请求失败 (状态码 {response.status_code}): {response.text}")

        except Exception as e:
            st.error(f"请求发生错误: {e}")

# --- F. 个人中心 ---
def page_account():
    st.markdown("## 👤 我的账户")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.metric("会员状态", "VIP 专业版", delta="永久激活")
            st.text_input("绑定 IP", value=get_remote_ip(), disabled=True)
    with col2:
        with st.container(border=True):
            st.markdown("#### 💬 联系客服")
            st.markdown("**微信 ID**: `TG777188`")

# ==========================================
# 4. 侧边栏导航 (含 API 配置与充值)
# ==========================================

with st.sidebar:
    st.markdown("### 💠 爆款工场 Pro")
    st.markdown(f"<small>IP: {get_remote_ip()}</small>", unsafe_allow_html=True)
    st.markdown("---")
    
    # 🔥 商业化核心：API Key 配置区 🔥
    with st.expander("🔑 豹剪 Key 配置", expanded=True):
        st.caption("使用海报改图功能需配置 Key")
        baojian_key = st.text_input("输入 Key", type="password", key="baojian_api_key", label_visibility="collapsed")
        
        # 充值直达按钮 (带分销参数)
        st.markdown("""
            <a href="https://bj.nfai.lol/register?aff=Mzx2" target="_blank" class="recharge-btn">
                ⚡ 前往获取 / 充值 Key
            </a>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    menu_option = st.radio(
        "导航",
        ["📝 文案改写", "💡 爆款选题库", "🎭 创建别名", "🎨 海报生成", "🏷️ 账号起名", "👤 我的账户"],
        index=0, label_visibility="collapsed"
    )
    
    st.markdown("---")
    with st.container(border=True):
        st.info("系统更新：\n🎨 海报生成已接入 **Nano Banana Pro** 模型。", icon="🍌")

if menu_option == "📝 文案改写": page_rewrite()
elif menu_option == "💡 爆款选题库": page_brainstorm()
elif menu_option == "🎭 创建别名": page_alias_creation()
elif menu_option == "🎨 海报生成": page_poster_gen()
elif menu_option == "🏷️ 账号起名": page_naming()
elif menu_option == "👤 我的账户": page_account()
