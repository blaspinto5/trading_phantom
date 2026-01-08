╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║            MANUAL DE ORGANIZACIÓN Y PROCEDIMIENTOS OPERATIVOS              ║
║                      Trading Phantom v1.1.0                                ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

================================================================================
📋 ÍNDICE DE CONTENIDOS
================================================================================

1. ESTRUCTURA DE DATOS Y ALMACENAMIENTO
2. PROCEDIMIENTOS OPERATIVOS ESTÁNDAR
3. GUÍA DE OPERACIÓN DIARIA
4. FLUJOS DE NEGOCIO (END-TO-END)
5. MATRIZ DE RESPONSABILIDADES
6. PROTOCOLOS DE MONITOREO
7. PROCEDIMIENTOS DE EMERGENCIA

================================================================================
1. ESTRUCTURA DE DATOS Y ALMACENAMIENTO
================================================================================

1.1 JERARQUÍA DE DATOS
────────────────────────────────────────────────────────────────────────────

RAÍZ: C:\Users\Peruano Pinto\Desktop\PROYECTO 2
│
├─ DATOS EN TIEMPO REAL
│  │
│  ├─ logs/                                  [LOGS ACTIVOS]
│  │  ├─ trading_phantom.log                 [Log principal (rotativo)]
│  │  ├─ trade_history.json                  [Historial trades JSON]
│  │  └─ *.log                               [Logs diarios]
│  │
│  └─ data/                                  [DATOS PERSISTENTES]
│     ├─ trading_phantom.db                  [BASE DE DATOS SQLITE]
│     │  ├─ trades table                     [Operaciones registradas]
│     │  └─ backtest_runs table              [Resultados backtest]
│     │
│     ├─ models/                             [MODELOS ENTRENADOS]
│     │  └─ random_forest.pkl                [Modelo ML serializado]
│     │
│     └─ knowledge_base/                     [TRANSFER LEARNING]
│        ├─ feature_importance.json          [Ranking de features]
│        ├─ feature_embeddings.json          [Estadísticas features]
│        ├─ correlation_matrix.json          [Correlaciones]
│        ├─ decision_patterns.json           [Reglas de decisión]
│        └─ performance_metrics.json         [Métricas modelo]
│
├─ CÓDIGO FUENTE
│  │
│  └─ src/trading_phantom/                   [CÓDIGO PRINCIPAL]
│     ├─ modules/                            [Lógica core]
│     ├─ mt5/                                [Integración broker]
│     ├─ core/                               [Orquestación]
│     ├─ backtest/                           [Simulación]
│     ├─ analytics/                          [ML + datos]
│     ├─ config/                             [Configuración]
│     └─ utils/                              [Utilidades]
│
└─ DOCUMENTACIÓN
   │
   ├─ docs/                                  [Documentación técnica]
   ├─ documentacion/                         [Documentación detallada]
   └─ [*.md en raíz]                         [Documentación corporativa]

1.2 TIPOS DE DATOS Y SUS CICLOS DE VIDA
────────────────────────────────────────────────────────────────────────────

TIPO DE DATO          UBICACIÓN              CICLO DE VIDA
──────────────────────────────────────────────────────────────────────────
Trade data            trading_phantom.db     PERMANENTE (archivable anualmente)
                      trade_history.json     PERMANENTE (backup cada semana)

