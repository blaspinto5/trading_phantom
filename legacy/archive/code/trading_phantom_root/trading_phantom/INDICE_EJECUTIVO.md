╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                    ÍNDICE EJECUTIVO - TRADING PHANTOM                      ║
║                          Guía de Referencia Rápida                         ║
║                             v1.1.0 | Enero 2026                            ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

================================================================================
🎯 NAVEGACIÓN RÁPIDA
================================================================================

¿QUÉ NECESITAS?                          DOCUMENTO A LEER
────────────────────────────────────────────────────────────────────────────
Entender qué es Trading Phantom          → README.md
Comenzar a operar en 5 minutos           → QUICK_START.md
Instalar y configurar                    → QUICK_START.md
Estado actual del proyecto               → AUDITORIA_CORPORATIVA.md
Procedimientos operativos diarios        → MANUAL_OPERATIVO.md
Entrenar el modelo ML                    → QUICK_START_NEW_FEATURES.md
Realizar backtesting                     → docs/QUICKSTART.md
Entender arquitectura técnica            → docs/ARCHITECTURE.md
Documentación API REST                   → docs/API.md
Listar todos los archivos y funciones    → documentacion/ARCHIVOS_Y_FUNCIONES.md
Cambios recientes realizados             → CAMBIOS_REALIZADOS.md
Historial de versiones                   → CHANGELOG.md
Cómo contribuir al proyecto              → CONTRIBUTING.md

================================================================================
📊 ESTADO ACTUAL DEL PROYECTO (RESUMEN)
================================================================================

ESTADO GENERAL:                    ✅ OPERATIVO Y PRODUCTIVO

COMPONENTES PRINCIPALES:
  ✅ Módulos de trading            100% funcionales
  ✅ Integración MetaTrader 5       100% funcional
  ✅ Machine Learning               Entrenado (60% accuracy)
  ✅ Backtesting                    100% funcional
  ✅ API REST                       8+ endpoints activos
  ✅ Base de datos                  SQLite operativa
  ✅ Documentación                  100% completa

LÍNEAS DE CÓDIGO:                  ~8,500+
MÓDULOS ACTIVOS:                   8 componentes independientes
DOCUMENTACIÓN:                      15+ archivos profesionales

ÚLTIMA AUDITORÍA:                  Enero 8, 2026
PRÓXIMA AUDITORÍA:                 Enero 2027

================================================================================
🚀 INICIO RÁPIDO (3 OPCIONES)
================================================================================

OPCIÓN 1: LO MÁS FÁCIL (Recomendado para principiantes)
─────────────────────────────────────────────────────────

Abre PowerShell en la carpeta del proyecto y escribe:

  .\INSTALL.bat
  (Espera 1-2 minutos mientras instala)

Luego:

  .\RUN.bat
  (El bot inicia automáticamente)

Accede a:

  http://127.0.0.1:5000
  (Dashboard en navegador)


OPCIÓN 2: DESDE PowerShell
──────────────────────────

cd "C:\Users\Peruano Pinto\Desktop\PROYECTO 2"
.\RUN.ps1


OPCIÓN 3: DESDE TERMINAL PYTHON
────────────────────────────────

cd "C:\Users\Peruano Pinto\Desktop\PROYECTO 2"
python main.py

================================================================================
📁 ESTRUCTURA DE CARPETAS (LO IMPORTANTE)
================================================================================

CARPETA                 CONTENIDO                       IMPORTANCIA
────────────────────────────────────────────────────────────────────────
src/trading_phantom/    Código principal (8,500+ líneas) ⭐⭐⭐ CRÍTICO
config/                 Configuración YAML              ⭐⭐⭐ CRÍTICO
data/                   BD + modelos ML entrenados      ⭐⭐⭐ CRÍTICO
logs/                   Logs y historial de trades      ⭐⭐⭐ CRÍTICO
docs/                   Documentación técnica           ⭐⭐  IMPORTANTE
scripts/                Scripts de utilidad             ⭐   OPCIONAL
tests/                  Tests automatizados             ⭐   OPCIONAL
backtest/               Backtesting secundario          ⭐   OPCIONAL
.git/                   Historial de versiones          ⭐⭐  IMPORTANTE

