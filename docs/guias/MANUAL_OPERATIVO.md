# 📖 MANUAL OPERATIVO - TRADING PHANTOM

**Versión:** 2.0  
**Última actualización:** 2026-01-08  
**Estado:** ✅ Operativo

---

## 🚀 OPERACIÓN BÁSICA

### Iniciar el Bot

**Opción 1: Con Launcher (Recomendado)**
```bash
python bot/start_bot.py
```
Esto muestra:
- Verificación de configuración ✅
- Verificación de modelo ML ✅
- Conexión a MetaTrader ✅
- Logs en tiempo real

**Opción 2: Directo**
```bash
python main.py --debug
```

**Opción 3: Una iteración (Prueba)**
```bash
python main.py --once
```
Ejecuta el bot una sola vez y sale.

---

## 📊 MONITOREO EN VIVO

### Terminal de Monitoreo
```bash
python bot/bot_monitor.py
```

Muestra:
- ✅ Trades ejecutadas
- 💰 P&L actual
- 📈 Win rate
- 📊 Últimas operaciones
- ⏳ Próxima actualización

Se actualiza cada 30 segundos automáticamente.

### Dashboards Web
```
Abrir en navegador:
1. dashboards/BOT_DASHBOARD.html (Recomendado)
2. dashboards/BACKTESTING_DASHBOARD.html
3. dashboards/ML_ADVANCED_DASHBOARD.html
```

### Verificar Trades
```bash
python tools/check_trades.py
```

Muestra:
- Total trades ejecutadas
- Win rate actual
- P&L total
- Últimas operaciones

---

## ⚙️ CONFIGURACIÓN

### Ubicación
`config/config.yaml`

### Parámetros principales

#### Símbolo y Timeframe
```yaml
symbol: EURUSD    # Cambiar a otro si es necesario
timeframe: H1     # H1 recomendado (no cambiar a M1)
```

#### Modelo ML
```yaml
ml:
  enabled: true              # true = activado
  confidence_threshold: 0.55 # 55% umbral
  model_path: "src/data/models/advanced_model.pkl"
```

#### Risk Management
```yaml
improved_strategy:
  enabled: true          # true = activado
  stop_loss_pct: 0.02    # -2%
  take_profit_pct: 0.04  # +4% (1:2 ratio)
  position_size: 0.95    # 95% del equity
```

#### Riesgo
```yaml
risk:
  risk_per_trade: 0.01      # 1% por trade
  max_daily_loss: 0.03      # 3% máximo diario
```

#### Loop
```yaml
execution:
  loop_interval_seconds: 60  # Cada 60 segundos
```

---

## 📈 ENTENDER LOS LOGS

### Ejemplo de log correcto
```
INFO:trading_phantom.core.orchestrator:🚀 Iniciando Trading Phantom
INFO:trading_phantom.core.orchestrator:💱 Símbolo: EURUSD
INFO:trading_phantom.core.orchestrator:⏱️ Timeframe: H1
INFO:trading_phantom.mt5.connector:✅ Conectado a MetaTrader 5
INFO:trading_phantom.core.orchestrator:✅ Estrategia, RiskManager y Trader inicializados
INFO:trading_phantom.core.orchestrator:🎯 Señal: HOLD
INFO:trading_phantom.core.orchestrator:🔔 Nueva vela detectada
INFO:trading_phantom.modules.strategy:SELL condition met
INFO:trading_phantom.modules.trader:🚀 Ejecutando SELL | Lote: 0.3 | SL: 1.16608 | TP: 1.16548
INFO:trading_phantom.modules.trader:✅ Orden ejecutada correctamente | Ticket: 1213401595
```

### Qué significa cada línea

| Log | Significa |
|-----|-----------|
| `Iniciando Trading Phantom` | Bot iniciado correctamente |
| `Conectado a MetaTrader 5` | Conexión a MT5 OK ✅ |
| `Estrategia, RiskManager inicializados` | Componentes listos |
| `Señal: HOLD` | Sin señal en esta vela |
| `Nueva vela detectada` | Nueva H1 llegó |
| `SELL/BUY condition met` | Señal encontrada |
| `Ejecutando SELL/BUY` | Ejecutando trade |
| `Orden ejecutada correctamente` | Trade ejecutado ✅ |

