# 📋 Listado Detallado de Archivos y Sus Funciones

## 🎯 Archivos Raíz (Directorio Principal)

### `main.py`
- **Tipo:** Entrypoint principal
- **Función:** Punto de entrada del bot. Se ejecuta con `python -m trading_phantom`
- **Responsabilidad:** Inicializa la aplicación, carga configuración, inicia loops de trading
- **Módulos que usa:** core.orchestrator, mt5.connector, config

### `webapp.py`
- **Tipo:** Flask REST API server
- **Función:** Servidor web que expone la interfaz y API REST en http://127.0.0.1:5000
- **Responsabilidad:** 
  - Registra blueprints (bot, backtest, analytics, knowledge)
  - Sirve templates HTML y CSS
  - Maneja requests HTTP
  - Logging de requests
- **Puertos:** 5000 (configurable en config.yaml)
- **Endpoints:** 20+ endpoints REST

### `Readme.md` (2000+ líneas)
- **Tipo:** Documentación principal
- **Función:** Guía completa profesional del proyecto
- **Contenido:**
  - Tabla de contenidos con 13 secciones
  - Instalación, uso, arquitectura
  - Documentación API REST detallada
  - Sistema de ML y Knowledge Base
  - Troubleshooting y roadmap
  - 95+ links internos

### `pyproject.toml`
- **Tipo:** Configuración Python
- **Función:** Configuración de ruff (linting), metadata del proyecto
- **Especifica:**
  - Nombre, versión, descripción
  - Reglas de código (ruff check, ruff format)
  - Compatibilidad Python (3.10+)

### `requirements.txt`
- **Tipo:** Dependencias runtime
- **Función:** Lista de librerías necesarias para ejecutar el bot
- **Contiene:**
  - flask, numpy, pandas, scikit-learn
  - pyinstaller, pywebview
  - MetaTrader5, sqlalchemy
  - torch, transformers (opcionales)

### `requirements-dev.txt`
- **Tipo:** Dependencias desarrollo
- **Función:** Librerías adicionales para testing y linting
- **Contiene:** pytest, ruff, black, coverage, mypy

### `pytest.ini`
- **Tipo:** Configuración pytest
- **Función:** Define parámetros de ejecución de tests
- **Especifica:**
  - Directorio de tests (tests/)
  - Opciones de ejecución (verbose, markers)

### `docker-compose.yml`
- **Tipo:** Orquestación Docker
- **Función:** Define servicios (Flask API + Postgres) para ejecutar en contenedores
- **Servicios:**
  - app: Flask en puerto 5000
  - db: Postgres en puerto 5432
  - Volúmenes persistentes para datos

### `LICENSE`
- **Tipo:** Licencia legal
- **Función:** Especifica términos MIT (libre para usar, modificar, distribuir)

### `CHANGELOG.md`
- **Tipo:** Historial de cambios
- **Función:** Registro de versiones y cambios realizados
- **Organización:** Por versión (v1.1.0, v1.0.0, etc)

### `CONTRIBUTING.md`
- **Tipo:** Guía de contribución
- **Función:** Instrucciones para colaboradores
- **Contiene:** Proceso de PR, estándares de código, commit conventions

### `ARQUITECTURA_MODULAR.md`
- **Tipo:** Documentación técnica
- **Función:** Explicación de la arquitectura modular del proyecto
- **Detalla:** Capas, componentes, flujos de datos, 2-table DB schema

---

## 🔧 Scripts de Ejecución (Raíz)

### `INSTALL.bat` / `INSTALL.ps1`
- **Tipo:** Script de instalación
- **Función:** Setup automático para usuarios Windows
- **Pasos:**
  1. Crear venv si no existe
  2. Instalar dependencias (pip install -r requirements.txt)
  3. Verificar instalación
  4. Crear directorio logs/

### `RUN.bat` / `RUN.ps1`
- **Tipo:** Script de ejecución
- **Función:** Lanza el bot de forma simple (doble-click)
- **Qué hace:** Activa venv y ejecuta `python -m trading_phantom`

