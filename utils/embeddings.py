from typing import List
import numpy as np
import google.generativeai as genai

def embed_texts(texts: List[str], task_type: str = "SEMANTIC_SIMILARITY") -> np.ndarray:
    vectors = []

    for text in texts:
        result = genai.embed_content(
            model="models/gemini-embedding-001",
            content=text,
            task_type=task_type
        )

        # result is expected to contain one embedding for one input text
        vectors.append(result["embedding"])

    return np.array(vectors, dtype=np.float32)


def embed_query(query: str) -> np.ndarray:
    result = genai.embed_content(
        model="models/gemini-embedding-001",
        content=query,
        task_type="SEMANTIC_SIMILARITY"
    )
    return np.array(result["embedding"], dtype=np.float32)