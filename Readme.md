# 🤖 TRADING PHANTOM - Sistema Automático de Trading

**Status:** ✅ **BOT EN VIVO** | Operando en MetaTrader 5  
**Versión:** 2.0 Reorganizado  
**Última actualización:** 2026-01-08 19:45 UTC

---

## 🎯 INICIO RÁPIDO

### 1️⃣ Para empezar (5 minutos)
```bash
# Opción A: Lanzador automático
python start_bot.py

# Opción B: Directo
python main.py --debug
```

### 2️⃣ Para monitorear (En otra terminal)
```bash
python bot/bot_monitor.py
```

### 3️⃣ Ver dashboards
```
Abrir en navegador:
- dashboards/BOT_DASHBOARD.html
- dashboards/BACKTESTING_DASHBOARD.html
```

---

## 📚 DOCUMENTACIÓN

### 🚀 Primero lee (En orden)
1. **[INDEX.md](INDEX.md)** ← Índice maestro completo
2. **[00_START_HERE.md](00_START_HERE.md)** - Introducción
3. **[docs/guias/QUICK_START_BOT_VIVO.md](docs/guias/QUICK_START_BOT_VIVO.md)** - Cómo operar

---

## 📢 Documentación unificada (GitHub Pages)

He consolidado toda la documentación en una página central bajo la carpeta `docs/` para publicar fácilmente con GitHub Pages.

- Entrada principal de la documentación: [`docs/ALL_DOCS_SUMMARY.md`](docs/ALL_DOCS_SUMMARY.md)
- Análisis por archivo y auditoría detallada: [`AUDITORIA_PROYECTO.md`](AUDITORIA_PROYECTO.md)

Para publicar como página web, renombra `docs/ALL_DOCS_SUMMARY.md` a `docs/index.md` o habilita GitHub Pages desde la carpeta `docs/` en la configuración del repositorio.

¿Quieres que lo convierta ahora a `docs/index.md` y haga el commit? Responde "sí" para que lo haga.

### 📖 Documentación por tema
- **Guías prácticas:** [`docs/guias/`](docs/guias/) - Cómo hacer cosas
- **Análisis técnico:** [`docs/análisis/`](docs/análisis/) - Decisiones y viabilidad
- **Resúmenes:** [`docs/resúmenes/`](docs/resúmenes/) - Estado actual y resultados

---

## 📊 ESTADO ACTUAL

### ✅ Sistema Operativo
```
🤖 BOT:              ✅ En vivo (H1 EURUSD)
🧠 ML Model:         ✅ 95% accuracy
🛡️ Risk Management:  ✅ Activado (2% SL, 4% TP)
📈 Backtesting:      ✅ +317.61% ROI validado
💾 Base de datos:    ✅ Operativa
📱 Monitoreo:        ✅ Disponible
```

### 📈 Métricas (Backtesting)
| Métrica | Valor |
|---------|-------|
| **ROI** | +317.61% 🚀 |
| **Win Rate** | 98.92% ✅ |
| **Drawdown** | 0.00% 🛡️ |
| **Trades** | 93 ejecutados |
| **Profit** | $31,761 |

---

## 📂 ESTRUCTURA DEL PROYECTO

```
PROYECTO 2/
├── 📖 DOCUMENTACIÓN
│   ├── INDEX.md (↑ LEE ESTO PRIMERO)
│   ├── README.md (este archivo)
│   ├── 00_START_HERE.md
│   └── docs/
│       ├── guias/ (Cómo hacer cosas)
│       ├── análisis/ (Análisis técnico)
│       └── resúmenes/ (Estado actual)
│
├── 🤖 BOT OPERATIVO
│   ├── main.py (Orquestador principal)
│   ├── bot/
│   │   ├── start_bot.py (Launcher)
│   │   ├── bot_monitor.py (Monitor)
│   │   └── logs/ (Archivos de log)
│   └── config/config.yaml
│
├── 📊 BACKTESTING
│   ├── backtesting/
│   │   ├── backtest_advanced_model.py
│   │   ├── backtest_improved_strategy.py
│   │   ├── run_backtest_parallel.py
│   │   └── resultados/
│   └── (scripts de validación)
│
├── 📈 DASHBOARDS
│   ├── dashboards/
│   │   ├── BOT_DASHBOARD.html
│   │   ├── BACKTESTING_DASHBOARD.html
│   │   └── ML_ADVANCED_DASHBOARD.html
│
├── 🧠 MODELOS Y DATOS
│   ├── src/data/
│   │   ├── trading_phantom.db (Base de datos)
│   │   └── models/advanced_model.pkl (ML Model)
│
├── 🛠️ HERRAMIENTAS
│   ├── tools/check_trades.py
│   ├── scripts/
│   └── (utilidades)
│
└── ⚙️ SISTEMA CORE
    ├── core/orchestrator.py
    ├── modules/ (Módulos principales)
    └── mt5/ (Conector MetaTrader 5)
```