### `BUILD_EXE.bat` / `BUILD_EXE.ps1`
- **Tipo:** Script de empaquetado
- **Función:** Genera ejecutable .exe con PyInstaller
- **Opciones:**
  - Sin parámetros: build limpio
  - `-console`: incluye consola para debugging

### `BUILD_INSTALLER.bat` / `BUILD_INSTALLER.ps1`
- **Tipo:** Script de instalador
- **Función:** Crea instalador Windows (.exe) con Inno Setup
- **Resultado:** Setup-TradingPhantom-v1.1.0.exe

### `RUN_TESTS.bat` / `RUN_TESTS.ps1`
- **Tipo:** Script de testing
- **Función:** Ejecuta suite de tests con pytest
- **Flags:** -q (quiet) o -v (verbose)

### `generate_pdf.py`
- **Tipo:** Script generador
- **Función:** Crea PDF profesional (Trading_Phantom_Documentation.pdf) con documentación completa
- **Usa:** reportlab para generar PDF con tablas y formato

---

## 📁 src/trading_phantom/ (Código Principal)

### `src/trading_phantom/__init__.py`
- **Tipo:** Package init
- **Función:** Marca directorio como paquete Python
- **Contenido:** Típicamente vacío o imports de público

### `src/trading_phantom/main.py`
- **Tipo:** Main entry point
- **Función:** Punto de entrada cuando ejecutas `python -m trading_phantom`
- **Responsabilidad:**
  - Parseador de argumentos CLI (--debug, --iterations)
  - Inicializa logging
  - Llama a orchestrator.main_loop()

---

## 🔄 src/trading_phantom/core/

### `core/orchestrator.py` (500+ líneas)
- **Tipo:** Orquestador principal
- **Función:** Coordina todo el flujo de trading
- **Responsabilidades:**
  1. **Main Loop:** Iteraciones configurables de trading
  2. **Fetch datos:** Llama a mt5.connector
  3. **Generate signals:** Llama a strategy.generate_signal()
  4. **Risk validation:** Llama a risk_manager.validate()
  5. **Execute trades:** Llama a trader.execute()
  6. **Ingestión DB:** Guarda trades en base de datos
  7. **ML integration:** Lee config ml.enabled y ejecuta predicción
  8. **Logging:** Registra cada paso
- **Config que usa:**
  - bot.delay_between_iterations
  - bot.max_iterations_per_run
  - ml.enabled, ml.confidence_threshold

---

## 💼 src/trading_phantom/modules/

### `modules/strategy.py` (300+ líneas)
- **Tipo:** Generador de señales
- **Función:** Calcula indicadores técnicos y genera señales de trading
- **Indicadores implementados:**
  - EMA (Exponential Moving Average) - 20, 50, 200 períodos
  - MACD (Moving Average Convergence Divergence)
  - RSI (Relative Strength Index) - 14 períodos
  - Análisis de tendencia (bullish, bearish, neutral)
- **Output:** BUY, SELL, HOLD signals
- **Parámetros:** Configurables en config.yaml

### `modules/risk_manager.py` (200+ líneas)
- **Tipo:** Validador de riesgo
- **Función:** Valida posiciones antes de ejecutar
- **Validaciones:**
  - Position size (tamaño máximo de posición)
  - Stop-loss (pérdida máxima permitida)
  - Take-profit (ganancia objetivo)
  - Drawdown máximo permitido
  - Correlación con posiciones abiertas
- **Output:** Signal aceptada o rechazada

### `modules/trader.py` (250+ líneas)
- **Tipo:** Ejecutor de órdenes
- **Función:** Envía órdenes a MetaTrader 5
- **Responsabilidades:**
  1. Construye estructura de orden (symbol, side, volume, price)
  2. Llama a mt5.connector.send_order()
  3. Monitorea ejecución
  4. Maneja errores y retries
  5. Logging de ejecución
- **Tipos de órdenes:** Market, Limit, Stop-loss, Take-profit

