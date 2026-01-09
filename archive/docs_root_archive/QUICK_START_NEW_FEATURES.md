# 🚀 INICIO RÁPIDO - NUEVAS FUNCIONES

## ¿Qué se cambió?

✅ **Estrategia mejorada** (EMA + MACD + RSI)
✅ **Historial automático** de operaciones
✅ **Resumen de P/L** cada 30 minutos

---

## 🎯 COMIENZA AQUÍ

### Opción 1: Lo más fácil 👇

```
1. Doble-click en: RUN.bat
2. Espera a que conecte con MT5
3. ¡Listo! El bot está operando
```

### Opción 2: PowerShell

```powershell
.\RUN.ps1
```

---

## 📊 QUÉ VAS A VER

### En la terminal cada tick:

```
🕒 Tick: 2026-01-07 15:30:45
💱 EURUSD-T | BID: 1.16523 | ASK: 1.16525
⏸️ HOLD: EMA12=1.16523 | EMA26=1.16410 | MACD=0.00113 | RSI=52.34
```

Cuando genera una señal:

```
🟢 BUY: MACD crossover ✓ | EMA12 > EMA26 ✓ | RSI=52.34 ✓ | Close=1.16500
✅ Orden ejecutada correctamente | Ticket: 12345
📝 Trade abierto: BUY | Ticket: 12345 | Precio: 1.16525
```

### Cada 30 minutos - Resumen:

```
============================================================
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

---

## 📈 LA NUEVA ESTRATEGIA

### Indicadores:
- **EMA 12 y 26**: Detecta tendencias
- **MACD**: Detecta cambios de momentum
- **RSI**: Confirma overbought/oversold

### Señales:

🟢 **BUY (Compra)** cuando:
- MACD sube su línea de señal ✓
- EMA rápida > EMA lenta ✓
- RSI > 45 ✓

🔴 **SELL (Venta)** cuando:
- MACD baja su línea de señal ✓
- EMA rápida < EMA lenta ✓
- RSI < 55 ✓

---

## 💾 HISTORIAL AUTOMÁTICO

Los datos se guardan en:
```
logs/trade_history.json
```

Estructura de cada operación:
```json
{
  "ticket": 12345,
  "signal": "BUY",
  "symbol": "EURUSD",
  "entry_price": 1.16500,
  "entry_time": "2026-01-07T15:30:45",
  "exit_price": 1.16700,
  "exit_time": "2026-01-07T16:45:30",
  "profit_loss": 200.00,
  "status": "CLOSED"
}
```

---

## ⚙️ CONFIGURACIÓN

Archivo: `config/config.yaml`

```yaml
symbol: EURUSD
timeframe: H1
max_positions: 3

risk:
  risk_per_trade: 0.01    # 1% por operación
  max_daily_loss: 0.03    # 3% máximo diario

orders:
  sl_pips: 20             # Stop loss
  tp_pips: 40             # Take profit
```

---

## 🧪 PRUEBA EL HISTORIAL

```bash
# Ejecuta el ejemplo
python scripts/example_trade_history.py
```

Verás:
- ✅ Cómo se registran operaciones
- ✅ Cómo se cierran
- ✅ Cómo se calculan estadísticas
- ✅ JSON guardado

---

## 📋 CHECKLIST

- [ ] Bot conectado a MT5 en modo Demo
- [ ] Terminal mostrando logs
- [ ] Carpeta `logs/` existe
- [ ] Archivo `trade_history.json` se crea automáticamente
- [ ] Cada 30 min ves el resumen

---

## ❓ PREGUNTAS COMUNES

**P: ¿Por qué no hay operaciones?**
R: La estrategia espera confirmación en 3 indicadores. Paciencia, es mejor que muchas falsas señales.

**P: ¿Dónde veo las ganancias?**
R: En los resúmenes cada 30 min o al cerrar el bot con `CTRL + C`.

**P: ¿Puedo cambiar los parámetros?**
R: Sí, edita `config/config.yaml` y reinicia el bot.

**P: ¿Dónde están los datos históricos?**
R: En `logs/trade_history.json` - es un JSON normal, puedes abrirlo en cualquier editor.

---

## 🔗 ARCHIVOS IMPORTANTES

```
├── config/config.yaml              ← Configuración
├── modules/strategy.py             ← Nueva estrategia
├── modules/trade_history.py        ← Nuevo: Historial
├── core/orchestrator.py            ← Integración
├── logs/trade_history.json         ← Datos (se crea auto)
├── CAMBIOS_REALIZADOS.md           ← Resumen detallado
└── UPDATES_STRATEGY_AND_HISTORY.md ← Documentación técnica
```

---

## 💡 TIPS

1. **Monitorea en tiempo real**: Mantén la terminal abierta
2. **Revisa cada 30 min**: Los resúmenes son informativos
3. **Cierra ordenadamente**: Presiona `CTRL + C` para ver resumen final
4. **Guarda datos**: El JSON se mantiene aunque cierres
5. **Ajusta si es necesario**: Usa `config.yaml` para cambiar parámetros

---

## ✅ LISTO

Ahora ejecuta:
```
.\RUN.bat
```

Y observa el bot operando con la nueva estrategia IA 🚀

---

**Última actualización:** 7 Enero 2026
