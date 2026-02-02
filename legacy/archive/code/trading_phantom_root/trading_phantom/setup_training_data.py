#!/usr/bin/env python3
"""
Script para inicializar la BD e insertar datos de prueba para entrenar el modelo ML.
"""
import os
import sys
from pathlib import Path

# Agregar src/ al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import logging
from datetime import datetime, timedelta

import numpy as np

from trading_phantom.analytics.db import Trade, get_session, init_db

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)


def generate_training_data():
    """Genera 200 trades de prueba para entrenar el modelo."""
    logger.info("🚀 Generando datos de entrenamiento...")

    # Inicializar BD
    init_db()
    session = get_session()

    try:
        # Limpiar trades anteriores
        session.query(Trade).delete()
        session.commit()
        logger.info("✅ BD limpiada")

        # Generar 200 trades simulados
        base_date = datetime(2024, 1, 1)
        trades = []

        for i in range(200):
            # Generar datos aleatorios pero realistas
            date = base_date + timedelta(hours=i * 4)
            side = np.random.choice(["BUY", "SELL"])
            price = 1.1650 + np.random.randn() * 0.002
            exit_price = price + np.random.randn() * 0.005
            volume = 1.0
            sl = price - 0.002 if side == "BUY" else price + 0.002
            tp = price + 0.004 if side == "BUY" else price - 0.004

            # Calcular PnL realista
            if side == "BUY":
                pnl = (exit_price - price) * 100000 * volume  # ~1000 points = $100
            else:
                pnl = (price - exit_price) * 100000 * volume

            trade = Trade(
                timestamp=date,
                ticket=100000 + i,
                symbol="EURUSD",
                side=side,
                price=price,
                volume=volume,
                sl=sl,
                tp=tp,
                exit_price=exit_price,
                exit_time=date + timedelta(hours=2),
                pnl=pnl,
                meta={"strategy": "EMA+MACD+RSI"},
            )
            trades.append(trade)

        # Insertar en BD
        session.add_all(trades)
        session.commit()
        logger.info(f"✅ {len(trades)} trades insertados correctamente")

        # Verificar
        count = session.query(Trade).count()
        logger.info(f"✅ Total de trades en BD: {count}")

        # Mostrar ejemplos
        examples = session.query(Trade).limit(3).all()
        logger.info("\n📊 Ejemplos de trades:")
        for trade in examples:
            logger.info(
                f"  - {trade.side} {trade.symbol} @ {trade.price:.5f} | PnL: ${trade.pnl:.2f}"
            )

    finally:
        session.close()


if __name__ == "__main__":
    generate_training_data()
    logger.info(
        "\n✅ Datos de entrenamiento listos. Ejecuta: python scripts/ml_train.py --save"
    )
