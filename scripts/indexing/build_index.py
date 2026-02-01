"""Build vector index scaffold (uses sentence-transformers/faiss)"""
def build_index(chunks_file="data/chunks.json", index_out="data/vector_store/faiss.index"):
    # placeholder: load chunks, compute embeddings, build faiss index
    print("TODO: build index from", chunks_file)


if __name__ == "__main__":
    build_index()
