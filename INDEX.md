# 📚 ÍNDICE MAESTRO - TRADING PHANTOM PROJECT

**Última actualización:** 2026-01-08  
**Versión:** 2.0 - Reorganizado  
**Estado:** ✅ Bot en vivo H1 + Documentación centralizada

---

## 🎯 INICIO RÁPIDO

### Para empezar (PRIMERO LEE):
1. **[00_START_HERE.md](00_START_HERE.md)** - Introducción general
2. **[QUICK_START_BOT_VIVO.md](docs/guias/QUICK_START_BOT_VIVO.md)** - Cómo operar el bot
3. **[README.md](README.md)** - Documentación completa

---

## 📂 ESTRUCTURA DEL PROYECTO

```
PROYECTO 2/
├── 📖 DOCUMENTACIÓN GENERAL
│   ├── 00_START_HERE.md (Inicio)
│   ├── README.md (Principal)
│   └── LICENSE
│
├── 📁 /docs (Documentación organizada)
│   ├── /guias
│   │   ├── QUICK_START_BOT_VIVO.md
│   │   ├── QUICK_BACKTEST_PARALELO.md
│   │   └── MANUAL_OPERATIVO.md
│   ├── /análisis
│   │   ├── ANALISIS_M1_VIABILIDAD.md
│   │   ├── BACKTESTING_PARALELO.md
│   │   └── ANALISIS_MEJORAS_ESTRATEGIA.md
│   └── /resúmenes
│       ├── BOT_EN_VIVO.md
│       ├── QUE_PASO_RESUMEN.md
│       └── RESUMEN_EJECUTIVO_BACKTEST_MEJORAS.md
│
├── 🤖 /bot (Bot operativo)
│   ├── main.py (Orquestador)
│   ├── start_bot.py (Launcher)
│   ├── bot_monitor.py (Monitor)
│   └── /logs (Logs de ejecución)
│
├── 📊 /backtesting (Backtesting)
│   ├── backtest_advanced_model.py
│   ├── backtest_improved_strategy.py
│   ├── run_backtest_parallel.py
│   └── /resultados (JSON results)
│
├── 📈 /dashboards (Dashboards web)
│   ├── BOT_DASHBOARD.html
│   ├── BACKTESTING_DASHBOARD.html
│   └── ML_ADVANCED_DASHBOARD.html
│
├── 🛠️ /tools (Herramientas útiles)
│   ├── check_trades.py
│   └── setup_training_data.py
│
├── ⚙️ /config (Configuración)
│   ├── config.yaml
│   └── config_loader.py
│
├── 🧠 /src (Datos y modelos)
│   ├── /data
│   │   ├── trading_phantom.db
│   │   └── /models
│   │       └── advanced_model.pkl
│   └── /logs
│
└── 📦 /core, /modules, /mt5 (Sistema core)
    ├── core/orchestrator.py
    ├── modules/*.py
    └── mt5/connector.py
```

---

## 📖 DOCUMENTACIÓN POR CATEGORÍA

### 🚀 EMPEZAR (Lee primero)
| Archivo | Descripción |
|---------|-------------|
| [00_START_HERE.md](00_START_HERE.md) | Introducción general |
| [QUICK_START_BOT_VIVO.md](docs/guias/QUICK_START_BOT_VIVO.md) | Cómo correr el bot |
| [README.md](README.md) | Documentación completa |

### 📊 ESTADO ACTUAL
| Archivo | Descripción |
|---------|-------------|
| [BOT_EN_VIVO.md](docs/resúmenes/BOT_EN_VIVO.md) | Estado del bot operativo |
| [QUE_PASO_RESUMEN.md](docs/resúmenes/QUE_PASO_RESUMEN.md) | Resumen de ejecución |
| [RESUMEN_EJECUTIVO_BACKTEST_MEJORAS.md](docs/resúmenes/RESUMEN_EJECUTIVO_BACKTEST_MEJORAS.md) | Resultados backtest |

### 🔧 GUÍAS TÉCNICAS
| Archivo | Descripción |
|---------|-------------|
| [QUICK_BACKTEST_PARALELO.md](docs/guias/QUICK_BACKTEST_PARALELO.md) | Backtesting paralelo |
| [MANUAL_OPERATIVO.md](docs/guias/MANUAL_OPERATIVO.md) | Manual de operación |
| [ARQUITECTURA_MODULAR.md](ARQUITECTURA_MODULAR.md) | Arquitectura del sistema |

### 📈 ANÁLISIS TÉCNICO
| Archivo | Descripción |
|---------|-------------|
| [ANALISIS_M1_VIABILIDAD.md](docs/análisis/ANALISIS_M1_VIABILIDAD.md) | Por qué no cambiar a M1 |
| [BACKTESTING_PARALELO.md](docs/análisis/BACKTESTING_PARALELO.md) | Backtesting concurrent |
| [ANALISIS_MEJORAS_ESTRATEGIA.md](docs/análisis/ANALISIS_MEJORAS_ESTRATEGIA.md) | Mejoras implementadas |

