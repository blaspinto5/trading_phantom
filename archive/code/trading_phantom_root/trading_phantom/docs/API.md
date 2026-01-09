# API Reference

Documentación completa de todos los endpoints REST de Trading Phantom.

## Base URL

```
http://127.0.0.1:5000
```

## Autenticación

Actualmente sin autenticación. Recomendado: agregar en futuras versiones.

## Endpoints

### GET /

Retorna la UI principal en HTML.

**Response:**
- `200 OK`: HTML page
- Content-Type: `text/html; charset=utf-8`

---

### POST /api/bot/start

Arranca el bot en un subprocess.

**Request Body:**
```json
{
  "debug": false,
  "iterations": null
}
```

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `debug` | bool | No | Enable debug logging (default: false) |
| `iterations` | int | No | Run N iterations and exit (default: null = infinite) |

**Response (200 OK):**
```json
{
  "status": "started",
  "pid": 12345
}
```

**Response si ya está corriendo (200 OK):**
```json
{
  "status": "already_running",
  "pid": 12345
}
```

**Response en error (500):**
```json
{
  "status": "error",
  "error": "Failed to start bot subprocess"
}
```

**Ejemplo (PowerShell):**
```powershell
$payload = @{ debug = $true; iterations = 10 }
$body = $payload | ConvertTo-Json -Depth 5
$response = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/bot/start" `
  -Method Post `
  -Body $body `
  -ContentType 'application/json'
$response | ConvertTo-Json
```

**Ejemplo (Python):**
```python
import requests
response = requests.post(
    'http://127.0.0.1:5000/api/bot/start',
    json={'debug': True, 'iterations': 1}
)
print(response.json())
```

---

### POST /api/bot/stop

Detiene el bot (envía SIGTERM).

**Request Body:** Vacío

**Response (200 OK):**
```json
{
  "status": "stopped",
  "pid": 12345
}
```

**Response si no está corriendo (200 OK):**
```json
{
  "status": "not_running"
}
```

**Ejemplo:**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/bot/stop" -Method Post
```

---

### GET /api/bot/status

Obtiene el estado actual del bot.

**Response (200 OK, en ejecución):**
```json
{
  "running": true,
  "pid": 12345
}
```

**Response (200 OK, detenido):**
```json
{
  "running": false
}
```

**Ejemplo:**
```powershell
$status = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/bot/status"
$status
```

---

### GET /api/logs

Obtiene los logs del bot.

**Query Parameters:**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `lines` | int | Número de líneas a retornar (default: 200) |
| `bot` | bool/str | Si `true`, retorna logs del bot específicamente (default: false) |
| `file` | str | Nombre específico del archivo de log (opcional) |

**Response (200 OK):**
```json
{
  "logs": "🚀 Iniciando Trading Phantom\n✅ Conectado a MetaTrader 5\n..."
}
```

**Response si no hay logs (200 OK):**
```json
{
  "logs": ""
}
```

**Ejemplos:**

```powershell
# Últimas 200 líneas del log del bot
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/logs?bot=true&lines=200"

# Últimas 50 líneas del log más reciente
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/logs?lines=50"
```

---

### POST /api/analytics/ingest_trade

Persiste un trade/operación en la base de datos.

**Request Body:**
```json
{
  "symbol": "EURUSD-T",
  "side": "BUY",
  "entry_price": 1.1205,
  "exit_price": 1.1235,
  "pnl": 30.0,
  "opened_at": "2025-12-01T10:00:00Z",
  "closed_at": "2025-12-01T12:00:00Z"
}
```

**Response (200 OK):**
```json
{ "status": "ok" }
```

---

### POST /api/analytics/ml/train

Entrena el modelo ML (RandomForest) usando el dataset persistido.

**Request Body:** Vacío

**Response (200 OK):**
```json
{ "status": "trained", "n_samples": 1234 }
```

---

### POST /api/analytics/ml/predict

Predice la señal (`BUY`/`SELL`/`HOLD`) a partir de features actuales.

**Request Body:**
```json
{ "close": 1.1234, "sma": 1.1200, "rsi": 55, "prev_close": 1.1210 }
```

**Response (200 OK):**
```json
{ "signal": "BUY", "prob": 0.72 }
```

---

### GET /api/analytics/export/trades

Exporta el dataset de trades.

**Query Parameters:**
- `format`: `json` (default), `csv`, `parquet` (requiere `pyarrow`).

**Response (200 OK, json):**
```json
{ "format": "json", "data": [ { "symbol": "EURUSD-T", "side": "BUY", "pnl": 30.0, ... } ] }
```

**Response (200 OK, csv):** Content-Type `text/csv`, attachment `trades.csv`.

**Response (200 OK, parquet):** Content-Type `application/octet-stream`, attachment `trades.parquet`.

---

### GET /api/analytics/export/backtests

Exporta el dataset de backtests.

**Query Parameters:**
- `format`: `json` (default), `csv`, `parquet` (requiere `pyarrow`).

**Response (200 OK, json):**
```json
{ "format": "json", "data": [ { "symbol": "EURUSD-T", "winrate": 60.0, ... } ] }
```

**Response (200 OK, csv):** Content-Type `text/csv`, attachment `backtests.csv`.

**Response (200 OK, parquet):** Content-Type `application/octet-stream`, attachment `backtests.parquet`.

### POST /api/backtest

Lanza un backtest en background.

