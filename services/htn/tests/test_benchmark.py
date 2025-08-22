import time
from services.htn.planner import HTNPlanner

def test_htn_latency():
    planner = HTNPlanner()
    start = time.time()
    for _ in range(1000):
        planner.plan("MinerarBloco")
    elapsed = time.time() - start
    print(f"HTN latency for 1000 plans: {elapsed:.4f}s")
    assert elapsed < 1.0
