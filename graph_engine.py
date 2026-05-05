import networkx as nx
import matplotlib.pyplot as plt
import time
from llm import LLMService

class GraphBuilder:
    def __init__(self):
        self.G = nx.DiGraph()
        self.build_time = 0

    def build_graph(self, corpus):
        start_time = time.time()
        for doc in corpus:
            triples = LLMService.extract_triples(doc)
            for triple in triples:
                if len(triple) == 3:
                    subj, rel, obj = triple
                    self.G.add_edge(subj, obj, label=rel)
        self.build_time = time.time() - start_time
        return self.G

    def visualize(self, filename="graph.png"):
        plt.figure(figsize=(16, 12))
        pos = nx.spring_layout(self.G, k=0.8, seed=42)
        nx.draw(self.G, pos, with_labels=True, node_color='lightgreen', node_size=2500, font_size=9, font_weight='bold', edge_color='gray', arrows=True)
        edge_labels = nx.get_edge_attributes(self.G, 'label')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, font_size=8, font_color='red')
        plt.title("Tech Company Knowledge Graph")
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Đã lưu ảnh đồ thị vào {filename}")
