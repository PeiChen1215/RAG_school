import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from transformers import pipeline
import torch


class RAGPipeline:
    def __init__(self, index_path='data/faiss.index', meta_path='data/metadata.json', embed_model='all-MiniLM-L6-v2', gen_model='google/flan-t5-small'):
        self.index = faiss.read_index(index_path)
        with open(meta_path, 'r', encoding='utf-8') as f:
            self.metas = json.load(f)
        self.embedder = SentenceTransformer(embed_model)
        device = 0 if torch.cuda.is_available() else -1
        self.generator = pipeline('text2text-generation', model=gen_model, device=device)

    def query(self, question: str, top_k: int = 5):
        q_emb = self.embedder.encode([question], convert_to_numpy=True)
        D, I = self.index.search(q_emb, top_k)
        hits = []
        ctx = []
        for idx in I[0]:
            meta = self.metas[idx] if idx < len(self.metas) else {}
            text = meta.get('text', '')
            # meta may not include full text; stored externally in chunks.json if needed
            hits.append({'idx': idx, 'meta': meta})
        # For simplicity, load chunks texts from data/chunks.json
        chunks = json.load(open('data/chunks.json', 'r', encoding='utf-8'))
        contexts = [chunks[i]['text'] for i in I[0]]
        prompt = 'Context:\n' + '\n\n'.join(contexts) + '\n\nQuestion: ' + question + '\nAnswer in 2-3 sentences.'
        out = self.generator(prompt, max_length=256, do_sample=False)
        answer = out[0]['generated_text']
        evidence = []
        for i in I[0]:
            if i < len(chunks):
                evidence.append({'text': chunks[i]['text'], 'meta': chunks[i].get('meta', {})})
        return {'answer': answer, 'evidence': evidence}


if __name__ == '__main__':
    rag = RAGPipeline()
    while True:
        q = input('Question: ')
        if not q.strip():
            break
        res = rag.query(q)
        print('Answer:', res['answer'])
        print('Evidence count:', len(res['evidence']))