Log files             logs/*.log             ROTACIÓN: 7 días
                                             ARCHIVADO: 30 días
                                             ELIMINACIÓN: 1 año

Configuration        config/config.yaml     PERMANENTE (con versioning)

Models               models/                 PERMANENTE (reentrenamiento mensual)
                     random_forest.pkl       VERSIONING cada actualización

Knowledge Base       knowledge_base/*        PERMANENTE (actualización con reentrenamiento)

Backtest results     data/backtest_runs     TEMPORAL (30 días) o PERMANENTE si necesario
                     (en BD)

1.3 ESTRUCTURA DE BASE DE DATOS
────────────────────────────────────────────────────────────────────────────

BASE DE DATOS: trading_phantom.db (SQLite)
UBICACIÓN: C:\Users\Peruano Pinto\Desktop\PROYECTO 2\src\data\

TABLA 1: trades
┌─────────────────────────────────────────────────────────────────────────┐
│ COLUMNA          │ TIPO      │ DESCRIPCIÓN                              │
├──────────────────┼───────────┼──────────────────────────────────────────┤
│ id               │ INTEGER   │ ID único (PRIMARY KEY)                  │
│ timestamp        │ DATETIME  │ Cuándo se abrió trade                  │
│ ticket           │ INTEGER   │ ID orden MetaTrader5                   │
│ symbol           │ STRING    │ Símbolo (EURUSD, GBPUSD, etc)          │
│ side             │ STRING    │ BUY o SELL                             │
│ price            │ FLOAT     │ Precio de entrada                      │
│ volume           │ FLOAT     │ Tamaño posición (lotes)                │
│ sl               │ FLOAT     │ Stop loss                              │
│ tp               │ FLOAT     │ Take profit                            │
│ exit_price       │ FLOAT     │ Precio cierre                          │
│ exit_time        │ DATETIME  │ Cuándo se cerró                        │
│ pnl              │ FLOAT     │ Ganancia/pérdida en dinero             │
│ meta             │ JSON      │ Datos adicionales (indicadores, etc)   │
└─────────────────────────────────────────────────────────────────────────┘

TABLA 2: backtest_runs
┌─────────────────────────────────────────────────────────────────────────┐
│ COLUMNA          │ TIPO      │ DESCRIPCIÓN                              │
├──────────────────┼───────────┼──────────────────────────────────────────┤
│ id               │ INTEGER   │ ID único                                │
│ created_at       │ DATETIME  │ Cuándo se ejecutó                      │
│ symbol           │ STRING    │ Símbolo testeado                       │
│ bars             │ INTEGER   │ Número de velas (datos históricos)     │
│ sma_period       │ INTEGER   │ Período SMA usado                      │
│ rsi_period       │ INTEGER   │ Período RSI usado                      │
│ metrics          │ JSON      │ Resultados (Sharpe, DrawDown, etc)     │
│ details          │ JSON      │ Detalles adicionales                   │
└─────────────────────────────────────────────────────────────────────────┘

Crecimiento esperado:
  • 1 trade cada 30 minutos (en operación 24/5) = ~50 trades/día
  • Tamaño BD: <1MB mensual
  • Retención: Permanente

1.4 CONFIGURACIÓN CENTRALIZADA
────────────────────────────────────────────────────────────────────────────

UBICACIÓN: config/config.yaml

Parámetros que DEBEN estar aquí (NUNCA hardcodeados):
  ├─ symbol                [EURUSD]
  ├─ timeframe             [H1]
  ├─ risk.risk_per_trade   [1%]
  ├─ risk.max_daily_loss   [3%]
  ├─ orders.sl_pips        [20]
  ├─ orders.tp_pips        [40]
  ├─ ml.enabled            [true/false]
  ├─ ml.threshold          [0.55]
  └─ logging.level         [INFO/DEBUG]

Cambios en config.yaml toman efecto inmediatamente (sin reiniciar bot).

================================================================================
2. PROCEDIMIENTOS OPERATIVOS ESTÁNDAR
================================================================================

2.1 PROCEDIMIENTO: PREPARAR ENTORNO PARA OPERACIÓN
────────────────────────────────────────────────────────────────────────────

PASO 1: VERIFICACIÓN PREVIA A LA OPERACIÓN
────────────────────────────────────────────
[ ] Revisar AUDITORIA_CORPORATIVA.md (estado del proyecto)
[ ] Verificar config.yaml está correcta
[ ] Confirmar MetaTrader 5 está instalado y activo
[ ] Revisar logs del día anterior: logs/trading_phantom.log
[ ] Verificar saldo y disponibilidad en cuenta MT5

PASO 2: INICIAR ENTORNO VIRTUAL (si es necesario)
────────────────────────────────────────────────────
# PowerShell
cd "C:\Users\Peruano Pinto\Desktop\PROYECTO 2"
.\.venv\Scripts\Activate.ps1

PASO 3: INSTALAR DEPENDENCIAS (primera vez o después de cambios)
────────────────────────────────────────────────────────────────
pip install -r requirements.txt

PASO 4: EJECUTAR BACKTESTING (validación previa)
────────────────────────────────────────────────────
python backtest/run_backtest.py
# Revisar resultados en consola

PASO 5: INICIAR OPERACIÓN
────────────────────────────
# Opción 1: PowerShell
.\RUN.ps1

# Opción 2: Doble-click
RUN.bat

# Opción 3: Terminal directa
python main.py

PASO 6: ACCEDER A DASHBOARD
────────────────────────────
Abre en navegador: http://127.0.0.1:5000
└─ Confirma que el bot está conectado a MT5

2.2 PROCEDIMIENTO: ENTRENAMIENTO DEL MODELO ML
────────────────────────────────────────────────────────────────────────────

FRECUENCIA: Una vez al inicio, luego mensual o cuando haya 50+ trades nuevos

PASO 1: GENERAR DATOS DE ENTRENAMIENTO (primera vez)
──────────────────────────────────────────────────────
python setup_training_data.py

PASO 2: ENTRENAR MODELO
──────────────────────────
python scripts/ml_train.py --save

OUTPUT ESPERADO:
  ✅ Modelo entrenado | accuracy=XX% | muestras=XXX

PASO 3: VERIFICAR MODELO
──────────────────────────
[ ] Revisar accuracy > 55%
[ ] Verificar archivos en: src/data/models/
[ ] Revisar logs: src/data/knowledge_base/

PASO 4: ACTIVAR EN CONFIG (si es necesario)
────────────────────────────────────────────
Editar: config/config.yaml
  ml:
    enabled: true
    threshold: 0.55

2.3 PROCEDIMIENTO: BACKTESTING Y VALIDACIÓN
────────────────────────────────────────────────────────────────────────────

CUANDO: Antes de cambiar parámetros de estrategia

PASO 1: EJECUTAR BACKTEST
─────────────────────────
python backtest/run_backtest.py

PASO 2: REVISAR MÉTRICAS
──────────────────────────
Buscar:
  ├─ Sharpe Ratio > 1.0        [Bueno]
  ├─ Sortino Ratio > 1.5       [Muy bueno]
  ├─ Max Drawdown < 20%        [Aceptable]
  ├─ Win Rate > 45%            [Positivo]
  └─ Profit Factor > 1.2       [Viable]

PASO 3: VALIDAR PARÁMETROS
──────────────────────────
Si métricas son OK:
  [ ] Parámetros listos para operación
Si métricas son MALAS:
  [ ] Ajustar en config.yaml
  [ ] Volver al PASO 1

2.4 PROCEDIMIENTO: MONITOREO DIARIO
────────────────────────────────────────────────────────────────────────────

FRECUENCIA: Al final de cada sesión de operación

PASO 1: REVISAR LOGS
────────────────────
Abrir: logs/trading_phantom.log
Buscar ERRORES (ERROR, EXCEPTION):
  └─ Si hay: revisar causa y documentar

PASO 2: REVISAR TRADES EJECUTADOS
──────────────────────────────────
Abrir: logs/trade_history.json
Contar:
  ├─ Total trades cerrados
  ├─ Ganados vs perdidos
  ├─ Promedio PnL
  └─ Máximo PnL (ganador)
  └─ Mínimo PnL (perdedor)

PASO 3: VERIFICAR ESTADO BD
─────────────────────────────
Usar DB Browser for SQLite:
  └─ Abrir: src/data/trading_phantom.db
  └─ Contar filas tabla 'trades'
  └─ Verificar tamaño archivo

PASO 4: CREAR REPORTE DIARIO (opcional)
───────────────────────────────────────────
Documento: REPORTE_DIARIO_YYYY-MM-DD.md

Contenido:
  # Reporte Diario [FECHA]
  
  ## Estadísticas
  - Operaciones: X
  - Ganadas: X (X%)
  - PnL Total: $XXX
  - Sharpe: X.XX
  
  ## Incidentes
  [Si hubo problemas]
  
  ## Acciones Próximo Día
  [Próximos pasos]

================================================================================
3. GUÍA DE OPERACIÓN DIARIA
================================================================================

3.1 CHECKLIST DE INICIO DE DÍA
────────────────────────────────────────────────────────────────────────────

[ ] ¿MT5 está abierto?
[ ] ¿Conexión a internet está activa?
[ ] ¿config.yaml es el correcto?
[ ] ¿Saldo en cuenta MT5 es suficiente?
[ ] ¿Calendario económico de hoy permite trading?
[ ] ¿Último backup existe? (logs/ y data/)

3.2 HORARIOS DE OPERACIÓN RECOMENDADOS
────────────────────────────────────────────────────────────────────────────

HORARIO RECOMENDADO: 08:00 - 22:00 (14 horas)
  └─ Mayor liquidez en Forex
  └─ Menor spread
  └─ Menos riesgo de gap overnight

HORARIO NO RECOMENDADO: 22:00 - 08:00
  └─ Bajo volumen
  └─ Mayor riesgo en reportes nocturnos
  └─ Posibilidad de gap grande

EVENTOS A EVITAR: 
  ├─ NFP (Non-Farm Payroll) - 1er viernes mes
  ├─ FOMC - cada 6 semanas
  ├─ BCE - mensualmente
  └─ Datos de empleo principales

3.3 GESTIÓN DE POSICIONES ACTIVAS
────────────────────────────────────────────────────────────────────────────

POLÍTICA DE POSICIONES ABIERTAS:

  Máximo por símbolo:       1 posición
  Máximo simultáneas:       3 posiciones
  Duración máxima:          4 horas
  
  Si posición > duración máxima:
    └─ Cerrar manual o automático (según config)

MONITOREO:
  ├─ Cada 15 minutos: revisar en MT5
  ├─ Cada hora: revisar logs
  ├─ Cada 4 horas: revisar PnL acumulado
  └─ Fin de día: resumen de operaciones

3.4 PROCEDIMIENTO DE PARADA SEGURA (SHUTDOWN)
────────────────────────────────────────────────────────────────────────────

PASO 1: CERRAR POSICIONES ABIERTAS
───────────────────────────────────
En MT5:
  [ ] Cerrar manualmente cualquier trade abierto
  [ ] Cancelar órdenes pendientes

PASO 2: PARAR BOT GRACEFULLY
─────────────────────────────
En terminal:
  Ctrl+C
  └─ El bot se detiene ordenadamente

PASO 3: VERIFICAR ESTADO
────────────────────────
[ ] No hay posiciones en MT5
[ ] último log en logs/trading_phantom.log termina con "Shutdown complete"

PASO 4: BACKUP (importante)
──────────────────────────────
Respaldar carpetas:
  ├─ data/
  ├─ logs/
  └─ src/data/

================================================================================
4. FLUJOS DE NEGOCIO (END-TO-END)
================================================================================

4.1 FLUJO: OPERACIÓN COMPLETA (Desde inicio hasta cierre)
─────────────────────────────────────────────────────────────────────────────

START [Bot inicia]
   ↓
[CADA SEGUNDO]
   ├─ Lee últimas 20 velas de MT5 (timeframe H1)
   ├─ Calcula EMA 12, EMA 26, MACD, RSI 14
   ├─ Genera señal: BUY / SELL / HOLD
   └─ Si no hay señal → ESPERA 1 segundo, vuelve a leer
   
   Si señal = BUY y no hay posición:
     ├─ Risk Manager: calcula SL (20 pips abajo), TP (40 pips arriba)
     ├─ Trader: envía orden MARKET a MT5
     ├─ MT5: ejecuta orden
     ├─ Trade History: registra en BD y JSON
     └─ Continúa monitoreando
   
   Mientras posición abierta:
     ├─ Monitorea precio en tiempo real
     ├─ Actualiza logs cada 10 segundos
     └─ Esperando que SL o TP se ejecute
   
   Cuando posición se cierra:
     ├─ Calcula PnL real
     ├─ Registra en BD (exit_price, pnl)
     ├─ Opcional: Envía a Analytics para reentrenamiento
     └─ Espera nueva señal
   
   Si usuario presiona Ctrl+C:
     ├─ Cierra conexión MT5
     ├─ Guarda estado actual
     ├─ Escribe "Shutdown complete" en logs
     └─ Termina programa

RESULTADO FINAL: BD actualizada con trade completo

4.2 FLUJO: BACKTESTING Y VALIDACIÓN
────────────────────────────────────────────────────────────────────────────

START [Usuario ejecuta: python backtest/run_backtest.py]
   ↓
   Obtiene datos históricos (últimas 1000 velas de MT5)
   ↓
   PARA CADA VELA (i=1 a 1000):
     ├─ Ejecuta strategy.generate_signal() con velas 1..i
     ├─ Genera señal: BUY / SELL / HOLD
     ├─ Si hay posición abierta y señal es opuesta:
     │   └─ Cierra posición, calcula PnL
     ├─ Si no hay posición y hay señal:
     │   └─ Abre posición simulada
     └─ Continúa vela siguiente
   ↓
   Calcula métricas sobre todas operaciones:
     ├─ Sharpe Ratio
     ├─ Sortino Ratio
     ├─ Max Drawdown
     ├─ Win Rate
     ├─ Profit Factor
     └─ Otros...
   ↓
   Genera gráficos:
     ├─ Precio + Indicadores (EMA, MACD, RSI)
     ├─ Puntos de entrada/salida
     ├─ Equity curve
     └─ Drawdown chart
   ↓
END [Muestra resultados en consola y gráficos]

RESULTADO: Validación de estrategia (¿es viable?)

4.3 FLUJO: ENTRENAMIENTO DEL MODELO ML
────────────────────────────────────────────────────────────────────────────

START [Usuario ejecuta: python scripts/ml_train.py --save]
   ↓
   Carga todos los trades de BD (tabla 'trades')
   ↓
   ENGINEERING (crea features):
     ├─ side (BUY=1, SELL=-1)
     ├─ price
     ├─ volume
     ├─ abs_pnl
     ├─ pnl_lag1
     ├─ pnl_ma_5 (promedio móvil 5 días)
     └─ pnl_std_5 (desviación estándar 5 días)
   ↓
   Target = pnl > 0 ? (1 si ganador, 0 si perdedor)
   ↓
   Train/test split (80/20):
     ├─ Entrena Random Forest con 80% datos
     └─ Valida con 20% datos
   ↓
   Calcula accuracy, precision, recall, F1-score
   ↓
   Guarda modelo en: src/data/models/random_forest.pkl
   ↓
   Genera Knowledge Base para futuras IAs
   ↓
END [Imprime: "✅ Modelo entrenado | accuracy=60% | muestras=200"]

RESULTADO: Modelo listo para predicciones

================================================================================
5. MATRIZ DE RESPONSABILIDADES (RACI)
================================================================================

TAREA                        RESPONSABLE    APROBADOR   CONSULTOR   INFORMADO
─────────────────────────────────────────────────────────────────────────────
Iniciar bot                  OPERADOR       —           —           —

Revisar logs diarios         OPERADOR       ADMIN       —           —

Entrenar modelo ML           ADMIN          —           CIENTÍFICO  OPERADOR

Cambiar parámetros config    OPERADOR       ADMIN       CIENTÍFICO  —

Parada de emergencia         OPERADOR       —           —           ADMIN

Backup de datos              ADMIN          —           —           OPERADOR

Optimización parámetros      CIENTÍFICO     ADMIN       —           OPERADOR

Mantenimiento BD             ADMIN          —           —           OPERADOR

Actualización código          DESARROLLADOR  ADMIN       —           OPERADOR

Monitoreo de conformidad     ADMIN          —           —           TODAS

ROLES:
  OPERADOR:      Ejecuta bot, monitorea trades, revisa logs
  ADMIN:         Configuración, backups, deuda técnica
  CIENTÍFICO:    Mejora ML, feature engineering, análisis
  DESARROLLADOR: Cambios en código, nuevas features

================================================================================
6. PROTOCOLOS DE MONITOREO
================================================================================

6.1 MÉTRICAS CLAVE DE MONITOREO
─────────────────────────────────────────────────────────────────────────────

MÉTRICA                  META            FRECUENCIA      ACCIÓN SI FALLA
─────────────────────────────────────────────────────────────────────────────
Conexión MT5            ✅ Activa        Cada tick       PARAR BOT inmediatamente
Trades cerrados/día     > 2              Diaria          Revisar estrategia
Win rate                > 45%            Semanal         Reentrenar ML
Sharpe ratio            > 1.0            Semanal         Ajustar parámetros
Max drawdown            < 20%            Semanal         Reducir riesgo
PnL diario              > 0              Diaria          Análisis de causa
Tamaño BD               < 50 MB          Mensual         Archivar y limpiar
Log file size           < 100 MB         Semanal         Rotar logs

6.2 DASHBOARD DE MONITOREO (En desarrollo)
─────────────────────────────────────────────────────────────────────────────

Acceso: http://127.0.0.1:5000/dashboard

Información en tiempo real:
  ├─ Estado conexión MT5          [verde/rojo]
  ├─ Última señal generada        [BUY/SELL/HOLD]
  ├─ Posición abierta actual       [Sí/No]
  ├─ PnL diario acumulado         [$XXX]
  ├─ Trades hoy                   [X]
  ├─ Sharpe ratio últimos 7 días  [X.XX]
  └─ Próximo evento importante    [XXX]

6.3 ALERTAS AUTOMÁTICAS
─────────────────────────────────────────────────────────────────────────────

EVENTO DE ALERTA            ACCIÓN AUTOMÁTICA              NOTIFICACIÓN
───────────────────────────────────────────────────────────────────────────
Desconexión MT5             PAUSAR bot + retry             [LOG] ERROR
Error en generación señal   LOG + continuar               [LOG] WARNING
Posición abierta > 4h       CERRAR automáticamente         [LOG] INFO
PnL diario < -3%            PAUSAR trading                 [LOG] CRITICAL
BD corrompida               SHUTDOWN + alerta              [LOG] CRITICAL
Modelo accuracy < 50%       NO usar predicciones          [LOG] WARNING

================================================================================
7. PROCEDIMIENTOS DE EMERGENCIA
================================================================================

7.1 PROCEDIMIENTO: CONEXIÓN PERDIDA CON MT5
────────────────────────────────────────────────────────────────────────────

PASO 1: DETECCIÓN AUTOMÁTICA (Bot detecta automáticamente)
───────────────────────────────────────────────────────────
  └─ Log: "[ERROR] MT5 connection lost"

PASO 2: ACCIÓN AUTOMÁTICA DEL BOT
───────────────────────────────────
  ├─ Intenta reconectar cada 5 segundos
  ├─ Máximo 10 intentos (total: 50 segundos)
  └─ Si falla después: pausar trading

PASO 3: ACCIÓN MANUAL DEL OPERADOR (si sigue fallando)
──────────────────────────────────────────────────────
  [ ] Abrir MetaTrader 5
  [ ] Verificar usuario/contraseña
  [ ] Reiniciar MT5 si es necesario
  [ ] En terminal: presionar "r" para retry manual

PASO 4: ESCALACIÓN
──────────────────
  Si sigue sin conectar después de 5 minutos:
    ├─ Parar bot: Ctrl+C
    ├─ Contactar soporte MT5/broker
    └─ Documentar incidente

7.2 PROCEDIMIENTO: CRASH DEL BOT
──────────────────────────────────────────────────────────────────────────

INDICADORES:
  ├─ Proceso Python termina inesperadamente
  ├─ "Application stopped unexpectedly" en terminal
  └─ No hay nuevos logs después de cierto tiempo

PASO 1: REVISAR CAUSA
──────────────────────
Abiralchivo: logs/trading_phantom.log
Buscar últimas líneas:
  ├─ ERROR: [descripción del error]
  ├─ Exception: [stack trace]
  └─ Timestamp exacto

PASO 2: ANÁLISIS
────────────────
¿Cuál es el error?
  ├─ KeyError / ValueError      → Error en cálculo
  ├─ ConnectionError            → Problema MT5
  ├─ OutOfMemory                → Problema de recursos
  └─ Otro                        → Revisar documentación

PASO 3: RECUPERACIÓN
─────────────────────
  [ ] Cerrar posiciones manuales en MT5 (si hay)
  [ ] Esperar 1 minuto
  [ ] Reiniciar bot: python main.py
  [ ] Verificar reconexión en logs

PASO 4: ESCALACIÓN
──────────────────
Si crash se repite:
  ├─ NO reiniciar automáticamente
  ├─ Documentar: fecha, hora, error exacto
  ├─ Revisión de código necesaria
  └─ Contactar desarrollador

7.3 PROCEDIMIENTO: PÉRDIDAS ANORMALES
───────────────────────────────────────────────────────────────────────────

DEFINICIÓN: Pérdida > 5% del capital en 1 hora

PASO 1: PARADA INMEDIATA
─────────────────────────
PRESIONAR: Ctrl+C en terminal
  └─ Detiene bot inmediatamente

PASO 2: EVALUAR SITUACIÓN
──────────────────────────
Abrir MT5:
  [ ] ¿Hay posiciones abiertas?
  [ ] ¿Cuál es el PnL actual?
  [ ] ¿Qué señal estaba activa?

PASO 3: DECISIÓN
────────────────
OPCIÓN A: Recuperar posiciones manualmente
  ├─ Cerrar trades perdedores
  ├─ Esperar nueva oportunidad
  └─ Reiniciar bot con parámetros conservadores

OPCIÓN B: Parar operación por hoy
  ├─ Cerrar todas las posiciones
  ├─ Apagar bot
  └─ Revisar qué salió mal

PASO 4: POST-MORTEM
────────────────────
Crear documento: INCIDENT_YYYY-MM-DD_HHMMSS.md

Contenido:
  # Incidente [fecha/hora]
  
  ## Causa raíz
  [Explicación de qué pasó]
  
  ## Impacto
  [Pérdida total, operaciones afectadas]
  
  ## Acciones preventivas
  [Qué cambiar para evitarlo]
  
  ## Implementado
  [Sí / En progreso / Pendiente]

================================================================================
8. INFORMACIÓN DE CONTACTO Y ESCALACIÓN
================================================================================

EN CASO DE PROBLEMA CRÍTICO:

Paso 1: Parar bot (Ctrl+C)
Paso 2: Documentar error en logs
Paso 3: Contactar administrador técnico

ESCALACIÓN INTERNA:
  Nivel 1 (OPERADOR)    → Revisar logs, reintentar
  Nivel 2 (ADMIN)       → Revisar config, BD
  Nivel 3 (DESARROLLADOR) → Analizar código
  Nivel 4 (GERENCIA)     → Decisión de parada/cambio

================================================================================
REGISTRO DE CAMBIOS A ESTE MANUAL
================================================================================

Versión    Fecha      Cambios
────────────────────────────────────────────────────────────────────────────
1.0        2026-01-08 Creación inicial del manual
1.1        [PENDIENTE] Agregar alertas por email
1.2        [PENDIENTE] Integrar con SIEM
2.0        [PENDIENTE] Automatización de procedimientos

================================================================================
