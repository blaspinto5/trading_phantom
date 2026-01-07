# Arquitectura de Trading Phantom

Este documento describe el diseño, componentes y flujos principales del sistema.

## Índice
- [Visión general](#visión-general)
- [Componentes principales](#componentes-principales)
- [Flujo de datos](#flujo-de-datos)
- [Patrones de diseño](#patrones-de-diseño)
- [Decisiones arquitectónicas](#decisiones-arquitectónicas)

## Visión general

Trading Phantom es un bot de trading algorítmico modular con:
- **Estrategia pluggable**: Señales SMA+RSI (extensible)
- **Gestión de riesgo centralizada**: Cálculo automático de lotes, SL/TP
- **Interfaz dual**: API REST (Flask) + UI nativa (pywebview)
- **Backtesting integrado**: Simulador y adapter visual
- **Empaquetado desktop**: PyInstaller para .exe autónomo

## Componentes principales

### 1. Core

**`core/orchestrator.py`**: Loop principal del bot
- Conecta a MT5
- Obtiene precios y velas cada `loop_interval_seconds`
- Genera señales de estrategia
- Delega ejecución a `Trader`
- Maneja ciclo de vida (connect → loop → shutdown)

```python
# Inicialización
config = load_config()
strategy = Strategy(symbol, timeframe, mt5_conn)
risk_manager = RiskManager(config, mt5_conn)
trader = Trader(mt5_conn, risk_manager)

# Loop
while iterations not reached:
    price = mt5_conn.get_price(symbol)
    rates = mt5_conn.get_rates(symbol, timeframe, 1)
    
    if new_candle:
        signal = strategy.generate_signal()
        if signal != "HOLD":
            trader.execute(signal, price)
    
    sleep(loop_interval)
```

### 2. Modules

**`modules/strategy.py`**: Generación de señales
- RSI > 50 + close > SMA + close > prev_close → **BUY**
- RSI < 50 + close < SMA + close < prev_close → **SELL**
- Inyectable `data_provider` para backtesting offline
- Extensible para agregar indicadores

**`modules/risk_manager.py`**: Validación y cálculo de riesgo
- Valida: HOLD, MAX_POSITIONS, MAX_DAILY_LOSS, SL/TP, LOT
- Calcula lote: risk_per_trade % de balance / (SL_pips * pip_value)
- SL/TP: respeta stop level del broker

**`modules/trader.py`**: Ejecución de órdenes
- Pending orders (BUY_LIMIT, SELL_LIMIT)
- Verifica riesgo antes de ejecutar
- Actualiza pérdida diaria tras cada operación

**`modules/data_loader.py`**: Normalización de datos
- MT5 raw → pandas DataFrame
- Columnas estándar: Date, Open, High, Low, Close, Volume

### 3. MT5

**`mt5/connector.py`**: Wrapper de MetaTrader5
- Conexión con retry/backoff exponencial
- Resolución de símbolos (ej. "EURUSD" → "EURUSD-T")
- Obtención de rates y precios
- Ejecución de pending orders

Flujo:
```
initialize() → symbol_select() → symbol_info_tick() / copy_rates_from_pos()
```

### 4. Config

**`config/config_loader.py`**: Carga YAML desde `config/config.yaml`
- Parámetros de trading, riesgo, loops
- Fácil override sin código

### 5. Backtest

**`backtest/simulation.py`**: Simulador numérico
- Itera velas simulando entradas/salidas
- Calcula PnL por trade
- Output: lista de trades cerrados

**`backtest/visual_backtest.py`**: Adapter visual
- `StrategyAdapter`: implementa `Strategy` de `backtesting` lib
- Inyecta estrategia core en el framework
- Output: estadísticas, gráficos (opcional)

**`backtest/metrics.py`**: Métricas
- Trades: total, ganadoras, perdedoras
- Winrate, PnL total/promedio, mejor/peor trade

### 6. Web

**`webapp.py`**: Servidor Flask
- `POST /api/bot/start`: Arranca bot en subprocess con `python -m trading_phantom.main`
- `POST /api/bot/stop`: Termina el subprocess
- `GET /api/bot/status`: Estado del proceso
- `POST /api/backtest`: Lanza backtest en background (thread)
- `GET /api/backtest/<job_id>`: Status/resultado
- `GET /api/logs`: Lee logs del archivo

## Flujo de datos

### Flujo de trading en vivo

```
MT5 (tick/vela)
    ↓
get_price() → price dict
get_rates(1) → current_candle
    ↓
check_new_candle() → signal = strategy.generate_signal()
    ↓
risk_manager.check(signal, price) → {allowed, signal, volume, sl, tp}
    ↓
trader.execute() → mt5.send_order()
    ↓
Orden enviada a MT5
```

### Flujo de backtest

```
DataFrame (OHLCV)
    ↓
BacktestSimulator → itera velas
    ↓
strategy.generate_signal() (con data_provider inyectado)
    ↓
Simula entrada/salida
    ↓
trades = [{"type": "BUY", "pnl": X}, ...]
    ↓
metrics = calculate_metrics(trades)
    ↓
output: {"metrics": {...}, "visual_results": {...}}
```

## Patrones de diseño

### 1. Inyección de dependencias

```python
# MT5Connector es inyectado en Strategy y RiskManager
strategy = Strategy(symbol, timeframe, mt5_connector=conn)
risk_manager = RiskManager(config, mt5_connector=conn)

# data_provider es inyectado dinámicamente para backtesting
strategy.data_provider = lambda bars: df
```

### 2. Adapter pattern

`StrategyAdapter` implementa la interfaz de `backtesting.Strategy` pero delega a `trading_phantom.Strategy`.

```python
class StrategyAdapter(BacktestStrategy):
    def next(self):
        signal = self._core_strategy.generate_signal()
        if signal == 'BUY':
            self.buy()
```

### 3. Singleton implícito

MT5 es un singleton implícito (una sola conexión global per proceso).

### 4. Command pattern

`Trader.execute(signal, price)` encapsula la lógica de ejecución de una orden.

## Decisiones arquitectónicas

### 1. Layout `src/`
- **Pro**: Separa código de tests; evita imports accidentales desde raíz
- **Con**: Requiere `PYTHONPATH=src` en CI y desarrollo
- **Alternativa rechazada**: Flat structure (más simple pero más propenso a errores)

### 2. Pending orders vs Market orders
- **Decisión**: Pending orders (BUY_LIMIT, SELL_LIMIT)
- **Razón**: Más control sobre ejecución; permite retrasos sin preocuparse
- **Trade-off**: Menos garantía de ejecución inmediata

### 3. Threading para backtest
- `webapp.py` ejecuta backtest en thread separado para no bloquear la API
- **Pro**: UI responsiva
- **Con**: Requiere thread-safe job store

### 4. Flask + pywebview
- **Pro**: Simpleza; UI web reutilizable; escritorio embebido
- **Con**: Requiere pywebview (solo en dev con GUI)
- **Alternativa para CI**: `plot=False` en backtest visual

### 5. Configuración YAML
- **Pro**: Fácil edición sin código
- **Con**: Menos validación que dataclasses/pydantic
- **Mejora futura**: Migrar a `pydantic` models

## Extensibilidad

### Agregar una nueva estrategia

1. Heredar de `Strategy`
2. Sobrescribir `generate_signal()`
3. Inyectar en `orchestrator.py`

```python
class MyStrategy(Strategy):
    def generate_signal(self) -> str:
        df = self.get_data()
        # tu lógica aquí
        return "BUY", "SELL", o "HOLD"
```

### Agregar un nuevo módulo de riesgo

1. Crear clase que implemente `check()` y `calculate_lot()`
2. Reemplazar en `orchestrator.py`

### Agregar un nuevo endpoint

1. Añadir ruta en `webapp.py`
2. Documentar en `docs/API.md`
3. Añadir tests en `tests/test_*.py`

## Testing

- **Unit tests**: Mockeamos MT5, estrategia pura
- **Integration tests**: Simulador con datos reales
- **E2E tests**: Opcional; requiere MT5 real

## Performance

- Bot loop: ~1s por iteración (ajustable)
- Backtest 1000 velas: ~2s (simulator), ~5s (visual)
- Memory: ~50MB en idle, ~150MB con backtest

## Seguridad

- No almacenar secretos en código
- MT5 credentials en variables de entorno
- Validar inputs en endpoints
- Rate limiting en `/api/backtest` (recomendado)

---

Para más detalles, ver [docs/README.md](README.md) y [docs/API.md](API.md).
