import argparse
import logging

from trading_phantom.analytics.ml_pipeline import StrategyModel
from trading_phantom.analytics.db import init_db
from trading_phantom.analytics.transfer_learning import TransferLearningPipeline

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Entrena el modelo ML y genera Knowledge Base para futuras IAs")
    parser.add_argument("--save", action="store_true", help="(Opcional) Solo muestra métricas, no hace nada extra")
    args = parser.parse_args()

    logger.info("🚀 Iniciando entrenamiento de ML...")
    
    init_db()
    model = StrategyModel()
    res = model.train()
    
    if res.get("status") == "no_data":
        logger.info("⚠️  No hay datos suficientes en DB. Ejecuta el bot o carga trades antes de entrenar.")
        return

    logger.info("✅ Modelo entrenado | accuracy=%.4f | muestras=%s", res.get("accuracy", 0.0), res.get("n_samples"))
    
    # =========================================================
    # 🆕 GENERAR KNOWLEDGE BASE PARA FUTURAS IAs
    # =========================================================
    logger.info("\n📚 Generando Knowledge Base para futuras IAs...")
    
    try:
        # Obtener datos de entrenamiento
        X_train = model.X_train
        y_train = model.y_train
        X_val = model.X_val
        y_val = model.y_val
        feature_names = model.feature_names
        class_names = model.class_names
        
        # Exportar conocimiento
        pipeline = TransferLearningPipeline()
        summary = pipeline.export_rf_knowledge(
            rf_model=model.rf,
            X_train=X_train,
            y_train=y_train,
            X_val=X_val,
            y_val=y_val,
            feature_names=feature_names,
            class_names=class_names,
            trades_history=None  # Opcional: pasar trades si disponibles
        )
        
        logger.info("\n✅ Knowledge Base generada correctamente!")
        logger.info("📂 Ubicación: data/knowledge_base/")
        logger.info("\n📋 Archivos creados:")
        logger.info("   ✓ feature_importance.json (ranking de features)")
        logger.info("   ✓ feature_embeddings.json (estadísticas)")
        logger.info("   ✓ correlation_matrix.json (relaciones)")
        logger.info("   ✓ decision_patterns.json (reglas)")
        logger.info("   ✓ performance_metrics.json (accuracy, precision, recall)")
        logger.info("   ✓ training_data/feature_stats.json (distribución)")
        logger.info("   ✓ models/random_forest.pkl (modelo guardado)")
        logger.info("   ✓ KNOWLEDGE_TRANSFER_GUIDE.md (guía para futuras IAs)")
        
        # Mostrar métricas
        perf = summary.get('performance_metrics', {})
        if perf:
            logger.info("\n📊 Métricas del Modelo:")
            logger.info(f"   • Accuracy:  {perf.get('accuracy', 0):.2%}")
            logger.info(f"   • Precision: {perf.get('precision', 0):.3f}")
            logger.info(f"   • Recall:    {perf.get('recall', 0):.3f}")
            logger.info(f"   • F1-Score:  {perf.get('f1_score', 0):.3f}")
            logger.info(f"   • Confidence: {perf.get('model_confidence', 'UNKNOWN')}")
        
        imp = summary.get('feature_importance', {})
        if imp:
            top_5 = imp.get('top_5_features', [])
            logger.info(f"\n🎯 Top 5 Features Importantes:")
            for i, feat in enumerate(top_5, 1):
                logger.info(f"   {i}. {feat}")
        
        logger.info("\n" + "="*60)
        logger.info("🤖 PRÓXIMOS PASOS PARA FUTURAS IAs:")
        logger.info("="*60)
        logger.info("1. Lee: data/knowledge_base/KNOWLEDGE_TRANSFER_GUIDE.md")
        logger.info("2. Consulta API: GET /api/knowledge/summary")
        logger.info("3. Importa conocimiento en tu IA:")
        logger.info("   from trading_phantom.analytics.transfer_learning import TransferLearningPipeline")
        logger.info("   knowledge = TransferLearningPipeline().import_knowledge()")
        logger.info("\n✅ Listo. El bot puede usar este modelo cuando esté habilitado en config.yaml")
        
    except Exception as e:
        logger.error(f"❌ Error generando Knowledge Base: {e}", exc_info=True)


if __name__ == "__main__":
    main()

