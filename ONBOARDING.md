# 快速上手（For colleagues）

本指南面向新加入的同事，帮助在 Windows（PowerShell）环境下快速配置并运行本项目的开发/演示环境。

注意：项目中已提供两条环境搭建路线：推荐使用 Conda（便于 GPU/Faiss），若无 Conda 可使用 `venv`。

先决条件
- Python 3.10+
- Git
- 可选：Conda (Miniconda/Anaconda) — 若需 GPU / faiss-cuda 推荐使用

1. 克隆仓库

```powershell
git clone <repo-url>
cd JSJSJDS
```

2A. 推荐（Conda）

```powershell
cd /d D:\Gitproject\JSJSJDS
conda env create -f environment.yml
conda activate jsjsjds
# 确保 pip 依赖也安装完整
python -m pip install -r requirements.txt
python -m pip list
```

说明：若需要 GPU 版 Faiss，请在 Linux + Conda 下安装 `faiss-cuda`（例如 `conda install -c pytorch faiss-cuda cudatoolkit=12.1`，依据你本机 CUDA 版本）。

2B. 备用（venv）

```powershell
cd /d D:\Gitproject\JSJSJDS
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
python -m pip install -U pip setuptools wheel
python -m pip install -r requirements.txt
python -m pip list
```

3. 配置 Hugging Face Token（可选，下载大型受限模型时需要）

```powershell
#$env:HF_TOKEN = "hf_xxx..."   # 临时设置
setx HF_TOKEN "hf_xxx..."    # 保存到用户环境（重启终端后生效）
```

4. 下载并验证模型（推荐先用小模型做本地验证）

- 已包含的测试脚本：
  - `scripts/models/download_and_test_models.py` — 下载并测试嵌入模型（all-MiniLM-L6-v2）并尝试下载 ChatGLM3（若无 token 会受限）。
  - `scripts/models/download_and_test_small_generator.py` — 下载并测试小型生成模型 `EleutherAI/gpt-neo-125M`（快速且占用小，推荐开发阶段使用）。

在激活环境后运行：

```powershell
. .\.venv\Scripts\Activate.ps1    # 或 conda activate jsjsjds
python scripts\models\download_and_test_small_generator.py
python scripts\models\download_and_test_models.py   # 如需尝试 ChatGLM3-6B，请预先设置 HF_TOKEN
```

模型文件保存位置：
- 嵌入模型：`models/embeddings/all-MiniLM-L6-v2`
- 小型生成模型：`models/generators/gpt-neo-125M`

注意：ChatGLM3-6B 为大型模型（需数十 GB 磁盘），无 HF_TOKEN 时可能失败或被限速，建议先用小模型开发。

5. 数据准备（示例流程）

```powershell
. .\.venv\Scripts\Activate.ps1
python scripts\data_processing\extract_text.py   # 将 data/raw 中的 txt 提取到 data/processed（目前只处理 txt）
python scripts\data_processing\split_chunks.py   # 根据 config 切分并生成 data/chunks.json
```

6. 构建向量索引（占位脚本）

当前脚本为占位：`scripts/indexing/build_index.py`。实现流程通常为：读取 `data/chunks.json` → 调用嵌入模型生成向量 → 使用 Faiss 构建索引 → 保存到 `data/vector_store/`。

运行示例（占位）：

```powershell
python scripts\indexing\build_index.py
```

7. 运行后端/前端演示

- 后端（FastAPI）示例：

```powershell
# 运行 uvicorn（示例路由为 backend.api.v1.routes）
python -m uvicorn backend.api.v1.routes:app --reload --port 8000
```

- 前端（Streamlit demo）：

```powershell
streamlit run frontend/streamlit_app/app.py
```

8. 常见问题与提示

- 下载 Hugging Face 模型慢或失败：设置 `HF_TOKEN` 或使用稳定网络/镜像。若模型私有或 gated，需要相应权限。  
- Windows 上对 symlink 支持有限，Hugging Face 缓存可能提示警告（可忽略或启用开发者模式）。
- Faiss GPU：Windows 下 pip 通常没有 `faiss-cuda`，需在 Linux + Conda 下安装。  
- 模型、索引和数据文件较大，请勿提交到 Git；仓库中已有 `.gitignore` 排除这些文件。

9. 后续建议

- 本地开发优先使用小型生成模型完成端到端流程（摄取→索引→检索→生成），评估后再在服务器/云上部署 ChatGLM3-6B 或更大模型。  
- 我可以帮你把小模型接入后端 API，并改造 `frontend/streamlit_app/app.py` 做演示（需要我做请回复“接入小模型”）。

如需我为团队执行 `git init` 并提交初次 commit，或为同事生成一份精简的 README（包含上述命令），请告诉我。
