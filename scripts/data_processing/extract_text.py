"""Extract text from raw documents and produce processed files and chunks.json"""
import os
from pathlib import Path


def extract_all(raw_dir="data/raw", out_dir="data/processed"):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    # placeholder: copy text files or extract from PDFs
    for p in Path(raw_dir).glob("**/*"):
        if p.suffix.lower() in [".txt"]:
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
            out_path = Path(out_dir) / p.name
            with open(out_path, "w", encoding="utf-8") as o:
                o.write(text)


if __name__ == "__main__":
    extract_all()
