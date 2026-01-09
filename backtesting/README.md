# Backtesting — Guía y uso

Carpeta con herramientas para evaluar estrategias: backtests numéricos, pruebas
de robustez y utilidades para ejecutar backtests en paralelo.

Contenido clave:
- `backtest_improved_strategy.py` — Backtest de la estrategia con gestión de riesgo.
- `backtest_advanced_model.py` — Backtest orientado a evaluación de modelos ML.
- `run_backtest_parallel.py` — Ejecuta backtests en paralelo y guarda resultados en `resultados/`.

Buenas prácticas:
- No comitees datasets grandes; guarda solo resúmenes y métricas en `resultados/`.
- Registra los parámetros del backtest (símbolo, timeframe, seed) para reproducibilidad.

Comandos de ejemplo:
```bash
python backtesting/backtest_improved_strategy.py
python backtesting/run_backtest_parallel.py
```

Resultados y métricas se almacenan en `backtesting/resultados/`. Para reproducir
experimentos, usa `pyproject.toml`/`requirements.txt` con versiones fijas.
