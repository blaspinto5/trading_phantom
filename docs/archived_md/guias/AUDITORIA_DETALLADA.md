```markdown
# Auditoría Detallada y Correcciones Aplicadas

Fecha: 2026-01-08

Resumen: se realizó una auditoría de estructura, documentación y prácticas. A continuación se listan malas prácticas detectadas, acciones realizadas y recomendaciones adicionales.

## 1. Malas prácticas detectadas

1. Documentación dispersa: demasiados `.md` y `.txt` en la raíz -> confusión para colaboradores.
2. Archivos y scripts importantes en la raíz (`main.py`, `webapp.py`, `backtest_advanced.py`) -> mezcla de responsabilidades.
3. Carpetas duplicadas (`backtest/` vs `backtesting/`, `docs/` vs `documentacion/`, `tools/` vs `scripts/` vs `utils/`).
4. Logs y artefactos en raíz: `*.log`, `*.pid`, `dist_*`.
5. `.gitignore` no cubría exactamente el patrón deseado.
6. Algunos scripts y assets no estaban en carpetas coherentes (`static/`, `templates/`, dashboards HTML).
7. Submódulo sin sincronización previa que generó conflictos al push.

... (archivo movido a docs/archived_md)

```
