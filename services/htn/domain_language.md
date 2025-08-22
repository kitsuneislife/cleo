# Especificação Inicial — Linguagem de Domínio HTN & GOAP

Este documento define a estrutura mínima para tarefas, operadores e objetivos usados no planejamento hierárquico (HTN) e GOAP do Cleo.

## HTN — Hierarchical Task Networks

### Exemplo de Tarefa
```yaml
- name: MinerarBloco
  subtasks:
    - name: IrAteBloco
    - name: UsarFerramenta
    - name: ColetarDrop
```

### Operador HTN
```yaml
- name: IrAteBloco
  preconditions:
    - agente.pos != bloco.pos
  effects:
    - agente.pos = bloco.pos
```

## GOAP — Goal-Oriented Action Planning

### Objetivo Exemplo
```yaml
- goal: agente.tem_item("diamante")
```

### Operador GOAP
```yaml
- name: MinerarDiamante
  preconditions:
    - agente.pos = bloco_diamante.pos
    - agente.tem_ferramenta("picareta")
  effects:
    - agente.tem_item("diamante")
```

## Notas
- A linguagem pode ser expandida para YAML, JSON ou PDDL conforme necessidade.
- Recomenda-se manter exemplos simples e incrementais para facilitar testes e integração.
