# 🏗️ Arquitectura Modular - Trading Phantom v1.1.0

## ✅ Estado: Completamente Modularizado

Tu proyecto **SÍ está modularizado** y puedes modificar componentes sin romper dependencias si sigues las reglas de las capas.

---

## 📊 Estructura de Capas (Clean Architecture)

```
┌─────────────────────────────────────────┐
│         WEBAPP (Flask UI)               │  ← Panel visual, rutas HTTP
├─────────────────────────────────────────┤
│   API Layer (Blueprints en src/api/)    │  ← Endpoints desacoplados
├─────────────────────────────────────────┤
│    CORE: Orchestrator (controlador)     │  ← Dirige flujos principales
├─────────────────────────────────────────┤
│  MODULES: Strategy, Trader, RiskMgr     │  ← Lógica de negocio
├─────────────────────────────────────────┤
│  MT5 Connector (abstracción plataforma) │  ← Integración externa
├─────────────────────────────────────────┤
│   ANALYTICS: DB + ML Pipeline           │  ← Persistencia y modelos
├─────────────────────────────────────────┤
│ CONFIG (YAML) + UTILS (helpers)         │  ← Configuración global
└─────────────────────────────────────────┘
```

### Flecha de dependencias (siempre hacia abajo):
- `webapp` → `api` → `orchestrator` → `modules` → `mt5` + `analytics` + `config`
- **Nunca al revés**: un módulo no debe importar de webapp o orchestrator.

---

## 🗄️ Base de Datos: 2 Tablas Principales

### **Tabla 1: `trades`**
```sql
CREATE TABLE trades (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp         DATETIME DEFAULT CURRENT_TIMESTAMP,
    ticket            INTEGER,              -- ID de orden MT5 (nullable)
    symbol            VARCHAR(50),          -- EURUSD-T
    side              VARCHAR(10),          -- BUY o SELL
    price             FLOAT,                -- Precio de entrada
    volume            FLOAT,                -- Tamaño
    sl                FLOAT,                -- Stop loss (nullable)
    tp                FLOAT,                -- Take profit (nullable)
    exit_price        FLOAT,                -- Precio de cierre (nullable)
    exit_time         DATETIME,             -- Hora de cierre (nullable)
    pnl               FLOAT,                -- Ganancia/pérdida (nullable)
    meta              JSON                  -- Datos adicionales (indicadores, etc)
);
```

**Índices:** `ticket` (búsqueda rápida de órdenes activas)  
**Uso:** Almacena cada trade ejecutado. La columna `meta` permite guardar EMA, MACD, RSI, ML score, etc.

---

### **Tabla 2: `backtest_runs`**
```sql
CREATE TABLE backtest_runs (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at        DATETIME DEFAULT CURRENT_TIMESTAMP,
    symbol            VARCHAR(50),          -- EURUSD-T
    bars              INTEGER,              -- Número de velas
    sma_period        INTEGER,              -- SMA lookback
    rsi_period        INTEGER,              -- RSI lookback
    metrics           JSON,                 -- Sharpe, DD, etc
    details           JSON                  -- Resultados brutos
);
```

**Uso:** Historial de backtests ejecutados. Permite auditar y reproducir runs.

---

## ✨ Modularización por Componentes

### **1. MODULES (Lógica de Trading)**

```
src/trading_phantom/modules/
├── __init__.py
├── strategy.py          ← Señales técnicas (EMA+MACD+RSI)
├── trader.py            ← Ejecución de órdenes
├── risk_manager.py      ← SL/TP, lotaje
├── data_loader.py       ← Normalización MT5 → pandas
└── trade_history.py     ← Persistencia trades (DB+JSON)
```

**Desacoplamiento:**
- `strategy.py` NO importa `trader.py`. Solo retorna señal `{"action": "BUY", "price": X}`.
- `trader.py` consume esa señal y ejecuta.
- `risk_manager.py` es agnóstico: calcula SL/TP para cualquier signal.

**Puedo modificar sin romper:**
✅ Cambiar EMA(12,26) a otras bandas en `strategy.py`  
✅ Alternar entre MT5 y otra plataforma sin afectar `trader.py` (cambio en `mt5/connector.py`)  
✅ Ajustar ratios de riesgo en `risk_manager.py`

---

### **2. MT5 (Abstracción Plataforma)**

```
src/trading_phantom/mt5/
├── __init__.py
├── connector.py         ← Wrapper con retry + error handling
└── symbol_debugger.py   ← Debug de símbolos
```

**Patrón:** `connector.py` encapsula toda la lógica MT5. Si cambias a otra plataforma:
- Solo reemplazas `mt5/connector.py` → tu `Trader` sigue igual.
- `modules/trader.py` llama a `mt5_connector.execute()`, no directamente a MT5.

---

### **3. ANALYTICS (Datos + ML)**

```
src/trading_phantom/analytics/
├── __init__.py
├── db.py                ← Schemas SQLAlchemy (trades, backtest_runs)
├── collector.py         ← Ingesta de trades a BD
├── ml_pipeline.py       ← RandomForest + escalado
```

**Aislamiento:**
- Cambiar de SQLite a PostgreSQL: solo actualiza `db.py` (conexión + schemas).
- Cambiar RandomForest a XGBoost: solo `ml_pipeline.py`.
- `orchestrator.py` no conoce los detalles; solo llama `collector.ingest_trade()`.

---

### **4. CORE (Orquestación)**

```
src/trading_phantom/core/
├── __init__.py
└── orchestrator.py      ← Loop principal, coordina módulos
```

**Responsabilidad única:** Conecta Strategy → Risk Manager → Trader → History.  
**Fácil de entender:** Lee el código, ves el flujo de datos linealmente.

---

