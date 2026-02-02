import json
import pickle
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import joblib


def _timestamp() -> str:
    return datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")


def save_model_versioned(
    model_data: dict[str, Any],
    base_name: str = "advanced_model",
    models_dir: str = "src/data/models",
    keep: int = 5,
) -> Path:
    dst = Path(models_dir)
    dst.mkdir(parents=True, exist_ok=True)

    ts = _timestamp()
    filename = f"{base_name}_{ts}.joblib"
    out_path = dst / filename

    # Use joblib for more robust model serialization (compatible with scikit-learn)
    try:
        joblib.dump(model_data, out_path)
    except Exception:
        # Fallback to pickle if joblib fails for any reason
        with open(out_path, "wb") as f:
            pickle.dump(model_data, f)

    index_path = dst / "models_index.json"
    entry = {
        "filename": filename,
        "path": str(out_path.as_posix()),
        "timestamp": ts,
        "metrics": model_data.get("metrics", {}),
        "model_type": model_data.get("model_type"),
    }

    try:
        if index_path.exists():
            with open(index_path, encoding="utf-8") as f:
                index = json.load(f)
        else:
            index = []
    except Exception:
        index = []

    index.insert(0, entry)

    if len(index) > keep:
        to_remove = index[keep:]
        index = index[:keep]
        for rem in to_remove:
            p = Path(rem.get("path", ""))
            try:
                if p.exists():
                    p.unlink()
            except Exception:
                pass

    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    latest_path = dst / "latest_model.json"
    with open(latest_path, "w", encoding="utf-8") as f:
        json.dump(entry, f, indent=2)

    return out_path


def load_latest_model(models_dir: str = "src/data/models") -> Optional[dict[str, Any]]:
    dst = Path(models_dir)
    latest_path = dst / "latest_model.json"
    if not latest_path.exists():
        return None

    try:
        with open(latest_path, encoding="utf-8") as f:
            entry = json.load(f)
        p = Path(entry.get("path"))
        if not p.exists():
            return None
        # Prefer joblib format; fall back to pickle for older files
        try:
            data = joblib.load(p)
            return data
        except Exception:
            try:
                with open(p, "rb") as f:
                    data = pickle.load(f)
                return data
            except Exception:
                return None
    except Exception:
        return None