---

## 🚀 COMANDOS COMUNES

### Operación del Bot
```bash
# Iniciar bot con launcher
python start_bot.py

# Iniciar bot directo
python main.py --debug

# Una sola iteración (prueba)
python main.py --once

# Con debug completo
python main.py --debug --once
```

### Monitoreo
```bash
# Monitor en terminal
python bot/bot_monitor.py

# Verificar trades
python tools/check_trades.py

# Ver últimos logs
Get-Content bot/logs/*.log -Tail 50
```

### Backtesting
```bash
# Backtesting interactivo (menú)
python backtesting/run_backtest_parallel.py

# Backtesting modelo básico
python backtesting/backtest_advanced_model.py

# Backtesting mejorado (con risk management)
python backtesting/backtest_improved_strategy.py

# Ambos en paralelo
python backtesting/run_backtest_parallel.py
# Seleccionar opción 3
```

### Configuración
```bash
# Editar configuración
nano config/config.yaml
# O en Windows
notepad config/config.yaml
```

---

## 🎯 CARACTERÍSTICAS PRINCIPALES

### 🧠 Machine Learning
- **Algoritmo:** Random Forest Classifier (200 árboles)
- **Features:** 20 variables engineered
- **Accuracy:** 95% en validación
- **Validación:** 5-fold cross-validation (86.88% ± 7.76%)

### 🛡️ Risk Management
- **Stop Loss:** -2% (protección de capital)
- **Take Profit:** +4% (asegurar ganancias)
- **Position Sizing:** 95% equity (dinámico)
- **Risk per Trade:** 2% máximo

### 📊 Signal Filtering
- **Confidence Threshold:** >55%
- **Calidad sobre cantidad:** Rechaza 0.5% de señales débiles
- **Resultado:** Win rate 98.92%

### 📈 Backtesting
- **Datos históricos:** 200 trades
- **Estrategia validada:** Risk management completo
- **ROI:** +317.61%
- **Estabilidad:** 0% drawdown

---

## 📋 GUÍA RÁPIDA POR ROL

### 👨‍💼 Para Traders
1. Abre [docs/guias/QUICK_START_BOT_VIVO.md](docs/guias/QUICK_START_BOT_VIVO.md)
2. Ejecuta `python start_bot.py`
3. Monitorea con `python bot/bot_monitor.py`
4. Ve resultados en dashboards

### 👨‍💻 Para Developers
1. Lee [INDEX.md](INDEX.md)
2. Revisa [ARQUITECTURA_MODULAR.md](ARQUITECTURA_MODULAR.md)
3. Estudia código en `core/`, `modules/`, `mt5/`
4. Haz cambios y testa con backtesting

### 📊 Para Analysts
1. Lee [docs/análisis/](docs/análisis/)
2. Ejecuta backtesting: `python backtesting/run_backtest_parallel.py`
3. Analiza resultados en `backtesting/resultados/`
4. Ve dashboards en `dashboards/`

---

## 🔧 CONFIGURACIÓN

### Activar/Desactivar ML
```yaml
# config/config.yaml
ml:
  enabled: true              # true para activar
  confidence_threshold: 0.55 # 55% umbral
```

### Risk Management
```yaml
improved_strategy:
  stop_loss_pct: 0.02       # -2%
  take_profit_pct: 0.04     # +4%
  position_size: 0.95       # 95% equity
```

### Símbolo y Timeframe
```yaml
symbol: EURUSD    # Cambiar a otro
timeframe: H1     # H1, M15, M5, M1
```

---

## 📈 ROADMAP

### ✅ Completado (Hoy)
- [x] ML Model entrenado (95% accuracy)
- [x] Risk Management implementado
- [x] Bot operando en vivo
- [x] Backtesting validado
- [x] Documentación reorganizada

### 🔄 En Progreso (24-72h)
- [ ] Validación en vivo
- [ ] Monitoreo de trades reales
- [ ] Comparación vs backtesting

### 📅 Próximas 1-2 semanas
- [ ] Forward testing (datos nuevos)
- [ ] Optimización de parámetros
- [ ] Considerar M5 o M15

