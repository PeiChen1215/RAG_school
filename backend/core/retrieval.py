"""Retrieval utilities scaffold"""
class Retriever:
    def __init__(self, index=None):
        self.index = index

    def retrieve(self, query, k=5):
        # return list of dicts: {"id":..., "text":..., "score":...}
        return []