================================================================================
🔧 PROCEDIMIENTOS ESENCIALES
================================================================================

PROCEDIMIENTO 1: INICIAR OPERACIÓN
───────────────────────────────────
1. Abrir MetaTrader 5
2. Ejecutar RUN.bat o python main.py
3. Acceder a http://127.0.0.1:5000
4. Monitorear logs: logs/trading_phantom.log

PROCEDIMIENTO 2: ENTRENAR MODELO ML
─────────────────────────────────────
(Hacer una sola vez o cuando haya 50+ trades nuevos)

python scripts/ml_train.py --save

PROCEDIMIENTO 3: VALIDAR ESTRATEGIA (Backtesting)
──────────────────────────────────────────────────

python backtest/run_backtest.py

Buscar en resultados:
  ✓ Sharpe Ratio > 1.0
  ✓ Win Rate > 45%
  ✓ Max Drawdown < 20%

PROCEDIMIENTO 4: PARAR BOT SEGURAMENTE
──────────────────────────────────────

En la terminal donde corre el bot:
  Ctrl+C
  (Espera a que escriba "Shutdown complete")

PROCEDIMIENTO 5: CAMBIAR PARÁMETROS
───────────────────────────────────

Editar: config/config.yaml
Cambios toman efecto inmediatamente (sin reiniciar)

================================================================================
💾 DATOS Y ALMACENAMIENTO
================================================================================

DÓNDE ESTÁN LOS DATOS:

Trading Phantom.db
  └─ Ubicación: src/data/trading_phantom.db
  └─ Contiene: Historial de todas las operaciones
  └─ Tamaño: < 1MB mensual
  └─ Importancia: ⭐⭐⭐ CRÍTICO - Respaldar semanalmente

Trade History.json
  └─ Ubicación: logs/trade_history.json
  └─ Contiene: Último historial en formato JSON
  └─ Importancia: ⭐⭐ IMPORTANTE - Respaldar diariamente

Logs
  └─ Ubicación: logs/trading_phantom.log
  └─ Contiene: Todos los eventos del bot
  └─ Rotación: Cada 7 días
  └─ Importancia: ⭐⭐ IMPORTANTE

Modelos ML
  └─ Ubicación: src/data/models/random_forest.pkl
  └─ Contiene: Modelo entrenado
  └─ Importancia: ⭐⭐⭐ CRÍTICO - Respaldar después de reentrenar

BACKUP RECOMENDADO:
  Carpetas a respaldar semanalmente:
    ├─ src/data/
    ├─ logs/
    ├─ config/
    └─ .git/

================================================================================
⚙️  CONFIGURACIÓN CENTRAL
================================================================================

ARCHIVO: config/config.yaml

Parámetros principales:

symbol: EURUSD              [Símbolo a tradear]
timeframe: H1              [Timeframe operación]

risk:
  risk_per_trade: 0.01     [1% del capital por trade]
  max_daily_loss: 0.03     [3% máximo pérdida diaria]

orders:
  sl_pips: 20              [Stop loss en pips]
  tp_pips: 40              [Take profit en pips]

ml:
  enabled: true            [Usar modelo ML]
  threshold: 0.55          [Confianza mínima para usar ML]

Cambiar parámetros → guarda archivo → cambios toman efecto inmediatamente

================================================================================
📈 INDICADORES TÉCNICOS IMPLEMENTADOS
================================================================================

INDICADORES QUE USA EL BOT:

1. EMA (Exponential Moving Average)
   └─ Períodos: 12, 26
   └─ Uso: Identificar tendencia
   └─ Señal: EMA12 > EMA26 = alcista

2. MACD (Moving Average Convergence Divergence)
   └─ Período: 12, 26, 9
   └─ Uso: Detectar cambios de momentum
   └─ Señal: Cruce de línea de señal

3. RSI (Relative Strength Index)
   └─ Período: 14
   └─ Uso: Detectar overbought/oversold
   └─ Señal: RSI > 70 = overbought, < 30 = oversold

