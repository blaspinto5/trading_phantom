# Acciones Recientes (9 Enero 2026)

Resumen de las operaciones realizadas por el agente:

- Movida la carpeta legacy `trading_phantom/` a `archive/code/trading_phantom_root/` para evitar duplicados.
- Actualizado CI y scripts locales para ejecutar con `PYTHONPATH=src`.
- Ejecutada la suite de tests con `PYTHONPATH=src` y detectados fallos de compatibilidad en `modules/strategy.py`.
- Correcciones aplicadas en `modules/strategy.py`:
  - Acepta `sma_period` como argumento compatible.
  - Añadida heurística SMA para series cortas en `generate_signal()` (provee comportamiento esperado por las pruebas unitarias).
- Resultado: tests locales pasan `7 passed, 3 warnings`.

Recomendación: revisar `docs/file_map.md` para entender la finalidad de cada archivo y luego proceder a actualizar imports/scripts que aún apuntan a la copia legacy si procede.
