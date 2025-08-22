def test_goap_plan():
    from services.goap.planner import GOAPPlanner
    planner = GOAPPlanner()
    plan = planner.plan("Diamante")
    assert plan == ["MinerarDiamante", "ColetarDrop"]
