# src/trading_phantom/analytics/transfer_learning.py

"""
Sistema de Transferencia de Conocimiento.

Permite que el conocimiento aprendido por RandomForest
sea accedido y utilizado por futuras IAs (LSTM, RL, Transformers).
"""

import json
import logging
from pathlib import Path
from typing import Dict, Optional, Any, List
import numpy as np

logger = logging.getLogger(__name__)


class TransferLearningPipeline:
    """
    Gestiona la transferencia de conocimiento entre modelos.
    
    Uso:
        pipeline = TransferLearningPipeline()
        
        # Guardar conocimiento del RF
        pipeline.export_rf_knowledge(rf_model, X_train, y_train, feature_names)
        
        # En el futuro, una IA puede hacer:
        knowledge = pipeline.import_knowledge()
        lstm = MyLSTMWithKnowledge(knowledge)
    """
    
    def __init__(self, kb_dir: str = 'data/knowledge_base'):
        self.kb_dir = Path(kb_dir)
        self.kb_dir.mkdir(parents=True, exist_ok=True)
    
    def export_rf_knowledge(self, rf_model, X_train: np.ndarray, y_train: np.ndarray,
                           X_val: np.ndarray, y_val: np.ndarray,
                           feature_names: List[str],
                           class_names: List[str],
                           trades_history: Optional[List[Dict]] = None) -> Dict:
        """
        Exporta TODO el conocimiento del RandomForest a la Knowledge Base.
        
        Esto es llamado después de entrenar el RF.
        """
        from .knowledge_base import KnowledgeBase
        
        logger.info("📚 Exportando conocimiento del RandomForest...")
        kb = KnowledgeBase(str(self.kb_dir))
        
        # 1. Feature importance
        kb.save_feature_importance(rf_model, feature_names)
        
        # 2. Feature embeddings
        kb.save_feature_embeddings(rf_model, X_train, feature_names)
        
        # 3. Correlation matrix
        kb.save_correlation_matrix(X_train, feature_names)
        
        # 4. Decision patterns
        kb.save_decision_patterns(rf_model, feature_names)
        
        # 5. Performance metrics
        y_pred = rf_model.predict(X_val)
        kb.save_performance_metrics(rf_model, X_val, y_val, y_pred)
        
        # 6. Training data stats
        kb.save_training_data_stats(X_train, y_train, feature_names, class_names)
        
        # 7. Trade patterns (si hay)
        if trades_history:
            kb.save_trade_patterns(trades_history)
        
        # 8. Guardar modelo y escalador
        kb.save_model(rf_model)
        
        logger.info("✅ Conocimiento exportado completamente")
        return kb.get_summary()
    
    def import_knowledge(self) -> Dict[str, Any]:
        """
        Importa TODO el conocimiento guardado.
        
        Las futuras IAs llaman esto para acceder al conocimiento del RF.
        """
        from .knowledge_base import KnowledgeBase
        
        kb = KnowledgeBase(str(self.kb_dir))
        
        knowledge = {
            'feature_importance': kb.get_feature_importance(),
            'embeddings': kb.get_feature_embeddings(),
            'correlation_matrix': kb.get_correlation_matrix(),
            'decision_patterns': kb.get_decision_patterns(),
            'performance_metrics': kb.get_performance_metrics(),
            'model': kb.load_model(),
            'scaler': kb.load_scaler()
        }
        
        logger.info("📖 Conocimiento importado correctamente")
        return knowledge
    
    def get_top_features(self, n: int = 5) -> List[str]:
        """Obtiene los N features más importantes"""
        from .knowledge_base import KnowledgeBase
        kb = KnowledgeBase(str(self.kb_dir))
        importance = kb.get_feature_importance()
        
        if importance:
            return importance.get('top_5_features', [])[:n]
        return []
    
    def get_model_confidence(self) -> str:
        """¿Cuán confiable es el conocimiento del RF?"""
        from .knowledge_base import KnowledgeBase
        kb = KnowledgeBase(str(self.kb_dir))
        metrics = kb.get_performance_metrics()
        
        if metrics:
            return metrics.get('model_confidence', 'UNKNOWN')
        return 'NO_DATA'
    
    def create_knowledge_transfer_guide(self) -> str:
        """
        Crea un documento guía para futuras IAs.
        Explica qué conocimiento está disponible y cómo usarlo.
        """
        from .knowledge_base import KnowledgeBase
        
        kb = KnowledgeBase(str(self.kb_dir))
        summary = kb.get_summary()
        
        guide = f"""
# 📚 GUÍA DE TRANSFERENCIA DE CONOCIMIENTO
## Trading Phantom v1.1.0

Generado: {summary['metadata']['last_updated']}

## ✅ Conocimiento Disponible

### 1. Feature Importance
- Archivo: {self.kb_dir}/feature_importance.json
- Contiene: Ranking de qué features son más importantes para la predicción
- Usa en IA: Inicializa pesos de atención, selecciona features top

### 2. Feature Embeddings
- Archivo: {self.kb_dir}/feature_embeddings.json
- Contiene: Estadísticas de features (mean, std, min, max)
- Usa en IA: Normaliza datos de entrada de la misma forma que RF

### 3. Correlation Matrix
- Archivo: {self.kb_dir}/correlation_matrix.json
- Contiene: Relaciones entre features (qué features son redundantes)
- Usa en IA: Identifica features colineales, evita duplicados

### 4. Decision Patterns
- Archivo: {self.kb_dir}/decision_patterns.json
- Contiene: Reglas extraídas de árboles del RF (ej: Si X>threshold → COMPRAR)
- Usa en IA: Inicializa lógica simbólica, validación

### 5. Performance Metrics
- Archivo: {self.kb_dir}/performance_metrics.json
- Contiene: Accuracy, Precision, Recall, F1-Score del RF
- Usa en IA: Benchmark, detección de degradación

### 6. Training Data Stats
- Archivo: {self.kb_dir}/training_data/feature_stats.json
- Contiene: Distribución de datos de entrenamiento
- Usa en IA: Data augmentation, anomaly detection

### 7. Trade Patterns
- Archivo: {self.kb_dir}/trade_patterns/
- Contiene: Análisis de trades ganadores vs perdedores
- Usa en IA: Refuerzo positivo, RL rewards

## 🤖 Cómo Usarlo en una IA Futura

### Opción A: LSTM con Knowledge Transfer
```python
from trading_phantom.analytics.transfer_learning import TransferLearningPipeline

pipeline = TransferLearningPipeline()
knowledge = pipeline.import_knowledge()

# LSTM hereda top features del RF
top_features = knowledge['feature_importance']['top_5_features']
model_confidence = knowledge['performance_metrics']['accuracy']

lstm = MyLSTMWithKB(
    input_features=top_features,
    initial_confidence=model_confidence
)
```

### Opción B: RL con Knowledge Transfer
```python
# Q-Learning inicializa valores usando patterns del RF
patterns = knowledge['decision_patterns']
q_table = initialize_from_patterns(patterns)

rl_agent = QLearningWithKB(q_table)
```

### Opción C: Ensemble (RF + Nueva IA)
```python
# Combina RF + LSTM para decisiones
rf_pred = knowledge['model'].predict(X)
lstm_pred = lstm.predict(X)

ensemble_pred = (rf_pred + lstm_pred) / 2
```

## 📊 Estadísticas Actuales

- Accuracy del RF: {summary.get('performance_metrics', {}).get('accuracy', 'N/A')}
- Features Disponibles: {len(summary.get('feature_importance', {}).get('features', []))}
- Trades Analizados: {summary.get('trade_patterns', {}).get('total_trades_analyzed', 0)}
- Confidence: {summary.get('performance_metrics', {}).get('model_confidence', 'UNKNOWN')}

## 🔄 Workflow Recomendado

1. **Hoy**: RF genera conocimiento → Knowledge Base
2. **Semana 1-2**: LSTM hereda del RF, entrena adicional
3. **Semana 3-4**: RL aprende desde rewards de trades reales
4. **Semana 5+**: Ensemble de RF + LSTM + RL

## ⚠️ Notas Importantes

- El escalador (feature_scaler.pkl) es CRÍTICO: las futuras IAs deben usarlo
- Si cambias features, regenera el KB completo
- Performance metrics indican confiabilidad del conocimiento
- Trade patterns revelan sesgos de horarios/símbolos

---
Documentación generada automáticamente.
Para más info: ver README.md o ARQUITECTURA_MODULAR.md
"""
        
        path = self.kb_dir / 'KNOWLEDGE_TRANSFER_GUIDE.md'
        with open(path, 'w', encoding='utf-8') as f:
            f.write(guide)
        
        logger.info(f"📖 Guía de transferencia creada: {path}")
        return guide


# ============================================================
# FUNCIONES HELPER PARA SCRIPTS
# ============================================================

def quick_export_knowledge(rf_model, X_train, y_train, X_val, y_val, 
                          feature_names, class_names, trades_history=None):
    """
    Helper para exportar conocimiento rápidamente.
    
    Uso en ml_train.py:
        pipeline = quick_export_knowledge(...)
    """
    pipeline = TransferLearningPipeline()
    summary = pipeline.export_rf_knowledge(
        rf_model, X_train, y_train, X_val, y_val,
        feature_names, class_names, trades_history
    )
    return pipeline


def quick_import_knowledge():
    """
    Helper para importar conocimiento rápidamente.
    
    Uso en futuro IA:
        knowledge = quick_import_knowledge()
        lstm = MyLSTM(knowledge)
    """
    pipeline = TransferLearningPipeline()
    return pipeline.import_knowledge()
