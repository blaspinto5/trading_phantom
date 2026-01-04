import time
import yaml
from datetime import datetime

import MetaTrader5 as mt5

from mt5_connector import MT5Connector
from strategy import Strategy
from risk_manager import RiskManager
from trader import Trader


# =========================
# CARGA DE CONFIGURACIÓN
# =========================
def load_config(path: str = "config.yaml") -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


# =========================
# MAIN
# =========================
def main():
    print("🚀 Iniciando Trading Phantom")

    # 1️⃣ Cargar configuración
    config = load_config()

    symbol = config["symbol"]
    timeframe_str = config["timeframe"]
    loop_interval = config["execution"]["loop_interval_seconds"]

    print(f"📊 Símbolo: {symbol}")
    print(f"🕒 Timeframe: {timeframe_str}")
    print(f"⏱️ Intervalo loop: {loop_interval} segundos")
    print(f"🧪 Modo: {config['mode']}")

    # 2️⃣ Inicializar MT5
    mt5_conn = MT5Connector()
    if not mt5_conn.connect():
        print("❌ No se pudo conectar a MT5. Abortando.")
        return

    # 3️⃣ Mapear timeframe del config a MT5
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
        print(f"❌ Timeframe inválido en config.yaml: {timeframe_str}")
        mt5_conn.shutdown()
        return

    # 4️⃣ Inicializar módulos
    strategy = Strategy(
        symbol=symbol,
        timeframe=timeframe,
        mt5_connector=mt5_conn
    )

    risk_manager = RiskManager(config, mt5_conn)
    trader = Trader(mt5_conn, risk_manager)

    print("✅ Estrategia, RiskManager y Trader inicializados")

    try:
        # 5️⃣ Loop principal
        while True:
            print("\n-----------------------------")
            print(f"🕒 Tick: {datetime.now()}")

            # Precio actual
            price = mt5_conn.get_price(symbol)
            if price is None:
                print("⚠️ No se pudo obtener precio")
                time.sleep(loop_interval)
                continue

            print(
                f"💱 {price['symbol']} | "
                f"BID: {price['bid']} | "
                f"ASK: {price['ask']}"
            )

            # Señal de la estrategia
            signal = strategy.generate_signal()
            print(f"📈 Señal: {signal}")

            # 👉 EJECUCIÓN REAL (DEMO)
            if signal != "HOLD":
                trader.execute(signal, price)

            time.sleep(loop_interval)

    except KeyboardInterrupt:
        print("\n🛑 Detenido manualmente por el usuario")

    except Exception as e:
        print(f"❌ Error crítico: {e}")

    finally:
        mt5_conn.shutdown()
        print("✅ Trading Phantom finalizado correctamente")


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    main()
