"""Training utilities: cross-validation, fit and evaluate helpers.

These helpers centralize common training steps so scripts can call them
and keep a single implementation for metrics calculation.
"""

from typing import Any

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import cross_val_score


def run_cross_validation(model, X, y, cv_folds=5, scoring="accuracy") -> dict[str, Any]:
    scores = cross_val_score(model, X, y, cv=cv_folds, scoring=scoring)
    return {"cv_scores": scores, "cv_mean": float(scores.mean()), "cv_std": float(scores.std())}


def fit_and_evaluate(model, X_train, X_test, y_train, y_test) -> dict[str, Any]:
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    # some models have predict_proba
    try:
        y_proba = model.predict_proba(X_test)[:, 1]
    except Exception:
        y_proba = np.array([1.0 if p == 1 else 0.0 for p in y_pred])

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    roc_auc = roc_auc_score(y_test, y_proba) if len(set(y_test)) > 1 else 0.0

    return {
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "roc_auc": float(roc_auc),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
    }
