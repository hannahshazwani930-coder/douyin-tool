# config.py
import streamlit as st

# --- 🔐 安全配置管理 ---

# 1. 管理员配置
# 使用 .get() 确保在 Secrets 缺失时不会抛出 KeyError
ADMIN_ACCOUNT = st.secrets.get("ADMIN_ACCOUNT", "13800138000")
ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "admin123456")

# 2. 数据库配置 (如果使用远程数据库，请在 Secrets 中配置相应字段)
DB_HOST = st.secrets.get("DB_HOST", "localhost")
DB_USER = st.secrets.get("DB_USER", "root")

# 3. 邀请系统配置
DEFAULT_INVITE_CODE = "888888"

# 4. 样式路径配置 (确保路径与您的目录结构一致)
STYLE_DIR = "styles"

# 5. 应用基本信息
APP_NAME = "抖音爆款工场 Pro"
APP_ICON = "💠"

# --- 💡 提示： ---
# 请确保在 Streamlit Cloud 的 "Manage App" -> "Settings" -> "Secrets" 中
# 填入了对应的键值对，例如：
# ADMIN_ACCOUNT = "您的手机号"
# ADMIN_PASSWORD = "您的自定义密码"
