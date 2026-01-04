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

```
```
