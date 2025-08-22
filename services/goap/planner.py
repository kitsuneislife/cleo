"""
Skeleton do GOAP planner para Cleo.
Segue o protocolo: Planejar → Implementar → Testar → Robustecer → Documentar
"""
class GOAPPlanner:
    def __init__(self):
        self.operators = []

    def add_operator(self, op):
        self.operators.append(op)

    def plan(self, goal):
        # Mock: retorna sequência de ações
        return ["MinerarDiamante", "ColetarDrop"]
