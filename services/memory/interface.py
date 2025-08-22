from services.memory.service import store as _store, query as _query, clear as _clear

def store(id, embedding, metadata):
    return _store(id, embedding, metadata)

def query(embedding, top_k=10):
    return _query(embedding, top_k=top_k)

def clear():
    return _clear()
