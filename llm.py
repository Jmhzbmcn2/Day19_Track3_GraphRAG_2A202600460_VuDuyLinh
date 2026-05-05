import json
import requests
from openai import OpenAI
from chromadb.utils import embedding_functions

from config import GROQ_API_KEY, GROQ_BASE_URL, LLM_MODEL, OLLAMA_URL, OLLAMA_MODEL

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url=GROQ_BASE_URL,
)

class LLMService:
    total_tokens_used = 0

    @classmethod
    def call_llm(cls, prompt, json_mode=False):
        try:
            kwargs = {
                "model": LLM_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0
            }
            if json_mode:
                kwargs["response_format"] = {"type": "json_object"}
                
            response = client.chat.completions.create(**kwargs)
            cls.total_tokens_used += response.usage.total_tokens
            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM Error: {e}")
            return "{}" if json_mode else ""

    @classmethod
    def extract_triples(cls, text):
        prompt = f"""
        Trích xuất các thực thể và quan hệ từ câu sau.
        Trả về định dạng JSON với key 'triples' là một danh sách các mảng 3 phần tử: [Subject, Relation, Object].
        Ví dụ: {{"triples": [["OpenAI", "FOUNDED_BY", "Sam Altman"], ["OpenAI", "FOUNDED_IN", "2015"]]}}
        Câu: "{text}"
        """
        response = cls.call_llm(prompt, json_mode=True)
        try:
            data = json.loads(response)
            return data.get("triples", [])
        except Exception as e:
            print(f"Lỗi parse JSON: {e} cho text: {text}")
            return []

class OllamaEmbeddingFunction(embedding_functions.EmbeddingFunction):
    def __init__(self, model_name=OLLAMA_MODEL, url=OLLAMA_URL):
        self.model_name = model_name
        self.url = url

    def __call__(self, input):
        embeddings = []
        for text in input:
            try:
                response = requests.post(self.url, json={"model": self.model_name, "prompt": text})
                if response.status_code == 200:
                    embeddings.append(response.json()["embedding"])
                else:
                    embeddings.append([0.0] * 768) # Fallback
            except Exception as e:
                print(f"Lỗi kết nối Ollama: {e}. Đảm bảo Ollama đang chạy.")
                embeddings.append([0.0] * 768)
        return embeddings
