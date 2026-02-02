"""Gym-like backtesting environment scaffold.

This module provides a minimal `BacktestEnv` with the common `reset()` and
`step(action)` interface so it can be used as a Gym environment by RL agents
once `gym` is available. The scaffold uses synthetic data and is intentionally
lightweight — replace with a wrapper over the project's backtesting engine for
real training.
"""


import numpy as np

try:
    import gym
    from gym import spaces
except Exception:
    gym = None
    spaces = None


if gym is not None:

    class BacktestEnv(gym.Env):
        metadata = {"render.modes": ["human"]}

        def __init__(self, seq_len: int = 12, n_features: int = 6, n_steps: int = 500):
            super().__init__()
            self.seq_len = seq_len
            self.n_features = n_features
            self.n_steps = n_steps
            self._pos = 0
            self._t = 0
            self._data = self._generate_data()
            # Gym spaces
            low = -np.inf * np.ones((self.seq_len, self.n_features), dtype=float)
            high = np.inf * np.ones((self.seq_len, self.n_features), dtype=float)
            self.observation_space = spaces.Box(low=low, high=high, dtype=float)
            self.action_space = spaces.Discrete(3)

        def _generate_data(self):
            # Synthetic price feature series
            return np.random.randn(self.n_steps, self.seq_len, self.n_features).astype(float)

        def reset(self) -> np.ndarray:
            self._t = 0
            self._pos = 0
            return self._data[self._t]

        def step(self, action: int) -> tuple[np.ndarray, float, bool, dict]:
            """Apply action and return (obs, reward, done, info)."""
            reward = float(
                np.random.randn() * 0.01
                + (0.001 if action == 1 else (-0.001 if action == 2 else 0.0))
            )
            self._t += 1
            done = self._t >= (self.n_steps - 1)
            obs = self._data[self._t] if not done else self._data[-1]
            info = {}
            return obs, reward, done, info

        def render(self, mode="human"):
            print(f"Step {self._t}/{self.n_steps}")

else:

    class BacktestEnv:
        """Minimal backtest environment with Gym-like API.

        Observations: vector of recent price features
        Actions: discrete {0: hold, 1: buy, 2: sell}
        Reward: simulated PnL for action at step
        """

        def __init__(self, seq_len: int = 12, n_features: int = 6, n_steps: int = 500):
            self.seq_len = seq_len
            self.n_features = n_features
            self.n_steps = n_steps
            self._pos = 0
            self._t = 0
            self._data = self._generate_data()
            # Gym compatibility (if gym installed)
            if spaces is not None:
                low = -np.inf * np.ones((self.seq_len, self.n_features), dtype=float)
                high = np.inf * np.ones((self.seq_len, self.n_features), dtype=float)
                self.observation_space = spaces.Box(low=low, high=high, dtype=float)
                self.action_space = spaces.Discrete(3)
            else:
                self.observation_space = None
                self.action_space = None

        def _generate_data(self):
            # Synthetic price feature series
            return np.random.randn(self.n_steps, self.seq_len, self.n_features).astype(float)

        def reset(self) -> np.ndarray:
            self._t = 0
            self._pos = 0
            return self._data[self._t]

        def step(self, action: int) -> tuple[np.ndarray, float, bool, dict]:
            """Apply action and return (obs, reward, done, info)."""
            # Simple synthetic reward: random centered around action
            reward = float(
                np.random.randn() * 0.01
                + (0.001 if action == 1 else (-0.001 if action == 2 else 0.0))
            )
            self._t += 1
            done = self._t >= (self.n_steps - 1)
            obs = self._data[self._t] if not done else self._data[-1]
            info = {}
            return obs, reward, done, info

        def render(self):
            print(f"Step {self._t}/{self.n_steps}")

    """Minimal backtest environment with Gym-like API.

    Observations: vector of recent price features
    Actions: discrete {0: hold, 1: buy, 2: sell}
    Reward: simulated PnL for action at step
    """

    def __init__(self, seq_len: int = 12, n_features: int = 6, n_steps: int = 500):
        self.seq_len = seq_len
        self.n_features = n_features
        self.n_steps = n_steps
        self._pos = 0
        self._t = 0
        self._data = self._generate_data()
        # Gym compatibility (if gym installed)
        if spaces is not None:
            low = -np.inf * np.ones((self.seq_len, self.n_features), dtype=float)
            high = np.inf * np.ones((self.seq_len, self.n_features), dtype=float)
            self.observation_space = spaces.Box(low=low, high=high, dtype=float)
            self.action_space = spaces.Discrete(3)
        else:
            self.observation_space = None
            self.action_space = None

    def _generate_data(self):
        # Synthetic price feature series
        return np.random.randn(self.n_steps, self.seq_len, self.n_features).astype(float)

    def reset(self) -> np.ndarray:
        self._t = 0
        self._pos = 0
        return self._data[self._t]

    def step(self, action: int) -> tuple[np.ndarray, float, bool, dict]:
        """Apply action and return (obs, reward, done, info)."""
        # Simple synthetic reward: random centered around action
        reward = float(
            np.random.randn() * 0.01 + (0.001 if action == 1 else (-0.001 if action == 2 else 0.0))
        )
        self._t += 1
        done = self._t >= (self.n_steps - 1)
        obs = self._data[self._t] if not done else self._data[-1]
        info = {}
        return obs, reward, done, info

    def render(self):
        print(f"Step {self._t}/{self.n_steps}")
