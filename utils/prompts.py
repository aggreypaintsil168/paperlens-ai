

def build_rag_prompt(user_question: str, retrieved_chunks: list) -> str:
    # retrieved_chunks: list of (idx, score, chunk_text)
    context_blocks = []
    for idx, score, chunk in retrieved_chunks:
        context_blocks.append(f"[SOURCE {idx}] {chunk}")

    context = "\n\n".join(context_blocks)

    return f"""
You are PaperLens AI. Answer user's question using ONLY the provided sources.
If the sources do not contain the answer, say: "I can't find that in the paper,"

User question:
{user_question}

Sources:
{context}

Rules:
- Be clear and structured.
- Always cite sources like: (SOURCE 12) after the sentence.
"""