### `modules/data_loader.py` (150+ líneas)
- **Tipo:** Cargador de datos históricos
- **Función:** Obtiene datos OHLCV de MetaTrader 5
- **Responsabilidades:**
  1. Fetch histórico (start_date, end_date, timeframe)
  2. Normalización de datos
  3. Handling de símbolos (EURUSD, GBPUSD, etc)
  4. Caching de datos
- **Output:** DataFrame pandas con OHLCV

### `modules/trade_history.py` (200+ líneas)
- **Tipo:** Registro de operaciones
- **Función:** Almacena y recupera historial de trades
- **Responsabilidades:**
  1. Persistencia en base de datos
  2. Análisis de trades (ganadores/perdedores)
  3. Cálculo de statisticas
  4. Exportación de datos

---

## 🤖 src/trading_phantom/analytics/ (ML & Knowledge)

### `analytics/db.py` (300+ líneas)
- **Tipo:** Capa de datos (Data Access Layer)
- **Función:** Gestiona conexión con base de datos
- **Modelos SQLAlchemy:**
  1. **Trade** - Registro de cada operación
     - Campos: symbol, side, entry_price, exit_price, pnl, opened_at, closed_at
     - Features: ema, macd, rsi, volume, etc
  2. **BacktestRun** - Resultados de backtesting
     - Campos: symbol, strategy, metrics, start_date, end_date
- **Configuración:**
  - SQLite local (default): `data/trading_phantom.db`
  - Postgres (producción): `DATABASE_URL` env var
- **Métodos:** session(), create_tables(), get_all_trades(), etc

### `analytics/collector.py` (150+ líneas)
- **Tipo:** Collector automático
- **Función:** Ingesta automática de trades y backtests
- **Responsabilidades:**
  1. Valida payload JSON
  2. Normaliza datos
  3. Persiste en DB
  4. Maneja errores
- **Funciones principales:**
  - `ingest_trade()` - Recibe trade JSON, valida, guarda
  - `ingest_backtest()` - Recibe resultado backtest, guarda

### `analytics/ml_pipeline.py` (400+ líneas)
- **Tipo:** Pipeline de ML
- **Función:** Entrena y predice con RandomForest
- **Componentes:**
  1. **StrategyModel** class
     - Método `train()` - Entrena RF con datos del DB
     - Método `predict()` - Predice con features nuevas
     - Feature engineering: 7 features derivados
  2. **Feature scaling** - Normaliza inputs
  3. **Model evaluation** - Calcula metrics (accuracy, precision, recall, F1)
- **Modelos:** RandomForestClassifier con 100 árboles
- **Features:** close, sma, macd, rsi, prev_close, volume, volatility

### `analytics/knowledge_base.py` (450+ líneas) ⭐ NUEVO
- **Tipo:** Sistema de Knowledge modular
- **Función:** Captura y expone 8 tipos de aprendizaje del RandomForest
- **8 Tipos de Conocimiento:**
  1. **Feature Importance** - Ranking de qué features importan más
  2. **Feature Embeddings** - Estadísticas (media, std, min, max) de cada feature
  3. **Correlation Matrix** - Relaciones entre features
  4. **Decision Patterns** - Reglas extraídas de árboles de decisión
  5. **Performance Metrics** - Accuracy, precision, recall, F1-score
  6. **Training Data Stats** - Distribución del dataset de entrenamiento
  7. **Trade Patterns** - Análisis de trades ganadores vs perdedores
  8. **Model Serialization** - Modelo RandomForest guardado en pickle
- **Almacenamiento:** src/trading_phantom/data/knowledge_base/ (JSON + pickle)
- **Métodos principales:**
  - `export_from_rf()` - Extrae conocimiento de RF entrenado
  - `load_from_disk()` - Carga conocimiento guardado
  - `get_top_features()` - Retorna top N features importantes

### `analytics/transfer_learning.py` (300+ líneas) ⭐ NUEVO
- **Tipo:** Orquestador de transferencia de aprendizaje
- **Función:** Permite que futuras IAs consuman Knowledge Base
- **Responsabilidades:**
  1. **Export:** `export_rf_knowledge()` - Guarda todo el conocimiento
  2. **Import:** `import_knowledge()` - Carga conocimiento para futuras IAs
  3. **Guide:** `create_knowledge_transfer_guide()` - Genera markdown explicativo
