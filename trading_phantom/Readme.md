````md
# 🤖 Trading Phantom
### Plataforma de Trading Algorítmico en MetaTrader 5 (Python)

> **Trading Phantom** es una plataforma de trading algorítmico diseñada con enfoque profesional para operar en **MetaTrader 5 (MT5)** mediante su **API oficial en Python**.

---

## 📌 Descripción General

El objetivo del proyecto es construir una **arquitectura robusta, extensible y segura**, capaz de:

- ⚙️ Ejecutar estrategias de trading automáticas
- 🛡️ Gestionar el riesgo de forma estricta
- 🔌 Interactuar de manera segura con brokers reales
- 🚫 Evitar errores comunes de MT5 (volumen, stops, horarios, permisos)
- 📈 Servir como base para backtesting, optimización y trading en real

> ⚠️ Este **no es un bot “rápido”**, sino una **base sólida de trading algorítmico real**.

---

## 🧠 Filosofía del Proyecto

Trading Phantom sigue principios **profesionales y realistas**:

- ❌ No forzar operaciones
- ❌ No ignorar reglas del broker
- ❌ No “parchear” errores sin entenderlos

- ✅ Validar todo antes de enviar una orden
- ✅ Fallar de forma controlada y explicable
- ✅ Separar responsabilidades (arquitectura limpia)

> Muchos bots fallan por **no respetar MT5**.
> **Trading Phantom existe para no cometer esos errores.**

---

## 🧱 Arquitectura del Sistema

```text
trading_phantom/
│
├── main.py              # Orquestador principal
├── config.yaml          # Configuración central
│
├── mt5_connector.py     # Comunicación con MetaTrader 5
├── strategy.py          # Lógica de señales
├── risk_manager.py      # Gestión de riesgo y validaciones
├── trader.py            # Ejecutor de órdenes
│
├── debug_symbol.py      # Diagnóstico de símbolos MT5
└── README.md            # Documentación
````

---

## 🔧 Componentes y Justificación Técnica

### 1️⃣ MT5Connector

📄 `mt5_connector.py`

Responsable de **toda la comunicación con MetaTrader 5**.

**Funciones clave**

* Inicializar conexión con MT5
* Resolver símbolos con sufijos (`EURUSD` → `EURUSD-T`)
* Obtener precios y ticks
* Enviar órdenes (**pending**)
* Cerrar posiciones
* Consultar posiciones abiertas

**Decisiones importantes**

* ❗ Uso de **PENDING ORDERS** en lugar de MARKET
* ❗ Uso de `ORDER_FILLING_RETURN`
* ❗ Normalización estricta del símbolo
* ❗ Cumplimiento de `trade_stops_level`

---

### 2️⃣ Strategy

📄 `strategy.py`

Encapsula la **lógica de generación de señales**.

* Usa datos históricos desde MT5
* Puede usar indicadores técnicos (SMA, RSI, etc.)
* Devuelve señales: `BUY`, `SELL`, `HOLD`

---

### 3️⃣ RiskManager

📄 `risk_manager.py`

🧠 **El corazón del sistema**.

**Validaciones**

* Máximo número de posiciones
* Riesgo por trade
* Lotes válidos según broker
* Hard cap de seguridad
* Stop Level
* Pérdida diaria máxima
* SL / TP siempre válidos

---

### 4️⃣ Trader

📄 `trader.py`

Ejecuta órdenes **solo si**:

* La señal es válida
* El riesgo es aprobado
* El mercado está abierto

---

### 5️⃣ main.py

📄 `main.py`

**Flujo principal**

1. Cargar configuración
2. Conectar a MT5
3. Inicializar módulos
4. Loop de ejecución
5. Manejo de errores y cierre limpio

---

## ⚙️ Configuración (`config.yaml`)

```yaml
mode: demo
log_level: INFO

symbol: EURUSD
timeframe: H1
max_positions: 1

risk:
  risk_per_trade: 0.01
  fixed_lot: null
  max_daily_loss: 0.03

orders:
  sl_pips: 20
  tp_pips: 40
  deviation: 50

execution:
  loop_interval_seconds: 60
