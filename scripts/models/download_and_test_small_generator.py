import logging
from pathlib import Path

LOG_PATH = Path("logs")
LOG_PATH.mkdir(exist_ok=True)
logging.basicConfig(filename=LOG_PATH / "small_model_download.log", level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')


def download_and_test():
    try:
        logging.info("Start download/test of EleutherAI/gpt-neo-125M")
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch

        model_name = "EleutherAI/gpt-neo-125M"
        tok = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)

        out = Path('models/generators/gpt-neo-125M')
        out.mkdir(parents=True, exist_ok=True)
        tok.save_pretrained(out)
        try:
            model.save_pretrained(out)
        except Exception:
            logging.warning("Model.save_pretrained not supported for this model in this env")

        # quick generation test
        inputs = tok("你好，介绍一下自己。", return_tensors='pt')
        outputs = model.generate(**inputs, max_new_tokens=32)
        text = tok.batch_decode(outputs, skip_special_tokens=True)[0]
        logging.info("Generation output: %s", text)
        print("Generation test output:\n", text)
        return True
    except Exception as e:
        logging.exception("Small model download/test failed: %s", e)
        print("Failed: ", e)
        return False


if __name__ == '__main__':
    download_and_test()
