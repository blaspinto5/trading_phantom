# Trading Phantom — Guía completa (src layout)

Esta guía amplía y especifica la documentación del proyecto, alineada a la nueva estructura basada en `src/` y buenas prácticas.

## Índice
- Introducción y objetivos
- Estructura del repositorio
- Instalación y entorno
- Configuración (YAML)
- Desarrollo: UI y API
- Orquestación del bot
- Backtesting (numérico y visual)
- Pruebas y linter
- Empaquetado (.exe) y instalador
- CI (GitHub Actions)
- Seguridad, secretos y auditoría
- Troubleshooting (FAQ)
- Contribuir y roadmap

---

## Introducción
Trading Phantom es una plataforma de trading algorítmico en Python orientada a MetaTrader 5 (MT5). Provee UI (Flask + pywebview), API para control del bot, backtesting numérico y visual, y herramientas de empaquetado.

## Estructura del repositorio

```
.
├─ src/
│  └─ trading_phantom/
│     ├─ __init__.py
│     ├─ main.py               # entrada del bot (python -m trading_phantom.main)
│     ├─ webapp.py             # servidor Flask (UI + API)
│     ├─ core/
│     │  └─ orchestrator.py    # loop principal del bot
│     ├─ modules/
│     │  ├─ data_loader.py     # carga y normalización de datos (MT5 → OHLCV)
│     │  ├─ strategy.py        # lógica de señales (SMA + RSI)
│     │  ├─ risk_manager.py    # reglas de riesgo, lotes, SL/TP
│     │  └─ trader.py          # ejecución de órdenes (pending orders)
│     ├─ mt5/
│     │  └─ connector.py       # wrapper de MetaTrader5 (conexión + helpers)
│     ├─ backtest/
│     │  ├─ metrics.py         # métricas básicas de rendimiento
│     │  ├─ simulation.py      # simulador sencillo
│     │  └─ visual_backtest.py # adapter para librería backtesting
│     ├─ config/
│     │  ├─ config_loader.py   # carga YAML
│     │  └─ config.yaml        # valores por defecto
│     ├─ utils/
│     │  └─ trade_logger.py    # CSV de trades
│     ├─ templates/
│     │  └─ index.html         # UI principal
│     └─ static/
│        └─ style.css
├─ scripts/
│  ├─ launcher.py              # arranca Flask y pywebview
│  ├─ call_bot.py              # helper HTTP para start/stop del bot
│  └─ build_exe.ps1            # empaquetado PyInstaller
├─ tests/
│  ├─ conftest.py
│  ├─ test_mt5_connector.py
│  ├─ test_strategy.py
│  └─ test_visual_adapter.py
├─ .github/workflows/ci.yml    # CI con lint + tests + audit
├─ requirements.txt            # runtime
├─ requirements-dev.txt        # dev (pytest, ruff)
├─ pytest.ini                  # descubre tests/ en raíz
└─ pyproject.toml              # configuración de ruff (y puedes añadir PEP621)
```

Beneficios del layout `src/`:
- Evita imports accidentales desde la raíz al desarrollar.
- Facilita empaquetado, tests y CI; `PYTHONPATH=src` es explícito.
- Ordena código, tests y scripts de forma clara.