```

---

## 🧪 Errores Reales de MT5

### ❌ Error 10027

* Volumen inválido
* SL / TP incorrectos
* Restricciones del broker

### ❌ Error 10018

* Mercado cerrado
* Horarios Forex

---

## 🔐 Seguridad y Buenas Prácticas

* ❌ No operar sin SL
* ❌ No forzar lotes
* ✅ Consultar siempre `symbol_info`
* ✅ Separar decisión y ejecución

---

## 🚀 Roadmap

* 📊 Logging profesional
* 📈 Backtesting
* 🧠 Machine Learning
* 🌐 Dashboard
* 💼 Cuenta real

---

## ⚠️ Advertencia

Proyecto **educativo y experimental**.
Usar **SIEMPRE en demo** antes de real.

---

## 🧑‍💻 Autor

Desarrollado con enfoque profesional y experiencia real en MT5.

---

## ⭐ Contribuciones

* Estrategias
* Tests
* Optimización
* Documentación

---

## ✅ Estado del Proyecto

* 🟢 Funcional en demo
* 🟡 En expansión
* 🔵 Arquitectura estable

---

## 🧪 Tests & Calidad

- Ejecutar tests: `python -m pytest -q`
- Las pruebas están en `trading_phantom/tests/`
- Añade más pruebas para mejorar cobertura y seguridad del bot.

---
## ⚡ Quickstart — ejecutar (demo)

Sigue estos pasos rápidos para ejecutar el bot en modo **demo**:

1. Crear y activar un entorno virtual (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

2. Ejecutar el bot (recomendado, con control de iteraciones):

- PowerShell (con el script):
  - `scripts\run_demo.ps1 -Iterations 40 -Debug`
- Windows CMD (ejecuta el batch):
  - `run_demo.bat 40 debug`
- Módulo Python (cross-platform):
  - `python -m trading_phantom.main --iterations 40 --debug`

3. Detener el bot:

- En la terminal: presiona `Ctrl+C` para detenerlo de forma segura.
- Si el proceso se ejecuta en background (Windows PowerShell):
  - Obtener PID: `Get-Process -Name python`
  - Matar proceso: `Stop-Process -Id <PID>`
- En CMD: `tasklist` / `taskkill /PID <PID> /F`

> 💡 Usa `--iterations` para no quedarte colgado en un bucle infinito durante pruebas.

---
## ▶️ Ejecutar Backtest + Visual

Puedes ejecutar el backtest numérico y generar el plot interactivo (usando los mismos módulos/estrategia) de dos formas:

1) Desde la raíz del proyecto (recomendado):

```bash
pyt0hon -m trading_phantom.backtest.run_and_visual
python -m trading_phantom.backtest.run_backtest
python -m trading_phantom.backtest.visual_backtest
```

2) Desde dentro de la carpeta `trading_phantom` (alternativa):

```bash
cd trading_phantom
python -m backtest.run_and_visual
```

Opciones claves:
- `symbol`, `timeframe`, `bars`, `sma_period`, `rsi_period`
- Ejecutar el orquestador por un número limitado de iteraciones: `python -m trading_phantom.main --iterations 5` o `--once` para una iteración.
- En entornos sin GUI (CI/tests) llama a `run_visual_backtest(df, plot=False)` para evitar abrir una ventana.

---

## 🖥️ Aplicación de Escritorio (Windows .exe + instalador) ✅

He añadido un empaquetado básico para convertir la aplicación en un ejecutable de Windows y crear un instalador.

Características:
- Interfaz nativa (pywebview) que abre una ventana con el dashboard local.
- Servidor local (Flask) que sirve la app y expone APIs para: arrancar/detener el bot, ejecutar backtests y consultar logs.
- Scripts útiles:
  - `scripts/launcher.py` — Arranca el servidor y abre la ventana nativa (modo desarrollo y empaquetado). Ahora soporta import diferido y manejo de errores para builds empaquetadas.
  - `scripts/build_exe.ps1` — Script PowerShell que crea un `.exe` usando PyInstaller (agrega templates, assets y config). Incluye `--collect-all trading_phantom` para evitar módulos faltantes.
  - `installer/TradingPhantom.iss` — Plantilla Inno Setup para generar instalador `.exe` (ajusta rutas antes de compilar).

Interfaz de control del bot (one-click)

- La UI del dashboard incluye ahora un panel de control para el bot con:
  - **Iterations** (opcional): limitar número de iteraciones para pruebas.
  - **Debug** (checkbox): activar modo debug en el bot.
  - **Start Bot (one-click)**: arranca el orquestador con los parámetros indicados.
  - **Stop Bot**: detiene el proceso en ejecución.
  - **Bot Logs**: panel que muestra `trading_phantom/logs/bot.log` y se refresca automáticamente cuando el bot está corriendo.

Endpoints relacionados:
- `POST /api/bot/start` — inicia el bot. Body opcional JSON: `{ "iterations": 100, "debug": true }`.
- `POST /api/bot/stop` — detiene el bot.
- `GET /api/bot/status` — devuelve `{ "running": true, "pid": 1234 }` o `{ "running": false }`.
- `GET /api/logs?bot=true&lines=200` — obtiene las últimas N líneas de `bot.log`.

Quickstart:

1. Crear entorno e instalar dependencias:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r trading_phantom/requirements.txt
```

2. Ejecutar en modo desarrollo (abre ventana):

```powershell
python scripts/launcher.py --debug
```

3. Para generar un `.exe` (one-file) desde PowerShell:

```powershell
# Asegúrate de ejecutar PowerShell como Administrador si tienes restricciones de permisos.
# 1) Crea/activa venv e instala dependencias automáticamente (el script hace esto si falta):
.\.venv\Scripts\Activate.ps1  # o crea el venv si aún no existe
# 2) Ejecutar el builder (generará dist\TradingPhantom.exe)
.\scripts\build_exe.ps1 -onefile -windowed

# Opciones útiles:
# -onefile    : genera un único .exe (recomendado)
# -windowed   : empaqueta como aplicación de ventana (sin consola)

4. Compilar instalador (requiere Inno Setup): editar `installer\TradingPhantom.iss` si es necesario y ejecutar:

```powershell
# Si tienes ISCC en PATH
.\scripts\build_installer.ps1
```

El instalador resultante aparecerá en la carpeta `installer\` como `TradingPhantom_Setup.exe`.

> Nota: MetaTrader5 es necesario para la operativa en vivo; si no está disponible se recomienda usar `config.yaml` con `mode: demo`.

---

## ✅ Integración Continua (CI)

He añadido un Workflow de GitHub Actions para ejecutar linter (ruff) y pruebas (pytest) en cada push/PR sobre `main`/`master`.
El workflow se ejecuta en `windows-latest` para garantizar compatibilidad con el paquete `MetaTrader5`.

- Archivos añadidos:
  - `.github/workflows/ci.yml`
  - `requirements.txt` (dependencias runtime)
  - `requirements-dev.txt` (pytest, ruff)
  - `pyproject.toml` (config ruff)

---

```
