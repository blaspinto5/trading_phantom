
# 🤖 TRADING PHANTOM — Principal

Proyecto modular de trading algorítmico con ML, backtesting y dashboard.

Resumen breve:
- Bot modular para MetaTrader 5 (demo/real)
- Backtesting con métricas profesionales
- Sistema ML integrado (RandomForest por defecto)

Requisitos: Python 3.10+, pip, (opcional) MetaTrader 5

Inicio rápido (desarrollo):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q
```

Arrancar el bot (entorno configurado):
```powershell
python -m trading_phantom.core.orchestrator --run
```

Documentación completa en `docs/` y `documentacion/`.

Notas de organización:
- Scripts sueltos del root movidos a `scripts/legacy/`.
- El paquete principal está en `src/trading_phantom/`.

¿Quieres que abra un PR con estos cambios y los de la reorganización? Puedo crear la rama y preparar el commit.
