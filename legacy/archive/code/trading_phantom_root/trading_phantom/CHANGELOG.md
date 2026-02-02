# Changelog

Todos los cambios notables en Trading Phantom se documentan en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto sigue [Semantic Versioning](https://semver.org/es/).

---

## [Unreleased]

### Added
- **Restructuración a layout `src/`**: Ahora el código principal está en `src/trading_phantom/` para mejor separación entre código, tests y scripts
- **Documentación extendida**: Guía completa en `docs/README.md` con setup, configuración, endpoints, backtesting y empaquetado
- **CONTRIBUTING.md**: Pautas detalladas para contribuyentes (workflow, estándares de código, testing, commits)
- **ARCHITECTURE.md**: Explicación del diseño de arquitectura del bot
- **API.md**: Documentación detallada de todos los endpoints REST
- **LICENSE**: Incluido LICENSE para claridad legal
- **Configuración centralizada**: `pyproject.toml` en raíz con configuración de `ruff` y `pytest.ini` actualizado
- **CI mejorada**: Variable de entorno `PYTHONPATH=src` en GitHub Actions para el layout nuevo
- **Testeo mejorado**: `tests/conftest.py` actualizado para resolver `src/` automáticamente

### Changed
- **Imports**: Todos los imports ahora apuntan a `src/trading_phantom` en el layout nuevo
- **launcher.py**: Actualizado para buscar `src/` primero en desarrollo
- **webapp.py**: Ahora establece `PYTHONPATH=src` al lanzar subprocess del bot
- **pytest.ini**: Añadido `testpaths = tests` para descubrimiento explícito de tests en raíz
- **Localización de estructura**: Documentación traducida al español, ejemplos en PowerShell para Windows

### Deprecated
- Carpeta antigua `trading_phantom/` en raíz (será removida en v1.0.0 cuando migremos completamente)

### Removed
- Imports duplicados y módulos bajo la raíz `trading_phantom/`

### Fixed
- **MT5Connector**: Mejorada gestión de reintentos con backoff exponencial
- **Serialización JSON**: Helper `_make_jsonable` en `webapp.py` para evitar `TypeError` con pandas/numpy
- **Flask reloader**: Desactivado en modo threaded para evitar errores de signals

### Security
- `pip-audit` integrado en CI para detectar vulnerabilidades de alto impacto
- Recomendación: No almacenar secretos en el repo, usar variables de entorno

---

## [v0.9.0] - 2025-12-15

### Added
- Primer release: Bot core con Strategy (SMA+RSI), RiskManager, Trader
- Conexión a MT5 con retry/backoff
- Backtesting numérico y visual con librería `backtesting`
- Flask API para control del bot y UI con pywebview
- Empaquetado con PyInstaller
- Tests unitarios con pytest
- Linter y auditoría con ruff y pip-audit
- Configuración YAML centralizada

### Fixed
- Conectar a MT5 con reintentos automáticos
- Evitar múltiples trades por vela con `traded_this_candle`
- Serialización JSON de resultados de backtest

---

## Notas sobre versionado

- **0.x.x**: Fase beta; cambios pueden ser breaking
- **1.0.0**: Versión estable; garantías de compatibilidad para `pyproject.toml` y `config.yaml`

---

## Cómo contribuir

Lee [CONTRIBUTING.md](CONTRIBUTING.md) para conocer el proceso de contribución, estándares de código y mejores prácticas.

---

## Soporte

Para reportar issues: https://github.com/<owner>/Trading-Phantom/issues
