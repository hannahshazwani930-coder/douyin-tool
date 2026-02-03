# views/poster.py
import streamlit as st
from utils import render_copy_btn, render_page_banner
import streamlit.components.v1 as components

def view_poster():
    render_page_banner("智能海报工场", "接入专业级设计引擎，无需PS，3步生成电影级海报。")
    
    st.markdown("### 🛠️ 创作流程 (请按顺序操作)")
    
    c1, c2 = st.columns(2)
    
    # 第一步：复制邀请码
    with c1:
        with st.container(border=True):
            st.markdown("#### Step 1: 获取授权码")
            st.info("专属邀请码：**5yzMbpxn**")
            render_copy_btn("5yzMbpxn", "invite_code_poster")
            st.caption("点击上方按钮复制邀请码")
            
    # 第二步：跳转创作
    with c2:
        with st.container(border=True):
            st.markdown("#### Step 2: 进入创作台")
            st.markdown("""
            <a href="https://aixtdz.com" target="_blank" style="text-decoration:none;">
                <button style="width:100%; background:#2563eb; color:white; border:none; padding:10px; border-radius:8px; font-weight:bold; cursor:pointer;">
                    🚀 前往小提大作 (aixtdz.com)
                </button>
            </a>
            """, unsafe_allow_html=True)
            st.caption("点击跳转后，请使用左侧邀请码注册")

    st.markdown("---")
    
    # 教程区域
    with st.expander("📖 查看详细操作教程 (新手必读)", expanded=True):
        st.markdown("""
        **操作步骤详解：**
        1.  **注册登录**：点击上方按钮进入网站，填入邀请码 `5yzMbpxn` 完成注册。
        2.  **创建画布**：登录后，点击“创作画布”。
        3.  **创建节点**：在画布空白处 **右键** -> 选择 **“创建图片节点”**。
        4.  **上传素材**：在节点中点击 **“图生图”** -> 点击 **“+”** 号上传您需要改名的原始海报。
        5.  **输入指令**：在下方提示词框中输入：
            > `将海报剧名：'原剧名' 改成：'你的新剧名'`
        6.  **开始生成**：点击生成按钮，等待 AI 处理即可。
        """)