## Instalación y entorno (Windows)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt -r requirements-dev.txt
```

MT5 requiere el terminal de MetaTrader 5 instalado en Windows y que la API pueda inicializarse.

## Configuración (YAML)

Archivo: `src/trading_phantom/config/config.yaml`
- `symbol`: par a operar (ej. `EURUSD`)
- `timeframe`: `M1|M5|M15|H1|H4|D1`
- `max_positions`: límite de posiciones abiertas
- `risk`: `risk_per_trade`, `fixed_lot` (o `null`), `max_daily_loss`
- `orders`: `sl_pips`, `tp_pips`, `deviation`
- `execution`: `loop_interval_seconds`

Puedes sobreescribir valores en runtime mediante variables de entorno o copiar el YAML con tus ajustes.

## Desarrollo: UI y API

Servidor local:
```powershell
$env:PYTHONPATH="src"
python src/trading_phantom/webapp.py
```

Aplicación de escritorio (pywebview):
```powershell
.\.venv\Scripts\python.exe scripts/launcher.py --debug
```

Endpoints principales:
- `GET /` → UI HTML
- `POST /api/bot/start` → arranca el bot (parámetros: `debug`, `iterations`)
- `POST /api/bot/stop` → detiene el bot
- `GET /api/bot/status` → estado del bot
- `GET /api/logs?bot=true&lines=200` → últimos logs
- `POST /api/backtest` → lanza backtest; devuelve `job_id`
- `GET /api/backtest/<job_id>` → estado/resultado

Ejemplo rápido vía script:
```powershell
python scripts/call_bot.py --iterations 1 --debug
```

## Orquestación del bot

Entrada: `src/trading_phantom/main.py` (o `python -m trading_phantom.main`)
- Integra `Strategy`, `RiskManager`, `Trader` y `MT5Connector`.
- Ejecuta bucles con control por vela para evitar múltiples trades por candle.
- Soporta `--iterations` para testing; `--debug` para logging detallado.

## Backtesting

Numérico (simulador): `src/trading_phantom/backtest/simulation.py`
- Usa señales de la estrategia para simular entradas/salidas.
- Métricas: `metrics.py` → `Winrate`, `PnL` total/promedio, mejor/peor trade.

Visual: `src/trading_phantom/backtest/visual_backtest.py`
- Adapter `StrategyAdapter` para librería `backtesting`.
- Acepta `plot=False` para ejecutar en CI/entornos sin GUI.

Ejemplo:
```powershell
python - <<'PY'
from trading_phantom.backtest.visual_backtest import run_visual_backtest
import pandas as pd
idx = pd.date_range(end=pd.Timestamp.now(), periods=300, freq='h')
df = pd.DataFrame({'Open':[1]*300,'High':[1.01]*300,'Low':[0.99]*300,'Close':[1]*300,'Volume':[100]*300}, index=idx)
res = run_visual_backtest(df, sma_period=20, rsi_period=14, plot=False)
print(res)
PY
```

## Pruebas y linter

```powershell
$env:PYTHONPATH="src"
python -m pytest -q
ruff check .
```

`tests/` contiene pruebas de `MT5Connector` (mock), estrategia y adapter visual.

## Empaquetado (.exe)

Construcción con PyInstaller:
```powershell
scripts\build_exe.ps1 -onefile -console
```

Diagnóstico del `.exe`:
- Usa `scripts/run_exe_console.ps1` para redirigir logs a `dist_exe_stdout.log` y `dist_exe_stderr.log`.
- Excepciones del launcher se guardan en `%TEMP%/trading_phantom_crash.log`.

Instalador (Inno Setup):
```powershell
iscc installer\TradingPhantom.iss
```
Recomendado: firmar el instalador y probar en VM.

## CI (GitHub Actions)

Archivo: `.github/workflows/ci.yml`
- Matrix: Python 3.10 y 3.11
- `env: PYTHONPATH=src`
- Pasos: `pip install`, `ruff check .`, `pytest`, `pip-audit --fail-on high`

## Seguridad, secretos y auditoría

- No incluir credenciales en el repo; usar variables de entorno.
- Ejecutar `pip-audit` regularmente; actualizar dependencias.

## Troubleshooting (FAQ)

- `ImportError: flask`: instala dependencias (`requirements.txt`) en el venv activo.
- `MetaTrader5.initialize() False`: verifica que MT5 esté instalado y con sesión activa.
- El bot no arranca desde la UI: revisa `logs/bot.log` y `%TEMP%/trading_phantom_crash.log`.
- Visual backtest no muestra gráfico: usa `plot=False` (sin GUI) o instala dependencias gráficas.

## Contribuir y roadmap

Buenas prácticas:
- Pre-commit con `ruff` y `pytest` locales.
- Añadir tests y documentación en cada PR.
- Mantener funciones pequeñas y claras; evitar duplicación.

Roadmap sugerido:
- Añadir `console_scripts` en `pyproject.toml` para `trading-phantom`.
- Desacoplar `webapp` en `server/` y añadir auth básica.
- Extender estrategia y soporte de símbolos/timeframes.
