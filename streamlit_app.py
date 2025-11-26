# streamlit_app.py
import streamlit as st
from app.langgraph_builder import build_workflow
import tempfile, os

st.set_page_config(page_title="AI Pipeline Demo", layout="centered")
st.title("PDF Question Answering + Weather App")

workflow = build_workflow()

uploaded = st.file_uploader("Upload PDF (optional)", type=["pdf"])
pdf_path = None

if uploaded:
    tf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tf.write(uploaded.read())
    tf.close()
    pdf_path = tf.name
    st.success("PDF uploaded.")

query = st.text_input("Ask something:")

if st.button("Get Answer") and query.strip():


    
    state = {
        "query": query,
        "pdf_path": pdf_path  
    }
    
    res = workflow.invoke(state)
    st.markdown("**Answer:**")
    st.write(res.get("response"))

if pdf_path and st.button("Remove PDF"):
    os.remove(pdf_path)
    st.success("PDF removed.")
