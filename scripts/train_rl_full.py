#!/usr/bin/env python3
"""Train an RL agent on the BacktestEnv and save a versioned artifact.

If `stable-baselines3` is installed the script will train PPO; otherwise it
performs a lightweight random-policy rollout to produce a baseline artifact.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import argparse

import numpy as np

from trading_phantom.analytics.backtest_env import BacktestEnv
from trading_phantom.analytics.rl_agent import RLAgent

try:
    from trading_phantom.ml.store.model_store import save_model_versioned
except Exception:
    from trading_phantom.analytics.model_store import (
        save_model_versioned,  # type: ignore
    )


def train_random_baseline(env: BacktestEnv, steps: int = 1000):
    total = 0.0
    obs = env.reset()
    for _ in range(steps):
        action = int(np.random.randint(0, 3))
        obs, reward, done, _ = env.step(action)
        total += reward
        if done:
            obs = env.reset()
    return {"avg_reward": float(total / steps), "timesteps": steps}


def main():
    parser = argparse.ArgumentParser(description="Train RL agent prototype")
    parser.add_argument("--timesteps", type=int, default=2000)
    parser.add_argument("--base-name", type=str, default="rl_agent")
    parser.add_argument("--keep", type=int, default=5)
    args = parser.parse_args()

    env = BacktestEnv(n_steps=500)

    agent = RLAgent(algo="PPO")
    artifact = {
        "model_type": "rl_agent_proto",
        "framework": "stable-baselines3-or-random",
        "timestamp": __import__("datetime").datetime.utcnow().isoformat(),
    }

    try:
        # Try to train with stable-baselines3 via RLAgent
        res = agent.train(env, timesteps=args.timesteps)
        artifact["trained"] = True
        artifact["train_result"] = res
        # If the agent produced a stable-baselines3 model, save it separately
        # to avoid pickling non-serializable objects (file handles, envs, etc.).
        try:
            from datetime import datetime

            ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
            models_dir = Path("src") / "data" / "models"
            models_dir.mkdir(parents=True, exist_ok=True)
            sb3_path = models_dir / f"{args.base_name}_{ts}.zip"
            # stable-baselines3 models expose a `save` method
            if hasattr(agent.model, "save"):
                agent.model.save(str(sb3_path))
                artifact["model_file"] = str(sb3_path.as_posix())
            else:
                # Fallback: don't include the model object itself
                artifact["model_file"] = None
        except Exception:
            artifact["model_file"] = None
    except ImportError as e:
        print("stable-baselines3 not available, running random baseline:", e)
        res = train_random_baseline(env, steps=min(args.timesteps, 2000))
        artifact["trained"] = False
        artifact["train_result"] = res

    out_path = save_model_versioned(artifact, base_name=args.base_name, keep=args.keep)
    print(f"Saved RL artifact to: {out_path}")


if __name__ == "__main__":
    main()