### **5. CONFIG (Inyección de dependencias)**

```
config/
├── __init__.py
├── config_loader.py     ← Lee YAML
└── config.yaml          ← Parámetros centralizados
```

**Ventaja:** Sin hardcoding. Cambias un parámetro en YAML → toda la app se adapta.

---

### **6. BACKTEST (Aislado)**

```
src/trading_phantom/backtest/
├── __init__.py
├── simulation.py        ← Tu engine numérico
├── visual_backtest.py   ← Adapter para backtesting lib
├── metrics.py           ← Sharpe, DrawDown, etc
└── run_and_visual.py    ← Orquestación de backtest
```

**Independiente:** El backtest no toca MT5 ni la BD en vivo. Usa datos históricos.

---

### **7. WEBAPP (Presentación)**

```
src/trading_phantom/
├── webapp.py            ← Flask app + rutas
├── templates/
│   ├── index.html       ← Panel principal
│   └── ml_info.html     ← Documentación ML
└── static/
    └── style.css        ← Estilos
```

**Desacoplada:**
- No contiene lógica de trading.
- Solo llamadas HTTP a la API.
- Cambiar Flask a FastAPI: sin afectar `modules/` o `core/`.

---

### **8. API (Blueprints modulares)**

```
src/trading_phantom/api/
├── __init__.py          ← Registro de blueprints (toggleable)
├── backtest.py
├── bot.py
├── logs.py
└── analytics.py
```

**Patrón:**
```python
# Cada blueprint es independiente
@ENABLE_BACKTEST:
    app.register_blueprint(bp_backtest)
@ENABLE_BOT:
    app.register_blueprint(bp_bot)
```

Puedo deshabilitar un endpoint entero via env var sin tocar código.

---

## 🔄 Flujo de Datos (Sin Acoplamiento)

```
┌────────────┐
│ Config.yaml│ ← Todos leen de aquí
└────┬───────┘
     │
     ▼
┌─────────────────────┐
│ Orchestrator        │ (Lee config, orquesta)
│ ├─ Strategy.get()   │
│ ├─ RiskMgr.calc()   │
│ ├─ Trader.execute() │
│ └─ History.record() │
└──────┬──────────────┘
       │
       ├──────────────────┬──────────────┐
       ▼                  ▼              ▼
┌─────────────┐    ┌─────────────┐   ┌────────────┐
│ MT5         │    │ Analytics   │   │ File logs  │
│ Connector   │    │ DB + ML     │   │ (JSON)     │
└─────────────┘    └─────────────┘   └────────────┘
```

---

## 📋 Resumen: ¿Qué puedo modificar sin romper?

| Cambio | ¿Riesgo? | Cómo hacerlo |
|--------|----------|------------|
| **Estrategia** (EMA → Bollinger) | ✅ CERO | Modifica `strategy.py` solo |
| **Indicadores** (RSI → STOCH) | ✅ CERO | `strategy.py` + `config.yaml` |
| **Ratios de riesgo** | ✅ CERO | `config.yaml` → `risk_manager.py` |
| **Plataforma** (MT5 → IB) | ✅ CERO | Reemplaza `mt5/connector.py` |
| **BD** (SQLite → Postgres) | ✅ BAJO | Solo `analytics/db.py` |
| **ML** (RandomForest → XGBoost) | ✅ BAJO | `analytics/ml_pipeline.py` |
| **Framework web** (Flask → FastAPI) | ✅ BAJO | Reemplaza `webapp.py` |
| **Agregar nueva métrica** | ✅ CERO | Nuevo archivo en `analytics/` |
| **Panel visual** (CSS, layout) | ✅ CERO | `templates/` + `static/` |

---

## 🛡️ Buenas Prácticas Aplicadas

✅ **Single Responsibility:** Cada módulo hace una cosa bien.  
✅ **Dependency Injection:** Config inyectada, no hardcoded.  
✅ **Interface Contracts:** Cada módulo expone métodos claros (Strategy.get_signal(), etc).  
✅ **Abstracción de plataforma:** MT5 encapsulado.  
✅ **Persistencia agnóstica:** DB swappable.  
✅ **API toggleable:** Puedes activar/desactivar endpoints.  
✅ **Logging centralizado:** Toda la app usa mismo logger.  
✅ **Configuración centralizada:** YAML es la fuente de verdad.

---

## 🚨 Reglas de Oro (Evita Romper)

❌ **NO hagas:**
- Importar `webapp` desde `modules/`
- Hardcodear valores en código (siempre `config.yaml`)
- Que `strategy.py` abra conexiones a BD
- Que `trader.py` calcule indicadores

✅ **SÍ haz:**
- Pasar dependencias como argumentos
- Mantener cada archivo < 300 líneas
- Usar tipos (type hints) en firmas
- Documentar cambios en CHANGELOG.md

---

## 📈 Crecimiento Seguro

Puedo agregar sin riesgo:
- Nueva estrategia: archivo `strategies/macd_only.py`, registra en `orchestrator.py`
- Nuevo indicador: en `modules/indicators.py`, consume en `strategy.py`
- Nueva BD: clase en `analytics/db.py`, alterna en config
- Nuevo backtest lib: en `backtest/`
- Nuevos endpoints: nuevo blueprint en `api/`

---

## 🎯 Conclusión

Tu proyecto **está bien estructurado** y **totalmente modularizable**. Tienes 2 tablas de BD simples pero suficientes, separación clara de responsabilidades y patrones que permiten cambios sin cascadas de errores.

**Recomendación:** Mantén esta estructura. Si necesitas agregar algo, haz un archivo nuevo en la carpeta del módulo más cercano, no mezcles responsabilidades.

---

**Última actualización:** 7 enero 2026  
**Versión:** 1.1.0
