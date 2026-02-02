"""List saved ML models from src/data/models (index)."""

import json
from pathlib import Path


def main(models_dir: str = "src/data/models"):
    p = Path(models_dir)
    idx = p / "models_index.json"
    if not idx.exists():
        print("No index found in", models_dir)
        return
    try:
        with open(idx, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print("Error leyendo index:", e)
        return

    print(f"Modelos guardados en {models_dir}:\n")
    for i, entry in enumerate(data, 1):
        fn = entry.get("filename")
        ts = entry.get("timestamp")
        mt = entry.get("model_type")
        acc = entry.get("metrics", {}).get("accuracy")
        print(f"{i:2d}. {fn}  | type={mt}  | ts={ts}  | acc={acc}")


if __name__ == "__main__":
    main()
