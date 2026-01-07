# core/orchestrator.py

import logging
import time
import os
from datetime import datetime
from typing import Optional, Callable, Dict, Any

import MetaTrader5 as mt5

from trading_phantom.config.config_loader import load_config
from trading_phantom.modules.risk_manager import RiskManager
from trading_phantom.modules.strategy import Strategy  # A completar luego
from trading_phantom.modules.trader import Trader
from trading_phantom.mt5.connector import MT5Connector


def run_bot(iterations: Optional[int] = None) -> None:
    logger = logging.getLogger(__name__)
    logger.info("🚀 Iniciando Trading Phantom")

    config = load_config()
    symbol = config["symbol"]
    timeframe_str = config["timeframe"]
    loop_interval = config["execution"]["loop_interval_seconds"]

    # Ajustar el nivel de logging desde la configuración
    level = getattr(logging, config.get("log_level", "INFO").upper(), logging.INFO)
    logging.getLogger().setLevel(level)

    logger.info("📊 Símbolo: %s", symbol)
    logger.info("🕒 Timeframe: %s", timeframe_str)
    logger.info("⏱️ Intervalo loop: %s segundos", loop_interval)
    logger.info("🧪 Modo: %s", config.get("mode"))

    mt5_conn = MT5Connector()
    if not mt5_conn.connect():
        logger.error("❌ No se pudo conectar a MT5. Abortando.")
        return

    # iterations: None -> infinite, 1 -> one iteration, N -> N iterations
    remaining = iterations if iterations is not None and iterations > 0 else None

    timeframe_map = {
        "M1": mt5.TIMEFRAME_M1,
        "M5": mt5.TIMEFRAME_M5,
        "M15": mt5.TIMEFRAME_M15,
        "H1": mt5.TIMEFRAME_H1,
        "H4": mt5.TIMEFRAME_H4,
        "D1": mt5.TIMEFRAME_D1,
    }

    timeframe = timeframe_map.get(timeframe_str)
    if timeframe is None:
        logger.error("❌ Timeframe inválido: %s", timeframe_str)
        mt5_conn.shutdown()
        return

    strategy = Strategy(
        symbol, timeframe, mt5_conn,
        sma_period=int(config.get('strategy', {}).get('sma_period', 100)),
        rsi_period=int(config.get('strategy', {}).get('rsi_period', 14)),
        ml_predictor=None,
        ml_confidence_threshold=0.7
    )
    risk_manager = RiskManager(config, mt5_conn)
    trader = Trader(mt5_conn, risk_manager)

    # Initialize ML predictor if enabled
    ml_predictor: Optional[Callable[[Dict[str, float]], Dict[str, Any]]] = None
    ml_config = config.get('ml', {})
    if ml_config.get('enabled', False):
        try:
            from trading_phantom.analytics.ml_pipeline import StrategyModel
            ml_model = StrategyModel()
            ml_confidence_threshold = float(ml_config.get('confidence_threshold', 0.7))
            logger.info("🤖 ML habilitado (umbral confianza: %.2f)", ml_confidence_threshold)
            ml_predictor = ml_model.predict
            strategy.ml_predictor = ml_predictor
            strategy.ml_confidence_threshold = ml_confidence_threshold
        except Exception:
            logger.warning("⚠️ No se pudo inicializar ML; continuando sin él")
            ml_config['enabled'] = False

    logger.info("✅ Estrategia, RiskManager y Trader inicializados")

    last_candle_time = None
    traded_this_candle = False
    processed = 0

    try:
        while True:
            logger.debug("-----------------------------")
            now = datetime.now()
            logger.info("🕒 Tick: %s", now)

            price = mt5_conn.get_price(symbol)
            if price is None:
                logger.warning("⚠️ No se pudo obtener precio")
                time.sleep(loop_interval)
                continue

            logger.info("💱 %s | BID: %s | ASK: %s", price['symbol'], price['bid'], price['ask'])

            rates = mt5_conn.get_rates(price["symbol"], timeframe, 1)
            if rates is None or len(rates) == 0:
                time.sleep(loop_interval)
                continue

            current_candle_time = datetime.fromtimestamp(rates[0]["time"]) 

            if last_candle_time != current_candle_time:
                logger.info("🆕 Nueva vela detectada")
                last_candle_time = current_candle_time
                traded_this_candle = False

            if traded_this_candle:
                logger.debug("⛔ Trade ya ejecutado en esta vela")
                time.sleep(loop_interval)
                continue

            signal = strategy.generate_signal()
            if ml_config.get('enabled') and ml_predictor:
                logger.info("📈 Señal: %s (con ML)", signal)
            else:
                logger.info("📈 Señal: %s", signal)

            # count processed ticks (useful for --iterations testing)
            processed += 1
            if remaining is not None and processed >= remaining:
                logger.info("🔢 Alcanzado número de iteraciones solicitado (%s). Saliendo.", remaining)
                break

            if signal != "HOLD":
                executed = trader.execute(signal, price)
                if executed:
                    traded_this_candle = True

            time.sleep(loop_interval)

    except KeyboardInterrupt:
        logger.info("\n🛑 Detenido manualmente por el usuario")

    except Exception:
        logger.exception("❌ Error crítico")

    finally:
        mt5_conn.shutdown()
        logger.info("✅ Trading Phantom finalizado correctamente")
