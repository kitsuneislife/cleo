"""In-memory vector DB used for development and unit tests.
Provides store(id, embedding, metadata) and query(embedding, top_k).
Not suitable for production — use Qdrant/Milvus in prod.
"""
from typing import List, Dict, Any
import math

_STORE: Dict[str, Dict[str, Any]] = {}

def _dot(a: List[float], b: List[float]) -> float:
    return sum(x*y for x,y in zip(a,b))

def _norm(a: List[float]) -> float:
    return math.sqrt(sum(x*x for x in a))

def cosine_similarity(a: List[float], b: List[float]) -> float:
    na = _norm(a)
    nb = _norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return _dot(a,b) / (na*nb)

def store(id: str, embedding: List[float], metadata: Dict[str, Any]) -> bool:
    if not isinstance(embedding, list) or len(embedding) == 0:
        raise ValueError('embedding must be a non-empty list')
    _STORE[id] = {'embedding': embedding, 'metadata': metadata}
    return True

def query(embedding: List[float], top_k: int = 10) -> List[Dict[str, Any]]:
    if not isinstance(embedding, list) or len(embedding) == 0:
        raise ValueError('embedding must be a non-empty list')
    scores = []
    for id, doc in _STORE.items():
        try:
            score = cosine_similarity(embedding, doc['embedding'])
        except Exception:
            score = 0.0
        scores.append((score, id, doc['metadata']))
    scores.sort(key=lambda x: x[0], reverse=True)
    return [{'id': id, 'score': score, 'metadata': meta} for score, id, meta in scores[:top_k]]

def clear():
    _STORE.clear()
