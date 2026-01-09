# src/trading_phantom/analytics/knowledge_base.py

import json
import logging
import pickle
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

logger = logging.getLogger(__name__)


class KnowledgeBase:
    """
    Sistema de almacenamiento de conocimiento compartido.
    El ML actual (RandomForest) genera conocimiento aquí.
    Futuras IAs lo consumen sin necesidad de reintentar desde cero.

    Estructura:
    data/knowledge_base/
    ├── metadata.json              # Info sobre el KB
    ├── feature_importance.json    # Qué features importan
    ├── feature_embeddings.json    # Representaciones internas
    ├── decision_patterns.json     # Reglas aprendidas
    ├── correlation_matrix.json    # Relaciones entre features
    ├── performance_metrics.json   # Accuracy, precision, recall
    ├── models/
    │   ├── random_forest.pkl      # Modelo actual
    │   └── feature_scaler.pkl     # Escalador (importante!)
    ├── training_data/
    │   ├── feature_stats.json     # Media, std de cada feature
    │   └── class_distribution.json # Balance de clases
    └── trade_patterns/
        ├── winning_patterns.json  # Patrones que ganaron
        └── losing_patterns.json   # Patrones que perdieron
    """

    def __init__(self, kb_dir: str = "data/knowledge_base"):
        self.kb_dir = Path(kb_dir)
        self.kb_dir.mkdir(parents=True, exist_ok=True)

        # Crear subdirectorios
        (self.kb_dir / "models").mkdir(exist_ok=True)
        (self.kb_dir / "training_data").mkdir(exist_ok=True)
        (self.kb_dir / "trade_patterns").mkdir(exist_ok=True)

        self.metadata = self._load_or_create_metadata()

    def _load_or_create_metadata(self) -> Dict:
        """Metadata del KB (cuándo se actualizó, versión, etc)"""
        path = self.kb_dir / "metadata.json"
        if path.exists():
            with open(path) as f:
                return json.load(f)

        metadata = {
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "version": "1.0",
            "knowledge_types": [
                "feature_importance",
                "embeddings",
                "patterns",
                "correlations",
                "performance",
                "trade_insights",
            ],
        }
        self._save_metadata(metadata)
        return metadata

    def _save_metadata(self, data: Dict):
        """Guarda metadata"""
        data["last_updated"] = datetime.now().isoformat()
        with open(self.kb_dir / "metadata.json", "w") as f:
            json.dump(data, f, indent=2)
        self.metadata = data

    # ============================================================
    # FEATURE IMPORTANCE: Qué variables importan más
    # ============================================================

    def save_feature_importance(self, model, feature_names: List[str]) -> Dict:
        """
        Guarda ranking de importancia de features.

        Las futuras IAs sabrán: "Para predecir señal, importa EMA>MACD>RSI"
        """
        importances = model.feature_importances_
        ranking = sorted(
            zip(feature_names, importances), key=lambda x: x[1], reverse=True
        )

        data = {
            "timestamp": datetime.now().isoformat(),
            "features": [f[0] for f in ranking],
            "importance_scores": [float(f[1]) for f in ranking],
            "top_5_features": [f[0] for f in ranking[:5]],
            "bottom_5_features": [f[0] for f in ranking[-5:]],
            "total_features": len(feature_names),
            "model_type": "RandomForestClassifier",
        }

        path = self.kb_dir / "feature_importance.json"
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

        logger.info(f"✅ Feature importance guardada: {path}")
        return data

    # ============================================================
    # FEATURE EMBEDDINGS: Representaciones internas
    # ============================================================

    def save_feature_embeddings(
        self, model, X_train: np.ndarray, feature_names: List[str]
    ) -> Dict:
        """
        Extrae "embeddings" del RF (posiciones en árboles internos).
        Futuras IAs pueden usar esto como inicialización de redes neuronales.
        """
        # Obtener índices de hojas para cada muestra
        leaf_indices = model.apply(X_train)  # shape: (n_samples, n_trees)

        # Calcular "centroide" de cada feature
        embeddings_data = {
            "timestamp": datetime.now().isoformat(),
            "n_samples": X_train.shape[0],
            "n_features": X_train.shape[1],
            "n_trees": model.n_estimators,
            "feature_names": feature_names,
            "leaf_indices_stats": {
                "mean_per_feature": np.mean(X_train, axis=0).tolist(),
                "std_per_feature": np.std(X_train, axis=0).tolist(),
                "min_per_feature": np.min(X_train, axis=0).tolist(),
                "max_per_feature": np.max(X_train, axis=0).tolist(),
            },
            "description": "Statistical embeddings from RandomForest training data",
        }

        path = self.kb_dir / "feature_embeddings.json"
        with open(path, "w") as f:
            json.dump(embeddings_data, f, indent=2)

        logger.info(f"✅ Feature embeddings guardados: {path}")
        return embeddings_data

    # ============================================================
    # CORRELATION MATRIX: Relaciones entre features
    # ============================================================

    def save_correlation_matrix(
        self, X_train: np.ndarray, feature_names: List[str]
    ) -> Dict:
        """
        Matriz de correlación entre features.
        Las futuras IAs entienden qué features son redundantes o complementarios.
        """
        import warnings

        warnings.filterwarnings("ignore")

        # Calcular correlación
        corr_matrix = np.corrcoef(X_train.T)

        # Convertir a dict legible
        corr_dict = {}
        for i, feat1 in enumerate(feature_names):
            corr_dict[feat1] = {}
            for j, feat2 in enumerate(feature_names):
                corr_dict[feat1][feat2] = float(corr_matrix[i, j])

        data = {
            "timestamp": datetime.now().isoformat(),
            "correlation_matrix": corr_dict,
            "features": feature_names,
            "insights": {
                "highly_correlated_pairs": [
                    {
                        "feature_1": feature_names[i],
                        "feature_2": feature_names[j],
                        "correlation": float(corr_matrix[i, j]),
                    }
                    for i in range(len(feature_names))
                    for j in range(i + 1, len(feature_names))
                    if abs(corr_matrix[i, j]) > 0.7
                ][
                    :10
                ]  # Top 10
            },
        }

        path = self.kb_dir / "correlation_matrix.json"
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

        logger.info(f"✅ Correlation matrix guardada: {path}")
        return data

    # ============================================================
    # DECISION PATTERNS: Reglas aprendidas
    # ============================================================

    def save_decision_patterns(self, model, feature_names: List[str]) -> Dict:
        """
        Extrae reglas de decisión del RF.
        Ej: "Si EMA_fast > 100 y RSI < 70 → BUY"

        Futuras IAs pueden usar esto como conocimiento simbólico.
        """
        patterns = []

        # Extraer rules de primeros N árboles
        for tree_idx, tree in enumerate(model.estimators_[:10]):  # primeros 10
            tree_obj = tree.tree_

            # Recorrer nodos del árbol
            def recurse(node, depth=0):
                if tree_obj.feature[node] != -2:  # No es hoja
                    feat_idx = tree_obj.feature[node]
                    thresh = tree_obj.threshold[node]
                    feat_name = feature_names[feat_idx]

                    patterns.append(
                        {
                            "tree_id": int(tree_idx),
                            "depth": int(depth),
                            "feature": feat_name,
                            "threshold": float(thresh),
                            "operator": "<=",
                            "left_child": int(tree_obj.children_left[node]),
                            "right_child": int(tree_obj.children_right[node]),
                        }
                    )

                    recurse(tree_obj.children_left[node], depth + 1)
                    recurse(tree_obj.children_right[node], depth + 1)

            recurse(0)

        # Agrupar por feature
        patterns_by_feature = {}
        for p in patterns:
            feat = p["feature"]
            if feat not in patterns_by_feature:
                patterns_by_feature[feat] = []
            patterns_by_feature[feat].append(p)

        data = {
            "timestamp": datetime.now().isoformat(),
            "total_patterns": len(patterns),
            "patterns_by_feature": {
                feat: len(pats) for feat, pats in patterns_by_feature.items()
            },
            "sample_patterns": patterns[:20],  # Top 20 para visualizar
            "description": "Decision rules extracted from RandomForest trees",
        }

        path = self.kb_dir / "decision_patterns.json"
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

        logger.info(f"✅ Decision patterns guardados: {path}")
        return data

    # ============================================================
    # PERFORMANCE METRICS: Qué tan bien aprendió
    # ============================================================

    def save_performance_metrics(
        self, model, X_val: np.ndarray, y_val: np.ndarray, y_pred: np.ndarray
    ) -> Dict:
        """
        Guarda métricas de performance del modelo.
        Futuras IAs saben cuán confiable es este conocimiento.
        """
        from sklearn.metrics import (accuracy_score, confusion_matrix,
                                     f1_score, precision_score, recall_score)

        metrics = {
            "timestamp": datetime.now().isoformat(),
            "model_type": "RandomForestClassifier",
            "validation_set_size": X_val.shape[0],
            "accuracy": float(accuracy_score(y_val, y_pred)),
            "precision": float(
                precision_score(y_val, y_pred, average="weighted", zero_division=0)
            ),
            "recall": float(
                recall_score(y_val, y_pred, average="weighted", zero_division=0)
            ),
            "f1_score": float(
                f1_score(y_val, y_pred, average="weighted", zero_division=0)
            ),
            "confusion_matrix": confusion_matrix(y_val, y_pred).tolist(),
            "model_confidence": (
                "HIGH" if accuracy_score(y_val, y_pred) > 0.75 else "MEDIUM"
            ),
        }

        path = self.kb_dir / "performance_metrics.json"
        with open(path, "w") as f:
            json.dump(metrics, f, indent=2)

        logger.info(f"✅ Performance metrics guardados: {path}")
        logger.info(f"   Accuracy: {metrics['accuracy']:.2%}")
        logger.info(f"   F1-Score: {metrics['f1_score']:.3f}")

        return metrics

    # ============================================================
    # TRAINING DATA INSIGHTS: Estadísticas de entrenamiento
    # ============================================================

    def save_training_data_stats(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        feature_names: List[str],
        class_names: List[str],
    ) -> Dict:
        """
        Estadísticas del dataset de entrenamiento.
        Futuras IAs entienden la distribución de datos.
        """
        class_dist = {}
        for class_idx, class_name in enumerate(class_names):
            count = np.sum(y_train == class_idx)
            class_dist[class_name] = {
                "count": int(count),
                "percentage": float(count / len(y_train) * 100),
            }

        data = {
            "timestamp": datetime.now().isoformat(),
            "total_samples": len(X_train),
            "total_features": X_train.shape[1],
            "feature_names": feature_names,
            "class_distribution": class_dist,
            "feature_stats": {
                feat: {
                    "mean": float(np.mean(X_train[:, idx])),
                    "std": float(np.std(X_train[:, idx])),
                    "min": float(np.min(X_train[:, idx])),
                    "max": float(np.max(X_train[:, idx])),
                    "median": float(np.median(X_train[:, idx])),
                }
                for idx, feat in enumerate(feature_names)
            },
        }

        path = self.kb_dir / "training_data" / "feature_stats.json"
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

        logger.info(f"✅ Training data stats guardados: {path}")
        return data

    # ============================================================
    # TRADE PATTERNS: Patrones ganadores vs perdedores
    # ============================================================

    def save_trade_patterns(self, trades_history: List[Dict]) -> Dict:
        """
        Analiza trades históricos para identificar patrones.
        Ej: Trades de lunes 10am con RSI<30 ganan 75% de las veces.
        """
        if not trades_history:
            logger.warning("No hay trades históricos para analizar")
            return {}

        winning_trades = [t for t in trades_history if t.get("pnl", 0) > 0]
        losing_trades = [t for t in trades_history if t.get("pnl", 0) <= 0]

        # Estadísticas por patrón
        win_rate = len(winning_trades) / len(trades_history) if trades_history else 0

        patterns = {
            "timestamp": datetime.now().isoformat(),
            "total_trades_analyzed": len(trades_history),
            "winning_trades": len(winning_trades),
            "losing_trades": len(losing_trades),
            "win_rate": float(win_rate),
            "avg_win_pnl": (
                float(np.mean([t.get("pnl", 0) for t in winning_trades]))
                if winning_trades
                else 0
            ),
            "avg_loss_pnl": (
                float(np.mean([t.get("pnl", 0) for t in losing_trades]))
                if losing_trades
                else 0
            ),
            "patterns_by_hour": self._analyze_patterns_by_attribute(
                trades_history, "hour"
            ),
            "patterns_by_symbol": self._analyze_patterns_by_attribute(
                trades_history, "symbol"
            ),
        }

        # Guardar
        with open(self.kb_dir / "trade_patterns" / "winning_patterns.json", "w") as f:
            json.dump(winning_trades[:50], f, indent=2)  # Top 50

        with open(self.kb_dir / "trade_patterns" / "analysis.json", "w") as f:
            json.dump(patterns, f, indent=2)

        logger.info(f"✅ Trade patterns guardados")
        logger.info(f"   Win Rate: {win_rate:.1%}")

        return patterns

    def _analyze_patterns_by_attribute(self, trades: List[Dict], attr: str) -> Dict:
        """Helper para análisis por atributo"""
        analysis = {}
        for trade in trades:
            key = str(trade.get(attr, "unknown"))
            if key not in analysis:
                analysis[key] = {"wins": 0, "losses": 0}

            if trade.get("pnl", 0) > 0:
                analysis[key]["wins"] += 1
            else:
                analysis[key]["losses"] += 1

        # Calcular win rate por key
        for key in analysis:
            total = analysis[key]["wins"] + analysis[key]["losses"]
            analysis[key]["win_rate"] = (
                analysis[key]["wins"] / total if total > 0 else 0
            )

        return analysis

    # ============================================================
    # GUARDADO DE MODELOS Y ESCALADORES
    # ============================================================

    def save_model(self, model, filename: str = "random_forest.pkl"):
        """Guarda el modelo entrenado para referencia"""
        path = self.kb_dir / "models" / filename
        with open(path, "wb") as f:
            pickle.dump(model, f)
        logger.info(f"✅ Modelo guardado: {path}")

    def save_scaler(self, scaler, filename: str = "feature_scaler.pkl"):
        """Guarda el escalador (CRUCIAL para futuras IAs)"""
        path = self.kb_dir / "models" / filename
        with open(path, "wb") as f:
            pickle.dump(scaler, f)
        logger.info(f"✅ Escalador guardado: {path}")

    # ============================================================
    # LECTURA DE CONOCIMIENTO (para futuras IAs)
    # ============================================================

    def get_feature_importance(self) -> Optional[Dict]:
        """Lee importancia de features"""
        path = self.kb_dir / "feature_importance.json"
        if path.exists():
            with open(path) as f:
                return json.load(f)
        return None

    def get_feature_embeddings(self) -> Optional[Dict]:
        """Lee embeddings"""
        path = self.kb_dir / "feature_embeddings.json"
        if path.exists():
            with open(path) as f:
                return json.load(f)
        return None

    def get_correlation_matrix(self) -> Optional[Dict]:
        """Lee matriz de correlación"""
        path = self.kb_dir / "correlation_matrix.json"
        if path.exists():
            with open(path) as f:
                return json.load(f)
        return None

    def get_decision_patterns(self) -> Optional[Dict]:
        """Lee patrones de decisión"""
        path = self.kb_dir / "decision_patterns.json"
        if path.exists():
            with open(path) as f:
                return json.load(f)
        return None

    def get_performance_metrics(self) -> Optional[Dict]:
        """Lee métricas de performance"""
        path = self.kb_dir / "performance_metrics.json"
        if path.exists():
            with open(path) as f:
                return json.load(f)
        return None

    def load_model(self, filename: str = "random_forest.pkl"):
        """Carga el modelo guardado"""
        path = self.kb_dir / "models" / filename
        if path.exists():
            with open(path, "rb") as f:
                return pickle.load(f)
        return None

    def load_scaler(self, filename: str = "feature_scaler.pkl"):
        """Carga el escalador guardado"""
        path = self.kb_dir / "models" / filename
        if path.exists():
            with open(path, "rb") as f:
                return pickle.load(f)
        return None

    # ============================================================
    # RESUMEN GENERAL
    # ============================================================

    def get_summary(self) -> Dict:
        """Resumen de todo el conocimiento disponible"""
        return {
            "metadata": self.metadata,
            "feature_importance": self.get_feature_importance() is not None,
            "embeddings": self.get_feature_embeddings() is not None,
            "correlation_matrix": self.get_correlation_matrix() is not None,
            "decision_patterns": self.get_decision_patterns() is not None,
            "performance_metrics": self.get_performance_metrics(),
            "kb_directory": str(self.kb_dir),
        }
