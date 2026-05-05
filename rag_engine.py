import json
import chromadb
from llm import LLMService, OllamaEmbeddingFunction

class FlatRAG:
    def __init__(self, corpus):
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.create_collection(
            name="tech_companies", 
            embedding_function=OllamaEmbeddingFunction()
        )
        self.collection.add(
            documents=corpus,
            ids=[f"doc_{i}" for i in range(len(corpus))]
        )

    def query(self, question):
        try:
            results = self.collection.query(
                query_texts=[question],
                n_results=2
            )
            context = " ".join(results['documents'][0])
            prompt = f"Dựa vào thông tin sau: '{context}', hãy trả lời câu hỏi: '{question}'. Trả lời ngắn gọn và đi thẳng vào vấn đề."
            return LLMService.call_llm(prompt)
        except Exception:
            return "Lỗi Flat RAG."


class GraphRAG:
    def __init__(self, graph):
        self.G = graph

    def query(self, question):
        prompt_entity = f"Trích xuất danh sách các thực thể chính từ câu hỏi sau. Trả về JSON format: {{\"entities\": [\"Entity1\", \"Entity2\"]}}. Câu hỏi: '{question}'"
        res = LLMService.call_llm(prompt_entity, json_mode=True)
        try:
            entities = json.loads(res).get("entities", [])
        except:
            entities = []
            
        context = []
        for entity in entities:
            matched_node = None
            for node in self.G.nodes():
                if entity.lower() in str(node).lower() or str(node).lower() in entity.lower():
                    matched_node = node
                    break
                    
            if matched_node:
                for neighbor in self.G.neighbors(matched_node):
                    rel = self.G[matched_node][neighbor]['label']
                    context.append(f"{matched_node} {rel} {neighbor}")
                    for sec_neighbor in self.G.neighbors(neighbor):
                        rel2 = self.G[neighbor][sec_neighbor]['label']
                        context.append(f"{neighbor} {rel2} {sec_neighbor}")
                        
                for pred in self.G.predecessors(matched_node):
                    rel = self.G[pred][matched_node]['label']
                    context.append(f"{pred} {rel} {matched_node}")
                    for sec_pred in self.G.predecessors(pred):
                        rel2 = self.G[sec_pred][pred]['label']
                        context.append(f"{sec_pred} {rel2} {pred}")
                        
        context = list(set(context))
        context_text = ". ".join(context)
        
        if context_text:
            prompt = f"Dựa vào thông tin từ đồ thị: '{context_text}', hãy trả lời câu hỏi: '{question}'. Trả lời ngắn gọn."
        else:
            prompt = f"Trực tiếp trả lời câu hỏi sau (không tìm thấy thông tin trong knowledge graph): '{question}'. Trả lời ngắn gọn."
            
        return LLMService.call_llm(prompt)
