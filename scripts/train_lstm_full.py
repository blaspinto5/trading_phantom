#!/usr/bin/env python3
"""Train a minimal LSTM and save a versioned artifact into the model store.

This script uses the `LSTMModel` scaffold and the project's `model_store`
to save a joblib-versioned model artifact. It uses a tiny synthetic dataset
so it can run quickly as a smoke test. If `torch` is not installed the script
prints a clear message and exits.
"""
import sys
from pathlib import Path

# Ensure package imports use `src/`
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import argparse

import numpy as np

from trading_phantom.analytics.lstm_model import LSTMModel

try:
    from trading_phantom.ml.store.model_store import save_model_versioned
except Exception:
    # fallback import path if shim exists elsewhere
    from trading_phantom.analytics.model_store import (
        save_model_versioned,  # type: ignore
    )


def make_dummy_sequence_data(n_samples=200, seq_len=12, n_features=6):
    X = np.random.randn(n_samples, seq_len, n_features).astype(float)
    y = (np.random.rand(n_samples) > 0.5).astype(float)
    return X, y


def main():
    parser = argparse.ArgumentParser(description="Train minimal LSTM and save to model store")
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--base-name", type=str, default="lstm_model")
    parser.add_argument("--keep", type=int, default=5)
    args = parser.parse_args()

    X, y = make_dummy_sequence_data()

    model = LSTMModel()
    try:
        res = model.train(X, y, epochs=args.epochs)
    except ImportError as e:
        print("Dependency missing:", e)
        print(
            "Install torch to run this trainer, or run the lightweight stub in scripts/train_lstm.py"
        )
        return

    # Prepare artifact metadata and state for saving.
    # Prefer saving model state_dict and metadata rather than raw torch objects.
    artifact = {
        "framework": "pytorch",
        "model_type": "lstm_minimal",
        "metrics": res,
        "timestamp": __import__("datetime").datetime.utcnow().isoformat(),
    }

    # If the trained object exposes a state dict, include it; otherwise include the object.
    try:
        # Attempt to include state_dict (best practice)
        sd = None
        if hasattr(model, "model") and hasattr(model.model, "state_dict"):
            sd = model.model.state_dict()
            artifact["model_state_dict"] = sd
        else:
            artifact["model_object"] = model
    except Exception:
        artifact["model_object"] = model

    # Save versioned artifact
    out_path = save_model_versioned(artifact, base_name=args.base_name, keep=args.keep)
    print(f"Saved artifact to: {out_path}")


if __name__ == "__main__":
    main()
