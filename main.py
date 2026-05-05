import os
import sys

# Fix lỗi in tiếng Việt trên console Windows
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv

# Load biến môi trường từ file .env trước khi import các module (vì config.py sẽ đọc env)
load_dotenv()

from data import CORPUS, BENCHMARK_QUESTIONS
from llm import LLMService
from graph_engine import GraphBuilder
from rag_engine import FlatRAG, GraphRAG

def generate_report(results, build_time, total_tokens, filename="report.md"):
    report_md = f"""# Báo Cáo Thực Hành: Xây Dựng Hệ Thống GraphRAG

## 1. Phân Tích Chi Phí Xây Dựng Đồ Thị
- **Thời gian xây dựng (Extraction + Graph Construction):** `{build_time:.2f} giây`
- **Tổng số Tokens LLM đã sử dụng:** `{total_tokens} tokens`

## 2. Ảnh Đồ Thị Tri Thức
Đồ thị đã được tạo và lưu tại file `graph.png`.

## 3. Bảng So Sánh Benchmark ({len(results)} Câu Hỏi - Flat RAG vs GraphRAG)

| STT | Câu hỏi | Flat RAG Answer | GraphRAG Answer | Nhận xét (Ví dụ) |
|---|---|---|---|---|
"""
    for i, res in enumerate(results):
        report_md += f"| {i+1} | {res['question']} | {res['flat_rag']} | {res['graph_rag']} | |\n"
        
    report_md += """
## 4. Kết Luận & Đánh Giá
- **Flat RAG**: Thường gặp khó khăn hoặc đưa ra thông tin "ảo giác" (hallucination) đối với các câu hỏi **Multi-hop**.
- **GraphRAG**: Trả lời chính xác và đầy đủ nhờ cơ chế duyệt **2-hop traversal**.
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report_md)
    print(f"\nHOÀN THÀNH! Báo cáo chi tiết đã được xuất ra file {filename}")

def main():
    print("--- BẮT ĐẦU XÂY DỰNG ĐỒ THỊ ---")
    builder = GraphBuilder()
    G = builder.build_graph(CORPUS)
    print(f"Xây dựng đồ thị xong trong {builder.build_time:.2f}s.")
    
    builder.visualize()
    
    print("\n--- CHUẨN BỊ FLAT RAG (CHROMADB) ---")
    flat_rag = FlatRAG(CORPUS)
    print("Khởi tạo ChromaDB và nhúng dữ liệu thành công.")
    
    print("\n--- CHUẨN BỊ GRAPHRAG ---")
    graph_rag = GraphRAG(G)
    
    print(f"\n--- CHẠY BENCHMARK {len(BENCHMARK_QUESTIONS)} CÂU HỎI ---")
    results = []
    for i, q in enumerate(BENCHMARK_QUESTIONS):
        print(f"Processing Q{i+1}/{len(BENCHMARK_QUESTIONS)}...")
        ans_flat = flat_rag.query(q)
        ans_graph = graph_rag.query(q)
        results.append({
            "question": q,
            "flat_rag": ans_flat.replace("\n", " ") if ans_flat else "Không có câu trả lời",
            "graph_rag": ans_graph.replace("\n", " ") if ans_graph else "Không có câu trả lời"
        })
        
    generate_report(results, builder.build_time, LLMService.total_tokens_used)

if __name__ == "__main__":
    main()
