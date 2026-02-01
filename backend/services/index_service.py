"""Index management scaffold"""
class IndexService:
    def __init__(self, index_path=None):
        self.index_path = index_path

    def build(self, vectors, metadata):
        pass

    def save(self, path=None):
        pass

    def load(self, path=None):
        pass
