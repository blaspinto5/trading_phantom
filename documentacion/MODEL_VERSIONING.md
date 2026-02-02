**Versionado de Modelos ML**

- **Ubicación:** los modelos se almacenan por defecto en `src/data/models/`.
- **Formato:** cada modelo se guarda como archivo pickle timestamped: `base_YYYYMMDDThhmmssZ.pkl`.
- **Índice:** `models_index.json` contiene el historial con metadata (filename, path, timestamp, metrics, model_type).
- **Último:** `latest_model.json` apunta al último guardado.

Flujo recomendado:

1. Ejecutar entrenamiento con guardado versionado:

```bash
python scripts/ml_train_advanced.py --save
python scripts/ml_train.py --save
```

2. Listar modelos disponibles:

```bash
python scripts/list_models.py
```

3. Restaurar modelo más reciente (ejemplo en código):

```python
from trading_phantom.analytics.model_store import load_latest_model
model_data = load_latest_model()
```

Buenas prácticas:
- Mantener `keep` bajo control (por defecto 5) para no llenar disco.
- Hacer backups remotos (S3 / NAS) si los modelos son críticos.
- Guardar metadatos de entrenamiento (seed, data hashes) fuera del pickle para reproducibilidad.
