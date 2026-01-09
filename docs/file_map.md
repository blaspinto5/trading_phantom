# Mapa de Archivos Relevantes (por carpeta y archivo)

Este documento describe la finalidad de las carpetas y los archivos más relevantes del proyecto. Está pensado como referencia rápida para desarrolladores nuevos.

## Raíz del proyecto
- `main.py`: punto de entrada para ejecución del bot en local (arranca orquestador y scheduler).
- `README*` / `*.md`: documentación principal; mucha fue consolidada en `docs/archived_md/`.

## `src/trading_phantom/`
Carpeta canonical del paquete Python. Importar siempre desde `src`.

- `core/orchestrator.py`: orquestador que coordina el ciclo principal: obtención de datos, generación de señales, ejecución por `trader`, y registro en `trade_history`.
- `modules/strategy.py`: implementación de la lógica de trading. Contiene `Strategy` con `generate_signal()`, utilidades `compute_macd()` y `compute_rsi()`; ahora soporta `sma_period` para compatibilidad de tests.
- `modules/trader.py`: ejecuta órdenes usando el conector MT5, gestiona reintentos y devuelve detalles de ejecución (ticket, precios, sl/tp).
- `modules/risk_manager.py`: calcula tamaño de posición, controla límites de riesgo y lotaje por trade.
- `modules/trade_history.py`: registra operaciones abiertas/cerradas, exporta a JSON y calcula estadísticas (win rate, net profit).
- `mt5/connector.py`: encapsula interacción con MetaTrader5: login, `get_rates_df()`, `send_order()` y `close_order()`.
- `analytics/ml_pipeline.py`: (opcional) entrenamiento e inferencia de modelos ML usados para refinar señales.
- `api/`: (si presente) endpoints para exponer estado, métricas o comandos de control.
- `backtest/` y `backtest/visual_backtest.py`: adaptadores para backtesting; `visual_backtest` permite ejecutar backtests sobre DataFrames y generar gráficas.

## `src/data/`
- `trading_phantom.db`: SQLite para persistencia ligera (si se usa).
- `models/` (e.g. `advanced_model.pkl`): modelos serializados para inferencia rápida.

## `scripts/`
- `launcher.py`: helper para iniciar componentes y asegurar `PYTHONPATH=src` en entornos Windows/CI.
- `call_bot.py`: script utilitario para invocar el bot desde procesos externos o CI.

## `tests/`
- `tests/test_strategy.py`: pruebas unitarias de `Strategy` (casos BUY/SELL/HOLD).
- `tests/test_visual_adapter.py`: pruebas del adaptador/visual backtest sin interfaz gráfica.

## `docs/`
- `docs/archived_md/`: copias y reorganización de muchos `*.md` del repo raíz (guías, análisis, resúmenes).
- `docs/file_map.md`: este archivo (mapa y descripciones).
- `docs/RECENT_ACTIONS.md`: resumen de las acciones recientes del agente (migración, tests, correcciones).

## `scripts de ejecución / CI`
- `RUN_TESTS.bat`, `RUN_TESTS.ps1`: scripts locales para ejecutar tests — ya actualizados para establecer `PYTHONPATH=src`.
- `.github/workflows/ci.yml`: integración continua (ajustada para preferir `src` en el path).

## `archive/code/`
- `archive/code/trading_phantom_root/`: copia legacy de la antigua estructura `trading_phantom/` movida desde la raíz. Conserva código histórico para referencia.

## Archivos individuales clave (descripción breve)

Si quieres, amplío la sección "Archivos individuales clave" para cubrir TODOS los archivos dentro de una carpeta específica (por ejemplo `src/trading_phantom/modules/`) con una línea por archivo y un ejemplo de uso para cada uno. ¿Cuál carpeta quieres que documente primero en detalle?

### `src/trading_phantom/modules/` (detalle por archivo)

- `__init__.py`: Inicializa el subpaquete `modules` y expone símbolos públicos.
- `strategy.py`: Lógica de trading; clase `Strategy` con `generate_signal(df)` que devuelve `"BUY"|"SELL"|"HOLD"`. Ejemplo: `Strategy(config).generate_signal(df_recent)`.
- `trader.py`: Encapsula envío y gestión de órdenes; funciones `send_order(...)`, `close_order(ticket)` y manejo de reintentos. Ejemplo: `Trader(connector).send_order(symbol, side, lot)`.
- `risk_manager.py`: Calcula tamaño de posición y límites por operación (`position_size(capital, risk_pct, stop_pips)`). Ejemplo: `rm = RiskManager(cfg); size = rm.position_size(10000, 0.02, 50)`.
- `trade_history.py`: Registro persistente de operaciones; API: `add_trade()`, `close_trade()`, `get_summary()`. Ejemplo: `TradeHistory(db_path).add_trade(trade_dict)`.
- `data_loader.py`: Utilidades para cargar series de precios desde CSV/MT5/SQLite y normalizar DataFrames. Ejemplo: `df = load_prices('EURUSD', timeframe='H1', bars=500)`.

---

Si quieres, amplío la sección "Archivos individuales clave" para cubrir TODOS los archivos dentro de una carpeta específica (por ejemplo `src/trading_phantom/modules/`) con una línea por archivo y un ejemplo de uso para cada uno. ¿Cuál carpeta quieres que documente primero en detalle?
