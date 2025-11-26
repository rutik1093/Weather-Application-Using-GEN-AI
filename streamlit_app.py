import streamlit as st
import tempfile
import os

from langsmith import Client
from langsmith.run_helpers import trace  

from app.langgraph_builder import build_workflow

client = Client()

st.set_page_config(page_title="AI Pipeline Demo", layout="centered")
st.title("Weather Application")

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

    state = {"query": query, "pdf_path": pdf_path}

   
    with trace(
        name="User Query Execution",
        inputs=state,
        project="Weather-RAG-App"
    ) as run:
        result = workflow.invoke(state)
        run.end(outputs=result)

    st.markdown("### Answer:")
    st.write(result.get("response"))


# Remove PDF
if pdf_path and st.button("Remove PDF"):
    os.remove(pdf_path)
    st.success("Removed PDF.")