### 💻 HERRAMIENTAS
| Archivo | Descripción |
|---------|-------------|
| [bot_monitor.py](bot/bot_monitor.py) | Monitor en terminal |
| [run_backtest_parallel.py](backtesting/run_backtest_parallel.py) | Runner de backtests |
| [check_trades.py](tools/check_trades.py) | Verificador de trades |

### 📊 DASHBOARDS
| Archivo | Descripción |
|---------|-------------|
| [BOT_DASHBOARD.html](dashboards/BOT_DASHBOARD.html) | Dashboard del bot |
| [BACKTESTING_DASHBOARD.html](dashboards/BACKTESTING_DASHBOARD.html) | Dashboard de backtest |
| [ML_ADVANCED_DASHBOARD.html](dashboards/ML_ADVANCED_DASHBOARD.html) | Dashboard de ML |

---

## 🎯 COMANDOS RÁPIDOS

### Operar el bot
```bash
# Iniciar bot
python start_bot.py

# O directo
python main.py --debug

# Monitorear
python bot/bot_monitor.py
```

### Backtesting
```bash
# Backtesting paralelo interactivo
python backtesting/run_backtest_parallel.py

# Backtesting individual
python backtesting/backtest_advanced_model.py
python backtesting/backtest_improved_strategy.py
```

### Herramientas
```bash
# Ver trades ejecutados
python tools/check_trades.py

# Monitor en vivo
python bot/bot_monitor.py
```

### Ver dashboards
```
Abrir en navegador:
• dashboards/BOT_DASHBOARD.html
• dashboards/BACKTESTING_DASHBOARD.html
• dashboards/ML_ADVANCED_DASHBOARD.html
```

---

## 📊 ESTADO ACTUAL DEL PROYECTO

### ✅ Completado
- [x] ML Model: 95% accuracy
- [x] Risk Management: Implementado (2% SL, 4% TP)
- [x] Bot en vivo: Operando en MetaTrader 5
- [x] Backtesting: Validado (317.61% ROI)
- [x] Documentación: Reorganizada y centralizada

### 🔄 En progreso
- [ ] Validación en vivo (48-72 horas)
- [ ] Forward testing
- [ ] Optimización de parámetros

### 📅 Próximos pasos
1. **Hoy-Mañana:** Monitorear bot H1
2. **Día 3:** Ejecutar backtesting paralelo
3. **Semana 2:** Considerar M5 o M15
4. **Semana 3:** Deploy en cuenta real

---

## 🔍 BÚSQUEDA RÁPIDA

### Por tema
- **Bot:** `bot/`, `docs/guias/QUICK_START_BOT_VIVO.md`
- **Backtesting:** `backtesting/`, `docs/análisis/BACKTESTING_PARALELO.md`
- **ML Model:** `src/data/models/`, `docs/análisis/`
- **Configuración:** `config/`, `docs/guias/MANUAL_OPERATIVO.md`
- **Resultados:** `backtesting/resultados/`, `dashboards/`

### Por tipo de documento
- **Guías:** `docs/guias/`
- **Análisis:** `docs/análisis/`
- **Resúmenes:** `docs/resúmenes/`
- **Código:** `bot/`, `backtesting/`, `tools/`
- **Dashboards:** `dashboards/`

---

## 📚 REFERENCIAS CRUZADAS

### Para entender el ML
1. Leer: [QUICK_START_BOT_VIVO.md](docs/guias/QUICK_START_BOT_VIVO.md)
2. Ver: [ML_ADVANCED_DASHBOARD.html](dashboards/ML_ADVANCED_DASHBOARD.html)
3. Profundizar: [ARQUITECTURA_MODULAR.md](ARQUITECTURA_MODULAR.md)

### Para operar el bot
1. Empezar: [QUICK_START_BOT_VIVO.md](docs/guias/QUICK_START_BOT_VIVO.md)
2. Monitorear: `python bot/bot_monitor.py`
3. Ver: [BOT_DASHBOARD.html](dashboards/BOT_DASHBOARD.html)

### Para entender el backtesting
1. Leer: [BACKTESTING_PARALELO.md](docs/análisis/BACKTESTING_PARALELO.md)
2. Ejecutar: `python backtesting/run_backtest_parallel.py`
3. Ver resultados: `backtesting/resultados/`

---

## 🎓 GUÍA DE LECTURA RECOMENDADA

### Para nuevos usuarios (1-2 horas)
1. [00_START_HERE.md](00_START_HERE.md) - 10 min
2. [QUICK_START_BOT_VIVO.md](docs/guias/QUICK_START_BOT_VIVO.md) - 10 min
3. [BOT_EN_VIVO.md](docs/resúmenes/BOT_EN_VIVO.md) - 15 min
4. [README.md](README.md) - 30 min
5. Ejecutar bot - 10 min

