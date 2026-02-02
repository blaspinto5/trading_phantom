import argparse
import logging
import sys
from pathlib import Path

# Agregar src/ al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from trading_phantom.analytics.db import init_db
from trading_phantom.analytics.ml_pipeline import StrategyModel

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Entrena el modelo ML y genera Knowledge Base para futuras IAs"
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="(Opcional) Solo muestra métricas, no hace nada extra",
    )
    args = parser.parse_args()

    logger.info("🚀 Iniciando entrenamiento de ML...")

    init_db()
    model = StrategyModel()
    res = model.train()

    if res.get("status") == "no_data":
        logger.info(
            "⚠️  No hay datos suficientes en DB. Ejecuta el bot o carga trades antes de entrenar."
        )
        return

    logger.info(
        "✅ Modelo entrenado | accuracy=%.4f | muestras=%s",
        res.get("accuracy", 0.0),
        res.get("n_samples"),
    )

    logger.info("\n" + "=" * 60)
    logger.info("🎉 ENTRENAMIENTO COMPLETADO EXITOSAMENTE")
    logger.info("=" * 60)
    logger.info("\n📊 Métricas del Modelo:")
    logger.info(f"   • Accuracy:    {res.get('accuracy', 0):.2%}")
    logger.info(f"   • Muestras:    {res.get('n_samples', 0)}")
    logger.info("   • Modelo:      Random Forest (100 árboles)")
    logger.info("   • Features:    7 características derivadas de trades")
    logger.info("\n📂 Ubicación del modelo: src/data/models/")
    logger.info("\n✅ El bot puede usar este modelo cuando esté habilitado en config.yaml")
    logger.info("=" * 60 + "\n")

    # Save model if requested
    if args.save and res.get("status") == "trained":
        try:
            from trading_phantom.analytics.model_store import save_model_versioned

            model_data = {
                "model": getattr(model, "model", None),
                "metrics": res,
                "model_type": "random_forest",
                "timestamp": datetime.now().isoformat(),
            }
            saved = save_model_versioned(
                model_data, base_name="strategy_model", models_dir="src/data/models"
            )
            logger.info(f"💾 Modelo guardado (versionado) en: {saved}")
        except Exception:
            logger.exception("Error al guardar el modelo de forma versionada")


if __name__ == "__main__":
    main()
