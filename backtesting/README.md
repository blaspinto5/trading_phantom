# Backtesting

Este directorio contiene todo lo relativo a backtesting y evaluación de estrategias.

Contenido clave

- `backtest_advanced_model.py` — Backtest del modelo ML puro (archivos originales).
- `backtest_improved_strategy.py` — Backtest de la estrategia mejorada con gestión de riesgo.
- `run_backtest_parallel.py` — Script para ejecutar backtests en paralelo.
- `resultados/` — Resultados y JSONs con métricas y reportes.

Resumen de prácticas y recomendaciones

- Mantén los datos de resultados en `backtesting/resultados/` y evita almacenar archivos grandes en el repo.
- Documenta claramente los parámetros de cada backtest (periodo temporal, símbolo, tamaños de muestra).
- Usa `requirements.txt` o `pyproject.toml` para reproducibilidad de versión.

Comandos comunes

```bash
python backtesting/backtest_improved_strategy.py
python backtesting/run_backtest_parallel.py
```

Resultados principales

- Backtest estrategia mejorada: ROI +317.61%, Win Rate 98.92% (ver `backtesting/resultados/`).
