# Contributing to Trading Phantom

¡Gracias por tu interés en contribuir a Trading Phantom! Esta guía te ayudará a entender cómo colaborar de manera efectiva.

## Tabla de contenidos
- [Código de conducta](#código-de-conducta)
- [Cómo empezar](#cómo-empezar)
- [Proceso de contribución](#proceso-de-contribución)
- [Estándares de código](#estándares-de-código)
- [Testing](#testing)
- [Documentación](#documentación)
- [Commit messages](#commit-messages)
- [Pull requests](#pull-requests)

## Código de conducta

Este proyecto se adhiere a un código de conducta basado en el respeto, inclusión y profesionalismo. Se espera que todos los contribuyentes:
- Sean respetuosos con otros colaboradores
- Proporcionen feedback constructivo
- Creen un ambiente seguro y acogedor

## Cómo empezar

### Prerequisitos
- Python 3.10 o superior
- Windows (para desarrollo con MT5)
- Git

### Configuración del entorno de desarrollo

```powershell
# Clonar el repositorio
git clone https://github.com/<owner>/Trading-Phantom.git
cd Trading-Phantom

# Crear y activar venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt -r requirements-dev.txt
```

## Proceso de contribución

### 1. Crear una issue
Antes de comenzar trabajo significativo:
- Revisa las [issues existentes](https://github.com/<owner>/Trading-Phantom/issues)
- Crea una issue describiendo el problema o feature
- Espera feedback del mantenedor

### 2. Fork y rama
```powershell
# Fork el repositorio en GitHub (UI)
git clone https://github.com/<tu-usuario>/Trading-Phantom.git
git checkout -b feature/tu-feature-name
# o para bugfixes:
git checkout -b bugfix/descripcion-del-bug
```

### 3. Desarrollo e iteración
- Trabaja en tu rama
- Ejecuta tests y linter frecuentemente
- Haz commits pequeños y descriptivos

### 4. Testing antes de PR
```powershell
$env:PYTHONPATH="src"
python -m pytest -q              # tests unitarios
ruff check .                     # linter
ruff check --fix .               # auto-fix (si es posible)
```

### 5. Push y Pull Request
```powershell
git push origin feature/tu-feature-name
```

Abre un PR en GitHub con:
- Descripción clara del cambio
- Referencia a la issue (ej: `Closes #123`)
- Checklist de cambios

## Estándares de código

### Style guide

Usamos `ruff` para linting. Configuración en `pyproject.toml`:

```ini
[tool.ruff]
line-length = 88
select = ["E", "F", "W", "I", "C", "B"]
ignore = ["E203"]
```

### Convenciones

- **Nombres**: `snake_case` para funciones/variables, `PascalCase` para clases
- **Docstrings**: Google-style para funciones/métodos
- **Type hints**: Recomendado para nuevas funciones
- **Imports**: Agrupa std lib, terceros, y locales (separados por línea en blanco)

Ejemplo:

```python
import logging
import sys
from pathlib import Path

import pandas as pd

from trading_phantom.config.config_loader import load_config

logger = logging.getLogger(__name__)


class StrategyAnalyzer:
    """Analiza señales de estrategia con soporte para backtesting.
    
    Args:
        symbol (str): Par a operar (ej. 'EURUSD')
        config (dict): Configuración de estrategia
    """
    
    def __init__(self, symbol: str, config: dict) -> None:
        self.symbol = symbol
        self.config = config
    
    def analyze(self, data: pd.DataFrame) -> str:
        """Analiza datos y devuelve una señal.
        
        Args:
            data: DataFrame con OHLCV
            
        Returns:
            'BUY', 'SELL', o 'HOLD'
        """
        # implementación
        pass
```

### Estructura de carpetas

Respeta el layout `src/`:
```
src/
└─ trading_phantom/
   ├─ core/
   ├─ modules/
   ├─ mt5/
   ├─ backtest/
   ├─ config/
   ├─ utils/
   ├─ templates/
   └─ static/
```

## Testing

### Estructura de tests

Los tests están en `tests/` en raíz:
```
tests/
├─ conftest.py                   # fixtures compartidas
├─ test_mt5_connector.py         # pruebas del connector
├─ test_strategy.py              # pruebas de estrategia
└─ test_visual_adapter.py        # pruebas de backtest visual
```

### Escribiendo tests

```python
# tests/test_my_module.py
import pytest
from trading_phantom.modules.my_module import MyClass


class TestMyClass:
    """Suite de pruebas para MyClass."""
    
    def test_init_sets_attributes(self):
        """Verifica que __init__ asigna atributos correctamente."""
        obj = MyClass(param1="value")
        assert obj.param1 == "value"
    
    def test_method_returns_expected_type(self):
        """Verifica que el método retorna el tipo correcto."""
        obj = MyClass()
        result = obj.process()
        assert isinstance(result, dict)
    
    @pytest.mark.parametrize("input,expected", [
        ("BUY", True),
        ("SELL", True),
        ("HOLD", False),
    ])
    def test_is_signal_valid(self, input, expected):
        """Prueba parametrizada para validación de señales."""
        obj = MyClass()
        assert obj.is_valid_signal(input) == expected
```

### Ejecutar tests

```powershell
# Tests unitarios
$env:PYTHONPATH="src"
python -m pytest tests/ -v

# Con coverage (opcional)
pip install pytest-cov
python -m pytest tests/ --cov=src/trading_phantom
```

## Documentación

### Docstrings

Todas las funciones/clases públicas deben tener docstrings en formato Google:

```python
def load_rates(symbol: str, bars: int = 1000) -> Optional[pd.DataFrame]:
    """Carga datos históricos desde MT5 para un símbolo.
    
    Args:
        symbol: Par a operar (ej. 'EURUSD')
        bars: Número de velas a obtener (default: 1000)
        
    Returns:
        DataFrame con columnas OHLCV, o None si falla la conexión
        
    Raises:
        ValueError: Si symbol es inválido
        ConnectionError: Si MT5 no está disponible
        
    Example:
        >>> df = load_rates('EURUSD', bars=500)
        >>> print(df.head())
    """
    pass
```

### Documentación de módulos

Cada carpeta `src/trading_phantom/*` puede incluir un `_module_doc.md` describiendo su rol:

```markdown
# módulo: trading_phantom.modules

Contiene la lógica central del bot: estrategia, manejo de riesgo y ejecución.

## Componentes

- `strategy.py`: Estrategia SMA+RSI
- `risk_manager.py`: Cálculo de lotes, SL/TP
- `trader.py`: Ejecución de órdenes
- `data_loader.py`: Normalización de datos MT5
```

## Commit messages

Usa el formato convencional:

```
<tipo>(<scope>): <descripción corta>

<cuerpo detallado (opcional)>

<footer (opcional)>
```

Tipos:
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Formato, sin cambio de lógica
- `refactor`: Reorganización sin cambio de funcionalidad
- `perf`: Mejoras de rendimiento
- `test`: Añadir/actualizar tests
- `chore`: Dependencias, config, etc.

Ejemplos:

```
feat(strategy): agregar soporte para múltiples timeframes

- Extiende Strategy para aceptar lista de timeframes
- Valida timeframes contra MT5.TIMEFRAME_*
- Añade tests para validación

Closes #42
```

```
fix(connector): reintentos exponenciales en initialize()

Previene falla inmediata si MT5 no responde rápidamente.
Backoff: 0.5s, 1s, 2s, 4s

Fixes #35
```

## Pull requests

### Checklist pre-PR

- [ ] Rama creada desde `main` actualizada
- [ ] Tests locales pasan (`pytest`, `ruff`)
- [ ] Docstrings añadidos/actualizados
- [ ] Commits son pequeños y descriptivos
- [ ] No hay cambios no intencionados
- [ ] Issue asociada referenciada (`Closes #XX`)

### Template de PR

```markdown
## Descripción
Breve descripción del cambio (1-2 líneas)

## Tipo de cambio
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing realizado
- [ ] Tests unitarios pasan
- [ ] Ruff linter pasa
- [ ] Probado manualmente en Windows con MT5

## Screenshots / Logs
(Si aplica)

## Checklist
- [ ] Código sigue style guide
- [ ] Documentación actualizada
- [ ] Tests añadidos/actualizados
- [ ] No hay código comentado sin justificación
```

### Revisión y merge

- Mantenedores revisarán el código y el test coverage
- Se pueden solicitar cambios
- Una vez aprobado, el PR se hará merge a `main`
- El cambio se reflejará en CHANGELOG.md y se creará un tag de versión

## Reportar bugs

Usa GitHub Issues con el siguiente template:

```markdown
## Descripción del bug
Descripción clara de qué está pasando mal

## Pasos para reproducir
1. Abre launcher.py
2. Arranca el bot con X config
3. Observa que Y ocurre

## Comportamiento esperado
Debería ocurrir Z

## Entorno
- Windows 10/11
- Python 3.10/3.11
- MT5 versión X
- Rama: main

## Logs / Stacktrace
(Adjunta logs de %TEMP%/trading_phantom_crash.log si está disponible)
```

## Preguntas / Dudas

- Abre una discussion en GitHub (si está habilitado)
- O crea una issue con tag `question`

---

¡Gracias por tu contribución! 🚀
