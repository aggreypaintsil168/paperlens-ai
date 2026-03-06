from typing import List, Tuple
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def top_k_chunks(
    query_vec: np.ndarray,
    doc_vecs: np.ndarray,
    chunks: List[str],
    k: int = 5
) -> List[Tuple[int, float, str]]:
    # query_vec shape: (d,) -> (1, d)
    sims = cosine_similarity(query_vec.reshape(1, -1), doc_vecs).flatten()
    top_idx = np.argsort(sims)[::-1][:k]

    results = []
    for idx in top_idx:
        results.append((int(idx), float(sims[idx]), chunks[int(idx)]))
    return results