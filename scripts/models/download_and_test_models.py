import os
import logging
from pathlib import Path

LOG_PATH = Path("logs")
LOG_PATH.mkdir(exist_ok=True)
logging.basicConfig(filename=LOG_PATH / "model_download.log", level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def download_embedding():
    try:
        logging.info("Starting download of embedding model: all-MiniLM-L6-v2")
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        out = Path('models/embeddings/all-MiniLM-L6-v2')
        out.mkdir(parents=True, exist_ok=True)
        model.save(str(out))
        logging.info("Saved embedding model to %s", out)
        # quick load test
        model2 = SentenceTransformer(str(out))
        v = model2.encode(["测试句子"], show_progress_bar=False)
        logging.info("Embedding test vector shape: %s", getattr(v, 'shape', str(type(v))))
        return True
    except Exception as e:
        logging.exception("Embedding model download or load failed: %s", e)
        return False


def download_generator():
    # Try ChatGLM3-6B (trust_remote_code may be required)
    repo_candidates = [
        'THUDM/chatglm3-6b',
        'THUDM/chatglm3-6b-int4',
        'THUDM/chatglm3-6b-qlora',
    ]
    from transformers import AutoTokenizer, AutoModel
    for repo in repo_candidates:
        try:
            logging.info("Attempting to download generator model: %s", repo)
            tok = AutoTokenizer.from_pretrained(repo, trust_remote_code=True)
            model = AutoModel.from_pretrained(repo, trust_remote_code=True, low_cpu_mem_usage=True)
            out = Path('models/generators') / repo.replace('/', '_')
            out.mkdir(parents=True, exist_ok=True)
            tok.save_pretrained(out)
            try:
                model.save_pretrained(out)
            except Exception:
                logging.warning("Model.save_pretrained failed; model may be large or not serializable")
            logging.info("Downloaded generator model %s to %s", repo, out)
            # quick inference test if small: generate a tokenized input and forward
            try:
                inputs = tok("测试", return_tensors='pt')
                outputs = model(**inputs)
                logging.info("Generator forward output keys: %s", list(outputs.keys()) if hasattr(outputs, 'keys') else str(type(outputs)))
            except Exception as e:
                logging.warning("Quick forward pass failed: %s", e)
            return True
        except Exception as e:
            logging.exception("Failed to download/load %s: %s", repo, e)
    return False


def main():
    Path('models/embeddings').mkdir(parents=True, exist_ok=True)
    Path('models/generators').mkdir(parents=True, exist_ok=True)
    ok1 = download_embedding()
    ok2 = download_generator()
    logging.info('Embedding download success: %s, Generator download success: %s', ok1, ok2)
    print('Done. See logs/model_download.log for details.')


if __name__ == '__main__':
    main()