**Request Body:**
```json
{
  "symbol": "EURUSD-T",
  "timeframe": "H1",
  "bars": 1000,
  "sma_period": 50,
  "rsi_period": 14
}
```

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `symbol` | str | No | Símbolo a testear (default: "EURUSD-T") |
| `timeframe` | str | No | Timeframe (default: "H1") |
| `bars` | int | No | Número de velas (default: 1000) |
| `sma_period` | int | No | Período de SMA (default: 50) |
| `rsi_period` | int | No | Período de RSI (default: 14) |

**Response (200 OK):**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Ejemplo:**
```powershell
$payload = @{
  symbol = "EURUSD-T"
  bars = 500
  sma_period = 20
  rsi_period = 14
}
$response = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/backtest" `
  -Method Post `
  -Body ($payload | ConvertTo-Json) `
  -ContentType 'application/json'
Write-Host "Job ID: $($response.job_id)"
```

---

### GET /api/backtest/<job_id>

Obtiene el estado y resultado de un backtest.

**Path Parameters:**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `job_id` | str | UUID del job retornado por `/api/backtest` |

**Response (200 OK, en progreso):**
```json
{
  "status": "running",
  "result": null
}
```

**Response (200 OK, completado):**
```json
{
  "status": "done",
  "result": {
    "metrics": {
      "Total trades": 25,
      "Ganadoras": 15,
      "Perdedoras": 10,
      "Winrate (%)": 60.0,
      "PnL Total": 150.5,
      "PnL Promedio": 6.02,
      "Mejor trade": 45.3,
      "Peor trade": -25.1
    },
    "visual_results": {
      "Equity Final [$]": 10150.5,
      "Return [%]": 1.51,
      "Buy & Hold Return [%]": 0.5,
      "Return (Ann.) [%]": 19.5,
      "Volatility (Ann.) [%]": 15.2,
      "Sharpe Ratio": 1.28,
      "Max. Drawdown [%]": 8.5,
      "Avg. Drawdown [%]": 2.1
    }
  }
}
```

**Response (200 OK, error):**
```json
{
  "status": "error",
  "result": {
    "error": "No se pudieron obtener datos para EURUSD"
  }
}
```

**Response (404, job no existe):**
```json
{
  "error": "job not found"
}
```

**Ejemplo de polling:**
```powershell
$jobId = "550e8400-e29b-41d4-a716-446655440000"
while ($true) {
  $result = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/backtest/$jobId"
  if ($result.status -eq "done" -or $result.status -eq "error") {
    Write-Host "Resultado final:"
    $result.result | ConvertTo-Json | Write-Host
    break
  }
  Write-Host "Estado: $($result.status)... Esperando..."
  Start-Sleep -Seconds 2
}
```

---

## Error Handling

Todos los errores retornan con status code apropiado y un JSON con detalle:

```json
{
  "error": "Descripción del error"
}
```

Códigos HTTP comunes:
- `200 OK`: Operación exitosa
- `400 Bad Request`: Parámetro inválido
- `404 Not Found`: Recurso no encontrado
- `500 Internal Server Error`: Error del servidor

---

## Rate Limiting

Actualmente sin límite de velocidad. Recomendado agregar en futuras versiones:

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)
limiter.limit("100 per hour")(start_backtest)
```

---

## Autenticación (Futuro)

Planeado para v1.0.0+:

```python
from functools import wraps
def require_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not verify_token(token):
            return {'error': 'Unauthorized'}, 401
        return f(*args, **kwargs)
    return decorated

@app.route('/api/bot/start', methods=['POST'])
@require_token
def bot_start():
    ...
```

---

## Ejemplos de flujo completo

### 1. Iniciar bot, obtener logs, detener

```powershell
# Iniciar bot con 5 iteraciones y debug
$start = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/bot/start" `
  -Method Post `
  -Body (@{ iterations = 5; debug = $true } | ConvertTo-Json) `
  -ContentType 'application/json'
Write-Host "Bot started: PID $($start.pid)"

# Esperar un poco
Start-Sleep -Seconds 2

# Obtener logs
$logs = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/logs?bot=true&lines=50"
Write-Host "Logs:`n$($logs.logs)"

# Detener bot
$stop = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/bot/stop" -Method Post
Write-Host "Bot stopped"
```

### 2. Ejecutar backtest y esperar resultado

```powershell
# Lanzar backtest
$bt = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/backtest" `
  -Method Post `
  -Body (@{
    symbol = "EURUSD-T"
    bars = 1000
    sma_period = 50
    rsi_period = 14
  } | ConvertTo-Json) `
  -ContentType 'application/json'

$jobId = $bt.job_id
Write-Host "Backtest started: Job ID $jobId"

# Poll hasta completarse
$maxWait = 0
while ($maxWait -lt 60) {
  $status = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/backtest/$jobId"
  if ($status.status -eq "done") {
    Write-Host "Metrics:"
    $status.result.metrics | ConvertTo-Json | Write-Host
    break
  } elseif ($status.status -eq "error") {
    Write-Host "Backtest error: $($status.result.error)"
    break
  }
  Write-Host "Status: $($status.status)..."
  Start-Sleep -Seconds 2
  $maxWait += 2
}
```

---

## Notas

- Los logs se guardan en `logs/bot.log` (relativo a la raíz del proyecto)
- Los backtests en error retienen información en `result.error`
- Los jobs de backtest se almacenan en memoria; no persisten entre reinicios de la app
- Si `DATABASE_URL` está configurado, la analítica usa Postgres; de lo contrario, SQLite local.
- Los endpoints de analítica requieren `ENABLE_ANALYTICS=1`.

---

Para desarrollo y contribuciones, ver [CONTRIBUTING.md](../CONTRIBUTING.md).