- **Métodos útiles:**
  - `quick_export_knowledge()` - Exporta rápido
  - `quick_import_knowledge()` - Importa rápido
  - `get_top_features(n=5)` - Top features para inicializar LSTM

### `analytics/metrics.py` (200+ líneas)
- **Tipo:** Calculador de métricas
- **Función:** Calcula métricas profesionales de backtesting
- **Métricas calculadas:**
  - **Sharpe Ratio** - Return/Risk (>1 es bueno)
  - **Sortino Ratio** - Como Sharpe pero solo downside
  - **Calmar Ratio** - Return / Max Drawdown
  - **Max Drawdown** - Peor pérdida acumulada
  - **Win Rate** - % trades ganadores
  - **Profit Factor** - Total ganancias / Total pérdidas
  - **Recovery Factor** - Net profit / Max Drawdown
  - **Avg Trade Duration** - Tiempo promedio en trade

---

## 🌐 src/trading_phantom/api/ (REST Endpoints)

### `api/__init__.py`
- **Tipo:** Inicializador de blueprints
- **Función:** Registra todos los endpoints en Flask app
- **Blueprints registrados:**
  1. bot_bp (control del bot)
  2. backtest_bp (backtesting)
  3. analytics_bp (ML, ingestión)
  4. knowledge_bp (Knowledge Base) ⭐ NUEVO
- **Feature:** ENABLE_KNOWLEDGE toggle para activar/desactivar KB

### `api/bot.py` (150+ líneas)
- **Tipo:** Endpoints de control del bot
- **Endpoints:**
  - `POST /api/bot/start` - Inicia bot con iteraciones
  - `POST /api/bot/stop` - Detiene bot
  - `GET /api/bot/status` - Estado actual
- **Parámetros:** iterations, debug flag

### `api/backtest.py` (200+ líneas)
- **Tipo:** Endpoints de backtesting
- **Endpoints:**
  - `POST /api/backtest` - Ejecuta backtest con parámetros
  - `GET /api/backtest` - Obtiene resultados previos
- **Parámetros:** symbol, start_date, end_date, strategy

### `api/analytics.py` (250+ líneas)
- **Tipo:** Endpoints de ML y exportación
- **Endpoints:**
  - `POST /api/analytics/ml/train` - Entrena RandomForest
  - `POST /api/analytics/ml/predict` - Predicción con features
  - `GET /api/analytics/export/trades?format=json|csv|parquet`
  - `GET /api/analytics/export/backtests?format=json|csv|parquet`
  - `POST /api/analytics/ingest_trade` - Ingesta manual de trade

### `api/knowledge.py` (150+ líneas) ⭐ NUEVO
- **Tipo:** Endpoints Knowledge Base
- **Endpoints (8 total):**
  1. `GET /api/knowledge/summary` - Resumen completo del KB
  2. `GET /api/knowledge/feature-importance` - Top features
  3. `GET /api/knowledge/performance` - Métricas del modelo
  4. `GET /api/knowledge/embeddings` - Estadísticas de features
  5. `GET /api/knowledge/correlation` - Matriz de correlación
  6. `GET /api/knowledge/patterns` - Decisiones del árbol
  7. `GET /api/knowledge/guide` - Markdown transfer learning guide
  8. `GET /api/knowledge/status` - Qué archivos KB existen
- **Propósito:** Exponer conocimiento para futuras IAs

### `api/utils.py` (100+ líneas)
- **Tipo:** Utilidades API
- **Función:** Helpers para respuestas HTTP
- **Responsabilidades:**
  - Formateo de respuestas JSON
  - Error handling
  - CORS configuration
  - Logging de requests

---

## 💹 src/trading_phantom/mt5/ (MetaTrader 5)

