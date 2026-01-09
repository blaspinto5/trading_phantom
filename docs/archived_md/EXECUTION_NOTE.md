# Nota de ejecución — Archivos archivados

Estos documentos están en la carpeta `docs/archived_md/` como referencia histórica y de soporte. El código activo y canónico del proyecto está en `src/`.

Para ejecutar el proyecto o correr tests localmente, use una de las opciones siguientes desde la raíz del repositorio:

- Establecer `PYTHONPATH` a `src` y ejecutar scripts/tests, por ejemplo:

```powershell
$env:PYTHONPATH='src'; pytest -q
```

- Ejecutar como módulo para que Python resuelva correctamente el paquete:

```powershell
python -m trading_phantom.main
```

Evite ejecutar scripts que añadan la raíz del repo a `sys.path` o ejecutar código directamente desde la antigua carpeta `trading_phantom/` en la raíz. Esa copia fue archivada en `archive/code/trading_phantom_root/` y no debe usarse como fuente principal de ejecución.
