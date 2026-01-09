import argparse
import logging
import sys
from pathlib import Path

# Agregar src/ al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from trading_phantom.analytics.db import init_db
from trading_phantom.analytics.ml_pipeline import StrategyModel
from trading_phantom.analytics.transfer_learning import \
    TransferLearningPipeline

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s"
)
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
    logger.info(f"\n📊 Métricas del Modelo:")
    logger.info(f"   • Accuracy:    {res.get('accuracy', 0):.2%}")
    logger.info(f"   • Muestras:    {res.get('n_samples', 0)}")
    logger.info(f"   • Modelo:      Random Forest (100 árboles)")
    logger.info(f"   • Features:    7 características derivadas de trades")
    logger.info(f"\n📂 Ubicación del modelo: src/data/models/")
    logger.info(
        f"\n✅ El bot puede usar este modelo cuando esté habilitado en config.yaml"
    )
    logger.info("=" * 60 + "\n")


if __name__ == "__main__":
    main()
