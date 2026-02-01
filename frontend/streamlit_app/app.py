"""Streamlit demo scaffold"""
import streamlit as st


def main():
    st.title("Campus RAG Demo")
    q = st.text_input("输入问题")
    if st.button("查询") and q:
        st.info("TODO: 调用后端查询: {}".format(q))


if __name__ == "__main__":
    main()
