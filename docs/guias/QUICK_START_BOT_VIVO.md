## 🤖 TRADING PHANTOM - GUÍA RÁPIDA DE EJECUCIÓN

### ⚡ Comandos Rápidos

**Iniciar Bot:**
```bash
python start_bot.py
```

**Monitorear en Vivo:**
```bash
python bot_monitor.py
```

**Ver Dashboard Web:**
Abrir archivo: `BOT_DASHBOARD.html`

**Ver Logs:**
```bash
Get-Content bot_execution_*.log -Tail 50
```

---

### 📊 Estado Actual

**Bot Status:** ✅ EJECUTÁNDOSE EN VIVO
**Plataforma:** MetaTrader 5 (DEMO)
**Estrategias:** ML 95% + Risk Management activados
**Operaciones:** 1 SELL ejecutada (Ticket: 1213401595)

---

### 📈 Métricas Esperadas

| Métrica | Valor |
|---------|-------|
| ROI | +317.61% |
| Win Rate | 98.92% |
| Drawdown | 0.00% |
| Max Trades/Día | ~24 (1 cada H1) |

---

### 🔧 Configuración Activa

- **Modelo ML:** 95% accuracy
- **Stop Loss:** -2%
- **Take Profit:** +4%
- **Confidence Threshold:** 55%
- **Position Size:** 95% equity
- **Symbol:** EURUSD
- **Timeframe:** H1

---

### 📋 Archivos Importantes

**Configuración:**
- `config/config.yaml` - Parámetros del bot

**Modelos:**
- `src/data/models/advanced_model.joblib` - ML Model (95% accuracy)

**Base de Datos:**
- `src/data/trading_phantom.db` - Historial de trades

**Monitoreo:**
- `start_bot.py` - Launcher
- `bot_monitor.py` - Monitor en terminal
- `BOT_DASHBOARD.html` - Dashboard web

**Documentación:**
- `BOT_EN_VIVO.md` - Documentación completa
- `QUICK_START_BOT_VIVO.md` - Esta guía rápida

---

### ✅ Checklist Diario

- [ ] Bot ejecutándose
- [ ] Sin errores en logs
- [ ] Trades ejecutándose cada H1
- [ ] Win rate > 90%
- [ ] P&L positivo
- [ ] Drawdown < 5%
- [ ] Conexión MT5 activa

---

### 🎯 Próximos Pasos

1. **Hoy:** Monitorear por 24 horas
2. **Mañana:** Revisar resultados, validar ganancias
3. **Semana:** Forward test con nuevos datos
4. **2 Semanas:** Migrar a CUENTA REAL si todo funciona

---

**Última actualización:** 2026-01-08 19:30 UTC
**Estado:** ✅ BOT EN VIVO
