from services.memory.interface import store, query, clear
import pytest

def setup_function():
    clear()

def test_memory_store_query_happy():
    assert store('id1', [0.1,0.2], {'meta': 'x'})
    res = query([0.1,0.2], top_k=1)
    assert isinstance(res, list)
    assert len(res) == 1
    assert res[0]['id'] == 'id1'

def test_query_empty_embedding_raises():
    with pytest.raises(ValueError):
        query([], top_k=1)

def test_store_invalid_embedding_raises():
    with pytest.raises(ValueError):
        store('id2', [], {})

