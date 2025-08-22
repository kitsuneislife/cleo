"""
Mock de integração HTN+GOAP+Control para Cleo.
"""
from services.htn.planner import HTNPlanner
from services.goap.planner import GOAPPlanner

class ControlMock:
    def __init__(self):
        self.htn = HTNPlanner()
        self.goap = GOAPPlanner()
    def run(self, goal):
        htn_plan = self.htn.plan(goal)
        goap_plan = self.goap.plan(goal)
        return htn_plan + goap_plan
