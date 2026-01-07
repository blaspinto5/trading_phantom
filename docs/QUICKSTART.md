# Guía de instalación rápida

Instalación step-by-step para Trading Phantom en Windows.

## Requisitos previos

- **Windows 10/11**
- **Python 3.10+** (https://www.python.org/downloads/)
- **MetaTrader 5** instalado y con sesión activa (para live trading)
- **Git** (opcional, para clonar el repo)

## Pasos

### 1. Descargar / clonar el repositorio

```powershell
# Opción A: Clone con git
git clone https://github.com/<owner>/Trading-Phantom.git
cd Trading-Phantom

# Opción B: Descargar ZIP y extraer
# Navegar a la carpeta extraída en PowerShell
```

### 2. Crear y activar entorno virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si obtienes error de "execution policy", ejecuta:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Actualizar pip e instalar dependencias

```powershell
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt -r requirements-dev.txt
```

### 4. Verificar instalación

```powershell
$env:PYTHONPATH="src"
python -m pytest -q
```

Deberías ver algo como:
```
.... (tests pasan) ✓
```

## Primer uso

### Opción A: Interfaz gráfica (pywebview)

```powershell
python scripts/launcher.py --debug
```

Abrirá una ventana con la UI. Desde ahí puedes:
- Iniciar/detener el bot
- Ver logs en tiempo real
- Ejecutar backtests
- Descargarde los resultados

### Opción B: API REST local

```powershell
$env:PYTHONPATH="src"
python src/trading_phantom/webapp.py
```

Luego abre en navegador: `http://127.0.0.1:5000`

### Opción C: Bot directo (línea de comandos)

```powershell
$env:PYTHONPATH="src"
python -m trading_phantom.main --debug --iterations 1
```

## Configuración

Edita `src/trading_phantom/config/config.yaml`:
- `symbol`: Par a operar (ej. `EURUSD`)
- `timeframe`: `M1`, `M5`, `M15`, `H1`, `H4`, `D1`
- `risk`: Porcentaje por trade, lote fijo, pérdida diaria máxima
- `orders`: SL/TP en pips, desviación

## Troubleshooting rápido

| Problema | Solución |
|----------|----------|
| `No module named 'flask'` | Asegúrate que el venv está activo y pip install corrió sin errores |
| MT5 no se conecta | Abre MT5, inicia sesión, espera unos segundos, intenta de nuevo |
| Puerto 5000 en uso | Cambia `port` en launcher.py (línea ~60) o detén otro proceso: `Get-Process -Name python \| Stop-Process` |
| `ruff check` falla | Ejecuta `ruff check --fix .` para auto-corregir |

## Siguientes pasos

1. Lee [docs/README.md](../docs/README.md) para guía completa
2. Revisa [docs/API.md](../docs/API.md) para endpoints
3. Echa un vistazo a [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md) para entender el diseño
4. Para contribuir, ve a [CONTRIBUTING.md](../CONTRIBUTING.md)

## Soporte

- Issues: https://github.com/<owner>/Trading-Phantom/issues
- Discussions: https://github.com/<owner>/Trading-Phantom/discussions

---

¡Listo! Ya puedes empezar a explorar Trading Phantom. 🚀