### `mt5/connector.py` (300+ líneas)
- **Tipo:** Wrapper MetaTrader 5
- **Función:** Conecta con MT5 y ejecuta órdenes
- **Responsabilidades:**
  1. Inicialización de MT5
  2. Fetch de precios (bid/ask)
  3. Envío de órdenes (market, limit, stop)
  4. Monitoreo de posiciones
  5. Retry logic automático
  6. Error handling y logging
- **Métodos principales:**
  - `get_current_price(symbol)` - Obtiene precio actual
  - `send_order(symbol, side, volume, order_type)`
  - `close_position(ticket)`
  - `get_positions()` - Posiciones abiertas

### `mt5/symbol_debugger.py` (150+ líneas)
- **Tipo:** Herramienta de debugging
- **Función:** Ayuda a debuguear símbolos y conexión MT5
- **Responsabilidades:**
  - Listar símbolos disponibles
  - Verificar spread
  - Validar símbolos para trading
  - Mostrar especificaciones de símbolos

---

## 📊 src/trading_phantom/backtest/ (Backtesting)

### `backtest/simulation.py` (250+ líneas)
- **Tipo:** Simulador numérico
- **Función:** Simula trading histórico
- **Responsabilidades:**
  1. Itera sobre datos históricos
  2. Aplica estrategia en cada vela
  3. Ejecuta trades simulados
  4. Calcula PnL
  5. Genera equity curve
- **Output:** Equity array, trades list, metrics

### `backtest/visual_backtest.py` (200+ líneas)
- **Tipo:** Adapter para visualización
- **Función:** Adapta simulation a formato ploteableGraphing
- **Responsabilidades:**
  - Preparar datos para matplotlib/plotly
  - Annotations de entrada/salida
  - Drawdown visualization
  - Export de gráficos

### `backtest/metrics.py` (200+ líneas)
- **Tipo:** Calculador de métricas
- **Función:** Calcula todas las métricas de backtest
- **Métricas:** Sharpe, Sortino, Calmar, Max DD, Win Rate, etc

### `backtest/run_backtest.py` (150+ líneas)
- **Tipo:** Orquestador de backtest
- **Función:** Coordina ejecución de backtest completo
- **Pasos:**
  1. Load datos históricos
  2. Instanciar strategy
  3. Ejecutar simulation
  4. Calcular métricas
  5. Visualizar resultados

### `backtest/run_and_visual.py` (100+ líneas)
- **Tipo:** Integration testing
- **Función:** Corre backtest y muestra resultados
- **Uso:** Tests y demos del backtesting

---

## ⚙️ src/trading_phantom/config/

### `config/config_loader.py` (100+ líneas)
- **Tipo:** Parser de configuración
- **Función:** Carga y valida config.yaml
- **Responsabilidades:**
  1. Lee YAML
  2. Valida parámetros
  3. Retorna dict con config
  4. Maneja defaults si faltan valores

### `config/config.yaml` (100+ líneas)
- **Tipo:** Archivo de configuración
- **Contenido estructurado:**
  ```yaml
  bot:
    delay_between_iterations: 5
    max_iterations_per_run: 100
  
  flask:
    port: 5000
    debug: false
  
  ml:
    enabled: true
    confidence_threshold: 0.7
  
  mt5:
    request_timeout: 10
    retry_attempts: 3
  
  strategy:
    ema_fast: 12
    ema_slow: 26
    rsi_period: 14
  ```

---

## 🎨 src/trading_phantom/static/ (Assets Web)

### `static/style.css` (400+ líneas)
- **Tipo:** Estilos CSS
- **Función:** Estilos profesionales del dashboard
- **Características:**
  - Dark theme con gradientes
  - CSS variables para colores
  - Responsive design (media queries)
  - Animaciones suaves
  - Logbox personalizado
  - Cards y KPI styling
  - Botones con hover effects

---

## 📄 src/trading_phantom/templates/ (HTML Templates)

### `templates/index.html` (300+ líneas)
- **Tipo:** Dashboard principal
- **Función:** Interfaz web principal del bot
- **Secciones:**
  1. **Header** - Logo y título
  2. **KPI Grid** - 4 cards (Bot Status, Logs, Backtest, General Logs)
  3. **Status Indicator** - Dot coloreado (rojo/verde)
  4. **Bot Control** - Botones Start/Stop/Shutdown
  5. **Logbox** - Logs en tiempo real
  6. **Navigation** - Link a /info/ml
