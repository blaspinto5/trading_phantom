<p align="center">
  <img src="https://img.shields.io/badge/Trading-Phantom-blueviolet?style=for-the-badge&logo=python&logoColor=white" alt="Trading Phantom"/>
</p>

<h1 align="center">🤖 Trading Phantom</h1>

<p align="center">
  <strong>Framework Profesional de Trading Algorítmico para MetaTrader 5</strong>
</p>

<p align="center">
  <a href="#-qué-es-trading-phantom">¿Qué es?</a> •
  <a href="#-inicio-rápido-5-minutos">Inicio Rápido</a> •
  <a href="#-cómo-funciona">Cómo Funciona</a> •
  <a href="#-guía-completa-de-ejecución">Guía de Ejecución</a> •
  <a href="#-estrategia-de-trading">Estrategia</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/MetaTrader-5-orange?style=flat-square" alt="MT5"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License"/>
  <img src="https://img.shields.io/badge/Tests-11%20passed-success?style=flat-square" alt="Tests"/>
</p>

---

# 📖 Tabla de Contenidos

1. [¿Qué es Trading Phantom?](#-qué-es-trading-phantom)
2. [Inicio Rápido (5 minutos)](#-inicio-rápido-5-minutos)
3. [Requisitos del Sistema](#-requisitos-del-sistema)
4. [Instalación Paso a Paso](#-instalación-paso-a-paso)
5. [Guía Completa de Ejecución](#-guía-completa-de-ejecución)
6. [Cómo Funciona la Estrategia](#-estrategia-de-trading)
7. [Gestión de Riesgo](#-gestión-de-riesgo)
8. [Backtesting](#-backtesting)
9. [Machine Learning (Opcional)](#-machine-learning-opcional)
10. [Estructura del Proyecto](#-estructura-del-proyecto)
11. [Solución de Problemas](#-solución-de-problemas)
12. [Preguntas Frecuentes](#-preguntas-frecuentes)

---

# 🎯 ¿Qué es Trading Phantom?

**Trading Phantom** es un **robot de trading automático** (también llamado "bot" o "EA") que opera en el mercado de divisas (Forex) a través de la plataforma **MetaTrader 5**.

## ¿Qué hace exactamente?

```
📊 MERCADO FOREX                    🤖 TRADING PHANTOM                    📈 TU CUENTA MT5

  EURUSD = 1.0850                      1. Analiza precios                     Ejecuta BUY
  GBPUSD = 1.2650          ────────►   2. Detecta señales        ────────►   0.01 lotes
  USDJPY = 149.50                      3. Calcula riesgo                      SL: 25 pips
                                       4. Decide: BUY/SELL/HOLD               TP: 50 pips
```

### En palabras simples:

1. **Recibe datos** del mercado en tiempo real (precios de EURUSD, GBPUSD, etc.)
2. **Analiza** usando indicadores técnicos (como un trader profesional)
3. **Toma decisiones**: Comprar (BUY), Vender (SELL), o Esperar (HOLD)
4. **Gestiona el riesgo**: Nunca arriesga más del 1% de tu cuenta por operación
5. **Ejecuta órdenes** automáticamente en tu cuenta de MetaTrader 5

---

# ⚡ Inicio Rápido (5 minutos)

> **Para quienes quieren empezar YA** - Sigue estos 5 pasos y tendrás el bot corriendo.

## Paso 1: Descargar el Código

```powershell
# Abrir PowerShell y ejecutar:
git clone https://github.com/blaspinto5/trading_phantom.git
cd trading_phantom
```

## Paso 2: Crear Entorno Virtual

```powershell
# Crear entorno aislado de Python
python -m venv .venv

# Activar el entorno (IMPORTANTE: hacer esto siempre antes de trabajar)
.\.venv\Scripts\Activate.ps1
```

> 💡 **¿Qué es un entorno virtual?** Es una "caja" aislada donde instalamos las librerías del proyecto sin afectar otros proyectos de Python en tu computadora.

## Paso 3: Instalar Dependencias

```powershell
# Instalar todas las librerías necesarias
pip install -r requirements.txt
```

## Paso 4: Configurar MetaTrader 5

1. Abre **MetaTrader 5** en tu computadora
2. Ve a `Herramientas → Opciones → Expert Advisors`
3. Marca la casilla **"Permitir trading algorítmico"**
4. Haz clic en **Aceptar**

## Paso 5: Ejecutar el Bot

```powershell
# Ejecutar el bot de trading
python bot/start_bot.py
```

✅ **¡Listo!** El bot está corriendo y analizando el mercado.

---

# 💻 Requisitos del Sistema

## Software Necesario

| Software | Versión | ¿Para qué? | Descarga |
|----------|---------|------------|----------|
| **Python** | 3.10+ | Ejecutar el código | [python.org](https://www.python.org/downloads/) |
| **MetaTrader 5** | Última | Conectar con el broker | [metatrader5.com](https://www.metatrader5.com/es/download) |
| **Git** | Cualquiera | Descargar el código | [git-scm.com](https://git-scm.com/download/win) |

## Sistema Operativo

- ✅ **Windows 10/11** (Recomendado - MT5 solo funciona en Windows)
- ⚠️ Linux/Mac: Requiere Wine o máquina virtual

## Hardware Mínimo

- **RAM**: 4 GB (8 GB recomendado)
- **Almacenamiento**: 500 MB libres
- **Internet**: Conexión estable

---

# 📦 Instalación Paso a Paso

Esta guía está diseñada para **principiantes absolutos**. Sigue cada paso exactamente.

## 1️⃣ Instalar Python

### ¿Ya tienes Python?
```powershell
# Verificar en PowerShell:
python --version
# Debe mostrar: Python 3.10.x o superior
```

### Si no tienes Python:
1. Ve a [python.org/downloads](https://www.python.org/downloads/)
2. Descarga Python 3.10 o superior
3. **¡IMPORTANTE!** Durante la instalación, marca la casilla:
   - ✅ "Add Python to PATH"
4. Haz clic en "Install Now"

## 2️⃣ Instalar Git

### ¿Ya tienes Git?
```powershell
# Verificar en PowerShell:
git --version
# Debe mostrar: git version 2.x.x
```

### Si no tienes Git:
1. Ve a [git-scm.com](https://git-scm.com/download/win)
2. Descarga e instala con opciones por defecto

## 3️⃣ Descargar Trading Phantom

```powershell
# Abrir PowerShell (buscar "PowerShell" en el menú inicio)

# Ir a tu carpeta de proyectos (ejemplo: Escritorio)
cd ~\Desktop

# Clonar el repositorio
git clone https://github.com/blaspinto5/trading_phantom.git

# Entrar a la carpeta del proyecto
cd trading_phantom
```

## 4️⃣ Crear y Activar Entorno Virtual

```powershell
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
.\.venv\Scripts\Activate.ps1
```

> **Nota**: Verás `(.venv)` al inicio de tu línea de comandos. Esto indica que el entorno está activo.

```
(.venv) PS C:\Users\TuUsuario\Desktop\trading_phantom>
```

## 5️⃣ Instalar Dependencias

```powershell
# Instalar dependencias principales
pip install -r requirements.txt

# (Opcional) Para desarrollo/tests:
pip install -r requirements-dev.txt

# (Opcional) Para Machine Learning:
pip install -r requirements-ml.txt
```

## 6️⃣ Configurar MetaTrader 5

### Habilitar Trading Algorítmico:
1. Abre MetaTrader 5
2. Menú: `Herramientas` → `Opciones`
3. Pestaña: `Expert Advisors`
4. Marcar: ✅ "Permitir trading algorítmico"
5. Marcar: ✅ "Permitir importación de DLL"
6. Clic en "Aceptar"

### Iniciar sesión:
1. Asegúrate de estar conectado a tu broker
2. El icono de conexión (esquina inferior derecha) debe estar verde

## 7️⃣ Verificar Instalación

```powershell
# Ejecutar tests para verificar que todo funciona
pytest tests/ -v
```

✅ Si ves "**11 passed**", la instalación fue exitosa.

---

# 🎮 Guía Completa de Ejecución

## Modos de Operación

Trading Phantom puede ejecutarse en 3 modos:

| Modo | Descripción | ¿Para qué? |
|------|-------------|------------|
| **Bot en Vivo** | Opera en tiempo real | Trading real/demo |
| **Backtesting** | Simula con datos históricos | Probar estrategias |
| **Demo/Test** | Sin conexión a MT5 | Desarrollo/debugging |

---

## 🤖 Modo 1: Bot en Vivo

Este modo conecta con MetaTrader 5 y opera en tiempo real.

### Configuración previa

Edita el archivo `config/config.yaml`:

```yaml
# Ajustar según tu preferencia
trading:
  symbol: "EURUSD"        # Par a operar
  timeframe: "H1"         # Temporalidad (H1 = 1 hora)
  lot_size: 0.01          # Tamaño de lote inicial

risk:
  max_risk_percent: 1.0   # Máximo 1% por operación
  max_daily_loss: 3.0     # Parar si pierdes 3% en el día

demo_mode: true           # true = cuenta demo, false = cuenta real
```

### Ejecutar

```powershell
# Asegúrate de que el entorno está activo
.\.venv\Scripts\Activate.ps1

# Ejecutar el bot
python bot/start_bot.py
```

### Salida esperada

```
[2026-02-02 10:00:00] INFO - 🚀 Trading Phantom iniciando...
[2026-02-02 10:00:01] INFO - ✅ Conexión MT5 establecida
[2026-02-02 10:00:01] INFO - 📊 Analizando EURUSD en H1
[2026-02-02 10:00:02] INFO - 📈 Señal: HOLD (sin confirmación triple)
[2026-02-02 10:00:02] INFO - 💤 Esperando próxima vela...
```

### Detener el bot

Presiona `Ctrl + C` en la terminal.

---

## 📊 Modo 2: Backtesting

Prueba la estrategia con datos históricos antes de operar en vivo.

### Ejecutar backtest básico

```powershell
python backtesting/run_backtest.py
```

### Ejecutar backtest con visualización

```powershell
# Genera gráficos de resultados
python backtesting/run_and_visual.py
```

### Backtest paralelo (múltiples símbolos)

```powershell
# Prueba varios pares simultáneamente
python backtesting/run_backtest_parallel.py
```

### Interpretar resultados

```
═══════════════════════════════════════════════════
📊 RESULTADOS DEL BACKTEST
═══════════════════════════════════════════════════
Total trades:        156
Win rate:            58.3%
Profit factor:       1.45
Max drawdown:        -8.2%
Sharpe ratio:        1.23
Return:              +12.5%
═══════════════════════════════════════════════════
```

| Métrica | Significado | Valor Ideal |
|---------|-------------|-------------|
| **Win Rate** | % de operaciones ganadoras | > 50% |
| **Profit Factor** | Ganancias / Pérdidas | > 1.3 |
| **Max Drawdown** | Peor racha de pérdidas | < 15% |
| **Sharpe Ratio** | Retorno ajustado por riesgo | > 1.0 |

---

## 🧪 Modo 3: Tests y Desarrollo

Para verificar que todo funciona correctamente.

### Ejecutar todos los tests

```powershell
pytest tests/ -v
```

### Ejecutar tests específicos

```powershell
# Solo tests de estrategia
pytest tests/test_strategy.py -v

# Solo tests de conexión MT5
pytest tests/test_mt5_connector.py -v
```

### Verificar calidad del código

```powershell
# Linting (errores de estilo)
ruff check modules/ config/

# Formateo
black modules/ --check
```

---

# 📈 Estrategia de Trading

## Triple Confirmación

Trading Phantom usa una estrategia conservadora que requiere **3 señales alineadas** antes de operar:

```
    ┌─────────────────────────────────────────────────────────────┐
    │                   ESTRATEGIA TRIPLE CONFIRMACIÓN            │
    └─────────────────────────────────────────────────────────────┘

    SEÑAL DE COMPRA (BUY):
    ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
    │   📈 EMA    │ + │   📊 MACD   │ + │   📉 RSI    │ = BUY ✅
    │ Fast > Slow │   │ Cruce Arriba│   │   > 45      │
    └─────────────┘   └─────────────┘   └─────────────┘

    SEÑAL DE VENTA (SELL):
    ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
    │   📈 EMA    │ + │   📊 MACD   │ + │   📉 RSI    │ = SELL ✅
    │ Fast < Slow │   │ Cruce Abajo │   │   < 55      │
    └─────────────┘   └─────────────┘   └─────────────┘

    SI NO SE CUMPLEN LAS 3 → HOLD (No operar)
```

## Indicadores Explicados

### 1. EMA (Exponential Moving Average)

**¿Qué es?** Un promedio de precios que da más peso a los datos recientes.

**Parámetros:**
- EMA Rápida: 8 períodos
- EMA Lenta: 21 períodos

**Señal:**
- EMA 8 cruza **arriba** de EMA 21 → Tendencia alcista 📈
- EMA 8 cruza **abajo** de EMA 21 → Tendencia bajista 📉

### 2. MACD (Moving Average Convergence Divergence)

**¿Qué es?** Mide la fuerza y dirección de la tendencia.

**Parámetros:**
- Línea MACD: EMA(12) - EMA(26)
- Línea de Señal: EMA(9) del MACD

**Señal:**
- MACD cruza **arriba** de Señal → Impulso alcista 📈
- MACD cruza **abajo** de Señal → Impulso bajista 📉

### 3. RSI (Relative Strength Index)

**¿Qué es?** Mide si el precio está "sobrecomprado" o "sobrevendido" (escala 0-100).

**Parámetros:**
- Período: 14
- Umbral de compra: RSI > 45
- Umbral de venta: RSI < 55

**Señal:**
- RSI > 70 → Sobrecomprado (posible caída)
- RSI < 30 → Sobrevendido (posible subida)

## ¿Por qué Triple Confirmación?

| Estrategia Simple | Triple Confirmación |
|------------------|---------------------|
| 1 indicador | 3 indicadores |
| Muchas señales falsas | Menos señales, más precisas |
| Win rate ~45% | Win rate ~58% |
| Drawdown alto | Drawdown controlado |

---

# 🛡️ Gestión de Riesgo

El módulo de riesgo es **la parte más importante** del bot. Protege tu capital.

## Reglas de Riesgo

```yaml
# config/config.yaml

risk:
  # REGLA 1: Máximo 1% del balance por operación
  max_risk_percent: 1.0

  # REGLA 2: Máximo 3 operaciones abiertas simultáneamente
  max_positions: 3

  # REGLA 3: Si pierdes 3% en el día, el bot se detiene
  max_daily_loss_percent: 3.0

  # REGLA 4: Drawdown máximo antes de parar todo
  max_drawdown_percent: 10.0

orders:
  # Stop Loss: 25 pips (protección de pérdidas)
  stop_loss_pips: 25

  # Take Profit: 50 pips (objetivo de ganancia)
  take_profit_pips: 50

  # Ratio Riesgo/Recompensa: 1:2 (ganamos el doble de lo que arriesgamos)
```

## Cálculo de Tamaño de Posición

```
Ejemplo con balance de $10,000:

Balance:           $10,000
Riesgo máximo:     1% = $100
Stop Loss:         25 pips

Cálculo:
$100 / 25 pips = $4 por pip
$4 / $10 (valor pip mini lote) = 0.4 lotes

→ Tamaño de posición: 0.04 lotes
```

## Circuit Breaker (Protección Diaria)

```
           Balance Inicial: $10,000
                    │
    ┌───────────────┼───────────────┐
    │               │               │
   -1%             -2%             -3%
 ($9,900)        ($9,800)        ($9,700)
    │               │               │
 Continúa       Continúa         ⛔ STOP
                               Bot se detiene
                            hasta el día siguiente
```

---

# 🧪 Backtesting

## ¿Qué es Backtesting?

Es probar tu estrategia con **datos históricos** para ver cómo habría funcionado en el pasado.

```
              DATOS HISTÓRICOS                    SIMULACIÓN
    ┌───────────────────────────────┐    ┌─────────────────────────┐
    │ 2024-01-01: EURUSD = 1.1050   │    │ Señal: BUY              │
    │ 2024-01-02: EURUSD = 1.1080   │───►│ Resultado: +30 pips     │
    │ 2024-01-03: EURUSD = 1.1020   │    │ Win Rate: 58%           │
    │ ...                           │    │ Profit: +$1,250         │
    └───────────────────────────────┘    └─────────────────────────┘
```

## Ejecutar Backtesting

### Opción 1: Backtest Simple

```powershell
python backtesting/run_backtest.py
```

### Opción 2: Backtest con Gráficos

```powershell
python backtesting/run_and_visual.py
```

Genera un archivo HTML con gráficos interactivos.

### Opción 3: Backtest Paralelo (Múltiples Pares)

```powershell
python backtesting/run_backtest_parallel.py
```

Prueba EURUSD, GBPUSD, USDJPY, etc. simultáneamente.

## Archivos de Resultados

Los resultados se guardan en `backtesting/resultados/`:

```
backtesting/resultados/
├── backtest_results.json         # Datos crudos
├── backtest_results_advanced.json
└── equity_curve.html             # Gráfico de equidad
```

---

# 🤖 Machine Learning (Opcional)

Trading Phantom puede usar modelos de ML para mejorar las señales.

## ¿Cómo funciona?

```
Señal Técnica:  BUY (Triple Confirmación)
        │
        ▼
┌─────────────────────────────────┐
│   MODELO ML (Random Forest)    │
│   Confianza: 72%               │
│   Umbral: 65%                  │
│   72% > 65% ✅                 │
└─────────────────────────────────┘
        │
        ▼
Señal Final: BUY (confirmada por ML)
```

## Entrenar Modelo

```powershell
# Entrenar modelo básico
python scripts/ml_train.py

# Entrenar modelo avanzado con cross-validation
python scripts/ml_train_advanced.py
```

## Configurar ML

```yaml
# config/config.yaml

ml:
  enabled: true                    # Activar ML
  model_path: "src/data/models/"   # Donde guardar modelos
  confidence_threshold: 0.65       # Mínimo 65% de confianza
```

---

# 📁 Estructura del Proyecto

```
trading_phantom/
│
├── 📂 bot/                      # Bot de trading en vivo
│   ├── start_bot.py             # ← EJECUTAR ESTO para trading
│   └── bot_monitor.py           # Monitoreo del bot
│
├── 📂 modules/                  # Módulos principales
│   ├── strategy.py              # Estrategia de trading
│   ├── risk_manager.py          # Gestión de riesgo
│   ├── trader.py                # Ejecución de órdenes
│   └── data_loader.py           # Carga de datos
│
├── 📂 config/                   # Configuración
│   ├── config.yaml              # ← EDITAR ESTO para personalizar
│   └── config_loader.py         # Cargador de configuración
│
├── 📂 backtesting/              # Sistema de backtesting
│   ├── run_backtest.py          # ← Backtest simple
│   ├── run_and_visual.py        # ← Backtest con gráficos
│   └── metrics.py               # Métricas de performance
│
├── 📂 mt5/                      # Conexión con MetaTrader 5
│   └── connector.py             # API de MT5
│
├── 📂 scripts/                  # Scripts útiles
│   ├── ml_train.py              # Entrenar ML
│   └── ml_train_advanced.py     # ML avanzado
│
├── 📂 tests/                    # Tests automatizados
│   ├── test_strategy.py
│   └── test_risk_manager.py
│
├── 📂 src/trading_phantom/      # Paquete principal (desarrollo)
│
├── 📄 requirements.txt          # Dependencias principales
├── 📄 requirements-dev.txt      # Dependencias de desarrollo
├── 📄 requirements-ml.txt       # Dependencias de ML
├── 📄 config.yaml               # Configuración principal
└── 📄 README.md                 # Este archivo
```

---

# 🔧 Solución de Problemas

## Error: "ModuleNotFoundError: No module named 'MetaTrader5'"

**Causa:** La librería MT5 no está instalada.

**Solución:**
```powershell
pip install MetaTrader5
```

## Error: "MT5 initialize failed"

**Causa:** MetaTrader 5 no está abierto o no está conectado.

**Solución:**
1. Abre MetaTrader 5
2. Inicia sesión en tu cuenta
3. Verifica que el icono de conexión esté verde
4. Vuelve a ejecutar el bot

## Error: "Trading is not allowed"

**Causa:** El trading algorítmico no está habilitado en MT5.

**Solución:**
1. En MT5: `Herramientas → Opciones → Expert Advisors`
2. Marca: ✅ "Permitir trading algorítmico"
3. Clic en "Aceptar"

## Error: "Symbol EURUSD not found"

**Causa:** El símbolo no está disponible en tu broker.

**Solución:**
1. Verifica que el símbolo exista en tu broker
2. Algunos brokers usan "EURUSDm" o "EURUSD.raw"
3. Edita `config/config.yaml` con el nombre correcto

## El bot no genera señales

**Causa:** La estrategia requiere Triple Confirmación.

**Solución:**
- Esto es normal. El bot solo opera cuando las 3 condiciones se cumplen.
- En mercados laterales, puede haber pocas señales.
- Verifica los logs para ver el estado de cada indicador.

---

# ❓ Preguntas Frecuentes

## ¿Puedo usar esto en cuenta real?

Sí, pero **primero prueba en cuenta demo** durante al menos 1-3 meses. El trading conlleva riesgo de pérdida de capital.

## ¿Cuánto dinero necesito para empezar?

- **Mínimo recomendado:** $500-1000 en cuenta demo
- **Para cuenta real:** Depende de tu broker (algunos permiten desde $100)

## ¿Funciona en otros mercados (acciones, crypto)?

Actualmente está optimizado para Forex. Puede adaptarse a otros mercados, pero requiere modificaciones en la estrategia.

## ¿Cuántas operaciones hace por día?

Con la estrategia Triple Confirmación en H1:
- **Promedio:** 1-3 operaciones por día
- **En mercados laterales:** 0 operaciones
- **En tendencias fuertes:** Hasta 5 operaciones

## ¿Es legal usar bots de trading?

Sí, el trading algorítmico es completamente legal. La mayoría de brokers lo permiten.

## ¿Garantiza ganancias?

**NO.** Ningún sistema de trading garantiza ganancias. El trading siempre conlleva riesgo. Este bot implementa gestión de riesgo profesional, pero las pérdidas son posibles.

---

# 📞 Soporte y Comunidad

- **Issues:** [GitHub Issues](https://github.com/blaspinto5/trading_phantom/issues)
- **Documentación:** Carpeta `/docs` del proyecto

---

# 📜 Licencia

Este proyecto está bajo la licencia **MIT**. Ver [LICENSE](LICENSE) para más detalles.

---

<p align="center">
  <strong>Trading Phantom</strong> - Framework Profesional de Trading Algorítmico
</p>

<p align="center">
  ⚠️ <em>El trading conlleva riesgos significativos. Opera solo con dinero que puedas permitirte perder.</em>
</p>
