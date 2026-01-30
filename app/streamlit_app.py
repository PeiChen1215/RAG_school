import streamlit as st
from pathlib import Path
import subprocess
import os

st.set_page_config(page_title='Campus RAG Demo', layout='wide')

st.title('Campus RAG — 可检索问答原型')

uploaded = st.file_uploader('上传 PDF / TXT 文件（可多选）', accept_multiple_files=True)
if 'indexed' not in st.session_state:
    st.session_state['indexed'] = False

if st.button('Ingest and build index'):
    files = []
    Path('data').mkdir(exist_ok=True)
    for f in uploaded:
        out_path = Path('data') / f.name
        with open(out_path, 'wb') as wf:
            wf.write(f.getbuffer())
        files.append(str(out_path))
    if files:
        st.info('Running ingest...')
        # run ingest
        cmd = f"{os.sys.executable} -m src.ingest {' '.join(files)}"
        st.write(cmd)
        subprocess.run(cmd, shell=True)
        st.info('Building embeddings and index...')
        subprocess.run(f"{os.sys.executable} -m src.embed_index", shell=True)
        st.session_state['indexed'] = True
        st.success('Index built')

if st.session_state['indexed']:
    st.subheader('问答')
    question = st.text_input('输入问题')
    if st.button('查询') and question:
        st.info('查询中...')
        # call RAG
        import src.qa as qa
        rag = qa.RAGPipeline()
        res = rag.query(question)
        st.markdown('**答案：**')
        st.write(res['answer'])
        st.markdown('**证据段（Top）**')
        for e in res['evidence'][:5]:
            meta = e.get('meta', {})
            st.write('-', meta.get('source', 'unknown'))
            st.write(e['text'][:500] + ('...' if len(e['text'])>500 else ''))

st.sidebar.markdown('---')
st.sidebar.info('先上传文件并点击 `Ingest and build index`，再在主界面提问。')
