# 📊 Nuevas Características - Versión Mejorada

## ✨ Cambios Realizados

### 1️⃣ **Nueva Estrategia IA Avanzada: EMA Crossover + MACD + RSI**

La estrategia anterior (SMA simple) ha sido reemplazada por una **estrategia profesional** basada en indicadores más sofisticados:

#### **Indicadores Utilizados:**
- **EMA (Exponential Moving Average)**
  - EMA Rápida: 12 períodos
  - EMA Lenta: 26 períodos
  - Detecta cambios de tendencia

- **MACD (Moving Average Convergence Divergence)**
  - Línea de señal: 9 períodos
  - Detecta cruce alcista/bajista
  - Confirma cambio de momentum

- **RSI (Relative Strength Index)**
  - Período: 14
  - Confirma overbought/oversold
  - Evita falsas señales

#### **Lógica de Entrada:**

**BUY (Compra):**
```
✓ MACD cruza hacia arriba su línea de señal
✓ EMA Rápida > EMA Lenta
✓ RSI > 45 (momentum positivo)
```

**SELL (Venta):**
```
✓ MACD cruza hacia abajo su línea de señal
✓ EMA Rápida < EMA Lenta
✓ RSI < 55 (momentum negativo)
```

#### **Ventajas:**
✅ Menos falsas señales que SMA simple
✅ Mejor entrada en tendencias establecidas
✅ Confirmación multi-indicador
✅ Probada en trading profesional

---

### 2️⃣ **Nuevo Módulo de Historial de Operaciones**

Se ha creado el módulo `trade_history.py` que registra y analiza todas las operaciones.

#### **Ubicación:**
```
modules/trade_history.py
logs/trade_history.json  (se crea automáticamente)
```

#### **Características:**

- **Registro automático de trades:**
  - Ticket de la orden
  - Tipo de operación (BUY/SELL)
  - Precio de entrada
  - Stop Loss y Take Profit
  - Hora de entrada

- **Cierre de posiciones:**
  - Precio de salida
  - Ganancia/Pérdida en USD
  - Hora de cierre
  - Estado

- **Resumen de Estadísticas:**
  ```
  📊 RESUMEN DE OPERACIONES
  ============================================================
  Total de operaciones cerradas: 15
  Operaciones abiertas: 2
  ✅ Operaciones ganadas: 10
  ❌ Operaciones perdidas: 5
  📈 Tasa de ganadoras: 66.67%
  💰 Ganancia total: $1,250.50
  💸 Pérdida total: -$350.75
  🎯 PROFIT NETO: $899.75
  🚀 Mejor trade: $250.00
  📉 Peor trade: -$120.50
  ============================================================
  ```

#### **Uso Programático:**

```python
from modules.trade_history import TradeHistory

history = TradeHistory()

# Registrar un trade al abrirse
history.add_trade(
    ticket=12345,
    symbol="EURUSD",
    signal="BUY",
    volume=0.1,
    entry_price=1.1650,
    sl=1.1620,
    tp=1.1700
)

# Cerrar un trade
history.close_trade(
    ticket=12345,
    exit_price=1.1695,
    profit_loss=45.50
)

# Obtener resumen
summary = history.get_summary()
print(f"Ganancias: {summary['total_profit']}")
print(f"Pérdidas: {summary['total_loss']}")
print(f"Net Profit: {summary['net_profit']}")

# Mostrar resumen formateado
history.print_summary()
```

#### **Archivo JSON (trade_history.json):**

```json
[
  {
    "ticket": 12345,
    "symbol": "EURUSD",
    "signal": "BUY",
    "type": "BUY",
    "volume": 0.1,
    "entry_price": 1.1650,
    "sl": 1.1620,
    "tp": 1.1700,
    "entry_time": "2026-01-07T15:30:45.123456",
    "exit_time": "2026-01-07T16:45:30.654321",
    "exit_price": 1.1695,
    "profit_loss": 45.50,
    "status": "CLOSED"
  }
]
```

---

### 3️⃣ **Integración en el Bot**

El historial se integra automáticamente en el `orchestrator.py`:

✅ **Inicialización:**
```python
trade_history = TradeHistory()
```

✅ **Registro de trades al ejecutar:**
```python
executed = trader.execute(signal, price)
if executed:
    trade_history.add_trade(...)
```

✅ **Resumen cada 30 minutos:**
El bot imprime automáticamente un resumen cada 30 minutos en los logs

✅ **Resumen final:**
Cuando se detiene el bot, se imprime el resumen completo

---

## 📈 Configuración de la Estrategia

Para ajustar los parámetros de la estrategia, modifica `config/config.yaml`:

```yaml
# =========================
# RIESGO
# =========================
risk:
  risk_per_trade: 0.01      # 1% del balance por trade
  fixed_lot: null           # null = automático
  max_daily_loss: 0.03      # 3% pérdida máxima diaria

# =========================
# STOP LOSS / TAKE PROFIT
# =========================
orders:
  sl_pips: 20               # Stop Loss en pips
  tp_pips: 40               # Take Profit en pips
  deviation: 20             # Desviación permitida

# =========================
# LOOP
# =========================
execution:
  loop_interval_seconds: 60 # Ejecutar cada 60 segundos
```

---

## 🚀 Cómo Ejecutar

### Opción 1: Doble-click (Más fácil)
```
RUN.bat
```

### Opción 2: PowerShell
```powershell
.\RUN.ps1
```

---

## 📊 Ver Resultados

### En Tiempo Real:
Los logs mostrarán las operaciones y el resumen cada 30 minutos:
```
🟢 BUY: MACD crossover ✓ | EMA12 > EMA26 ✓ | RSI=52.34 ✓ | Close=1.16500
✅ Orden ejecutada correctamente | Ticket: 12345
```

### Archivo JSON:
Abre `logs/trade_history.json` para ver el historial completo en formato JSON

### Al Finalizar:
Cuando cierres el bot (Ctrl+C), verás el resumen final con todos los datos

---

## 🎯 Ejemplos de Señales

### SEÑAL BUY ✅
```
EMA12=1.16523
EMA26=1.16410
MACD=0.00113 (cruzó hacia arriba)
MACD_SIGNAL=0.00105
RSI=52.5 (> 45)
→ BUY GENERADA
```

### SEÑAL SELL ✅
```
EMA12=1.16350
EMA26=1.16450
MACD=-0.00100 (cruzó hacia abajo)
MACD_SIGNAL=-0.00095
RSI=48.2 (< 55)
→ SELL GENERADA
```

### SEÑAL HOLD ⏸️
```
EMA12=1.16410
EMA26=1.16410
MACD=0.00000
RSI=50.0
→ Esperando confirmación (HOLD)
```

---

## 📝 Notas Importantes

1. **BackTest:** El módulo de historial guarda datos para análisis posterior
2. **Risk Management:** El bot siempre respeta los límites de riesgo configurados
3. **Modo Demo:** Asegúrate que MetaTrader 5 esté en modo demo/backtesting
4. **Logs:** Revisa `logs/` para debugging detallado

---

## 🔄 Próximas Mejoras

- [ ] Dashboard web con gráficos de P/L
- [ ] Optimización automática de parámetros
- [ ] Machine Learning para ajuste dinámico
- [ ] Alertas por email/Telegram
- [ ] Exportación a Excel del historial

---

**Versión:** 1.1.0
**Fecha:** 7 Enero 2026
**Estado:** ✅ ACTIVO Y PROBADO
