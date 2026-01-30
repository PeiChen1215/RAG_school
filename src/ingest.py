import json
from pathlib import Path
from typing import List, Dict
from pypdf import PdfReader


def extract_text_from_pdf(path: str) -> str:
    reader = PdfReader(path)
    parts = []
    for p in reader.pages:
        text = p.extract_text()
        if text:
            parts.append(text)
    return "\n\n".join(parts)


def extract_text_from_txt(path: str) -> str:
    return Path(path).read_text(encoding='utf-8')


def segment_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[Dict]:
    words = text.split()
    chunks = []
    i = 0
    idx = 0
    while i < len(words):
        part = words[i:i+chunk_size]
        chunks.append({
            'id': f'chunk-{idx}',
            'text': ' '.join(part),
            'meta': {}
        })
        i += chunk_size - overlap
        idx += 1
    return chunks


def ingest_files(paths: List[str], out_chunks_path: str = 'data/chunks.json') -> None:
    Path('data').mkdir(exist_ok=True)
    all_chunks = []
    for p in paths:
        pth = Path(p)
        if not pth.exists():
            continue
        if pth.suffix.lower() in ['.pdf']:
            txt = extract_text_from_pdf(str(pth))
        else:
            txt = extract_text_from_txt(str(pth))
        chunks = segment_text(txt)
        # attach source meta
        for c in chunks:
            c['meta']['source'] = pth.name
        all_chunks.extend(chunks)
    Path(out_chunks_path).write_text(json.dumps(all_chunks, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    import sys
    paths = sys.argv[1:]
    if not paths:
        print('Usage: python ingest.py file1.pdf file2.txt ...')
    else:
        ingest_files(paths)
        print('Ingest complete')
