from services.memory.interface import store, query

def test_memory_store_query():
    assert store('id1', [0.1,0.2], {'meta': 'x'})
    res = query([0.1,0.2], top_k=1)
    assert isinstance(res, list)
