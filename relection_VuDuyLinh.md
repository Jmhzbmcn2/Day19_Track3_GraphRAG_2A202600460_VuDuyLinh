# BÀI THU HOẠCH & PHẢN BIỆN (REFLECTION) - LAB 19
**Học viên:** Vũ Duy Linh  
**Project:** Đánh giá GraphRAG vs Flat RAG trên tập dữ liệu Tech Company Corpus (Wikipedia)

## 1. Tóm tắt quá trình thực nghiệm
Trong bài Lab này, tôi đã xây dựng thành công một pipeline RAG hoàn chỉnh và mở rộng tự động lấy dữ liệu:
- Tự động thu thập (crawl) tóm tắt các trang Wikipedia của 13 công ty công nghệ lớn.
- Sử dụng LLM (Groq: Llama-3.3-70b-versatile) để phân tích và trích xuất các bộ ba thực thể (Knowledge Triples: Subject - Relation - Object).
- Xây dựng Đồ thị tri thức (Knowledge Graph) với `networkx` và nhúng văn bản (Embeddings) bằng mô hình local `Ollama` vào ChromaDB.
- Tiến hành chạy benchmark 16 câu hỏi phức tạp để đối chiếu hiệu năng giữa **Flat RAG** (tìm kiếm vector truyền thống) và **GraphRAG** (tìm kiếm dựa trên đồ thị 2-hop).
- **Chi phí**: Quá trình extract và build graph tiêu tốn khoảng `21.16 giây` và sử dụng `22788 tokens` của LLM.

## 2. Phân tích điểm khác biệt giữa Flat RAG và GraphRAG (Dựa trên report)
Kết quả từ 16 câu hỏi benchmark (`report.md`) đã minh họa rất rõ rệt sự khác biệt về bản chất của hai hệ thống:

### 2.1. Điểm yếu trí mạng của Flat RAG
Flat RAG chủ yếu dựa vào độ tương đồng Cosine (Cosine Similarity) để kéo các đoạn văn bản (chunks) gần với câu hỏi nhất. Hệ thống này liên tục thất bại ở hầu hết các câu hỏi (Trả lời *"Không có thông tin..."* ở các Câu 1, 2, 3, 5, 9, 12, 13, 14, 15). 
- **Phân mảnh ngữ cảnh:** Văn bản được cắt thành chunk khiến các thông tin không có từ khóa tương đồng (Lexical Match / Semantic Match) với câu hỏi bị ChromaDB loại bỏ.
- **Kém ở Multi-hop Query:** Với câu hỏi như *"Elon Musk có liên quan đến những công ty nào trong danh sách này?"* (Câu 13), Flat RAG không thể tổng hợp thông tin từ nhiều documents khác nhau do bị giới hạn bởi tham số `top_k` của vector database.

### 2.2. Sự vượt trội của GraphRAG
Ngược lại, GraphRAG đã hoàn thành xuất sắc các câu hỏi trên nhờ tiếp cận theo hướng "truy xuất mạng lưới thực thể". Hệ thống này xác định Node chính trong câu hỏi, sau đó duyệt 2-hop (2 bước) để gom các Node lân cận. Nhờ vậy:
- **Khả năng tổng hợp thông tin phân tán**: Ở Câu 13, từ node `Elon Musk`, đồ thị dễ dàng lần theo các cạnh (Edges) để lôi ra toàn bộ cụm `SpaceX, OpenAI, PayPal, Tesla Motors` dù chúng nằm ở các trang Wikipedia khác nhau.
- **Khắc phục "ảo giác"**: Ngữ cảnh lấy từ Graph luôn là tập hợp các sự kiện cô đọng `(Entity A -> Relation -> Entity B)`. Nó giúp LLM đi thẳng vào trọng tâm (Ví dụ Câu 14: Apple -> Trụ sở -> Cupertino), tránh việc LLM phải tự bịa ra thông tin.

### 2.3. Hạn chế còn tồn tại của GraphRAG
Dù xuất sắc, GraphRAG bộc lộ 2 điểm yếu cần lưu tâm trong quá trình thực hành:
1. **Phụ thuộc hoàn toàn vào khâu Extract (Indexing)**: Một bất ngờ ở Câu 16 (Mark Zuckerberg là CEO tập đoàn nào?), GraphRAG lại trả lời là *không có thông tin*, trong khi Flat RAG lại trả lời đúng. Nguyên nhân do ở bước Indexing, LLM trích xuất có thể đã **bỏ sót** không đưa thông tin `(Mark Zuckerberg, CEO, Meta)` vào đồ thị. Flat RAG làm việc với văn bản thô nên không bị dính lỗi "loss of information" này.
2. **Chi phí thời gian & tiền bạc lớn**: Mất hơn 22,000 tokens chỉ để trích xuất đồ thị cho 13 đoạn văn tóm tắt. Nếu dự án có hàng triệu văn bản, quá trình tạo GraphRAG sẽ vô cùng tốn kém và mất thời gian so với nhúng Vector của Flat RAG.

## 3. Bài học rút ra & Hướng phát triển
- Không có mô hình nào hoàn hảo tuyệt đối: GraphRAG mạnh ở khả năng kết nối và lập luận đa chiều (Multi-hop), còn Flat RAG mạnh ở khả năng tra cứu văn bản thô đầy đủ, chi phí rẻ.
- **Kiến trúc tối ưu (Hybrid RAG / Cascade Retrieval)**: Trên thực tế công nghiệp, hệ thống nên kết hợp cả hai. Dùng Vector Search (BM25 + Semantic) kết hợp với Graph Traversal để vừa tránh mất mát thông tin (lossy extraction), vừa duy trì được mạng lưới logic thực thể. (LightRAG là một kiến trúc tiêu biểu cho hướng đi này).
- Trong tương lai, để giảm chi phí tạo đồ thị, có thể ứng dụng các SLM (Small Language Models) hoặc tinh chỉnh chunk size thông minh hơn thay vì chạy LLM khổng lồ cho toàn bộ corpus thô.
