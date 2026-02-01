"""Split processed texts into chunks and produce chunks.json"""
from pathlib import Path
import json


def split_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


def build_chunks(processed_dir="data/processed", out_file="data/chunks.json"):
    items = []
    for p in Path(processed_dir).glob("*.txt"):
        text = p.read_text(encoding='utf-8')
        segs = split_text(text)
        for i, s in enumerate(segs):
            items.append({"doc": p.name, "segment_id": f"{p.stem}-{i}", "text": s})
    Path(out_file).parent.mkdir(parents=True, exist_ok=True)
    Path(out_file).write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == "__main__":
    build_chunks()
