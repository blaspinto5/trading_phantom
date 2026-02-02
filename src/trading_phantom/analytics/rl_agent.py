"""Scaffold RL agent wrapper.

This module provides a small wrapper around RL agents. If `stable_baselines3`
and `gym` are available the `train()` method can be implemented to run an
agent in a Gym-like environment built on top of the backtesting engine.

When dependencies are missing, the class provides clear error messages and a
minimal interface usable for integration/testing.
"""

from typing import Any


class RLAgent:
    def __init__(self, algo: str = "PPO"):
        self.algo = algo
        self.model = None
        self.is_trained = False

    def _sb3_available(self) -> bool:
        try:

            return True
        except Exception:
            return False

    def train(self, env, timesteps: int = 1000, **kwargs) -> dict[str, Any]:
        """Train the RL agent in a provided environment.

        `env` should be a Gym-like environment. This is a stub: it will raise
        a helpful message if stable-baselines3 is not installed.
        """
        if not self._sb3_available():
            raise ImportError(
                "stable-baselines3 not installed. Install 'stable-baselines3' to train RL agents."
            )

        from stable_baselines3 import PPO  # type: ignore

        model = PPO("MlpPolicy", env, verbose=1, **kwargs)
        model.learn(total_timesteps=timesteps)
        self.model = model
        self.is_trained = True
        return {"status": "trained", "timesteps": timesteps}

    def act(self, observation):
        if not self.is_trained:
            raise RuntimeError("Agent not trained")
        return self.model.predict(observation)

    def save(self, path: str):
        if not self.is_trained:
            raise RuntimeError("No trained model to save")
        self.model.save(path)

    def load(self, path: str):
        if not self._sb3_available():
            raise ImportError("stable-baselines3 required to load models saved by SB3")
        from stable_baselines3 import PPO  # type: ignore

        self.model = PPO.load(path)
        self.is_trained = True
