import os
import sys

# ==========================================
# CẤU HÌNH API VÀ MODEL
# ==========================================
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("Vui lòng thiết lập biến môi trường GROQ_API_KEY trước khi chạy script.")
    print("Ví dụ (PowerShell): $env:GROQ_API_KEY='your_api_key'")
    sys.exit(1)

GROQ_BASE_URL = "https://api.groq.com/openai/v1"
LLM_MODEL = "llama-3.3-70b-versatile"

# Cấu hình Ollama Embedding cho Flat RAG
OLLAMA_URL = "http://localhost:11434/api/embeddings"
OLLAMA_MODEL = "nomic-embed-text" # Thay đổi thành model của bạn nếu cần (vd: llama3)