SALIDAS DEL BOT:
  ├─ BUY    [Comprar - todos los indicadores alcistas]
  ├─ SELL   [Vender - todos los indicadores bajistas]
  └─ HOLD   [Esperar - sin señal clara]

================================================================================
🤖 MACHINE LEARNING
================================================================================

MODELO: Random Forest (100 árboles)

ENTRENAMIENTO:
  • Estado: ✅ COMPLETADO
  • Muestras: 200 trades
  • Accuracy: 60%
  • Features: 7 características derivadas
  • Ubicación: src/data/models/random_forest.pkl

FEATURES (características):
  1. side (BUY/SELL)
  2. price (precio entrada)
  3. volume (tamaño posición)
  4. abs_pnl (PnL absoluto)
  5. pnl_lag1 (PnL anterior)
  6. pnl_ma_5 (promedio móvil 5 períodos)
  7. pnl_std_5 (desviación estándar 5 períodos)

TARGET (predicción):
  0 = Trade perdedor
  1 = Trade ganador

CÓMO SE USA:
  └─ Si ML.enabled = true en config.yaml
  └─ Bot pide predicción antes de ejecutar
  └─ Solo ejecuta si confianza > threshold (0.55)

================================================================================
🔍 MONITOREO Y MÉTRICAS
================================================================================

MÉTRICAS PRINCIPALES:

Win Rate
  └─ Porcentaje de operaciones ganadoras
  └─ Meta: > 45%
  └─ Cálculo: (trades ganados / total trades) * 100

Sharpe Ratio
  └─ Rentabilidad ajustada por riesgo
  └─ Meta: > 1.0
  └─ Interpretación: > 1.0 es bueno, > 2.0 es excelente

Sortino Ratio
  └─ Como Sharpe pero solo cuenta desviación a la baja
  └─ Meta: > 1.5
  └─ Mejor que Sharpe para estrategias asimétricas

Max Drawdown
  └─ Pérdida máxima desde un pico
  └─ Meta: < 20%
  └─ Crítico: si > 30%, revisar estrategia

Profit Factor
  └─ Ganancias totales / Pérdidas totales
  └─ Meta: > 1.2
  └─ Interpretación: > 1.2 es viable

CÓMO REVISAR MÉTRICAS:

1. Dashboard web: http://127.0.0.1:5000
2. Logs: logs/trading_phantom.log
3. Historial: logs/trade_history.json
4. Backtesting: python backtest/run_backtest.py

================================================================================
📋 CHECKLIST PARA COMENZAR A OPERAR
================================================================================

ANTES DE OPERAR POR PRIMERA VEZ:

[ ] Leer README.md (entender qué es Trading Phantom)
[ ] Leer QUICK_START.md (instalación)
[ ] Ejecutar setup_training_data.py (crear datos entrenamiento)
[ ] Ejecutar ml_train.py (entrenar modelo)
[ ] Ejecutar backtest/run_backtest.py (validar estrategia)
[ ] Revisar métricas de backtest (Sharpe > 1.0)
[ ] Abrir MetaTrader 5
[ ] Revisar config.yaml (parámetros correctos)
[ ] Ejecutar RUN.bat o RUN.ps1
[ ] Acceder a http://127.0.0.1:5000
[ ] Verificar conexión a MT5 en dashboard
[ ] Monitorear primeros 30 minutos
[ ] Respaldar datos importantes

DURANTE LA OPERACIÓN:

[ ] Revisar logs cada 1 hora
[ ] Monitorear trades en MT5
[ ] Verificar PnL acumulado
[ ] Parar si losses > 3% diarios

================================================================================
🆘 SOLUCIÓN DE PROBLEMAS RÁPIDA
================================================================================

PROBLEMA: "ModuleNotFoundError: No module named 'trading_phantom'"
SOLUCIÓN: pip install -r requirements.txt

PROBLEMA: "MT5 connection failed"
SOLUCIÓN: Abrir MetaTrader 5, verificar usuario/contraseña