- **Assets:** Usa style.css, JavaScript para interactividad

### `templates/ml_info.html` (250+ líneas)
- **Tipo:** Panel de información ML
- **Función:** Documentación y estado del sistema ML
- **Secciones:**
  1. **Overview** - Qué es el ML
  2. **Architecture** - Diagrama de componentes
  3. **Data Collection** - Cómo recolectar datos
  4. **Training** - Cómo entrenar
  5. **Live Prediction** - Cómo activar ML en vivo
  6. **Knowledge Base** - Explicación de KB
  7. **Top Features** - Features importantes (dinámico)
  8. **Metrics** - Métricas del modelo (dinámico)
  9. **Checklist** - Steps para activar ML

---

## 🛠️ src/trading_phantom/utils/

### `utils/trade_logger.py` (150+ líneas)
- **Tipo:** Logger personalizado
- **Función:** Logging con colores y formato profesional
- **Responsabilidades:**
  1. Setup de logging
  2. Colores por nivel (DEBUG, INFO, WARNING, ERROR)
  3. Timestamps personalizados
  4. Salida a console y archivo (logs/)

---

## 📁 src/trading_phantom/data/ (Base de datos)

### `data/trading_phantom.db`
- **Tipo:** Base de datos SQLite
- **Función:** Almacena trades y backtests
- **Tablas:**
  - **trades** - Historial de operaciones
  - **backtest_runs** - Resultados de backtests
- **Creación:** Automática en primer run

---

## 📁 data/knowledge_base/ (Knowledge Base) ⭐ NUEVO

### `data/knowledge_base/feature_importance.json`
- Contiene top 5 features con scores de importancia

### `data/knowledge_base/feature_embeddings.json`
- Estadísticas (mean, std, min, max) de cada feature

### `data/knowledge_base/correlation_matrix.json`
- Matriz de correlación entre features

### `data/knowledge_base/decision_patterns.json`
- Reglas extraídas de árboles de decisión

### `data/knowledge_base/performance_metrics.json`
- Accuracy, precision, recall, F1-score del modelo

### `data/knowledge_base/training_data/feature_stats.json`
- Distribución del dataset de entrenamiento

### `data/knowledge_base/trade_patterns/winners_losers.json`
- Análisis de trades ganadores vs perdedores

### `data/knowledge_base/models/random_forest.pkl`
- Modelo RandomForest serializado

### `data/knowledge_base/models/scaler.pkl`
- Scaler para normalización de features

### `data/knowledge_base/KNOWLEDGE_TRANSFER_GUIDE.md`
- Guía markdown para futuras IAs sobre cómo usar el KB

---

## 🧪 tests/ (Tests Unitarios)

### `tests/conftest.py`
- **Tipo:** Configuración pytest
- **Función:** Setup de tests
- **Contiene:** Fixtures, sys.path setup, mocks

### `tests/test_mt5_connector.py`
- **Tipo:** Tests unitarios
- **Función:** Valida conectividad y métodos de MT5Connector

### `tests/test_strategy.py`
- **Tipo:** Tests unitarios
- **Función:** Valida generación de señales (BUY/SELL/HOLD)

