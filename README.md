# Lab Day 19: Xây Dựng Hệ Thống GraphRAG Với Tech Company Corpus

**Học viên:** Vũ Duy Linh  
**ID/MSSV:** 2A202600460  

Dự án này là bài Lab triển khai một hệ thống Pipeline hoàn chỉnh nhằm đối chiếu hiệu suất giữa **Flat RAG** (tìm kiếm vector truyền thống) và **GraphRAG** (tìm kiếm theo đồ thị tri thức đa bước) thông qua kho dữ liệu tự động crawl từ Wikipedia về các công ty công nghệ lớn.

## 🗂️ Cấu Trúc Dự Án

```text
Day19_Track3_GraphRAG_2A202600460_VuDuyLinh/
├── config.py             # Quản lý cấu hình API Key (Groq) và thông số Ollama Embeddings.
├── data.py               # Tự động crawl tóm tắt Wikipedia của các công ty công nghệ và lưu thành Corpus.
├── llm.py                # Xử lý kết nối Groq LLM (llama-3.3-70b-versatile) để trích xuất Triples.
├── graph_engine.py       # Xây dựng Knowledge Graph bằng NetworkX và xuất ảnh trực quan đồ thị.
├── rag_engine.py         # Chứa logic của FlatRAG (ChromaDB) và GraphRAG (2-hop traversal).
├── main.py               # Orchestrator: Tự động chạy toàn bộ pipeline và xuất file báo cáo.
├── report.md             # Báo cáo Benchmark đánh giá độ chuẩn xác giữa Flat RAG và Graph RAG.
└── relection_VuDuyLinh.md # Bài thu hoạch và phản biện cá nhân.
```

## 🚀 Hướng Dẫn Cài Đặt Và Chạy

### 1. Cài đặt các thư viện Python
Chắc chắn rằng bạn đã kích hoạt môi trường ảo (nếu có), sau đó chạy:
```bash
pip install networkx matplotlib openai chromadb python-dotenv requests
```

### 2. Khởi chạy Ollama (dành cho Local Embeddings)
Đảm bảo bạn đã cài đặt phần mềm [Ollama](https://ollama.com/) và đã pull model dùng để nhúng văn bản (trong bài dùng `nomic-embed-text`):
```bash
ollama run nomic-embed-text
```

### 3. Thiết lập API Key
Tạo một file có tên `.env` ở thư mục gốc của project và dán API Key của Groq vào:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Thực thi toàn bộ hệ thống
Khởi chạy script chính để mô phỏng toàn bộ tiến trình:
```bash
python main.py
```
> **Lưu ý:** Tiến trình có thể mất từ 1-2 phút do phải crawl dữ liệu từ Wikipedia và trích xuất thực thể qua API.
Sau khi chạy xong, chương trình sẽ sinh ra ảnh đồ thị **`graph.png`** và file **`report.md`**.