### Para desarrolladores (2-4 horas)
1. [ARQUITECTURA_MODULAR.md](ARQUITECTURA_MODULAR.md) - 30 min
2. [MANUAL_OPERATIVO.md](docs/guias/MANUAL_OPERATIVO.md) - 30 min
3. [ANALISIS_MEJORAS_ESTRATEGIA.md](docs/análisis/ANALISIS_MEJORAS_ESTRATEGIA.md) - 30 min
4. Revisar código en `bot/`, `backtesting/`, `tools/` - 1 hora
5. Ejecutar backtesting - 30 min

### Para traders (30 min)
1. [QUICK_START_BOT_VIVO.md](docs/guias/QUICK_START_BOT_VIVO.md) - 10 min
2. Ejecutar `python bot/bot_monitor.py` - 5 min
3. Ver [BOT_DASHBOARD.html](dashboards/BOT_DASHBOARD.html) - 10 min
4. Leer [QUE_PASO_RESUMEN.md](docs/resúmenes/QUE_PASO_RESUMEN.md) - 5 min

---

## 🔗 NAVEGACIÓN

### Volver a índice
**En cualquier documento:** Ve a la raíz y abre `INDEX.md`

### Estructura de carpetas
- `/docs` - Toda la documentación
- `/bot` - Sistema operativo del bot
- `/backtesting` - Sistema de backtesting
- `/dashboards` - Visualizaciones
- `/tools` - Herramientas auxiliares
- `/config` - Configuración
- `/src` - Datos y modelos

---

## 📞 SOPORTE RÁPIDO

### Problema: Bot no arranca
→ Ver: [docs/guias/MANUAL_OPERATIVO.md](docs/guias/MANUAL_OPERATIVO.md)

### Problema: Backtesting falla
→ Ver: [docs/análisis/BACKTESTING_PARALELO.md](docs/análisis/BACKTESTING_PARALELO.md)

### Pregunta: ¿Cómo monitorear?
→ Ejecutar: `python bot/bot_monitor.py`

### Pregunta: ¿Cambiar a M1?
→ Ver: [docs/análisis/ANALISIS_M1_VIABILIDAD.md](docs/análisis/ANALISIS_M1_VIABILIDAD.md)

---

## 📊 MAPA DE DOCUMENTOS

```
├── 📖 Inicio
│   ├── 00_START_HERE.md ...................... Entrada principal
│   ├── README.md ............................ Documentación completa
│   └── INDEX.md ............................ Este documento
│
├── 🚀 Guías prácticas (/docs/guias/)
│   ├── QUICK_START_BOT_VIVO.md ............. Cómo operar bot
│   ├── QUICK_BACKTEST_PARALELO.md ......... Backtesting
│   └── MANUAL_OPERATIVO.md ................. Manual completo
│
├── 📊 Resúmenes (/docs/resúmenes/)
│   ├── BOT_EN_VIVO.md ..................... Estado actual
│   ├── QUE_PASO_RESUMEN.md ............... Qué pasó
│   └── RESUMEN_EJECUTIVO_BACKTEST_MEJORAS.md .. Resultados
│
├── 🔬 Análisis técnico (/docs/análisis/)
│   ├── ANALISIS_M1_VIABILIDAD.md ......... Análisis timeframes
│   ├── BACKTESTING_PARALELO.md .......... Backtesting concurrent
│   └── ANALISIS_MEJORAS_ESTRATEGIA.md .. Mejoras implementadas
│
├── 💻 Código operativo (/bot/, /backtesting/, /tools/)
│   ├── bot/main.py ....................... Orquestador
│   ├── bot/start_bot.py .................. Launcher
│   ├── bot/bot_monitor.py ............... Monitor
│   ├── backtesting/backtest_*.py ....... Backtests
│   └── tools/check_trades.py ........... Herramientas
│
└── 📈 Dashboards (/dashboards/)
    ├── BOT_DASHBOARD.html ................ Dashboard bot
    ├── BACKTESTING_DASHBOARD.html ....... Dashboard backtest
    └── ML_ADVANCED_DASHBOARD.html ....... Dashboard ML
```

---

## ✅ CHECKLIST DE REFERENCIA

- [ ] Leí [00_START_HERE.md](00_START_HERE.md)
- [ ] Leí [QUICK_START_BOT_VIVO.md](docs/guias/QUICK_START_BOT_VIVO.md)
- [ ] Ejecuté `python start_bot.py`
- [ ] Ejecuté `python bot/bot_monitor.py`
- [ ] Abrí dashboards en navegador
- [ ] Entiendo el estado actual
- [ ] Sé cuál es el próximo paso

---

**Generado:** 2026-01-08  
**Versión:** 2.0 - Reorganizado y centralizado  
**Mantenedor:** Trading Phantom Project

---

[↑ Volver al inicio](#-índice-maestro---trading-phantom-project)
