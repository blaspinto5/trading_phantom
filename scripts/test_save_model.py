"""Script de prueba: guarda un modelo dummy usando model_store.save_model_versioned
"""


from trading_phantom.analytics.model_store import save_model_versioned


def main():
    model_data = {
        "model": {"type": "dummy"},
        "scaler": None,
        "feature_names": ["f1", "f2"],
        "metrics": {"accuracy": 0.5, "n_samples": 10},
        "model_type": "dummy",
    }

    out = save_model_versioned(
        model_data, base_name="test_dummy_model", models_dir="src/data/models", keep=3
    )
    print(f"Saved test model to: {out}")


if __name__ == "__main__":
    main()
