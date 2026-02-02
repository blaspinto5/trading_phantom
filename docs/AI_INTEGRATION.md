% AI Integration Plan for Trading Phantom

This document summarizes the LSTM vs Reinforcement Learning recommendations and provides concrete next steps and code scaffolding included in this repo.

Summary
- Start with a supervised LSTM prototype (fast to implement) using historical OHLCV + engineered indicators.
- In parallel design an RL agent (PPO / DQN / SAC) that can be trained in the backtesting engine as an environment.
- Combine both in a hybrid ensemble: LSTM as feature extractor / predictor, RL agent for action selection and position sizing.

Files added by the agent
- `src/trading_phantom/analytics/lstm_model.py` — lightweight LSTM wrapper (PyTorch optional). If `torch` missing, functions raise informative error.
- `src/trading_phantom/analytics/rl_agent.py` — RL agent scaffold (stable-baselines3 optional). Graceful fallback if not installed.
- `scripts/train_lstm.py` — CLI stub to run a small training pipeline or to call your real training function.
- `scripts/train_rl.py` — CLI stub to start RL training using backtesting environment (placeholder).
- `requirements-ml.txt` — suggested ML requirements (torch, gym, stable-baselines3). Install only what you need.

Actionable next steps
1. Install ML deps in a separate env: `pip install -r requirements-ml.txt`.
2. Implement dataset extraction in `analytics/data_loader_for_ml()` or reuse `data_loader.py` to provide sequences.
3. Replace the stubbed `train()` methods with real training loops (use GPU when available: `torch.cuda.is_available()`).
4. Add unit/integration tests: small synthetic-data trains for LSTM and a fast unit test for RL agent interface.
5. After validating offline, integrate the trained model into `core/orchestrator.py` using the existing ML hook (`ml.enabled`).

Notes & safety
- RL training must be done in simulation / demo accounts first. Avoid online exploration on real accounts.
- Use versioned model store (`src/data/models/`) to save artifacts (already migrated to joblib).

References
- FinRL, Stable-Baselines3, PyTorch docs (see original attachment for links and references).

If you want, I can now implement a minimal LSTM training loop (PyTorch) that runs on a tiny synthetic dataset and produces a saved model in the model store. Approve to proceed.
