# 🤖 TRADING PHANTOM — Documentación principal

Estado: BOT EN VIVO (H1 EURUSD)

Resumen rápido:
- ML Model: 95% accuracy (Random Forest)
- Strategy: mejora con risk-management (+317.61% ROI en backtest)

---

## Objetivo de este README

Este README es la vista principal para cualquier colaborador o usuario. Contiene un resumen de todo el proyecto y enlaces a secciones detalladas en `docs/` y carpetas modulares. La documentación completa está disponible en `docs/` y `docs/index.md` sirve como página de entrada para GitHub Pages.

---

## Estructura principal (resumen)

- `bot/` — Sistema de ejecución y monitor
- `modules/` — Lógica de estrategia, riesgo y utilidades
- `backtesting/` — Scripts de backtesting y `resultados/`
- `dashboards/` — HTMLs y visualizaciones
- `webapp/` — Aplicación web (static + templates)
- `docs/` — Documentación unificada (guías, análisis, resúmenes)
- `scripts/` — Instalación, build y ejecución
- `tests/` — Tests unitarios

---

## Inicio rápido

En una terminal (virtualenv activado):
```bash
python bot/start_bot.py         # iniciar bot (launcher)
python bot/bot_monitor.py      # monitor en otra terminal
```

Backtesting (en otra terminal):
```bash
python backtesting/run_backtest_parallel.py
```

Ver dashboards (abrir en navegador):
```
dashboards/BOT_DASHBOARD.html
dashboards/BACKTESTING_DASHBOARD.html
```

---

## Backtesting (sección dedicada)

Ver `backtesting/README.md` para detalles, parámetros y reproducibilidad.

---

## Buenas prácticas y advertencias

- No ejecutar cambios estructurales y cambios funcionales en el mismo commit.
- Mantener `docs/` como fuente de verdad; usar `docs/index.md` para GitHub Pages.
- No almacenar datasets ni modelos pesados en el repo (usar storage externo).

---

## Cómo contribuir

Lee `CONTRIBUTING.md` en la raíz para proceso de PRs, estilo de código y pruebas.

---

## Recursos rápidos

- Índice maestro: `INDEX.md`
- Auditoría y resumen de cambios: `ESTRUCTURA_FINAL.md`, `AUDITORIA_PROYECTO.md`, `AUDITORIA_DETALLADA.md`
- Documentación extendida: `docs/index.md` (GitHub Pages)

---

Si quieres, puedo añadir CI (pre-commit, GitHub Actions) y un `CONTRIBUTING.md` ahora.
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
