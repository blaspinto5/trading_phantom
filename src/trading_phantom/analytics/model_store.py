"""Compatibility shim: re-export model_store from new ml.store package."""

from trading_phantom.ml.store.model_store import load_latest_model, save_model_versioned

__all__ = ["save_model_versioned", "load_latest_model"]
