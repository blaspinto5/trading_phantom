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

## ⚡ Inicio rápido (5 minutos)

### Requisitos previos
- **Windows 10+** (requerido para MT5 y PyInstaller)
- **Python 3.10+** (descarga desde [python.org](https://www.python.org/downloads/))
- **MetaTrader 5 instalado** (si vas a operar en vivo)

### Instalación y setup

```powershell
# 1. Clonar/descargar repositorio
cd PROYECTO\ 2

# 2. Crear entorno virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Instalar dependencias
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. Lanzar aplicación (Flask + UI nativa)
python scripts/launcher.py --debug
```

La aplicación se abrirá en una ventana nativa. Accede también a:
- **API REST**: http://127.0.0.1:5000
- **Documentación API**: Ver [docs/API.md](docs/API.md)

### Primeros pasos

**Opción A: Backtesting interactivo (sin operación real)**
```powershell
# Ejecutar backtest desde la UI o mediante API
# POST http://127.0.0.1:5000/api/backtest con parámetros
```

**Opción B: Iniciar bot en demo/vivo**
```powershell
# Desde PowerShell:
$payload = @{ debug = $true; iterations = 1 }
Invoke-RestMethod -Uri http://127.0.0.1:5000/api/bot/start `
  -Method Post `
  -Body ($payload | ConvertTo-Json -Depth 5) `
  -ContentType 'application/json'
```

**Opción C: Ejecutar tests rápidos**
```powershell
# Verificar que todo funciona
python -m pytest -q
```

> 💡 **Más detalles**: Ver [docs/QUICKSTART.md](docs/QUICKSTART.md) para guía completa con pantallazos

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

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

**Última actualización**: 2024
**Status**: En desarrollo activo ✨
