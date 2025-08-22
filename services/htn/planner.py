"""
Skeleton do HTN planner para Cleo.
Segue o protocolo: Planejar → Implementar → Testar → Robustecer → Documentar
"""
class HTNPlanner:
    def __init__(self):
        self.operators = []
        self.decomposers = []

    def add_operator(self, op):
        self.operators.append(op)

    def add_decomposer(self, dec):
        self.decomposers.append(dec)

    def plan(self, goal):
        # Mock: retorna plano simples
        return ["IrAteBloco", "UsarFerramenta", "ColetarDrop"]
