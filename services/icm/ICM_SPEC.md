# ICM (Intrinsically-motivated reward) — Spec

Goal: definir sinal de recompensa intrínseca baseado em erro de predição de forward model.

Definition
- Input: estado s_t, ação a_t, estado s_{t+1}
- Prediction error: e = ||s_{t+1} - f(s_t, a_t)||_2
- Reward intrínseca r_i = normalize(clip(log(1 + e), 0, max))

Metrics
- Report mean and std of e per episode
- Track rolling window of r_i to avoid runaway exploration

Implementation
- Provide `services/icm/icm.py` stub that computes `r_i` from tensors/arrays. Keep configurable normalizer and clipping.
