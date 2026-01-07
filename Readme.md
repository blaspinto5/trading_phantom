# Trading Phantom

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows-lightblue.svg)](https://www.microsoft.com/windows)
[![CI/CD: GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-blue.svg)](.github/workflows/ci.yml)

**Trading Phantom** es una plataforma modular de trading algorítmico en Python, diseñada para operar en MetaTrader 5. Proporciona:

- 🤖 **Bot de trading automático**: Loop inteligente con indicadores técnicos (SMA, RSI)
- 📊 **Backtesting visual**: Herramienta interactiva para validar estrategias históricamente
- 💻 **Interfaz dual**: Servidor Flask REST API + Aplicación desktop nativa (pywebview)
- 🏗️ **Arquitectura modular**: Componentes desacoplados (Strategy, RiskManager, Trader, MT5Connector)
- 📦 **Empaquetado profesional**: Generador de .exe con PyInstaller e instalador con Inno Setup
- 🧪 **Pipeline CI/CD**: Pruebas automatizadas, linting y auditoría en GitHub Actions

---

## 📂 Estructura del repositorio

```
PROYECTO 2/
├── src/trading_phantom/          # 🎯 Código fuente principal (src-layout)
│   ├── __init__.py
│   ├── main.py                   # Entrypoint del bot (python -m trading_phantom.main)
│   ├── webapp.py                 # Flask server REST API + UI
│   ├── core/                     # Orquestación y coordinación
│   │   └── orchestrator.py       # Loop principal de trading
│   ├── modules/                  # Lógica de trading
│   │   ├── strategy.py           # Generador de señales (SMA + RSI)
│   │   ├── risk_manager.py       # Validación de posiciones y riesgo
│   │   ├── trader.py             # Ejecución de órdenes
│   │   └── data_loader.py        # Carga y normalización de datos
│   ├── mt5/                      # Integración MetaTrader 5
│   │   └── connector.py          # Wrapper con retry logic
│   ├── backtest/                 # Herramientas de backtesting
│   │   ├── simulation.py         # Simulador numérico
│   │   ├── visual_backtest.py    # Adapter para backtesting lib
│   │   └── metrics.py            # Cálculo de métricas (Sharpe, DD, etc)
│   ├── config/                   # Gestión de configuración
│   │   ├── config_loader.py      # YAML loader
│   │   └── config.yaml           # Parámetros por defecto
│   ├── templates/                # HTML para Flask
│   ├── static/                   # CSS y assets
│   └── utils/                    # Utilidades (logging, helpers)
│
├── tests/                        # 🧪 Tests unitarios e integración
│   ├── conftest.py               # Configuración pytest + sys.path fix
│   ├── test_mt5_connector.py
│   ├── test_strategy.py
│   └── test_visual_adapter.py
│
├── docs/                         # 📚 Documentación profesional
│   ├── README.md                 # Guía completa extendida
│   ├── ARCHITECTURE.md           # Diseño de arquitectura y patrones
│   ├── API.md                    # Documentación REST endpoints
│   ├── QUICKSTART.md             # Instalación rápida (5 min)
│   └── (archivos HTML generados)
│
├── scripts/                      # 🛠️ Scripts de desarrollo y empaquetado
│   ├── launcher.py               # Inicia Flask + pywebview
│   ├── build_exe.ps1             # Build PyInstaller
│   ├── run_exe_console.ps1       # Ejecuta EXE con captura de logs
│   ├── call_bot.py               # Helper E2E testing
│   └── (otros helpers)
│
├── installer/                    # 📦 Instalador Windows (Inno Setup)
│   └── TradingPhantom.iss
│
├── build/, dist/                 # 🔨 Artefactos de build (no versionados)
├── logs/                         # 📋 Logs de ejecución
│
├── CONTRIBUTING.md               # 👥 Pautas de contribución
├── CHANGELOG.md                  # 📝 Historial de cambios
├── LICENSE                       # 📄 MIT License
├── pyproject.toml                # 🐍 Config Python (ruff rules)
├── requirements.txt              # 📦 Dependencias runtime
├── requirements-dev.txt          # 📦 Dependencias desarrollo
└── pytest.ini                    # 🧪 Config pytest
```

**Nota**: Documentación extendida disponible en [docs/README.md](docs/README.md) (guía completa del layout `src/`, setup, endpoints, backtesting, empaquetado, CI y troubleshooting).

---

## ⚡ Instalación y ejecución (30 segundos)

### 🎯 La forma más fácil: Doble-click

**Opción 1 - Windows (Batch):**
1. Abre `INSTALL.bat` (doble-click)
2. Espera ~1-2 minutos
3. Ejecuta `RUN.bat` (doble-click)
4. Accede a http://127.0.0.1:5000

**Opción 2 - PowerShell:**
```powershell
.\INSTALL.ps1
.\RUN.ps1
```

### 📋 Requisitos previos
- **Windows 10+**
- **Python 3.10+** (si no lo tienes: [python.org](https://www.python.org/downloads/))
- **MetaTrader 5** (opcional, solo si operas en vivo)

### 🔧 Instalación manual (si prefieres)

```powershell
# 1. Crear entorno virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Instalar dependencias
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 3. Ejecutar
python scripts/launcher.py --debug
```

---

## 🚀 Primera ejecución

Después de instalar, la aplicación:
- ✅ Abre una ventana nativa
- ✅ Inicia servidor Flask en http://127.0.0.1:5000
- ✅ Accede a API REST, backtesting, logs

### Primeras acciones

**Backtesting**: Prueba una estrategia sin riesgo
```
UI → Backtest → Selecciona parámetros → Ejecuta
```

**Bot real**: Conecta con MetaTrader 5
```
UI → Bot → Start → (Requiere MT5 abierto)
```

**Logs**: Monitorea operaciones
```
UI → Logs → Ver histórico
```

> 📚 **Más info**: [QUICK_START.md](QUICK_START.md) (30 segundos) o [docs/QUICKSTART.md](docs/QUICKSTART.md) (5 minutos)

---

## 🧪 Testing, Linting y CI/CD

### Ejecutar localmente

```powershell
# Tests unitarios
.\.venv\Scripts\python.exe -m pytest -q

# Linting (ruff)
ruff check .

# Linting + auto-fix
ruff check --fix .
```

### GitHub Actions (CI/CD)

Cada push/PR a `main` ejecuta:
- ✅ Matrix: Python 3.10 y 3.11 en Windows
- ✅ `ruff check .` (linting strict)
- ✅ `pytest` con cobertura
- ✅ `pip-audit` (detecta vulnerabilidades críticas)

**Checklist antes de abrir PR:**
- [ ] Tests pasan: `pytest -q`
- [ ] Sin warnings de linting: `ruff check .`
- [ ] Cambios documentados en [CHANGELOG.md](CHANGELOG.md)
- [ ] Nuevas funciones incluyen tests

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para detalles completos.

---

## 📦 Empaquetado y distribución

### Generar ejecutable .exe (PyInstaller)

```powershell
# Build simple (con consola para debug)
.\scripts\build_exe.ps1 -console

# Build sin consola (usuario final)
.\scripts\build_exe.ps1

# Resultado: dist\TradingPhantom.exe
```

### Crear instalador Windows (Inno Setup)

```powershell
# 1. Instalar Inno Setup desde issetup.com
# 2. Ejecutar el compilador
iscc installer\TradingPhantom.iss

# Resultado: Setup-TradingPhantom-vX.X.X.exe
```

### Debugging del .exe

```powershell
# Ejecutar y capturar logs
.\scripts\run_exe_console.ps1

# Busca logs en:
# - dist_exe_stdout.log
# - dist_exe_stderr.log
# - %TEMP%\trading_phantom_crash.log (si hay crash)
```

**Problemas comunes:**
| Problema | Solución |
|----------|----------|
| "ModuleNotFoundError" en .exe | Agregar `--hidden-import` en `build_exe.ps1` |
| Puerto 5000 en uso | Cambiar en `webapp.py` línea de `app.run()` |
| Crash silencioso | Ver `dist_exe_stderr.log` o `trading_phantom_crash.log` |

---

## 🏗️ Arquitectura y componentes

```
User/Sistema
     ↓
[Flask REST API] ←→ [pywebview UI]
     ↓
[Orchestrator] — Main trading loop
     ├→ [MT5Connector] — Comunicación MetaTrader 5
     ├→ [DataLoader] — Fetch OHLCV histórico
     ├→ [Strategy] — Generar señales (SMA + RSI)
     ├→ [RiskManager] — Validar posiciones y riesgo
     └→ [Trader] — Ejecutar órdenes
     ↓
[Backtest Engine]
     ├→ [Simulation] — Simulador numérico
     ├→ [VisualBacktest] — Adapter para backtesting lib
     └→ [Metrics] — Cálculo de Sharpe, Drawdown, etc
```

**Patrones de diseño:**
- 🔌 **Dependency Injection**: MT5Connector inyectado en Strategy y RiskManager
- 🎭 **Adapter Pattern**: StrategyAdapter adapta core.Strategy a backtesting.Strategy
- 📋 **Command Pattern**: Trader.execute encapsula lógica de órdenes
- 🔄 **Separation of Concerns**: Cada módulo con una responsabilidad clara

Para detalles técnicos completos, ver [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## 📊 REST API Endpoints

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/bot/start` | POST | Iniciar bot (con parámetros de iteraciones y debug) |
| `/api/bot/stop` | POST | Detener bot en ejecución |
| `/api/bot/status` | GET | Estado actual del bot |
| `/api/logs` | GET | Obtener logs (bot, backtest, histórico) |
| `/api/backtest` | POST | Ejecutar backtest con parámetros |
| `/api/backtest` | GET | Obtener resultados backtest previos |
| `/api/analytics/ingest_trade` | POST | Ingesta de operación al DB |
| `/api/analytics/ml/train` | POST | Entrenamiento del modelo ML |
| `/api/analytics/ml/predict` | POST | Predicción de señal con features |
| `/api/analytics/export/trades` | GET | Exportar dataset de trades (`?format=json|csv|parquet`) |
| `/api/analytics/export/backtests` | GET | Exportar dataset de backtests (`?format=json|csv|parquet`) |

Nota: `parquet` requiere `pyarrow`.

**Documentación completa con ejemplos:** [docs/API.md](docs/API.md)

---

## 🐛 Debugging y diagnóstico

## 🐛 Debugging y diagnóstico

### Logs de ejecución

- **Bot en desarrollo**: Verifica `logs/` directorio
- **EXE en producción**: Verifica `dist_exe_stdout.log` y `dist_exe_stderr.log` tras ejecutar:
  ```powershell
  .\scripts\run_exe_console.ps1
  ```
- **Crash del launcher**: Busca `%TEMP%\trading_phantom_crash.log`

### Solución de problemas comunes

| Problema | Causa | Solución |
|----------|-------|----------|
| `ModuleNotFoundError: No module named 'flask'` | Python incorrecto | Usa `.venv\Scripts\python.exe` en lugar de `python` |
| API no responde en localhost:5000 | Puerto ocupado | Cambiar puerto en `webapp.py` line 195 |
| Crash silencioso del .exe | Import o exception | Ver `run_exe_console.ps1` y revisar stderr.log |
| MT5 no conecta | Terminal no abierta | Abre MetaTrader 5 antes de iniciar bot |

---

## 📚 Documentación adicional

- **[CONTRIBUTING.md](CONTRIBUTING.md)** — Pautas para contribuciones, estándares de código, commit conventions
- **[CHANGELOG.md](CHANGELOG.md)** — Historial detallado de cambios y releases
- **[docs/README.md](docs/README.md)** — Guía extendida (setup, configuración, endpoints, troubleshooting)
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** — Diseño técnico, patrones, flujos de datos
- **[docs/API.md](docs/API.md)** — Especificación completa de endpoints REST con ejemplos
- **[docs/QUICKSTART.md](docs/QUICKSTART.md)** — Guía instalación rápida con pantallazos
- **[LICENSE](LICENSE)** — Licencia MIT

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature: `git checkout -b feature/amazing-feature`
3. Commit tus cambios: `git commit -m "Add amazing feature"`
4. Push a la rama: `git push origin feature/amazing-feature`
5. Abre un Pull Request

**Antes de contribuir:**
- Lee [CONTRIBUTING.md](CONTRIBUTING.md)
- Ejecuta `ruff check --fix .` y `pytest -q`
- Asegúrate de documentar cambios en [CHANGELOG.md](CHANGELOG.md)

---

## 📋 Resumen de comandos

```powershell
# Desarrollo
.\.venv\Scripts\python.exe scripts/launcher.py --debug

# Testing
python -m pytest -q
ruff check .
ruff check --fix .

# Build EXE
.\scripts\build_exe.ps1

# Build with console (debug)
.\scripts\build_exe.ps1 -console

# Run EXE with logs
.\scripts\run_exe_console.ps1
```

---

## 📞 Soporte y contacto

- **Issues**: Usa GitHub Issues para reportar bugs o sugerir features
- **Documentación**: Ver directorio `docs/`
- **Logs**: Consulta los archivos en `logs/` o `%TEMP%\trading_phantom_crash.log`

---

## 📈 Analítica y ML

La plataforma integra un módulo de **Machine Learning opcional** que captura datos de trades, los almacena en una base de datos y entrena un modelo que sugiere señales. Este módulo es **desacoplado del bot** y se activa vía `config.yaml` cuando hay datos suficientes.

### Flujo completo de ML en vivo

```
1. RECOLECTA DE DATOS (Sin ML)
   ↓
   Bot ejecuta trades → automáticamente ingestados en DB
   Backtest completa → resultados guardados
   
2. ENTRENAR MODELO
   ↓
   API POST /api/analytics/ml/train
   → Carga dataset de trades (≥30 requeridos)
   → Feature engineering: (side, price, volume, pnl_lag, MA)
   → RandomForestClassifier entrenado
   
3. ACTIVAR ML EN VIVO (config.yaml)
   ↓
   ml:
     enabled: true
     confidence_threshold: 0.7
   
4. PREDICCIÓN EN VIVO
   ↓
   Cada vela nueva:
   - Strategy genera BUY/SELL/HOLD (SMA + RSI)
   - ML predictor valida: ¿prob ≥ 0.7?
   - Si sí: puede sobreescribir señal
   - Si no: mantiene regla original
   - Logs: "📈 Señal: BUY (con ML)"
```

### Componentes

- **db.py**: Modelos Trade/BacktestRun; SQLite local o Postgres en Docker
- **collector.py**: Ingesta automática desde bot y backtest
- **ml_pipeline.py**: RandomForestClassifier con feature engineering
- **orchestrator.py**: Lee `ml.enabled` y `ml.confidence_threshold` de config

### Paso a paso: Activar ML

**1. Recolectar datos (sin ML)**
```powershell
.\RUN.ps1
# Ejecutar ~50-100 iteraciones para acumular datos
```

**2. Entrenar**
```powershell
# Desde otra terminal
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/analytics/ml/train" -Method Post
```

**3. Editar config.yaml**
```yaml
ml:
  enabled: true
  confidence_threshold: 0.7
```

**4. Ejecutar con ML**
```powershell
.\RUN.ps1
# Verás: "🤖 ML habilitado (umbral confianza: 0.70)"
```

### Endpoints analítica

| Endpoint | Descripción |
|----------|-------------|
| `POST /api/analytics/ml/train` | Entrena modelo |
| `POST /api/analytics/ml/predict` | Predicción manual |
| `GET /api/analytics/export/trades?format=csv\|parquet` | Exporta dataset |
| `GET /api/analytics/export/backtests?format=csv\|parquet` | Exporta backtests |

### Notas

- **Mínimo datos**: ≥30 trades para entrenar
- **No garantiza ganancias**: Aprende patrones pasados; mercado cambia
- **Umbral**: `confidence_threshold=0.7` → solo usa ML si prob ≥ 0.7
- **Fallback**: Si ML falla, continúa con SMA+RSI automáticamente

---
- [src/trading_phantom/analytics/db.py](src/trading_phantom/analytics/db.py): Modelos SQLAlchemy (`Trade`, `BacktestRun`) y gestión de sesión. Por defecto usa SQLite; en Docker usa Postgres vía `DATABASE_URL`.
- [src/trading_phantom/analytics/collector.py](src/trading_phantom/analytics/collector.py): Funciones de ingesta (`ingest_trade`, `ingest_backtest`) que validan y persisten payloads.
- [src/trading_phantom/analytics/ml_pipeline.py](src/trading_phantom/analytics/ml_pipeline.py): `StrategyModel` con `train()` y `predict()` utilizando `RandomForestClassifier` y features básicos (SMA, RSI, variaciones de precio).

### Flujo de datos

Bot/Backtest → eventos JSON → API `/api/analytics/*` → Collector (normaliza) → DB (SQLAlchemy) → ML Train (`/api/analytics/ml/train`) → ML Predict (`/api/analytics/ml/predict`) → (opcional) combinación con reglas de `Strategy`.

### Endpoints de Analítica
- `POST /api/analytics/ingest_trade`: ingesta de una operación (campos: `symbol`, `side`, `entry_price`, `exit_price`, `pnl`, `opened_at`, `closed_at`).
- `POST /api/analytics/ml/train`: entrena el modelo con datos del DB.
- `POST /api/analytics/ml/predict`: predice señal (`BUY`/`SELL`/`HOLD`) con probabilidad dado un set de features.
- `GET /api/analytics/export/trades`: exporta dataset de trades en JSON.
- `GET /api/analytics/export/backtests`: exporta dataset de backtests en JSON.

### Variables de entorno de módulos
- `ENABLE_BACKTEST`, `ENABLE_BOT`, `ENABLE_LOGS`, `ENABLE_ANALYTICS`: controlan el registro de Blueprints en [src/trading_phantom/webapp.py](src/trading_phantom/webapp.py) y [src/trading_phantom/api/__init__.py](src/trading_phantom/api/__init__.py).

### Ejemplos rápidos (PowerShell)

Entrenar:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/analytics/ml/train" -Method Post
```

Predecir:
```powershell
$features = @{ close = 1.1234; sma = 1.1200; rsi = 55; prev_close = 1.1210 }
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/analytics/ml/predict" -Method Post -Body ($features | ConvertTo-Json) -ContentType 'application/json'
```

Ingestar trade:
```powershell
$trade = @{ symbol = "EURUSD-T"; side = "BUY"; entry_price = 1.1205; exit_price = 1.1235; pnl = 30.0; opened_at = "2025-12-01T10:00:00Z"; closed_at = "2025-12-01T12:00:00Z" }
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/analytics/ingest_trade" -Method Post -Body ($trade | ConvertTo-Json) -ContentType 'application/json'
```

## 🐳 Docker

`docker-compose.yml` define:
- `app`: API Flask (bot/backtest/analytics) con healthcheck.
- `db`: Postgres 15 con volumen persistente `pgdata`.

Configurar base de datos:
- `DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/trading_phantom`
- Alternativa local (por defecto): SQLite (`analytics.db`).

Arranque rápido:
```powershell
docker compose up -d --build
docker compose ps
```

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

**Última actualización**: 2026
**Status**: En desarrollo activo ✨