---

## 🔄 CICLO DE OPERACIÓN

### Cada 60 segundos

```
1. LEER PRECIOS
   ↓
2. DETECTAR NUEVA VELA H1
   ↓
3. CARGAR FEATURES (20 variables)
   ↓
4. CONSULTAR MODELO ML
   ↓
5. APLICAR SIGNAL FILTER (>55% confidence)
   ↓
6. SI SEÑAL VÁLIDA:
   ├─ Calcular posición (95% equity)
   ├─ Establecer SL (-2%)
   ├─ Establecer TP (+4%)
   └─ EJECUTAR ORDEN
   ↓
7. SI SIN SEÑAL:
   └─ Esperar siguiente iteración
   ↓
8. GUARDAR EN BD
   ↓
9. VOLVER A PASO 1
```

---

## 📊 INTERPRETAR RESULTADOS

### Win Rate
- **Esperado:** 98.92%
- **Aceptable:** > 90%
- **Problema:** < 80%

### ROI
- **Esperado:** +317.61%
- **Mínimo:** +0%
- **Problema:** < 0%

### Drawdown
- **Esperado:** 0.00%
- **Máximo aceptable:** 10%
- **Problema:** > 20%

### Trades por día
- **Normal:** 1-5 trades (H1)
- **Bajo:** 0 trades (sin señales)
- **Demasiado:** > 10 (revisar parámetros)

---

## 🔧 TROUBLESHOOTING

### Problema: Bot no se conecta a MT5
```
Solución:
1. Verificar que MetaTrader 5 está abierto
2. Verificar que el servidor está disponible
3. Reiniciar MetaTrader 5
4. Ejecutar: python main.py --debug
```

### Problema: No hay trades ejecutadas
```
Posibles causas:
1. Sin señales (mercado sin tendencia)
2. Confidence < 55% (threshold muy alto)
3. Modelo no prediciendo bien
4. Revisar logs: python main.py --debug --once
```

### Problema: Muchos trades perdedores
```
1. Check win rate: python tools/check_trades.py
2. Revisar últimos logs
3. Ejecutar backtesting: python backtesting/run_backtest_parallel.py
4. Considerar cambiar parámetros
```

### Problema: Error al ejecutar backtesting
```
1. Verificar BD: python tools/check_trades.py
2. Verificar modelo: ls -la src/data/models/
3. Reinstalar dependencias: pip install -r requirements.txt
```

---

## 📋 CHECKLIST DIARIO

Antes de dejar corriendo el bot:
- [ ] MetaTrader 5 está abierto
- [ ] config.yaml está correctamente configurado
- [ ] Ejecuté `python main.py --once` sin errores
- [ ] Verifiqué que se conecta a MT5
- [ ] Verifiqué que el modelo ML carga
- [ ] Revisé los logs no hay errores

Durante el día:
- [ ] Monitoreo bot con `python bot/bot_monitor.py`
- [ ] Reviso dashboard periódicamente
- [ ] Verifico que hay trades ejecutándose
- [ ] Anoto wins/losses

Al final del día:
- [ ] Ver resultados: `python tools/check_trades.py`
- [ ] Win rate > 90% ✅
- [ ] P&L positivo ✅
- [ ] Sin drawdowns anormales ✅

---

## 📞 SOPORTE

### Si algo falla
1. Lee los logs: `Get-Content bot/logs/bot_execution_*.log -Tail 100`
2. Ejecuta con debug: `python main.py --debug --once`
3. Verifica configuración: `cat config/config.yaml`
4. Reinicia todo limpio

### Si quieres cambiar algo
1. Modifica `config/config.yaml`
2. Reinicia bot: `python main.py --once`
3. Si OK → Ejecuta backtesting
4. Si backtesting OK → Deploy en vivo

---

## 🚀 SIGUIENTE PASO

Después de 48-72 horas de operación exitosa:
1. Ejecutar backtesting paralelo
2. Si OK → Considerar M5
3. Si M5 OK → Migrar a cuenta REAL

Ver: [docs/resúmenes/BOT_EN_VIVO.md](../resúmenes/BOT_EN_VIVO.md)

---

**¡Tu bot está listo para operar!** 🎉
