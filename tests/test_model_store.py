import shutil
from pathlib import Path

import pytest


def test_save_and_load_latest_tmpdir(tmp_path):
    # Prepare a temporary models dir
    models_dir = tmp_path / "models"
    models_dir.mkdir()

    # Import functions under test
    from trading_phantom.analytics.model_store import (
        save_model_versioned,
    )

    model_data = {
        "model": {"dummy": True},
        "metrics": {"accuracy": 0.42},
        "model_type": "test_dummy",
    }

    # Save several versions
    p1 = save_model_versioned(model_data, base_name="tst", models_dir=str(models_dir), keep=2)
    p2 = save_model_versioned(model_data, base_name="tst", models_dir=str(models_dir), keep=2)

    # Ensure files exist
    assert p1.exists() or p2.exists()

    # load_latest_model should find the latest file
    # monkeypatch default path by moving generated index into expected location
    # The function load_latest_model defaults to src/data/models, so copy files
    dest = Path("src/data/models_test_for_ci")
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    for f in models_dir.iterdir():
        if f.is_file():
            shutil.copy(f, dest / f.name)

    # Now load using the explicit dir by calling the loader directly
    loaded = None
    from trading_phantom.analytics.model_store import load_latest_model as loader

    loaded = loader(models_dir=str(dest))
    assert loaded is not None
    assert loaded.get("metrics", {}).get("accuracy") == pytest.approx(0.42)
