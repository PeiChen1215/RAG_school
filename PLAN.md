# 校园 RAG 项目计划书

## 一、项目概述
- 名称：Campus RAG（校园可检索问答知识库）
- 目标：把校园文件（公告、课程资料、FAQ、PPT）做成可检索的知识库，支持文件上传、向量检索与检索增强问答（RAG），并提供直观的前端界面以便学生与教职工快速查询。

## 二、核心功能与交付物
- 文档解析与分段（PDF/TXT）
- 向量嵌入与 FAISS 索引
- 检索增强问答（RAG）：返回简短答案 + 证据段落
- 前端演示：Streamlit 页面（上传/构建索引/问答/导出）
- 交付物：代码仓（GitHub）、requirements.txt、示例数据、预构建索引、演示视频（2 分钟）、答辩 PPT、README/用户手册

## 三、成功标准（可量化）
- 功能：支持上传并处理 ≥10 个文档并建立索引
- 准确性：top‑3 证据中 ≥70% 相关性；生成答案人工评分 ≥3.5/5
- 性能：单次问答平均响应 ≤5s（本地）或 ≤10s（云）
- 可复现：评审可通过 README 在本地或云上复现演示

## 四、技术方案要点
- 文档解析：`pypdf` / `pdfplumber` 提取文字，按语义或固定长度切分成段落
- 嵌入：`sentence-transformers/all-MiniLM-L6-v2`（本地）或 OpenAI Embeddings（可选）
- 索引：FAISS（本地持久化）
- 生成：本地 `flan-t5-small`（或 HF Inference）；检索到 top‑k 段落拼接到 prompt
- 前端：Streamlit（上传、触发索引、问答、展示证据）

## 五、工作范围与非功能约束
- 首阶段仅实现文本类文档（PDF/TXT）；语音转写/ASR 属后续扩展
- 本地优先（利用 RTX 4070）；按需使用付费 API（OpenAI/HF）以提升效果

## 六、6 周里程碑（可压缩为 2 周 MVP）
- 预备日（Day0）: 确认团队、权限、GitHub 仓库、环境（CUDA/torch）
- Week1：文档解析 + 分段
  - Day1: 准备示例文档（至少 10 份）并建 repo（已完成）
  - Day2–3: 完成 `ingest.py`（PDF/TXT → 段落 JSON），异常处理
  - Day4–5: 设计分段策略（chunk_size/overlap），生成样本并人工复核
- Week2：嵌入与索引
  - Day1–2: 集成 `sentence-transformers`，实现批量嵌入
  - Day3: 构建 FAISS 索引并持久化（`data/faiss.index`），保存 metadata
  - Day4–5: 简单检索测试与评估（precision@k）
- Week3：RAG 管线
  - Day1–3: 实现 `qa.py`（检索+生成），设计 prompt 模板
  - Day4–5: 答案质量调优（top_k、prompt、生成长度）
- Week4：前端与集成
  - Day1–3: 完成 `streamlit_app.py`，实现上传/构建/问答/导出
  - Day4–5: 集成跳转证据、UI 美化、错误提示
- Week5：测试与优化
  - 性能测试、索引分片、缓存常见查询、显存管理（fp16）
- Week6：材料准备与答辩演练
  - 制作 2 分钟演示视频、PPT、README/用户手册、提交最终代码

## 七、2 周 MVP（快速交付）
- 目标：在 2 周内交付可演示的最小可行产品
  - Week1: 实现 `ingest.py` + `embed_index.py` 并建立索引（本地）
  - Week2: 实现 `qa.py`（本地 flan-t5-small） + `streamlit_app.py`，完成演示脚本

## 八、人员分工（3 人建议）
- 成员 A：数据与后端（`ingest.py`、文档采集/清洗）
- 成员 B：模型与检索（`embed_index.py`、FAISS、`qa.py`）
- 成员 C：前端与集成（`streamlit_app.py`、演示视频、PPT、部署）

## 九、开发流程与分支策略
- 主分支：`main`（用于提交可运行代码/Release）
- 功能分支：`feature/ingest`、`feature/index`、`feature/qa`、`feature/ui`
- Pull Request 流程：代码 review（至少一人 approve）后合并

## 十、运行与部署（快速命令）
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m src.ingest example.pdf
python -m src.embed_index
python -m src.qa   # 本地交互式问答
streamlit run app/streamlit_app.py
```

## 十一、验收与演示脚本（2 分钟）
1. 打开 Streamlit，上传 3–5 份校园文档（10s）
2. 点击 `Ingest`，显示索引构建完成（20s）
3. 输入问题（如：办奖学金需要哪些材料？），点击查询 → 展示答案和证据（30s）
4. 点击证据跳转至原文/时间轴，导出 Markdown（20s）
5. 总结项目价值与技术亮点（20s）

## 十二、风险与应对
- 数据格式不统一 → 强化解析与异常捕获、提供手动校正
- 生成模型偶发错误 → 必须返回证据段并标注置信度；对高风险问题提示人工复核
- 显存/性能限制 → 使用小模型/量化或把部分请求路由到云

## 十三、下一步（建议立即执行）
1. 按本计划把任务分配到每位组员并创建对应功能分支
2. 成员 A 上传首批 10 份示例文档到 `data/` 并运行 `src/ingest.py`
3. 成员 B 构建索引并做一次本地 `src/qa.py` 查询，调优 prompt
4. 成员 C 搭建 Streamlit 页面并准备首轮演示

---
*文件已加入仓库：`PLAN.md`*。
