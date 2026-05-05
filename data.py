import json
import re
import urllib.request
import urllib.parse

print("\n[Data Module] Đang khởi tạo Corpus... (Sẽ mất chút thời gian để crawl dữ liệu thực tế từ Wikipedia)")

def fetch_wikipedia_summary(title, lang="vi"):
    """Gọi Wikipedia API để lấy đoạn tóm tắt mở đầu của một bài viết"""
    url = f"https://{lang}.wikipedia.org/w/api.php?action=query&format=json&titles={urllib.parse.quote(title)}&prop=extracts&exintro=True&explaintext=True"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            pages = data.get("query", {}).get("pages", {})
            for page_id, page_data in pages.items():
                if page_id != "-1":
                    return page_data.get("extract", "")
    except Exception as e:
        print(f"Lỗi khi crawl {title}: {e}")
    return ""

def build_corpus_from_web():
    companies = [
        "OpenAI", "Google", "Microsoft", "Anthropic", "Amazon (công ty)", 
        "Tesla, Inc.", "DeepMind", "Meta Platforms", "Apple Inc.", 
        "Nvidia", "SpaceX", "Intel", "AMD"
    ]
    
    corpus_docs = []
    
    for company in companies:
        # Ưu tiên lấy tiếng Việt, nếu không có hoặc bài quá ngắn thì lấy tiếng Anh
        text = fetch_wikipedia_summary(company, lang="vi")
        if not text or len(text) < 100:
            text = fetch_wikipedia_summary(company, lang="en")
            
        if text:
            # Tách thành các câu dựa vào dấu câu
            sentences = re.split(r'(?<=[.!?])\s+', text)
            # Chọn 3-4 câu đầu tiên để tiết kiệm Token và tránh Rate Limit của LLM API
            valid_sentences = [s.strip() for s in sentences if len(s.strip()) > 30][:4]
            if valid_sentences:
                # Gộp lại thành 1 Document (chunk) duy nhất cho mỗi công ty
                doc_text = " ".join(valid_sentences)
                corpus_docs.append(doc_text)
                print(f" + Đã lấy và đóng gói thông tin trang: {company}")
                
    print(f"🚀 Hoàn tất crawl! Tổng số chunks (documents): {len(corpus_docs)}.\n")
    return corpus_docs

# Khởi tạo Corpus thực tế từ Web
CORPUS = build_corpus_from_web()

# Fallback dự phòng nếu máy không có mạng
if not CORPUS:
    CORPUS = [
        "OpenAI được thành lập bởi Sam Altman và Elon Musk vào năm 2015.",
        "Google được thành lập bởi Larry Page và Sergey Brin vào năm 1998."
    ]

# Danh sách câu hỏi đánh giá đã được điều chỉnh để phù hợp với lượng dữ liệu thực tế
BENCHMARK_QUESTIONS = [
    "Ai là người sáng lập OpenAI?",
    "Microsoft được thành lập vào năm nào?",
    "Google được biết đến với sản phẩm cốt lõi nào?",
    "Amazon do ai thành lập và ban đầu bán cái gì?",
    "Tesla sản xuất những loại sản phẩm nào?",
    "Meta Platforms trước đây được gọi là gì?",
    "Apple được thành lập bởi những ai?",
    "Nvidia nổi tiếng với sản phẩm nào?",
    "SpaceX do ai thành lập và mục tiêu của công ty là gì?",
    "Intel đóng vai trò gì trong ngành công nghiệp máy tính?",
    "AMD là đối thủ cạnh tranh của công ty nào?",
    "Anthropic tập trung vào lĩnh vực gì?",
    "Elon Musk có liên quan đến những công ty nào trong danh sách này?",
    "Công ty nào có trụ sở tại Cupertino, California?",
    "DeepMind là công ty chuyên về lĩnh vực gì?",
    "Mark Zuckerberg là CEO của tập đoàn nào?"
]
