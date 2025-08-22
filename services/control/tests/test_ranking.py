from services.control.decision import rank_operators


def test_rank_operators_basic():
    ops = rank_operators(b"{}");
    assert isinstance(ops, list)
    assert len(ops) == 2
    assert ops[0]["utility"] >= ops[1]["utility"]
