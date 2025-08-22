"""
Script para converter episódios MineRL para o formato JSONL usado em `data/worldmodel/validation.jsonl`.

Uso:
  python scripts/convert_minerl_to_validation.py --input <pasta_ou_arquivo_MineRL> --out data/worldmodel/validation.jsonl --max_episodes 50

Requisitos:
- O dataset MineRL deve estar disponível localmente (ex.: pasta com arquivos .npz ou .json).
- O script espera episódios com campos: timestamp, agent_id, pos (x,y,z), meta (opcional).

Exemplo de linha JSONL:
{"timestamp": 123, "agent_id": "Steve", "pos": [0.0, 64.0, 0.0], "meta": {"action": "move"}}
"""
import os
import json
import argparse

# Função de exemplo para converter um episódio MineRL para o formato Cleo
# (Aqui é mock, pois não temos o formato real do MineRL; adapte conforme necessário)
def convert_episode(minerl_episode):
    # Exemplo: minerl_episode = list de dicts com campos 'step', 'agent', 'position', 'action'
    cleo_traj = []
    for frame in minerl_episode:
        cleo_traj.append({
            "timestamp": frame.get("step", 0),
            "agent_id": frame.get("agent", "Steve"),
            "pos": frame.get("position", [0.0, 64.0, 0.0]),
            "meta": {"action": frame.get("action", "noop")}
        })
    return cleo_traj

def main():
    parser = argparse.ArgumentParser(description="Converter MineRL para Cleo JSONL")
    parser.add_argument('--input', required=True, help='Pasta ou arquivo com episódios MineRL')
    parser.add_argument('--out', required=True, help='Arquivo de saída JSONL')
    parser.add_argument('--max_episodes', type=int, default=50, help='Número máximo de episódios a converter')
    args = parser.parse_args()

    episodes = []
    # Se for pasta, procura arquivos .json; se for arquivo, carrega direto
    if os.path.isdir(args.input):
        files = [f for f in os.listdir(args.input) if f.endswith('.json')]
        if not files:
            print(f"Nenhum arquivo .json encontrado em {args.input}")
            return
        for fname in files[:args.max_episodes]:
            with open(os.path.join(args.input, fname), 'r') as f:
                minerl_episode = json.load(f)
                episodes.append(minerl_episode)
    elif os.path.isfile(args.input):
        with open(args.input, 'r') as f:
            minerl_episode = json.load(f)
            episodes.append(minerl_episode)
    else:
        print(f"Input {args.input} não encontrado como pasta ou arquivo.")
        return

    with open(args.out, 'w') as fout:
        count = 0
        for ep in episodes:
            cleo_traj = convert_episode(ep)
            for frame in cleo_traj:
                fout.write(json.dumps(frame) + '\n')
                count += 1
    print(f"Wrote {count} frames to {args.out} from {len(episodes)} episodes.")

if __name__ == "__main__":
    main()
