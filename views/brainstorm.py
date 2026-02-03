import streamlit as st
from openai import OpenAI
from utils import render_copy_btn

def view_brainstorm():
    st.markdown("### 💡 爆款选题灵感库")
    
    topic = st.text_input("输入你的赛道/关键词", placeholder="例如：美妆、职场、副业、育儿...")
    if st.button("🧠 开始头脑风暴", type="primary"):
        if not topic: st.warning("请输入关键词")
        else:
            api_key = st.secrets.get("DEEPSEEK_API_KEY", "")
            if not api_key:
                st.error("请配置 API Key")
            else:
                try:
                    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
                    with st.spinner("AI 正在分析全网爆款数据..."):
                        prompt = f"我是做【{topic}】赛道的。请生成10个颠覆认知的爆款选题，格式：标题+钩子。要求：反直觉、引发焦虑或好奇。"
                        res = client.chat.completions.create(model="deepseek-chat", messages=[{"role":"user", "content":prompt}], temperature=1.5)
                        st.session_state['brain_res'] = res.choices[0].message.content
                except Exception as e:
                    st.error(str(e))
    
    if 'brain_res' in st.session_state:
        st.markdown("#### 灵感结果")
        st.text_area("结果", value=st.session_state['brain_res'], height=400)
        render_copy_btn(st.session_state['brain_res'], "brain_res_copy")