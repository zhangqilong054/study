import os
from dotenv import load_dotenv

load_dotenv()

# AI API 配置（兼容 OpenAI 接口标准）
AI_API_KEY = os.getenv("AI_API_KEY", "")
AI_API_BASE = os.getenv("AI_API_BASE", "https://api.openai.com/v1")
AI_MODEL = os.getenv("AI_MODEL", "gpt-3.5-turbo")

# Flask 配置
SECRET_KEY = os.getenv("SECRET_KEY", "zhixiaotong-secret-key-2024")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB 上传限制

# 知识库路径
KNOWLEDGE_BASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "campus_knowledge.json")
