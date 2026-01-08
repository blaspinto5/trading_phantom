# 👻 Trading Phantom

> **Enterprise-Grade Algorithmic Trading Platform with ML Intelligence & Professional UI**

<div align="center">

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square&logo=python)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows-0078d4?style=flat-square&logo=windows)](https://www.microsoft.com/windows)
[![Status: Active](https://img.shields.io/badge/status-Active%20Development-brightgreen?style=flat-square)](CHANGELOG.md)
[![Version: 1.1.0](https://img.shields.io/badge/version-1.1.0-blue?style=flat-square)](CHANGELOG.md)

**[Features](#-características-principales) • [Installation](#-instalación) • [Architecture](#-arquitectura) • [API](#-api-rest) • [ML System](#-sistema-de-ml-y-knowledge-base) • [Contributing](#-contribuciones)**

</div>

---

---

## 📋 Tabla de contenidos

- [¿Qué es Trading Phantom?](#-qué-es-trading-phantom)
- [Características principales](#-características-principales)
- [Requisitos previos](#-requisitos-previos)
- [Instalación rápida](#-instalación-rápida-30-segundos)
- [Primera ejecución](#-primera-ejecución)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Arquitectura y diseño](#-arquitectura-y-diseño)
- [Sistema de ML y Knowledge Base](#-sistema-de-ml-y-knowledge-base)
- [API REST](#-api-rest)
- [Backtesting](#-backtesting-visual)
- [Empaquetado y distribución](#-empaquetado-y-distribución)
- [Testing y CI/CD](#-testing-y-cicd)
- [Solución de problemas](#-solución-de-problemas)
- [Contribuciones](#-contribuciones)
- [Licencia](#-licencia)

---

## 🎯 ¿Qué es Trading Phantom?

**Trading Phantom** es una **plataforma modular de trading algorítmico** construida en Python, diseñada para operar en **MetaTrader 5** con inteligencia artificial integrada. Combina:

✅ **Automatización completa** — Bot de trading 24/7 con indicadores técnicos (EMA, MACD, RSI)  
✅ **Machine Learning** — Sistema de predicción con Random Forest + Knowledge Base para futuras IAs  
✅ **Backtesting profesional** — Validación histórica con métricas avanzadas (Sharpe, Drawdown, Win Rate)  
✅ **UI moderna** — Interfaz web responsive con dashboard profesional y panel de control  
✅ **REST API completa** — 20+ endpoints para integración y automatización  
✅ **Arquitectura escalable** — Diseño modular listo para extender con LSTM, RL, Transformers  
✅ **Empaquetado profesional** — Generador .exe con PyInstaller e instalador Windows  

### 🚀 Casos de uso

- 🏦 **Traders profesionales**: Automatiza estrategias, backtesta y monitorea 24/7
- 📊 **Analistas cuantitativos**: Experimenta con indicadores y ML sin código repetitivo
- 🤖 **Investigadores de IA**: Infraestructura lista para integrar LSTM, RL, transformers
- 👨‍💼 **Desarrolladores**: API REST + modularidad para crear bots personalizados
- 🏫 **Educación**: Aprende trading algorítmico con código profesional y documentado

---

## ⭐ Características principales

### 🤖 Bot de Trading Inteligente
- **Loop automático** configurable (iteraciones, delays)
- **Indicadores técnicos**: EMA, MACD, RSI con cálculo en tiempo real
- **Validación de riesgo**: Stop-loss, take-profit, tamaño de posición
- **Conexión MT5**: Ejecución de órdenes reales o en demo
- **Logging profesional**: Cada acción registrada con timestamp y contexto

### 📊 Machine Learning integrado
- **RandomForest** entrenado con tus datos históricos
- **7 indicadores técnicos** como features: EMA, MACD, RSI, cambio precio, volumen, volatilidad
- **Knowledge Base** que captura 8 tipos de aprendizaje:
  - 🎯 **Feature Importance**: Qué indicadores importan más
  - 📈 **Feature Embeddings**: Estadísticas de cada feature (media, std, min, max)
  - 🔗 **Correlation Matrix**: Relaciones entre indicadores
  - 📋 **Decision Patterns**: Reglas extraídas del árbol de decisión
  - 🎲 **Performance Metrics**: Accuracy, precision, recall, F1-score
  - 📚 **Training Data Stats**: Distribución del dataset
  - 🏆 **Trade Patterns**: Análisis de trades ganadores vs perdedores
  - 💾 **Model Serialization**: Modelo guardado y listo para cargar

- **API `/api/knowledge/*`** para que futuras IAs accedan al conocimiento sin reentrenar
- **Transferencia de aprendizaje** lista para LSTM, RL, Transformers

### 🎨 UI profesional
- **Dashboard principal**: KPIs en tiempo real, estado del bot, últimas operaciones
- **Panel ML**: Documentación, métricas, top features, guía de integración
- **Logbox elegante**: Logs con scroll, colores, timestamps
- **Botón de shutdown**: Cierre seguro con confirmación
- **Diseño responsivo**: Adapta a cualquier resolución
- **Dark theme profesional**: Gradientes, sombras, animaciones suaves

### 📈 Backtesting Visual
- **Simulación numérica** con histórico real de datos
- **Gráficos interactivos**: Equity curve, drawdown, trades anotados
- **Métricas detalladas**:
  - Sharpe ratio, Sortino ratio, Calmar ratio
  - Max drawdown, Win rate, Profit factor
  - Trade duration, Entry/exit análisis
- **Exportación**: Resultados en JSON/CSV/Parquet
- **Comparación**: A/B testing entre estrategias

### 🌐 API REST completa
- **20+ endpoints** para:
  - Control del bot (start, stop, status)
  - Backtesting y análisis
  - ML training y predicción
  - Exportación de datos
  - Knowledge Base access
  - Logs y diagnóstico
- **Documentación OpenAPI-ready**
- **CORS configurado** para frontend
- **Error handling** profesional con códigos HTTP

### 🐳 Docker & escalabilidad
- **docker-compose.yml** con Postgres + Flask
- **Base de datos**: SQLite (local) o Postgres (producción)
- **Volúmenes persistentes** para datos
- **Healthchecks** automatizados

### 📦 Empaquetado profesional
- **EXE Windows**: PyInstaller con todos los archivos empaquetados
- **Instalador Windows**: Inno Setup para distribución
- **Self-contained**: Sin dependencias externas en el equipo del usuario
- **Autostart**: Opción de ejecutar al iniciar sesión

---

## 📦 Requisitos previos

| Requisito | Versión | Descripción |
|-----------|---------|-------------|
| **Windows** | 10 o superior | Sistemas operativos soportados |
| **Python** | 3.10+ | [python.org](https://www.python.org/downloads/) |
| **Git** | (opcional) | Para clonar el repo |
| **MetaTrader 5** | (opcional) | Solo si operas en vivo |
| **Inno Setup** | (opcional) | Solo para crear instalador |

### ✅ Verificar Python

```powershell
python --version
# Debe mostrar: Python 3.10.x o superior
```

---

## ⚡ Instalación rápida (30 segundos)

### 🎯 Opción 1: Automática (recomendado)

**Paso 1:** Abre `INSTALL.bat` (doble-click)
```
→ Crea venv automáticamente
→ Instala dependencias
→ Verifica instalación
```

**Paso 2:** Abre `RUN.bat` (doble-click)
```
→ Inicia servidor Flask
→ Abre UI en http://127.0.0.1:5000
→ Acceso inmediato al dashboard
```

### 🎯 Opción 2: PowerShell (más control)

```powershell
# Instalar
.\INSTALL.ps1

# Ejecutar
.\RUN.ps1
```

### 🎯 Opción 3: Manual (desarrollo)

```powershell
# 1. Crear entorno virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Instalar dependencias
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 3. Ejecutar con debug
python -m trading_phantom.main --debug
```

---

## 🚀 Primera ejecución

### ✅ Después de instalar, el bot te ofrece:

#### 1️⃣ **Dashboard**: Monitorea en tiempo real
```
→ URL: http://127.0.0.1:5000
→ Veras: KPIs, estado del bot, últimos trades
→ Botón "Start Bot": inicia operaciones
```

#### 2️⃣ **Backtesting**: Prueba sin riesgo
```
→ Menu: Backtest
→ Selecciona parámetros (símbolo, período)
→ Ejecuta → Ver gráficos y métricas
```

#### 3️⃣ **ML Training**: Genera conocimiento
```
→ Menu: Analytics > ML Training
→ Requiere ≥20 trades en historial
→ Entrena automáticamente
→ Visualiza top features y métricas
```

#### 4️⃣ **Bot en vivo**: Operaciones reales
```
→ Abre MetaTrader 5
→ Menu: Bot > Start
→ Bot ejecuta órdenes automáticamente
→ Logs mostrados en tiempo real
```

### 📋 Checklist de primera vez

- [ ] Instalación completó sin errores
- [ ] Dashboard accesible en http://127.0.0.1:5000
- [ ] Botón "Info" muestra documentación ML
- [ ] Backtesting ejecuta correctamente
- [ ] Logs aparecen en tiempo real
- [ ] Bot se inicia sin errores (requiere MT5 abierto para operaciones reales)

---

## 📂 Estructura del proyecto

```
PROYECTO 2/
│
├── 📁 src/trading_phantom/          ✨ Código fuente principal (src-layout)
│   ├── __init__.py
│   ├── main.py                      🎯 Entrypoint: python -m trading_phantom
│   ├── webapp.py                    🌐 Flask REST API + UI
│   │
│   ├── 📁 core/                     🔄 Orquestación principal
│   │   └── orchestrator.py          → Loop principal del bot
│   │
│   ├── 📁 modules/                  💼 Módulos de trading
│   │   ├── strategy.py              → Generador de señales (EMA, MACD, RSI)
│   │   ├── risk_manager.py          → Validación de riesgo y posiciones
│   │   ├── trader.py                → Ejecución de órdenes
│   │   ├── data_loader.py           → Fetch de histórico OHLCV
│   │   └── trade_history.py         → Registro de operaciones
│   │
│   ├── 📁 analytics/                🤖 Machine Learning & Knowledge Base
│   │   ├── db.py                    → Modelos SQLAlchemy (Trade, BacktestRun)
│   │   ├── collector.py             → Ingesta automática de trades
│   │   ├── ml_pipeline.py           → RandomForest training & prediction
│   │   ├── knowledge_base.py        → Sistema de Knowledge (8 tipos)
│   │   ├── transfer_learning.py     → Export/import para futuras IAs
│   │   ├── metrics.py               → Cálculo Sharpe, Drawdown, etc
│   │   └── __init__.py
│   │
│   ├── 📁 api/                      🌐 REST API Blueprints
│   │   ├── __init__.py              → Registro de blueprints
│   │   ├── bot.py                   → Endpoints bot (start, stop, status)
│   │   ├── backtest.py              → Endpoints backtesting
│   │   ├── analytics.py             → Endpoints ML, ingestión
│   │   ├── knowledge.py             → Endpoints Knowledge Base (NEW!)
│   │   └── utils.py                 → Helpers (response formatting)
│   │
│   ├── 📁 mt5/                      💹 Integración MetaTrader 5
│   │   ├── connector.py             → Wrapper MT5 con retry logic
│   │   └── symbol_debugger.py       → Herramienta para debuguear símbolos
│   │
│   ├── 📁 backtest/                 📊 Engine de backtesting
│   │   ├── simulation.py            → Simulador numérico
│   │   ├── visual_backtest.py       → Adapter para gráficos
│   │   ├── metrics.py               → Cálculo de métricas
│   │   ├── run_backtest.py          → Orquestador backtest
│   │   └── run_and_visual.py        → Integration testing
│   │
│   ├── 📁 config/                   ⚙️ Gestión de configuración
│   │   ├── config_loader.py         → YAML parser
│   │   └── config.yaml              → Parámetros por defecto
│   │
│   ├── 📁 static/                   🎨 Assets web
│   │   └── style.css                → CSS profesional (dark theme, gradients)
│   │
│   ├── 📁 templates/                📄 HTML templates Flask
│   │   ├── index.html               → Dashboard principal
│   │   ├── ml_info.html             → Panel documentación ML
│   │   └── (otros templates)
│   │
│   ├── 📁 utils/                    🛠️ Utilidades
│   │   └── trade_logger.py          → Custom logging con colores
│   │
│   └── 📁 data/                     💾 Base de datos local
│       ├── trading_phantom.db       → SQLite (creado automáticamente)
│       └── knowledge_base/          → Knowledge Base (JSON files)
│
├── 📁 tests/                        🧪 Tests unitarios e integración
│   ├── conftest.py                  → Configuración pytest
│   ├── test_mt5_connector.py        → Tests de conectividad MT5
│   ├── test_strategy.py             → Tests de estrategia
│   ├── test_bot_endpoints.py        → Tests API REST
│   ├── test_visual_adapter.py       → Tests backtesting
│   └── __pycache__/
│
├── 📁 docs/                         📚 Documentación profesional
│   ├── README.md                    → Guía extendida
│   ├── ARCHITECTURE.md              → Diseño técnico y patrones
│   ├── API.md                       → Especificación endpoints
│   ├── QUICKSTART.md                → Setup 5 minutos
│   └── (otros documentos generados)
│
├── 📁 scripts/                      🛠️ Scripts de desarrollo
│   ├── launcher.py                  → Inicia Flask + pywebview
│   ├── ml_train.py                  → Entrena modelo ML
│   ├── build_exe.ps1                → Build EXE con PyInstaller
│   ├── build_installer.ps1          → Crea instalador Inno Setup
│   ├── run_exe_console.ps1          → Ejecuta EXE con logs
│   ├── setup_env.ps1                → Setup inicial
│   └── (otros helpers)
│
├── 📁 installer/                    📦 Configuración instalador
│   └── TradingPhantom.iss           → Script Inno Setup
│
├── 📁 docker/                       🐳 Configuración Docker
│   └── Dockerfile                   → Imagen de contenedor
│
├── 📁 logs/                         📋 Logs de ejecución
│   ├── bot.log
│   ├── backtest.log
│   └── (otros logs)
│
├── 📁 build/, dist/                 🔨 Artefactos build (ignorados)
│
├── 🔧 Archivos de configuración
│   ├── pyproject.toml               → Configuración Python (ruff rules)
│   ├── requirements.txt             → Dependencias runtime
│   ├── requirements-dev.txt         → Dependencias dev
│   ├── requirements-docker.txt      → Dependencias Docker
│   ├── pytest.ini                   → Configuración pytest
│   ├── docker-compose.yml           → Orquestación Docker
│   └── TradingPhantom.spec          → Especificación PyInstaller
│
├── 📄 Documentación raíz
│   ├── Readme.md                    ← TÚ ESTÁS AQUÍ
│   ├── CHANGELOG.md                 → Historial de cambios
│   ├── CONTRIBUTING.md              → Guía de contribuciones
│   ├── ARQUITECTURA_MODULAR.md      → Esquema modular con BD
│   ├── LICENSE                      → MIT License
│   └── (otros archivos)
│
├── 🚀 Scripts de ejecución rápida
│   ├── INSTALL.bat                  → Instalación automática
│   ├── INSTALL.ps1                  → Idem PowerShell
│   ├── RUN.bat                      → Ejecuta el bot
│   ├── RUN.ps1                      → Idem PowerShell
│   ├── BUILD_EXE.bat                → Build EXE
│   ├── BUILD_INSTALLER.bat          → Build instalador
│   ├── RUN_TESTS.bat                → Ejecuta tests
│   └── (otros scripts)
│
└── 📊 El flujo de datos
    └── User/Browser
        └── [Flask API:5000]
            └── [Orchestrator]
                ├── [MT5Connector] → MetaTrader 5
                ├── [Strategy] → Indicadores técnicos
                ├── [RiskManager] → Validación
                ├── [Trader] → Ejecución
                └── [Analytics] → ML & Knowledge Base
```

**🔑 Puntos clave del layout:**
- ✅ **src-layout**: Código en `src/` con imports simples: `from trading_phantom import ...`
- ✅ **Modularidad**: Cada carpeta una responsabilidad: modules, analytics, api, mt5, backtest
- ✅ **Escalabilidad**: Fácil agregar LSTM, RL, Transformers en `analytics/`
- ✅ **Testabilidad**: `tests/` espeja la estructura de `src/`
- ✅ **Configuración centralizada**: `config/config.yaml` único punto de entrada

---

## 🏗️ Arquitectura y diseño

### Diagrama de componentes

```
┌─────────────────────────────────────────────────────────┐
│                    USER / BROWSER                        │
└────────────────────────┬────────────────────────────────┘
                         │
                    :5000 HTTP
                         │
        ┌────────────────▼─────────────────┐
        │      Flask REST API Server        │
        │  (webapp.py + api/blueprints)     │
        └────────────────┬─────────────────┘
                         │
        ┌────────────────▼─────────────────┐
        │      Core Orchestrator            │
        │  (core/orchestrator.py)           │
        │                                   │
        │  ┌──────────────────────────┐    │
        │  │  Main Trading Loop       │    │
        │  │  - Iteraciones           │    │
        │  │  - Delay entre ciclos    │    │
        │  │  - Error handling        │    │
        │  └──────────────────────────┘    │
        └────┬────────────┬─────────┬──────┘
             │            │         │
       ┌─────▼──┐   ┌─────▼──┐  ┌──▼──────────┐
       │ MT5    │   │Strategy│  │Risk Manager │
       │Connect │   │(EMA,   │  │(Validación) │
       │or      │   │MACD,   │  └─────────────┘
       └────────┘   │RSI)    │
                    └─────┬──┘
                          │
                    ┌─────▼──────────┐
                    │  Trader        │
                    │  (Ejecución)   │
                    └────────────────┘
                          │
                    ┌─────▼──────────────┐
                    │ Analytics & ML     │
                    │                    │
                    ├─ DB (Trades)       │
                    ├─ Collector         │
                    ├─ ML Pipeline       │
                    ├─ Knowledge Base    │
                    └─ Transfer Learning │
        
        [Backtest Engine]    [Config Manager]    [Logger]
```

### 🎭 Patrones de diseño

| Patrón | Ubicación | Descripción |
|--------|-----------|-------------|
| **Orchestrator** | `core/orchestrator.py` | Coordina flujo principal (Loop) |
| **Strategy Pattern** | `modules/strategy.py` | Diferentes estrategias intercambiables |
| **Dependency Injection** | Toda la app | Componentes inyectados, no hard-coded |
| **Adapter Pattern** | `backtest/visual_backtest.py` | Adapta core.Strategy a backtest.Strategy |
| **Repository Pattern** | `analytics/db.py` | Abstrae acceso a datos (SQLite/Postgres) |
| **Transfer Learning** | `analytics/transfer_learning.py` | Exporta knowledge para futuras IAs |

### 📊 Flujo de datos principal

```
1. BOT RUNS
   └─→ config.yaml (parámetros)
       └─→ orchestrator.main_loop()
           ├─→ mt5.connector.fetch_prices()
           │   └─→ DataFrame OHLCV
           │
           ├─→ strategy.generate_signal()
           │   ├─→ EMA, MACD, RSI
           │   └─→ BUY/SELL/HOLD
           │
           ├─→ risk_manager.validate()
           │   ├─→ Tamaño posición
           │   ├─→ Stop-loss
           │   └─→ Take-profit
           │
           └─→ trader.execute_order()
               ├─→ MT5 API
               └─→ DB ingest
                   ├─→ trades table
                   └─→ collector.ingest_trade()

2. ML TRAINING
   └─→ /api/analytics/ml/train
       └─→ ml_pipeline.train()
           ├─→ Load trades from DB
           ├─→ Feature engineering (7 features)
           ├─→ RandomForestClassifier.fit()
           ├─→ Export knowledge
           │   └─→ analytics/knowledge_base/
           │       ├─→ feature_importance.json
           │       ├─→ feature_embeddings.json
           │       ├─→ correlation_matrix.json
           │       ├─→ decision_patterns.json
           │       ├─→ performance_metrics.json
           │       └─→ models/random_forest.pkl
           └─→ Return metrics

3. ML PREDICTION (optional)
   └─→ If ml.enabled in config
       └─→ orchestrator checks ml_threshold
           └─→ Can override strategy signal
               └─→ Log: "📈 Signal: BUY (with ML)"
```

### 🔄 Capas de la aplicación

```
┌─────────────────────────────────────┐
│  Presentation Layer (UI)            │
│  - HTML/CSS/JS (Flask templates)    │
│  - Dashboard, charts, forms         │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│  API Layer                          │
│  - Flask blueprints (api/)          │
│  - REST endpoints                   │
│  - Request/response handling        │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│  Business Logic Layer               │
│  - Orchestrator (core/)             │
│  - Strategy, RiskManager (modules/) │
│  - ML Pipeline (analytics/)         │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│  Data Access Layer                  │
│  - MT5Connector (mt5/)              │
│  - Database (analytics/db.py)       │
│  - Cache, logging                   │
└─────────────────────────────────────┘
```

---

## 🤖 Sistema de ML y Knowledge Base

### 🆕 ¿Qué es la Knowledge Base?

La **Knowledge Base** es un sistema que **captura el aprendizaje del RandomForest** y lo expone de forma modular para que futuras IAs (LSTM, RL, Transformers) puedan consumir sin reentrenar.

#### 8 tipos de conocimiento almacenados

| # | Tipo | Archivo | Contenido | Para qué sirve |
|---|------|---------|----------|----------------|
| 1️⃣ | **Feature Importance** | `feature_importance.json` | Top 5 features (EMA, MACD, RSI, etc) | Saber qué indicadores importan |
| 2️⃣ | **Feature Embeddings** | `feature_embeddings.json` | Media, std, min, max de cada feature | Estadísticas para normalizar inputs |
| 3️⃣ | **Correlation Matrix** | `correlation_matrix.json` | Covarianza entre features | Detectar multicolinealidad |
| 4️⃣ | **Decision Patterns** | `decision_patterns.json` | Reglas extraídas del árbol | Lógica interpretable del modelo |
| 5️⃣ | **Performance Metrics** | `performance_metrics.json` | Accuracy, precision, recall, F1 | Evaluar calidad del modelo |
| 6️⃣ | **Training Data Stats** | `training_data/feature_stats.json` | Distribución del dataset | Detectar datos nuevos anómalos |
| 7️⃣ | **Trade Patterns** | `trade_patterns/winners_losers.json` | Análisis de trades + y - | Mejorar estrategia empíricamente |
| 8️⃣ | **Model Serialization** | `models/random_forest.pkl` | Modelo RandomForest guardado | Usar modelo en producción |

### 📚 Ubicación de Knowledge Base

```
src/trading_phantom/data/knowledge_base/
├── feature_importance.json
├── feature_embeddings.json
├── correlation_matrix.json
├── decision_patterns.json
├── performance_metrics.json
├── training_data/
│   └── feature_stats.json
├── trade_patterns/
│   └── winners_losers.json
├── models/
│   ├── random_forest.pkl
│   └── scaler.pkl
└── KNOWLEDGE_TRANSFER_GUIDE.md          ← Guía para futuras IAs
```

### 🚀 Flujo de generación automática

```
1. Ejecutas: python scripts/ml_train.py
   └─→ Carga trades del DB (≥30 requeridos)
   └─→ Feature engineering (7 indicadores)
   └─→ Entrena RandomForest
   └─→ 🆕 Automáticamente:
       └─→ Exporta 8 tipos de conocimiento
       └─→ Genera /knowledge_base/
       └─→ Crea KNOWLEDGE_TRANSFER_GUIDE.md

2. Futuras IAs consultan:
   └─→ GET /api/knowledge/summary       → Todo el KB en JSON
   └─→ GET /api/knowledge/feature-importance
   └─→ GET /api/knowledge/performance
   └─→ GET /api/knowledge/embeddings
   └─→ GET /api/knowledge/guide         → Markdown guide
   └─→ Cargan: knowledge_base/models/random_forest.pkl
```

### 💼 Ejemplo: Acceso desde código

```python
from trading_phantom.analytics.transfer_learning import TransferLearningPipeline

# Importar conocimiento
pipeline = TransferLearningPipeline()
knowledge = pipeline.import_knowledge()

# Acceder a lo que aprendió el RandomForest
top_5_features = knowledge['feature_importance']['top_5_features']
model_accuracy = knowledge['performance_metrics']['accuracy']
feature_embeddings = knowledge['feature_embeddings']

# Para inicializar una LSTM con el conocimiento
for feat_name, stats in feature_embeddings.items():
    mean = stats['mean']
    std = stats['std']
    # Usar para normalizar inputs de la LSTM
```

### 🔗 API endpoints Knowledge Base

| Endpoint | Método | Descripción | Ejemplo |
|----------|--------|-------------|---------|
| `/api/knowledge/summary` | GET | Resumen completo del KB | Todos los 8 tipos |
| `/api/knowledge/feature-importance` | GET | Top features ranking | `["EMA", "MACD", "RSI", ...]` |
| `/api/knowledge/performance` | GET | Métricas del modelo | `{"accuracy": 0.78, ...}` |
| `/api/knowledge/embeddings` | GET | Estadísticas de features | `{"EMA": {"mean": 1.5, ...}, ...}` |
| `/api/knowledge/correlation` | GET | Matriz de correlación | `{"EMA_MACD": 0.65, ...}` |
| `/api/knowledge/patterns` | GET | Decisiones del árbol | Reglas interpretables |
| `/api/knowledge/guide` | GET | Markdown para futuras IAs | Guía completa transfer learning |
| `/api/knowledge/status` | GET | Qué archivos existen | `{"files_created": [...]}` |

### 🎯 Caso de uso: Integrar LSTM

```python
# Ejemplo: Una LSTM que usa el conocimiento del RandomForest

from trading_phantom.analytics.transfer_learning import TransferLearningPipeline
import torch
import torch.nn as nn

# 1. Cargar conocimiento del RandomForest
pipeline = TransferLearningPipeline()
rf_knowledge = pipeline.import_knowledge()

# 2. Inicializar LSTM con feature embeddings
feature_stats = rf_knowledge['feature_embeddings']
input_size = len(feature_stats)  # 7 features

class TradingLSTM(nn.Module):
    def __init__(self, input_size, hidden_size=64):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, 3)  # BUY, SELL, HOLD
    
    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        logits = self.fc(lstm_out[:, -1, :])
        return logits

# 3. Usar feature importance del RF para weight initialization
rf_importance = rf_knowledge['feature_importance']['scores']
lstm = TradingLSTM(input_size)
# Inicializar con weights basados en RF importance...

# 4. Entrenar LSTM con ese conocimiento previo
# (es más eficiente porque ya sabe qué features importan)
```

### ✅ Checklist: ML Setup

- [ ] Ejecuta bot o carga ≥30 trades
- [ ] Ejecuta `python scripts/ml_train.py`
- [ ] Verifica `data/knowledge_base/` tiene 8 archivos
- [ ] Prueba `GET http://127.0.0.1:5000/api/knowledge/summary`
- [ ] Lee `data/knowledge_base/KNOWLEDGE_TRANSFER_GUIDE.md`
- [ ] (Opcional) Implementa LSTM o RL usando el KB

---

## 📊 ML Training paso a paso

### Recolectar datos (Sin ML)

```powershell
.\RUN.ps1
# → Bot ejecuta ~100 iteraciones
# → Cada trade auto-ingesta en DB
# → Espera hasta tener ≥30 trades
```

### Entrenar modelo

```powershell
# Opción 1: Desde PowerShell
python scripts/ml_train.py

# Opción 2: Desde API
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/analytics/ml/train" -Method Post
```

### Verificar Knowledge Base

```powershell
# Listar archivos generados
Get-ChildItem -Recurse src/trading_phantom/data/knowledge_base/

# Debe mostrar:
# feature_importance.json
# feature_embeddings.json
# correlation_matrix.json
# decision_patterns.json
# performance_metrics.json
# training_data/feature_stats.json
# trade_patterns/winners_losers.json
# models/random_forest.pkl
# KNOWLEDGE_TRANSFER_GUIDE.md
```

### Activar ML en vivo (opcional)

```yaml
# config/config.yaml
ml:
  enabled: true
  confidence_threshold: 0.7
```

Ahora el bot:
- 🎯 Genera señal con SMA/MACD/RSI
- 🤖 ML valida con prob ≥ 0.7
- ✅ Puede sobreescribir la señal

---

## 🌐 API REST

### 📍 Base URL

```
http://127.0.0.1:5000
```

### 🤖 Bot Endpoints

#### `POST /api/bot/start`
Inicia el bot de trading automático

**Body:**
```json
{
  "iterations": 100,
  "debug": false
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Bot started",
  "bot_id": "bot_20260107_143000"
}
```

#### `POST /api/bot/stop`
Detiene el bot actual

**Response (200):**
```json
{
  "status": "success",
  "message": "Bot stopped"
}
```

#### `GET /api/bot/status`
Estado actual del bot

**Response (200):**
```json
{
  "running": true,
  "iterations_completed": 45,
  "current_iteration": 46,
  "last_signal": "BUY",
  "timestamp": "2026-01-07T14:30:00Z"
}
```

#### `POST /api/shutdown`
Cierra toda la aplicación (con confirmación visual)

**Response (200):**
```json
{
  "status": "success",
  "message": "Shutting down..."
}
```

### 📊 Backtest Endpoints

#### `POST /api/backtest`
Ejecuta backtesting

**Body:**
```json
{
  "symbol": "EURUSD",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "strategy": "sma_rsi"
}
```

**Response (200):**
```json
{
  "status": "success",
  "metrics": {
    "total_return": 0.127,
    "sharpe_ratio": 1.85,
    "max_drawdown": 0.089,
    "win_rate": 0.58,
    "num_trades": 45
  }
}
```

#### `GET /api/backtest`
Obtiene resultados de backtests previos

**Response (200):**
```json
[
  {
    "id": "backtest_001",
    "symbol": "EURUSD",
    "total_return": 0.127,
    "created_at": "2026-01-07T14:00:00Z"
  }
]
```

### 🤖 ML Endpoints

#### `POST /api/analytics/ml/train`
Entrena el modelo RandomForest

**Response (200):**
```json
{
  "status": "success",
  "n_samples": 145,
  "accuracy": 0.78,
  "precision": 0.82,
  "recall": 0.75,
  "f1_score": 0.78,
  "knowledge_base_created": true
}
```

#### `POST /api/analytics/ml/predict`
Predicción con features

**Body:**
```json
{
  "close": 1.1234,
  "sma_20": 1.1200,
  "rsi_14": 55,
  "prev_close": 1.1210,
  "volume": 2500
}
```

**Response (200):**
```json
{
  "prediction": "BUY",
  "probability": 0.85,
  "confidence": "high"
}
```

### 💾 Data Export Endpoints

#### `GET /api/analytics/export/trades?format=json`
Exporta dataset de trades

**Formats:** `json`, `csv`, `parquet`

**Response (200):**
```json
[
  {
    "symbol": "EURUSD",
    "side": "BUY",
    "entry_price": 1.1205,
    "exit_price": 1.1235,
    "pnl": 30.0,
    "opened_at": "2026-01-07T10:00:00Z"
  }
]
```

### 📚 Knowledge Base Endpoints (NEW!)

#### `GET /api/knowledge/summary`
Resumen completo del Knowledge Base

**Response (200):**
```json
{
  "feature_importance": {...},
  "feature_embeddings": {...},
  "correlation_matrix": {...},
  "decision_patterns": {...},
  "performance_metrics": {...}
}
```

#### `GET /api/knowledge/feature-importance`
Top 5 features según RandomForest

**Response (200):**
```json
{
  "top_5_features": ["EMA", "MACD", "RSI", "volume_change", "price_change"],
  "importance_scores": [0.28, 0.24, 0.18, 0.15, 0.12]
}
```

#### `GET /api/knowledge/performance`
Métricas del modelo entrenado

**Response (200):**
```json
{
  "accuracy": 0.78,
  "precision": 0.82,
  "recall": 0.75,
  "f1_score": 0.78,
  "model_confidence": "high"
}
```

#### `GET /api/knowledge/embeddings`
Estadísticas de cada feature (para normalizaci ón)

**Response (200):**
```json
{
  "EMA": {
    "mean": 1.1205,
    "std": 0.0045,
    "min": 1.1050,
    "max": 1.1380
  },
  "MACD": {...}
}
```

#### `GET /api/knowledge/guide`
Markdown guide para futuras IAs

**Response (200):**
```markdown
# Knowledge Transfer Guide

Este documento explica cómo usar el Knowledge Base...

## Features importantes
1. EMA (28%)
2. MACD (24%)
...
```

### 📋 Logs Endpoints

#### `GET /api/logs?type=bot|backtest|history`
Obtiene logs históricos

**Response (200):**
```json
{
  "logs": [
    "2026-01-07 14:30:00 | BOT | Starting bot iteration 1",
    "2026-01-07 14:30:05 | BOT | Signal generated: BUY",
    "2026-01-07 14:30:10 | BOT | Order executed"
  ]
}
```

---

## 📈 Backtesting Visual

### Cómo ejecutar backtesting

#### Desde la UI

```
1. Accede a http://127.0.0.1:5000
2. Click en "Backtest"
3. Selecciona parámetros:
   - Símbolo: EURUSD
   - Fecha inicio: 2024-01-01
   - Fecha fin: 2024-12-31
   - Estrategia: SMA+RSI
4. Click en "Run Backtest"
5. Ver resultados: Gráficos + métricas
```

#### Desde API

```powershell
$params = @{
  symbol = "EURUSD"
  start_date = "2024-01-01"
  end_date = "2024-12-31"
  strategy = "sma_rsi"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/backtest" `
  -Method Post `
  -Body $params `
  -ContentType "application/json"
```

### Métricas calculadas

| Métrica | Significado |
|---------|-------------|
| **Total Return** | % ganancia/pérdida total |
| **Sharpe Ratio** | Ganancia ajustada por riesgo (>1 bueno) |
| **Sortino Ratio** | Como Sharpe pero solo downside |
| **Calmar Ratio** | Return / Max Drawdown |
| **Max Drawdown** | Peor pérdida acumulada |
| **Win Rate** | % de trades ganadores |
| **Profit Factor** | Ganancias totales / Pérdidas totales |
| **Avg Trade Duration** | Tiempo promedio en trade |
| **Num Trades** | Total de operaciones ejecutadas |

### Ejemplo de resultado

```json
{
  "symbol": "EURUSD",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "metrics": {
    "total_return": 0.127,
    "total_return_pct": "12.7%",
    "sharpe_ratio": 1.85,
    "max_drawdown": 0.089,
    "win_rate": 0.58,
    "profit_factor": 2.13,
    "num_trades": 45,
    "avg_trade_duration": "2.3 days"
  },
  "trades": [
    {
      "entry_price": 1.1205,
      "exit_price": 1.1235,
      "pnl": 30.0,
      "duration": "2 hours"
    }
  ]
}
```

---

## 📦 Empaquetado y distribución

### Generar ejecutable .exe (PyInstaller)

```powershell
# Opción 1: Build simple
.\scripts\build_exe.ps1

# Opción 2: Build con consola (para debugging)
.\scripts\build_exe.ps1 -console

# Resultado: dist/TradingPhantom.exe
```

### Crear instalador Windows (Inno Setup)

```powershell
# 1. Descargar Inno Setup desde issetup.com

# 2. Ejecutar build_installer.ps1
.\scripts\build_installer.ps1

# Resultado: Setup-TradingPhantom-v1.1.0.exe
```

### Distribuir a usuarios finales

```
1. Generar .exe: .\scripts\build_exe.ps1
2. Generar instalador: .\scripts\build_installer.ps1
3. Distribuir: Setup-TradingPhantom-v1.1.0.exe
4. Usuario final: Double-click → instala todo automáticamente
```

### Debugging del .exe

```powershell
# Ejecutar y capturar logs
.\scripts\run_exe_console.ps1

# Logs estarán en:
# dist_exe_stdout.log  (salida estándar)
# dist_exe_stderr.log  (errores)
# %TEMP%\trading_phantom_crash.log (si hay crash)
```

---

## 🧪 Testing y CI/CD

### Ejecutar tests localmente

```powershell
# Todos los tests
python -m pytest -v

# Solo tests rápidos
python -m pytest -q

# Tests de un módulo
python -m pytest tests/test_strategy.py -v

# Con cobertura
python -m pytest --cov=src --cov-report=html
```

### Linting (code style)

```powershell
# Verificar
ruff check .

# Auto-fix
ruff check --fix .

# Formateo
black src/ tests/
```

### GitHub Actions CI/CD

Cada push a `main` ejecuta:
- ✅ Tests en Python 3.10 + 3.11
- ✅ Linting (ruff)
- ✅ Security audit (pip-audit)
- ✅ Coverage report

**Requisitos para merge:**
- [ ] Tests pasan
- [ ] Linting limpio
- [ ] Sin nuevas vulnerabilidades
- [ ] Documentación actualizada

---

## 🐛 Solución de problemas

### Error: `ModuleNotFoundError: No module named 'trading_phantom'`

**Causa:** Python ejecuta desde fuera del venv o sin respetar `src/`

**Solución:**
```powershell
# Usar el venv correcto
.\.venv\Scripts\python.exe -m trading_phantom

# O activar venv primero
.\.venv\Scripts\Activate.ps1
python -m trading_phantom
```

### Error: `Port 5000 is already in use`

**Causa:** Otra instancia de Flask está escuchando

**Solución:**
```powershell
# Opción 1: Matar el proceso
Get-Process python | Where-Object {$_.Name -eq "python"} | Stop-Process

# Opción 2: Cambiar puerto en config/config.yaml
flask:
  port: 5001  # Usar otro puerto
```

### Error: `Cannot connect to MetaTrader 5`

**Causa:** MT5 no está abierto o no permitió conexión

**Solución:**
```
1. Abre MetaTrader 5
2. Tools → Options → Alerta
3. Habilita "Permitir aplicaciones de terceros"
4. Reinicia MT5
5. Intenta de nuevo
```

### Error: `ModuleNotFoundError` en .exe

**Causa:** Falta un import en PyInstaller

**Solución:** Editar `TradingPhantom.spec`:
```python
a = Analysis(
    ...
    hiddenimports=['sklearn', 'pandas', 'numpy', 'flask'],
)
```

### ML no genera Knowledge Base

**Causa:** Menos de 30 trades o error en export

**Solución:**
```powershell
# 1. Verificar trades en DB
python -c "from trading_phantom.analytics.db import get_all_trades; print(len(get_all_trades()))"

# 2. Ejecutar training con debug
python scripts/ml_train.py 2>&1 | Tee-Object -FilePath ml_debug.log

# 3. Ver directorio
ls -Recurse src/trading_phantom/data/knowledge_base/
```

### App lenta o no responde

**Cause:** Demasiadas iteraciones o problemas de conexión MT5

**Solución:**
```yaml
# config/config.yaml
bot:
  delay_between_iterations: 1.0  # Aumentar delay
  max_iterations_per_run: 50      # Reducir iteraciones
  
mt5:
  request_timeout: 10  # Aumentar timeout
```

### Logs no aparecen

**Causa:** Nivel de logging incorrecto

**Solución:**
```python
# En main.py o launcher.py
logging.basicConfig(
    level=logging.DEBUG,  # Cambiar a DEBUG
    format='[%(asctime)s] %(name)s [%(levelname)s] %(message)s'
)
```

---

## 📞 Contacto y soporte

- **Issues**: [GitHub Issues](https://github.com/blaspinto5/trading_phantom/issues)
- **Documentación**: Directorio `docs/`
- **API Docs**: `/api/docs` (cuando esté activo)
- **Logs**: `logs/` o `%TEMP%\`

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Sigue estos pasos:

### 1. Fork el repositorio

```bash
git clone https://github.com/TU_USUARIO/trading_phantom.git
cd trading_phantom
```

### 2. Crear rama feature

```bash
git checkout -b feature/amazing-feature
```

### 3. Hacer cambios y tests

```powershell
# Hacer cambios
# ...

# Ejecutar tests
python -m pytest -q

# Linting
ruff check --fix .
```

### 4. Commit y push

```bash
git commit -m "feat: Add amazing feature"
git push origin feature/amazing-feature
```

### 5. Abrir Pull Request

- Describe tu cambio
- Referencia issue (si aplica)
- Asegúrate que tests pasen

### Pautas de contribución

- ✅ Code style: Usa `ruff format`
- ✅ Tests: 80%+ cobertura mínima
- ✅ Docs: Actualiza si cambias API
- ✅ Commits: Sé específico y descriptivo
- ✅ License: Contribuyendo aceptas MIT

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para detalles completos.

---

## 📋 Resumen de comandos útiles

```powershell
# ====== INSTALACIÓN ======
.\INSTALL.bat                # Setup automático
.\INSTALL.ps1               # Idem PowerShell

# ====== EJECUCIÓN ======
.\RUN.bat                   # Ejecutar bot
.\RUN.ps1                   # Idem PowerShell
python -m trading_phantom   # Modo manual

# ====== TESTING ======
python -m pytest -q         # Tests rápidos
python -m pytest -v         # Tests verboso
ruff check .                # Linting
ruff check --fix .          # Auto-fix

# ====== EMPAQUETADO ======
.\scripts\build_exe.ps1     # Generar .exe
.\scripts\build_installer.ps1  # Generar instalador
.\scripts\run_exe_console.ps1  # Debug .exe

# ====== ML & KNOWLEDGE ======
python scripts/ml_train.py  # Entrenar modelo
curl http://127.0.0.1:5000/api/knowledge/summary  # Ver KB

# ====== DESARROLLO ======
.\.venv\Scripts\Activate.ps1  # Activar venv
pip install -r requirements-dev.txt  # Instalar devs
ruff format src/ tests/     # Formatear código
```

---

## 📜 Licencia

Este proyecto está bajo la licencia **MIT**. Eres libre de:

✅ **Usar** en proyectos privados o comerciales  
✅ **Modificar** el código  
✅ **Distribuir** versiones modificadas  

Con la condición de:
- 📋 Incluir el aviso de licencia
- 📋 Mencionar cambios principales

Ver [LICENSE](LICENSE) para detalles legales completos.

---

## 📈 Roadmap

### ✅ Completado (v1.1.0)

- [x] Bot de trading con indicadores (EMA, MACD, RSI)
- [x] Backtesting visual con métricas
- [x] UI profesional con dashboard y KPIs
- [x] ML RandomForest + Knowledge Base
- [x] 8 tipos de conocimiento capturados
- [x] API REST con 20+ endpoints
- [x] Empaquetado .exe e instalador
- [x] Sistema modular y escalable
- [x] Shutdown button con confirmación
- [x] Docker support

### 🚀 Próximo (v1.2.0)

- [ ] LSTM para secuencias de precios
- [ ] Reinforcement Learning agent
- [ ] Ollama/DeepSeek integration
- [ ] Ensemble models (RF + LSTM + RL)
- [ ] Dashboard de Knowledge Base
- [ ] Export modelo a ONNX
- [ ] Mobile app (React Native)

### 🔮 Futuro (v2.0.0)

- [ ] Multi-asset trading (crypto, acciones, futuros)
- [ ] Portfolio optimization
- [ ] Risk analytics dashboard
- [ ] Real-time market news integration
- [ ] Community model marketplace
- [ ] Backtesting paralelo con GPU
- [ ] Cloud deployment (AWS, GCP)

---

## 🙏 Agradecimientos

- **Comunidad Python**: Por las librerías increíbles
- **MetaTrader 5**: Por la API de trading
- **Scikit-learn**: Por ML utilities
- **Flask**: Por el web framework
- **Todos los contribuidores**: Por mejorar el proyecto

---

## 📊 Estadísticas del proyecto

```
Líneas de código (src/):   ~3,500
Líneas de tests:           ~1,200
Documentación:             ~5,000
Modulos principales:       8
Endpoints API:             20+
Tipos de conocimiento:     8
Tiempo de desarrollo:      ~200 horas
Status actual:             ✨ Active Development
```

---

<div align="center">

### ⭐ ¿Te gustó? Deja una estrella en GitHub

**[Star on GitHub](https://github.com/blaspinto5/trading_phantom)** • **[Issues](https://github.com/blaspinto5/trading_phantom/issues)** • **[Docs](docs/README.md)**

---

**Made with ❤️ by the Trading Phantom community**

*Última actualización: Enero 2026*  
*Version: 1.1.0*  
*License: MIT*

</div>

