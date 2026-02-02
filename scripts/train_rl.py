#!/usr/bin/env python3
"""CLI stub to demonstrate RL agent train hook."""
import argparse

from trading_phantom.analytics.rl_agent import RLAgent


def main():
    parser = argparse.ArgumentParser(description="Train RL agent stub")
    parser.add_argument("--timesteps", type=int, default=1000)
    args = parser.parse_args()

    agent = RLAgent()
    print("This is a scaffold. Provide a Gym-like `env` built on the backtesting engine to train.")
    print(
        "If stable-baselines3 and gym are installed, you can implement environment creation and call agent.train(env, timesteps=...)"
    )


if __name__ == "__main__":
    main()
