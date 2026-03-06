import streamlit as st
import numpy as np

from utils.pdf_reader import extract_text_from_pdf
from utils.chunking import chunk_text
from utils.gemini_client import get_gemini_models
from utils.embeddings import embed_texts, embed_query
from utils.retrieval import top_k_chunks
from utils.prompts import build_rag_prompt

st.set_page_config(page_title="PaperLens AI (Pro)", layout="wide")

st.title("📄 PaperLens AI (Pro)")
st.write("Upload a research paper PDF, then chat with it using Google Gemini + retrieval (RAG).")

# Session state storage
if "chunks" not in st.session_state:
    st.session_state.chunks = None
if "doc_vecs" not in st.session_state:
    st.session_state.doc_vecs = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar controls
with st.sidebar:
    st.header("Settings")
    k = st.slider("How many sources to retrieve (top-k)", min_value=2, max_value=10, value=5, step=1)
    chunk_size = st.slider("Chunk size (characters)", min_value=600, max_value=2000, value=1200, step=100)
    overlap = st.slider("Overlap (characters)", min_value=0, max_value=500, value=200, step=50)

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

# Build index button
if uploaded_file is not None:
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("1) Extract + Chunk Paper"):
            raw_text = extract_text_from_pdf(uploaded_file)
            chunks = chunk_text(raw_text, chunk_size=chunk_size, overlap=overlap)

            st.session_state.chunks = chunks
            st.session_state.doc_vecs = None
            st.success(f"Done! Extracted and chunked into {len(chunks)} chunks.")

    with col2:
        if st.button("2) Create Embeddings (Build Search Index)"):
            if not st.session_state.chunks:
                st.error("Please extract + chunk the paper first.")
            else:
                with st.spinner("Embedding chunks..."):
                    # embed documents
                    doc_vecs = embed_texts(st.session_state.chunks)
                    st.session_state.doc_vecs = doc_vecs
                st.success("Embeddings created! You can now chat with the paper.")

st.divider()

# Chat UI
st.subheader("💬 Chat with the Paper")

user_question = st.text_input("Ask a question about the paper:")

if st.button("Ask Gemini"):
    if not user_question.strip():
        st.warning("Type a question first.")
    elif st.session_state.chunks is None:
        st.error("Upload a PDF and click: Extract + Chunk Paper.")
    elif st.session_state.doc_vecs is None:
        st.error("Click: Create Embeddings (Build Search Index).")
    else:
        chat_model = get_gemini_models()

        with st.spinner("Retrieving sources + asking Gemini..."):
            q_vec = embed_query(user_question)
            retrieved = top_k_chunks(q_vec, st.session_state.doc_vecs, st.session_state.chunks, k=k)

            prompt = build_rag_prompt(user_question, retrieved)
            response = chat_model.generate_content(prompt)
            answer = response.text

        st.session_state.chat_history.append(("You", user_question))
        st.session_state.chat_history.append(("PaperLens AI", answer))

        # Show retrieved sources
        with st.expander("🔎 Sources used (retrieved chunks)"):
            for idx, score, chunk in retrieved:
                st.markdown(f"**SOURCE {idx}** — similarity: `{score:.4f}`")
                st.write(chunk)
                st.divider()

# Display chat history
if st.session_state.chat_history:
    for speaker, msg in st.session_state.chat_history:
        st.markdown(f"**{speaker}:** {msg}")