from services.icm.icm import intrinsic_reward

def test_intrinsic_reward():
    r = intrinsic_reward(0.1)
    assert 0.0 <= r <= 1.0
    r2 = intrinsic_reward(1000.0)
    assert r2 <= 1.0
