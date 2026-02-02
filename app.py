import streamlit as st
from openai import OpenAI
import time
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont # 引入图像处理库
import io
import os

# ==========================================
# 0. 核心配置
# ==========================================
st.set_page_config(
    page_title="抖音爆款工场 Pro", 
    layout="wide",
    page_icon="💠",
    initial_sidebar_state="expanded"
)

# 注入 CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    .stApp { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; background-color: #f8fafc; }
    div.block-container { max-width: 90% !important; min-width: 90% !important; background-color: #ffffff; padding: 3rem !important; margin: 2rem auto !important; border-radius: 16px; box-shadow: 0 10px 40px -10px rgba(0,0,0,0.05); }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #f1f5f9; }
    [data-testid="stVerticalBlockBorderWrapper"] { background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 24px; transition: all 0.3s ease; }
    [data-testid="stVerticalBlockBorderWrapper"]:hover { border-color: #cbd5e1; box-shadow: 0 4px 12px rgba(0,0,0,0.03); }
    h1 { color: #0f172a !important; font-weight: 800 !important; margin-bottom: 1.5rem !important; }
    h2, h3, h4, h5 { color: #334155 !important; font-weight: 700 !important; }
    .stMarkdown p, label { color: #475569 !important; }
    div.stButton > button { border-radius: 8px; font-weight: 600; height: 40px; transition: all 0.2s; }
    div.stButton > button:not([kind="primary"]) { background-color: #f1f5f9; color: #475569 !important; border: 1px solid transparent; }
    div.stButton > button:not([kind="primary"]):hover { background-color: #e0f2fe; color: #0284c7 !important; border-color: #bae6fd; }
    div.stButton > button[kind="primary"] { background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3); border: none; }
    div.stButton > button[kind="primary"] * { color: #ffffff !important; }
    div.stButton > button[kind="primary"]:hover { box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4); transform: translateY(-1px); }
    .stTextArea textarea, .stTextInput input { border-radius: 8px; border: 1px solid #cbd5e1; background-color: #f8fafc !important; color: #1e293b !important; caret-color: #2563eb; font-weight: 500; -webkit-text-fill-color: #1e293b !important; transition: border 0.2s, box-shadow 0.2s; }
    .stTextArea textarea:focus, .stTextInput input:focus { background-color: #ffffff !important; border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15); }
    ::placeholder { color: #94a3b8 !important; opacity: 1; }
    .empty-state-box { height: 200px; background-image: repeating-linear-gradient(45deg, #f8fafc 25%, transparent 25%, transparent 75%, #f8fafc 75%, #f8fafc), repeating-linear-gradient(45deg, #f8fafc 25%, #ffffff 25%, #ffffff 75%, #f8fafc 75%, #f8fafc); background-size: 20px 20px; border: 2px dashed #e2e8f0; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #94a3b8; font-weight: 500; flex-direction: column; gap: 10px; }
    .idea-card { background-color: #f0f9ff; border-left: 4px solid #0ea5e9; padding: 15px; margin-bottom: 10px; border-radius: 4px; color: #334155; }
    .login-spacer { height: 10vh; }
    /* 海报上传区域美化 */
    [data-testid="stFileUploader"] { background-color: #f8fafc; border: 2px dashed #cbd5e1; border-radius: 12px; padding: 20px; text-align: center;}
    [data-testid="stImage"] { border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
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

    # 总控台
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
        st.info("💡 看到喜欢的，直接复制到【文案改写】里让 AI 帮你扩写！")
        
        ideas = st.session_state['brainstorm_result'].split('\n')
        for idea in ideas:
            if idea.strip():
                st.markdown(f"<div class='idea-card'>{idea}</div>", unsafe_allow_html=True)

# --- 🔥 E. 新增功能：海报生成 (PIL实现) ---
def page_poster_gen():
    st.markdown("## 🎨 剧名海报生成")
    st.caption("上传原海报，自动在底部添加新剧名横幅，覆盖原有信息。")
    st.markdown("---")

    with st.container(border=True):
        c1, c2 = st.columns([1, 1], gap="large")
        with c1:
            uploaded_file = st.file_uploader("📤 上传原剧海报 (支持 JPG/PNG)", type=["jpg", "jpeg", "png"])
        with c2:
            new_title = st.text_input("🎬 输入新的推广别名", placeholder="例如：重生之我在豪门当保姆")
            
            # 字体选择逻辑
            font_path = "font.ttf" # 默认寻找当前目录下的 font.ttf
            font_status = "✅ 已检测到自定义字体 (font.ttf)" if os.path.exists(font_path) else "⚠️ 未检测到 font.ttf，将使用系统默认字体（中文可能显示为方框）"
            st.caption(font_status)

            generate_btn = st.button("✨ 生成新海报", type="primary", use_container_width=True, disabled=(not uploaded_file or not new_title))

    if generate_btn and uploaded_file and new_title:
        try:
            with st.spinner("正在绘制海报..."):
                # 1. 打开图片
                image = Image.open(uploaded_file).convert("RGBA")
                width, height = image.size
                
                # 2. 创建绘图对象
                draw = ImageDraw.Draw(image)
                
                # 3. 定义底部横幅区域 (高度为总高度的 15%)
                banner_height = int(height * 0.15)
                banner_y_start = height - banner_height
                
                # 绘制半透明黑色横幅背景 (覆盖原文字)
                # (左上x, 左上y, 右下x, 右下y), fill=(R,G,B,Alpha)
                draw.rectangle(
                    [(0, banner_y_start), (width, height)],
                    fill=(0, 0, 0, 200) # 黑色，200透明度
                )
                
                # 4. 加载字体
                font_size = int(banner_height * 0.5) # 字号为横幅高度的一半
                try:
                    if os.path.exists(font_path):
                        font = ImageFont.truetype(font_path, font_size)
                    else:
                        # 如果没有自定义字体，尝试加载系统默认字体（效果差）
                        font = ImageFont.load_default() 
                        st.toast("⚠️ 使用了默认字体，中文可能无法显示，请上传 font.ttf", icon="⚠️")
                except Exception as e:
                     st.error(f"字体加载失败: {e}")
                     font = ImageFont.load_default()

                # 5. 计算文字位置使其居中
                # 获取文字的边界框 (left, top, right, bottom)
                text_bbox = draw.textbbox((0, 0), new_title, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]

                text_x = (width - text_width) / 2
                # 垂直居中公式：横幅起始Y + (横幅高度 - 文字高度) / 2 - 文字顶部基线偏移
                text_y = banner_y_start + (banner_height - text_height) / 2 - text_bbox[1]

                # 6. 绘制白色文字
                draw.text((text_x, text_y), new_title, font=font, fill=(255, 255, 255, 255))
                
                # 7. 显示结果
                st.markdown("### ✨ 生成结果")
                st.image(image, use_column_width=True)
                
                # 8. 提供下载按钮
                # 将图片保存到内存 buffer
                buf = io.BytesIO()
                image.convert("RGB").save(buf, format="JPEG", quality=95)
                byte_im = buf.getvalue()
                
                st.download_button(
                    label="⬇️ 下载海报图片",
                    data=byte_im,
                    file_name=f"poster_{int(time.time())}.jpg",
                    mime="image/jpeg",
                    type="primary"
                )

        except Exception as e:
            st.error(f"海报生成失败: {e}")


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
        st.info("全新功能上线：\n🎨 **海报生成**：一键替换剧名，批量做图神器！", icon="🎉")

if menu_option == "📝 文案改写": page_rewrite()
elif menu_option == "💡 爆款选题库": page_brainstorm()
elif menu_option == "🎭 创建别名": page_alias_creation()
elif menu_option == "🎨 海报生成": page_poster_gen()
elif menu_option == "🏷️ 账号起名": page_naming()
elif menu_option == "👤 我的账户": page_account()
