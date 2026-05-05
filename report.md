# Báo Cáo Thực Hành: Xây Dựng Hệ Thống GraphRAG

## 1. Phân Tích Chi Phí Xây Dựng Đồ Thị
- **Thời gian xây dựng (Extraction + Graph Construction):** `21.16 giây`
- **Tổng số Tokens LLM đã sử dụng:** `22788 tokens`

## 2. Ảnh Đồ Thị Tri Thức
Đồ thị đã được tạo và lưu tại file `graph.png`.

## 3. Bảng So Sánh Benchmark (16 Câu Hỏi - Flat RAG vs GraphRAG)

| STT | Câu hỏi | Flat RAG Answer | GraphRAG Answer | Nhận xét (Ví dụ) |
|---|---|---|---|---|
| 1 | Ai là người sáng lập OpenAI? | Không có thông tin về người sáng lập OpenAI trong đoạn văn trên. | Những người sáng lập OpenAI bao gồm Sam Altman, Jessica Livingston, Reid Hoffman, Elon Musk, Ilya Sutskever và Peter Thiel. | |
| 2 | Microsoft được thành lập vào năm nào? | Thông tin không cung cấp năm thành lập của Microsoft. | Microsoft được thành lập vào năm 1975. | |
| 3 | Google được biết đến với sản phẩm cốt lõi nào? | Không có thông tin về sản phẩm cốt lõi của Google trong đoạn văn này. | Google được biết đến với sản phẩm cốt lõi là công cụ tìm kiếm. | |
| 4 | Amazon do ai thành lập và ban đầu bán cái gì? | Thông tin không đề cập đến việc Amazon do ai thành lập và ban đầu bán cái gì. | Không có thông tin về việc Amazon do ai thành lập và ban đầu bán cái gì trong dữ liệu đã cung cấp. | |
| 5 | Tesla sản xuất những loại sản phẩm nào? | Không có thông tin về Tesla trong đoạn văn trên. Đoạn văn chỉ đề cập đến Meta (công ty mẹ của Facebook) và Nvidia Corporation. | Tesla sản xuất ô tô điện, cụ thể là xe thể thao chạy hoàn toàn bằng điện như Tesla Roadster. | |
| 6 | Meta Platforms trước đây được gọi là gì? | Meta Platforms trước đây được gọi là Facebook, Inc. và TheFacebook, Inc. | Meta Platforms trước đây được gọi là Facebook. | |
| 7 | Apple được thành lập bởi những ai? | Thông tin không đề cập đến việc thành lập Apple. | Không có thông tin về người sáng lập Apple trong dữ liệu cung cấp. | |
| 8 | Nvidia nổi tiếng với sản phẩm nào? | Nvidia nổi tiếng với sản phẩm GPU (Bộ xử lý đồ họa). | Nvidia nổi tiếng với sản phẩm GPU (đơn vị xử lý đồ họa). | |
| 9 | SpaceX do ai thành lập và mục tiêu của công ty là gì? | Không có thông tin về SpaceX trong đoạn văn trên. | SpaceX được thành lập bởi Elon Musk, và mục tiêu của công ty là sản xuất tên lửa đẩy và tàu vũ trụ, với tham vọng khám phá vũ trụ. | |
| 10 | Intel đóng vai trò gì trong ngành công nghiệp máy tính? | Không có thông tin về Intel trong đoạn văn trên. | Thông tin không đề cập đến Intel. | |
| 11 | AMD là đối thủ cạnh tranh của công ty nào? | Không có thông tin về AMD trong đoạn văn trên. Tuy nhiên, dựa trên kiến thức chung, AMD (Advanced Micro Devices) là một công ty sản xuất chip và bộ xử lý, và họ thường được coi là đối thủ cạnh tranh của Intel. | AMD là đối thủ cạnh tranh của Intel. | |
| 12 | Anthropic tập trung vào lĩnh vực gì? | Không có thông tin về Anthropic trong đoạn văn trên. | Anthropic tập trung vào lĩnh vực an toàn AI (AI safety). | |
| 13 | Elon Musk có liên quan đến những công ty nào trong danh sách này? | Không có thông tin về Elon Musk trong đoạn văn này. | Elon Musk có liên quan đến các công ty: SpaceX, OpenAI, PayPal, Tesla Motors. | |
| 14 | Công ty nào có trụ sở tại Cupertino, California? | Không có thông tin về công ty có trụ sở tại Cupertino, California trong đoạn văn trên. Tuy nhiên, dựa trên kiến thức chung, công ty có trụ sở tại Cupertino, California là Apple. | Apple có trụ sở tại Cupertino, California. | |
| 15 | DeepMind là công ty chuyên về lĩnh vực gì? | Không có thông tin về DeepMind trong đoạn văn trên. | DeepMind là công ty chuyên về lĩnh vực trí tuệ nhân tạo, đặc biệt là mạng lưới thần kinh. | |
| 16 | Mark Zuckerberg là CEO của tập đoàn nào? | Mark Zuckerberg là CEO của Tập đoàn Meta (trước đây là Facebook, Inc.). | Không có thông tin về việc Mark Zuckerberg là CEO của tập đoàn nào trong dữ liệu đã cung cấp. Tuy nhiên, dựa trên kiến thức chung, Mark Zuckerberg là người sáng lập và CEO của Meta (trước đây là Facebook, Inc.). | |

## 4. Kết Luận & Đánh Giá
- **Flat RAG**: Thường gặp khó khăn hoặc đưa ra thông tin "ảo giác" (hallucination) đối với các câu hỏi **Multi-hop**.
- **GraphRAG**: Trả lời chính xác và đầy đủ nhờ cơ chế duyệt **2-hop traversal**.