PROBLEMA: "Port 5000 already in use"
SOLUCIÓN: Cambiar puerto en config.yaml o cerrar aplicación anterior

PROBLEMA: "No data sufficient in DB for ML training"
SOLUCIÓN: Ejecutar setup_training_data.py primero

PROBLEMA: El bot no genera señales
SOLUCIÓN: Revisar logs (logs/trading_phantom.log), buscar ERROR

PROBLEMA: Backtest muestra Sharpe < 0
SOLUCIÓN: Estrategia no es viable, revisar parámetros en config.yaml

PROBLEMA: Bot se detiene inesperadamente
SOLUCIÓN: Revisar logs de error, contactar administrador

================================================================================
📞 SOPORTE Y DOCUMENTACIÓN ADICIONAL
================================================================================

¿DÓNDE ENCONTRAR RESPUESTAS?

Documentación técnica completa:      docs/README.md
Arquitectura y diseño:               docs/ARCHITECTURE.md
API REST endpoints:                  docs/API.md
Qué hace cada archivo:               documentacion/ARCHIVOS_Y_FUNCIONES.md
Procedimientos operativos:           MANUAL_OPERATIVO.md
Auditoría corporativa:               AUDITORIA_CORPORATIVA.md
Guía de contribución:                CONTRIBUTING.md
Historial de cambios:                CHANGELOG.md

================================================================================
🎓 CONCEPTOS CLAVE (GLOSARIO)
================================================================================

BOT: Software que ejecuta operaciones automáticamente sin intervención

SEÑAL: Recomendación del sistema (BUY / SELL / HOLD)

BACKTEST: Simulación de operaciones con datos históricos

DRAWDOWN: Pérdida máxima desde un pico de ganancia

SHARPE RATIO: Métrica que mide rentabilidad ajustada por riesgo

STOP LOSS (SL): Nivel donde se cierra automáticamente para limitar pérdida

TAKE PROFIT (TP): Nivel donde se cierra automáticamente para asegurar ganancia

PnL: Profit and Loss (ganancia/pérdida en dinero)

TICK: Movimiento de precio más pequeño posible

TIMEFRAME: Período de velas (H1 = 1 hora, D1 = 1 día)

META TRADER 5 (MT5): Plataforma de trading del broker

OHLCV: Open, High, Low, Close, Volume (datos de velas)

MODELO ML: Inteligencia artificial que aprende patrones de trades

KNOWLEDGE BASE: Información extraída del modelo para futuras IAs

================================================================================
📅 PRÓXIMOS PASOS
================================================================================

AHORA MISMO:
  1. Leer este documento completo
  2. Ir a QUICK_START.md
  3. Ejecutar instalación

ESTA SEMANA:
  1. Entrenar modelo ML
  2. Validar con backtesting
  3. Realizar prueba de operación con dinero real (monto pequeño)

ESTE MES:
  1. Optimizar parámetros de estrategia
  2. Mejorar ML accuracy (objetivo: 75%+)
  3. Implementar monitoring automático
  4. Documentar incidentes

ESTE TRIMESTRE:
  1. Agregar más symbols (GBPUSD, USDJPY, etc)
  2. Implementar portfolio management
  3. Mejorar cobertura de testing
  4. Agregar alertas por email

================================================================================
✅ CONFIRMACIÓN DE COMPRENSIÓN
================================================================================

Después de leer este documento, deberías entender:

✓ Qué es Trading Phantom y qué hace
✓ Cómo instalarlo y ejecutarlo
✓ Dónde están almacenados los datos
✓ Cómo cambiar parámetros
✓ Qué indicadores técnicos usa
✓ Cómo revisar métricas
✓ Cómo entrenar el modelo ML
✓ Cómo validar con backtesting
✓ Qué hacer si algo falla

Si entiendes todos estos puntos: ✅ ESTÁS LISTO PARA OPERAR

================================================================================
ÚLTIMA ACTUALIZACIÓN
================================================================================

Documento creado: Enero 8, 2026
Próxima actualización: Enero 2027
Versión: 1.0

================================================================================
