import streamlit as st
from openai import OpenAI
import time
from concurrent.futures import ThreadPoolExecutor
import io
import os
import requests
import base64
import streamlit.components.v1 as components # 关键组件

# ==========================================
# 0. 核心配置
# ==========================================
st.set_page_config(
    page_title="抖音爆款工场 Pro", 
    layout="wide",
    page_icon="💠",
    initial_sidebar_state="expanded"
)

# 注入 CSS：全局样式美化
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
    .stMarkdown p, label { color: #475569 !important; }
    
    /* 6. Streamlit 原生按钮美化 */
    div.stButton > button {
        border-radius: 8px; font-weight: 600; height: 40px; transition: all 0.2s;
    }
    div.stButton > button:not([kind="primary"]) {
        background-color: #f1f5f9; color: #475569 !important; border: 1px solid transparent;
    }
    div.stButton > button:not([kind="primary"]):hover {
        background-color: #e0f2fe; color: #0284c7 !important; border-color: #bae6fd;
    }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        border: none;
    }
    div.stButton > button[kind="primary"] * { color: #ffffff !important; }
    div.stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4); transform: translateY(-1px);
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
    
    /* 8. 辅助样式 */
    .empty-state-box { height: 200px; background-image: repeating-linear-gradient(45deg, #f8fafc 25%, transparent 25%, transparent 75%, #f8fafc 75%, #f8fafc), repeating-linear-gradient(45deg, #f8fafc 25%, #ffffff 25%, #ffffff 75%, #f8fafc 75%, #f8fafc); background-size: 20px 20px; border: 2px dashed #e2e8f0; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #94a3b8; font-weight: 500; flex-direction: column; gap: 10px; }
    a.redirect-btn { display: block; width: 100%; text-align: center; background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); color: white !important; padding: 16px; border-radius: 12px; text-decoration: none; font-size: 18px; font-weight: 700; margin-top: 10px; box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3); transition: transform 0.2s; border: 1px solid #7c3aed; }
    a.redirect-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(139, 92, 246, 0.4); }
    .tutorial-box { background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; margin-top: 25px; }
    .tutorial-step { display: flex; align-items: center; margin-bottom: 15px; font-size: 15px; color: #334155; line-height: 1.5; }
    .step-num { background-color: #e0f2fe; color: #0284c7; font-weight: bold; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 12px; flex-shrink: 0; }
    .prompt-block { background-color: #1e293b; color: #cbd5e1; padding: 15px; border-radius: 8px; font-family: monospace; margin-top: 10px; border-left: 4px solid #3b82f6; font-size: 14px; }
    .login-spacer { height: 10vh; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# ⚡ 核心功能：前端 HTML 复制按钮组件
# ==========================================
def render_copy_button_html(text, unique_key):
    """
    生成一个完全由 HTML/CSS/JS 控制的复制按钮。
    这绕过了 Streamlit 的 Python 重载机制，直接在浏览器端操作剪贴板。
    """
    # 对文本进行转义，防止 JS 语法错误
    safe_text = text.replace("`", "\`").replace("${", "\${").replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@600&display=swap');
            body {{ margin: 0; padding: 0; background: transparent; overflow: hidden; }}
            
            /* 模仿 Streamlit 原生 Primary 按钮样式 */
            .copy-btn {{
                width: 100%;
                height: 42px;
                background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
                color: white;
                border: none;
                border-radius: 8px;
                font-family: 'Inter', sans-serif;
                font-weight: 600;
                font-size: 14px;
                cursor: pointer;
                box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
            }}
            .copy-btn:hover {{
                box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4);
                transform: translateY(-1px);
            }}
            .copy-btn:active {{
                transform: translateY(0);
                background: #1d4ed8;
            }}
            /* 成功状态 */
            .copy-btn.success {{
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
            }}
        </style>
    </head>
    <body>
        <button class="copy-btn" onclick="copyText(this)">
            <span>📋 一键复制纯文本</span>
        </button>

        <script>
            function copyText(btn) {{
                const text = `{safe_text}`;
                
                // 优先使用现代 API
                if (navigator.clipboard && window.isSecureContext) {{
                    navigator.clipboard.writeText(text).then(() => {{
                        showSuccess(btn);
                    }}).catch(err => {{
                        fallbackCopyText(text, btn);
                    }});
                }} else {{
                    fallbackCopyText(text, btn);
                }}
            }}

            // 兼容性方案 (针对没有 HTTPS 或旧浏览器)
            function fallbackCopyText(text, btn) {{
                const textArea = document.createElement("textarea");
                textArea.value = text;
                
                // 确保 textarea 不可见但可选中
                textArea.style.position = "fixed";
                textArea.style.left = "-9999px";
                textArea.style.top = "0";
                document.body.appendChild(textArea);
                textArea.focus();
                textArea.select();
                
                try {{
                    const successful = document.execCommand('copy');
                    if (successful) showSuccess(btn);
                }} catch (err) {{
                    console.error('Fallback: Oops, unable to copy', err);
                    btn.innerText = "❌ 复制失败";
                }}
                
                document.body.removeChild(textArea);
            }}

            function showSuccess(btn) {{
                const originalText = btn.innerHTML;
                btn.innerHTML = "<span>✅ 复制成功！</span>";
                btn.classList.add("success");
                
                setTimeout(() => {{
                    btn.innerHTML = originalText;
                    btn.classList.remove("success");
                }}, 2000);
            }}
        </script>
    </body>
    </html>
    """
    # 渲染组件，高度要刚好容纳按钮
    components.html(html_code, height=50)

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
# 2. API 配置
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

# --- A. 文案改写 (带前端JS复制) ---
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
        【输出】：直接输出文案，200字左右，不要任何 markdown 符号，直接给纯文本。
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
    
    # 5个工作台
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
                    # 1. 结果显示框 (只读，纯文本)
                    st.text_area(f"结果 #{i}", value=res_val, height=200, label_visibility="collapsed", key=f"res_area_{i}")
                    
                    # 2. 🔥 注入前端 JS 复制按钮 (不刷新页面，极速) 🔥
                    render_copy_button_html(res_val, f"copy_btn_{i}")
                    
                else:
                    st.markdown("""
                    <div class="empty-state-box">
                        <div style="font-size: 24px;">⏳</div>
                        <div>等待指令...</div>
                        <div style="font-size: 12px; color: #94a3b8;">Input content to generate</div>
                    </div>
                    """, unsafe_allow_html=True)

# --- B. 别名创建 (带前端JS复制) ---
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
            输出：只输出别名列表，一行一个，不要带序号，纯文本。
            """
            try:
                with st.spinner("生成中..."):
                    res = client.chat.completions.create(
                        model="deepseek-chat", messages=[{"role": "user", "content": prompt}], temperature=1.4
                    )
                    st.session_state['alias_result'] = res.choices[0].message.content
            except Exception as e: st.error(f"Error: {e}")

    if 'alias_result' in st.session_state:
        res_text = st.session_state['alias_result']
        st.info("👇 别名列表已生成，点击下方按钮一键复制", icon="📋")
        
        st.text_area("结果", value=res_text, height=300, label_visibility="collapsed")
        
        # 前端复制按钮
        render_copy_button_html(res_text, "alias_copy_btn")

# --- C. 账号起名 (带前端JS复制) ---
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
        res_text = st.session_state['naming_result']
        st.text_area("结果", value=res_text, height=400, label_visibility="collapsed")
        
        # 前端复制按钮
        render_copy_button_html(res_text, "name_copy_btn")

# --- D. 选题灵感库 (带前端JS复制) ---
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
        res_text = st.session_state['brainstorm_result']
        st.text_area("灵感列表", value=res_text, height=400, label_visibility="collapsed")
        
        # 前端复制按钮
        render_copy_button_html(res_text, "brain_copy_btn")


# --- E. 海报生成 (跳转独立站导流版 + 精准教程) ---
def page_poster_gen():
    st.markdown("## 🎨 AI 智能海报改图 (专业版)")
    st.caption("基于 Flux/Banana Pro 算力集群，提供好莱坞级改图效果。")
    st.markdown("---")

    st.info("💡 提示：为了提供更稳定的算力支持，海报改图功能已升级至 **小提大作 独立站**。")

    # 导流卡片
    with st.container(border=True):
        
        st.markdown("### 🚀 前往 小提大作 专业版控制台")
        st.markdown("支持：**智能去字、无痕融合、艺术字特效、4K高清导出**。")
        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2 = st.columns([1, 1.5], gap="large")
        
        with c1:
            st.markdown("##### 第 1 步：复制专属邀请码")
            st.caption("注册时填写，可获赠额外算力点数")
            
            # 使用前端复制按钮来复制邀请码
            invite_code = "5yzMbpxn"
            st.text_input("邀请码", value=invite_code, disabled=True, label_visibility="collapsed")
            render_copy_button_html(invite_code, "invite_code_btn")
            
        with c2:
            st.markdown("##### 第 2 步：前往生成")
            st.caption("点击下方按钮跳转至 aixtdz.com")
            st.markdown("""
                <a href="https://aixtdz.com/" target="_blank" class="redirect-btn">
                    🚀 立即前往 小提大作 生成海报
                </a>
            """, unsafe_allow_html=True)

    # 🔥 新增：保姆级教程 (内容已更新) 🔥
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("#### 📖 新手保姆级改图教程")
        st.caption("按照以下步骤操作，1分钟搞定电影级海报")
        
            st.markdown("""
            <div class="tutorial-box">
                <div class="tutorial-step">
                    <div class="step-num">1</div>
                    <div>注册登录后，点击 <b>“创建自由画布”</b></div>
                </div>
                <div class="tutorial-step">
                    <div class="step-num">2</div>
                    <div>根据提示 <b>双击</b> 或者 <b>右键点击</b> 空白处，选择 <b>“图生图”</b></div>
                </div>
                <div class="tutorial-step">
                    <div class="step-num">3</div>
                    <div>点击组件上的 <b>“+”</b> 号，上传你需要修改的 <b>原剧海报</b></div>
                </div>
                <div class="tutorial-step">
                    <div class="step-num">4</div>
                    <div>点击 <b>右边边框</b>，在下方输入指令（点击右上角复制）：</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("如有疑问，请联系客服微信：TG777188")

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
# 4. 侧边栏导航
# ==========================================

with st.sidebar:
    st.markdown("### 💠 爆款工场 Pro")
    st.markdown(f"<small>IP: {get_remote_ip()}</small>", unsafe_allow_html=True)
    st.markdown("---")
    
    menu_option = st.radio(
        "导航",
        ["📝 文案改写", "💡 爆款选题库", "🎭 创建别名", "🎨 海报生成", "🏷️ 账号起名", "👤 我的账户"],
        index=0, label_visibility="collapsed"
    )
    
    st.markdown("---")
    with st.container(border=True):
        st.info("系统公告：\n🎨 **海报改图** 功能已升级至独立站，算力更强！", icon="🚀")

if menu_option == "📝 文案改写": page_rewrite()
elif menu_option == "💡 爆款选题库": page_brainstorm()
elif menu_option == "🎭 创建别名": page_alias_creation()
elif menu_option == "🎨 海报生成": page_poster_gen()
elif menu_option == "🏷️ 账号起名": page_naming()
elif menu_option == "👤 我的账户": page_account()

