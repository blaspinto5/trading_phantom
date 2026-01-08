# core/orchestrator.py

import logging
import time
from datetime import datetime
from typing import Optional

from trading_phantom.config.config_loader import load_config
from trading_phantom.mt5.connector import MT5Connector
from trading_phantom.modules.strategy import Strategy
from trading_phantom.modules.risk_manager import RiskManager
from trading_phantom.modules.trader import Trader
from trading_phantom.modules.trade_history import TradeHistory

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

    strategy = Strategy(symbol, timeframe, mt5_conn)
    risk_manager = RiskManager(config, mt5_conn)
    trader = Trader(mt5_conn, risk_manager)
    trade_history = TradeHistory()

    logger.info("✅ Estrategia, RiskManager, Trader e Historial inicializados")

    last_candle_time = None
    traded_this_candle = False
    processed = 0
    last_summary_time = datetime.now()

    try:
        while True:
            logger.debug("-----------------------------")
            now = datetime.now()
            logger.info("🕒 Tick: %s", now)

            # Mostrar resumen cada 30 minutos
            if (now - last_summary_time).total_seconds() > 1800:
                trade_history.print_summary()
                last_summary_time = now

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
            logger.info("📈 Señal: %s", signal)

            # count processed ticks (useful for --iterations testing)
            processed += 1
            if remaining is not None and processed >= remaining:
                logger.info("🔢 Alcanzado número de iteraciones solicitado (%s). Saliendo.", remaining)
                break

            if signal != "HOLD":
                executed = trader.execute(signal, price)
                if executed:
                    trade_history.add_trade(
                        ticket=executed["ticket"],
                        symbol=executed["symbol"],
                        signal=executed["signal"],
                        volume=executed["volume"],
                        entry_price=executed["entry_price"],
                        sl=executed["sl"],
                        tp=executed["tp"]
                    )
                    traded_this_candle = True

            time.sleep(loop_interval)

    except KeyboardInterrupt:
        logger.info("\n🛑 Detenido manualmente por el usuario")
        trade_history.print_summary()

    except Exception:
        logger.exception("❌ Error crítico")

    finally:
        trade_history.print_summary()
        mt5_conn.shutdown()
        logger.info("✅ Trading Phantom finalizado correctamente")
