import faiss
import numpy as np
import pickle
from typing import List

INDEX_FILE = "question_index.faiss"
MAPPING_FILE = "question_map.pkl"  # maps index -> question_id

class QuestionIndex:
    def __init__(self, dim):
        self.dim = dim
        try:
            self.index = faiss.read_index(INDEX_FILE)
            with open(MAPPING_FILE, "rb") as f:
                self.id_map = pickle.load(f)
        except Exception:
            self.index = faiss.IndexFlatIP(dim)  # inner product on normalized vectors == cosine
            self.id_map = []

    def add(self, vecs: np.ndarray, q_ids: List[int]):
        # vecs shape (n, dim), must be normalized for cosine sim
        faiss.normalize_L2(vecs)
        self.index.add(vecs)
        self.id_map.extend(q_ids)
        self._persist()

    def search(self, vec: np.ndarray, top_k=5):
        faiss.normalize_L2(vec)
        D, I = self.index.search(vec, top_k)
        # D: similarity scores (cosine), I: indices
        results = []
        for dist, idx in zip(D[0], I[0]):
            if idx == -1 or idx >= len(self.id_map):
                continue
            results.append((self.id_map[idx], float(dist)))
        return results

    def _persist(self):
        faiss.write_index(self.index, INDEX_FILE)
        with open(MAPPING_FILE, "wb") as f:
            pickle.dump(self.id_map, f)