### `tests/test_bot_endpoints.py`
- **Tipo:** Tests integración
- **Función:** Prueba endpoints REST (/api/bot/*, etc)

### `tests/test_visual_adapter.py`
- **Tipo:** Tests de backtesting
- **Función:** Valida visualización y métricas de backtest

---

## 🛠️ scripts/ (Scripts de Desarrollo)

### `scripts/launcher.py` (100+ líneas)
- **Tipo:** Launcher de aplicación
- **Función:** Inicia Flask + pywebview (interfaz nativa)
- **Responsabilidades:**
  - Inicializa Flask
  - Abre ventana pywebview
  - Maneja ciclo de vida de aplicación

### `scripts/ml_train.py` (150+ líneas) ⭐ MEJORADO
- **Tipo:** Script de entrenamiento
- **Función:** Entrena RandomForest y genera Knowledge Base
- **Pasos:**
  1. Carga datos del DB (≥30 trades)
  2. Feature engineering
  3. Entrena RandomForest
  4. **🆕 Exporta Knowledge Base automáticamente**
  5. Muestra métricas y top features
  6. Genera guía para futuras IAs

### `scripts/build_exe.ps1`
- **Tipo:** Build script PowerShell
- **Función:** Crea ejecutable .exe con PyInstaller
- **Opciones:** console o sin consola

### `scripts/build_installer.ps1`
- **Tipo:** Build script PowerShell
- **Función:** Crea instalador Windows con Inno Setup

### `scripts/run_exe_console.ps1`
- **Tipo:** Debug script
- **Función:** Ejecuta .exe y captura logs (stdout/stderr)

### `scripts/setup_env.ps1`
- **Tipo:** Setup script
- **Función:** Setup inicial (Python check, venv creation)

### `scripts/run_pytest.py`
- **Tipo:** Test runner
- **Función:** Ejecuta pytest con configuración

### `scripts/call_bot.py`
- **Tipo:** Helper script
- **Función:** Llamadas HTTP a API desde CLI

---

## 📦 installer/ (Instalador Windows)

### `installer/TradingPhantom.iss`
- **Tipo:** Script Inno Setup
- **Función:** Define cómo crear instalador Windows
- **Contiene:**
  - Archivos a incluir (EXE, DLLs)
  - Directorios de instalación
  - Shortcuts
  - Opciones de instalación
  - Instrucciones post-install

---

## 🐳 docker/ (Docker)

### `docker/Dockerfile`
- **Tipo:** Imagen Docker
- **Función:** Define cómo construir imagen del bot
- **Contiene:**
  - Base: Python 3.10
  - Instalación de dependencias
  - Setup de app
  - Healthcheck

---

## 📋 logs/ (Logs de Ejecución)

### `logs/bot.log`
- Logs del bot de trading

### `logs/backtest.log`
- Logs de backtesting

### `logs/general.log`
- Logs generales de la aplicación

---

## 📚 docs/ (Documentación Profesional)

### `docs/README.md`
- Guía extendida completa

### `docs/ARCHITECTURE.md`
- Diseño técnico y patrones

### `docs/API.md`
- Especificación completa de endpoints

### `docs/QUICKSTART.md`
- Instalación rápida (5 minutos)

---

## 📊 Archivos Especiales

### `TradingPhantom.spec`
- **Tipo:** Especificación PyInstaller
- **Función:** Define cómo empaquetar código a .exe

### `pytest.ini`
- **Tipo:** Configuración pytest
- **Función:** Define opciones de testing

### `Trading_Phantom_Documentation.pdf` ⭐ NUEVO
- **Tipo:** PDF profesional
- **Función:** Documentación completa en un archivo PDF
- **Generado por:** generate_pdf.py

### `generate_pdf.py` ⭐ NUEVO
- **Tipo:** Script generador
- **Función:** Crea PDF profesional con reportlab

---

## 📊 Resumen Estadístico

| Categoría | Cantidad | Descripción |
|-----------|----------|-------------|
| **Archivos Python principales** | 25+ | Código funcional |
| **Archivos de configuración** | 8 | Setup y parámetros |
| **Scripts de ejecución** | 12 | Instalación, build, test |
| **Tests unitarios** | 5 | Validación de componentes |
| **Documentación** | 7+ | README, API, ARCHITECTURE, PDF |
| **Templates HTML** | 2 | Dashboard, ML Info |
| **Archivos CSS** | 1 | Estilos (400+ líneas) |
| **Total líneas de código** | 5000+ | Python + configs |
| **Endpoints REST** | 20+ | API completa |
| **Conocimiento almacenado** | 8 tipos | Knowledge Base |

---

**Última actualización:** Enero 2026  
**Versión:** 1.1.0  
**Total de descripción:** 18,000+ palabras
