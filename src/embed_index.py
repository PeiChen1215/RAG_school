import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss


def build_index(chunks_path: str = 'data/chunks.json', model_name: str = 'all-MiniLM-L6-v2', index_path: str = 'data/faiss.index', meta_path: str = 'data/metadata.json'):
    Path('data').mkdir(exist_ok=True)
    with open(chunks_path, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    texts = [c['text'] for c in chunks]
    metas = [c.get('meta', {}) for c in chunks]

    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    faiss.write_index(index, index_path)

    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(metas, f, ensure_ascii=False, indent=2)
    print(f'Index saved to {index_path}, metadata to {meta_path}')


def load_index(index_path: str = 'data/faiss.index'):
    return faiss.read_index(index_path)


if __name__ == '__main__':
    build_index()
