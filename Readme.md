🤖 Trading Phantom
Plataforma de Trading Algorítmico en MetaTrader 5 (Python)
📌 Descripción General

Trading Phantom es una plataforma de trading algorítmico desarrollada en Python, diseñada para operar con MetaTrader 5 (MT5) mediante su API oficial.

El objetivo del proyecto es construir una arquitectura profesional, robusta y extensible, capaz de:

Ejecutar estrategias de trading automáticas

Gestionar riesgo de forma estricta

Interactuar de manera segura con brokers reales

Evitar errores comunes de MT5 (volumen, stops, horarios, permisos)

Servir como base para backtesting, optimización y despliegue en real

Este proyecto no es un bot “rápido”, sino una base sólida de trading algorítmico real.

🧠 Filosofía del Proyecto

Este proyecto está diseñado siguiendo principios profesionales:

❌ No forzar operaciones

❌ No ignorar reglas del broker

❌ No “parchear” errores sin entenderlos

✅ Validar todo antes de enviar una orden

✅ Fallar de forma controlada y explicable

✅ Separar responsabilidades (arquitectura limpia)

Muchos bots fallan por no respetar MT5.
Trading Phantom existe para no cometer esos errores.

🧱 Arquitectura del Sistema
trading_phantom/
│
├── main.py              # Orquestador principal
├── config.yaml          # Configuración central
│
├── mt5_connector.py     # Comunicación con MetaTrader 5
├── strategy.py          # Lógica de señales
├── risk_manager.py      # Gestión de riesgo y validaciones
├── trader.py            # Ejecutor de órdenes
│
├── debug_symbol.py      # Diagnóstico de símbolos MT5
└── README.md            # Documentación

🔧 Componentes y Justificación Técnica
1️⃣ MT5Connector

📄 mt5_connector.py

Responsable de toda la comunicación con MetaTrader 5.

Funciones clave:

Inicializar conexión con MT5

Resolver símbolos con sufijos (EURUSD → EURUSD-T)

Obtener precios y ticks

Enviar órdenes (pending)

Cerrar posiciones

Consultar posiciones abiertas

Decisiones importantes:

❗ Se usan PENDING ORDERS en lugar de MARKET
👉 Muchos brokers (como Admirals) bloquean órdenes market vía API

❗ Se respeta ORDER_FILLING_RETURN

❗ Se evita enviar price en órdenes market

❗ Se normaliza el símbolo antes de operar

2️⃣ Strategy

📄 strategy.py

Encapsula la lógica de generación de señales.

Actualmente:

Usa datos históricos de MT5

Puede basarse en indicadores técnicos (SMA, RSI, etc.)

Devuelve señales simples: BUY, SELL, HOLD

Justificación:

Separar la estrategia del trading permite:

Cambiar la lógica sin tocar el resto del sistema

Usar múltiples estrategias

Integrar ML / RL en el futuro

3️⃣ RiskManager

📄 risk_manager.py

El corazón del sistema.

Ninguna operación se ejecuta sin pasar por aquí.

Validaciones implementadas:

Máximo número de posiciones abiertas

Riesgo por trade (% del balance)

Lote mínimo, máximo y step del broker

Hard cap de seguridad por usuario

Stop Level (trade_stops_level)

Pérdida diaria máxima

Señales HOLD bloqueadas

SL / TP siempre válidos

Justificación:

La mayoría de bots pierden dinero por no tener risk management real.

Este módulo evita:

Lotes inválidos (error 10027)

SL/TP demasiado cercanos

Operar fuera de reglas del broker

Overtrading

4️⃣ Trader

📄 trader.py

Ejecuta la orden solo si:

La estrategia da señal válida

El RiskManager la aprueba

El mercado está abierto

Este módulo:

Traduce la intención (BUY / SELL) en órdenes MT5

Centraliza la ejecución

Maneja el resultado de order_send

5️⃣ main.py

📄 main.py

Es el orquestador del sistema.

Flujo principal:

Cargar configuración

Conectar a MT5

Inicializar Strategy, RiskManager y Trader

Loop de ejecución:

Obtener precio

Generar señal

Validar riesgo

Ejecutar orden

Manejar errores y cierre limpio

⚙️ Configuración (config.yaml)

Ejemplo:

mode: demo
log_level: INFO

symbol: EURUSD
timeframe: H1
max_positions: 1

risk:
  risk_per_trade: 0.01
  fixed_lot: null
  max_daily_loss: 0.03

orders:
  sl_pips: 20
  tp_pips: 40
  deviation: 50

execution:
  loop_interval_seconds: 60

Justificación:

Toda la lógica crítica es configurable

No hay valores “hardcodeados” peligrosos

Facilita backtesting y optimización

🧪 Errores Reales de MT5 y Lecciones Aprendidas

Durante el desarrollo se enfrentaron errores reales, comunes en trading algorítmico:

❌ Error 10027

Volumen inválido

SL/TP demasiado cerca

Market orders bloqueadas por broker

Pending orders mal posicionadas

➡️ Solución:

Normalización estricta

Uso de trade_stops_level

Pending orders seguras

❌ Error 10018

Mercado cerrado

Horarios Forex

Roll-over / fin de semana

➡️ Solución:

Validar trade_mode

No operar fuera de mercado

🔐 Seguridad y Buenas Prácticas

❌ Nunca operar sin SL

❌ Nunca forzar lotes

❌ Nunca asumir reglas del broker

✅ Siempre consultar symbol_info

✅ Manejar errores explícitamente

✅ Separar lógica de ejecución y decisión

🚀 Roadmap Futuro

📊 Logging profesional (CSV / DB)

📈 Backtesting histórico

🧠 Machine Learning / Reinforcement Learning

🌐 Dashboard web

🧪 Optimización de parámetros

💼 Preparación para cuenta real

⚠️ Advertencia

Este proyecto es educativo y experimental.

No se garantiza rentabilidad

El trading conlleva riesgo

Usar SIEMPRE en demo antes de real

🧑‍💻 Autor

Proyecto desarrollado con enfoque profesional, basado en experiencia real con MetaTrader 5, evitando atajos y soluciones frágiles.

⭐ Contribuciones

Si quieres contribuir:

Mejora estrategias

Añade tests

Optimiza el risk manager

Documenta más casos reales de MT5

✅ Estado del Proyecto

🟢 Funcional en demo
🟡 En proceso de expansión
🔵 Arquitectura estable