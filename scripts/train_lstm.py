#!/usr/bin/env python3
"""CLI to run a quick LSTM training stub."""
import argparse
from pathlib import Path

import numpy as np

from trading_phantom.analytics.lstm_model import LSTMModel


def make_dummy_sequence_data(n_samples=100, seq_len=10, n_features=4):
    X = np.random.randn(n_samples, seq_len, n_features).astype(float)
    y = (np.random.rand(n_samples) > 0.5).astype(float)
    return X, y


def main():
    parser = argparse.ArgumentParser(description="Train a small LSTM stub")
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--out", type=str, default="src/data/models/lstm_stub.joblib")
    args = parser.parse_args()

    X, y = make_dummy_sequence_data(n_samples=200)

    model = LSTMModel()
    try:
        res = model.train(X, y, epochs=args.epochs)
    except ImportError as e:
        print("Dependency missing:", e)
        return

    # Attempt to save via model_store if available (joblib)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        model.save(str(out_path))
        print(f"Saved LSTM stub to {out_path}")
    except Exception as e:
        print("Could not save model with torch.save:", e)


if __name__ == "__main__":
    main()
