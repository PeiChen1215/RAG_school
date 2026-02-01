"""RAG orchestration scaffold"""
def run_rag(question, retriever, generator, k=5):
    """Retrieve top-k and call generator. Placeholder implementation."""
    docs = retriever.retrieve(question, k=k)
    context = "\n\n".join(d['text'] for d in docs)
    answer = generator.generate(question, context)
    return {"answer": answer, "sources": docs}
