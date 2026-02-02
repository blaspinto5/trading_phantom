"""Lightweight LSTM model wrapper (optional PyTorch).

This file provides a minimal, import-safe wrapper around a PyTorch LSTM-based
predictor. If `torch` is not installed, methods raise a clear ImportError message.

Intended use: replace or extend the stubbed training/predict methods with
real dataset/architectures. Saving/loading uses `torch.save`/`torch.load` when
available, otherwise users should install `torch` or use the model-store.
"""

from typing import Any, Optional


class LSTMModel:
    def __init__(self, device: Optional[str] = None):
        self.device = device or (
            "cuda" if self._torch_available() and __import__("torch").cuda.is_available() else "cpu"
        )
        self.model = None
        self.is_trained = False

    def _torch_available(self) -> bool:
        try:

            return True
        except Exception:
            return False

    def train(self, X, y, epochs: int = 1, lr: float = 1e-3) -> dict[str, Any]:
        """Train a lightweight LSTM on data arrays X, y.

        This is a stub: replace with real training loop. Will raise if torch
        is not installed.
        """
        if not self._torch_available():
            raise ImportError("PyTorch is required to train LSTMModel. Install 'torch' and retry.")

        import torch  # type: ignore
        import torch.nn as nn  # type: ignore

        # Minimal stub network (users should replace)
        input_size = X.shape[2] if X.ndim == 3 else X.shape[1]
        hidden_size = 16

        class SmallLSTM(nn.Module):
            def __init__(self, in_size, hid):
                super().__init__()
                self.lstm = nn.LSTM(in_size, hid, batch_first=True)
                self.fc = nn.Linear(hid, 1)

            def forward(self, x):
                out, _ = self.lstm(x)
                out = out[:, -1, :]
                return self.fc(out)

        net = SmallLSTM(input_size, hidden_size).to(self.device)

        # Convert data to tensors
        X_t = torch.tensor(X, dtype=torch.float32).to(self.device)
        y_t = torch.tensor(y, dtype=torch.float32).to(self.device)

        opt = torch.optim.Adam(net.parameters(), lr=lr)
        loss_fn = nn.BCEWithLogitsLoss()

        net.train()
        for _ in range(max(1, int(epochs))):
            opt.zero_grad()
            out = net(X_t)
            loss = loss_fn(out.view(-1), y_t.view(-1))
            loss.backward()
            opt.step()

        self.model = net
        self.is_trained = True
        return {"status": "trained", "loss": float(loss.item())}

    def predict(self, X):
        if not self.is_trained:
            raise RuntimeError("Model not trained")
        if not self._torch_available():
            raise ImportError("PyTorch is required for prediction with LSTMModel.")
        import torch  # type: ignore

        self.model.eval()
        with torch.no_grad():
            X_t = torch.tensor(X, dtype=torch.float32).to(self.device)
            out = self.model(X_t).cpu().numpy()
        return out

    def save(self, path: str):
        if not self._torch_available():
            raise ImportError("PyTorch is required to save LSTMModel with torch.save.")
        import torch  # type: ignore

        torch.save({"model_state_dict": self.model.state_dict()}, path)

    def load(self, path: str):
        if not self._torch_available():
            raise ImportError("PyTorch is required to load LSTMModel with torch.load.")
        import torch  # type: ignore

        # Loading logic must match saved structure; stub assumes SmallLSTM
        data = torch.load(path, map_location=self.device)
        # Users must reconstruct architecture before loading state_dict.
        return data
