def test_htn_plan():
    from services.htn.planner import HTNPlanner
    planner = HTNPlanner()
    plan = planner.plan("MinerarBloco")
    assert plan == ["IrAteBloco", "UsarFerramenta", "ColetarDrop"]