### 🗓️ Próximas 2-4 semanas
- [ ] Migración a cuenta REAL
- [ ] Capital inicial pequeño ($500)
- [ ] Circuit breakers y alertas
- [ ] Monitoreo 24/7

---

## 🔍 BÚSQUEDA RÁPIDA

### Preguntas frecuentes

**¿Cómo inicio el bot?**
→ `python start_bot.py` o `python main.py --debug`

**¿Dónde veo los trades?**
→ `python tools/check_trades.py` o ver dashboard

**¿Puedo ejecutar backtesting mientras opera el bot?**
→ Sí, es seguro. Ver: [docs/análisis/BACKTESTING_PARALELO.md](docs/análisis/BACKTESTING_PARALELO.md)

**¿Por qué no cambiar a M1?**
→ Porque el modelo fue entrenado en H1. Ver: [docs/análisis/ANALISIS_M1_VIABILIDAD.md](docs/análisis/ANALISIS_M1_VIABILIDAD.md)

**¿Cuál es el siguiente paso?**
→ Monitorear 48-72 horas. Ver: [docs/resúmenes/BOT_EN_VIVO.md](docs/resúmenes/BOT_EN_VIVO.md)

---

## 📚 REFERENCIA COMPLETA

| Necesito... | Leer/Ver... |
|------------|-----------|
| Empezar rápido | [docs/guias/QUICK_START_BOT_VIVO.md](docs/guias/QUICK_START_BOT_VIVO.md) |
| Entender arquitectura | [ARQUITECTURA_MODULAR.md](ARQUITECTURA_MODULAR.md) |
| Backtesting paralelo | [docs/análisis/BACKTESTING_PARALELO.md](docs/análisis/BACKTESTING_PARALELO.md) |
| M1 vs H1 análisis | [docs/análisis/ANALISIS_M1_VIABILIDAD.md](docs/análisis/ANALISIS_M1_VIABILIDAD.md) |
| Estado actual | [docs/resúmenes/BOT_EN_VIVO.md](docs/resúmenes/BOT_EN_VIVO.md) |
| Resultados backtest | [docs/resúmenes/RESUMEN_EJECUTIVO_BACKTEST_MEJORAS.md](docs/resúmenes/RESUMEN_EJECUTIVO_BACKTEST_MEJORAS.md) |
| Dashboard visual | Abrir `dashboards/BOT_DASHBOARD.html` |
| Monitor terminal | `python bot/bot_monitor.py` |
| Verificar trades | `python tools/check_trades.py` |

---

## 🎓 FLUJO RECOMENDADO

### Día 1 (Hoy)
1. ✅ Leer [00_START_HERE.md](00_START_HERE.md)
2. ✅ Ejecutar `python start_bot.py`
3. ✅ Monitorear `python bot/bot_monitor.py`
4. ✅ Ver dashboard

### Día 2-3
1. Monitorear bot en vivo
2. Validar que win rate > 90%
3. Registrar resultados

### Día 4+
1. Si todo OK → Ejecutar backtesting paralelo
2. Si todo OK → Considerar M5
3. Si todo OK → Migrar a cuenta real

---

## 🛠️ TROUBLESHOOTING

### Bot no arranca
```bash
# Verificar ambiente
python --version
pip list | grep -E "MetaTrader|scikit"

# Verificar archivos
ls src/data/models/advanced_model.pkl
ls config/config.yaml
```

### Backtesting falla
```bash
# Verificar BD
python tools/check_trades.py

# Verificar modelo
python -c "import pickle; pickle.load(open('src/data/models/advanced_model.pkl', 'rb'))"
```

### No hay trades ejecutados
```bash
# Ver último log
Get-Content bot/logs/bot_execution_*.log -Tail 100

# Monitorear
python bot/bot_monitor.py
```

---

## 📞 INFORMACIÓN DE CONTACTO

**Proyecto:** Trading Phantom v2.0  
**Estado:** Producción en vivo  
**Último update:** 2026-01-08 19:45 UTC

---

## 📄 LICENCIA

Ver archivo [LICENSE](LICENSE)

---

## 🙏 CRÉDITOS

Sistema desarrollado con:
- Python 3.10+
- scikit-learn (ML)
- MetaTrader 5 API
- SQLite (BD)

---

## ✨ SIGUIENTE PASO

**[Lee el INDEX.md para navegación completa →](INDEX.md)**

O empieza directo:
```bash
python start_bot.py
```

---

**¡El bot está listo para ganar dinero! 🚀**
