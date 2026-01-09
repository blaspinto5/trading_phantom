"""
Script para generar PDF profesional del proyecto Trading Phantom
Instala: pip install reportlab pillow
"""

import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (Image, PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

# Crear PDF
pdf_path = "Trading_Phantom_Documentation.pdf"
doc = SimpleDocTemplate(
    pdf_path, pagesize=letter, topMargin=0.5 * inch, bottomMargin=0.5 * inch
)

# Estilos
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    "CustomTitle",
    parent=styles["Heading1"],
    fontSize=28,
    textColor=colors.HexColor("#FF6B35"),
    spaceAfter=6,
    alignment=TA_CENTER,
    fontName="Helvetica-Bold",
)

heading_style = ParagraphStyle(
    "CustomHeading",
    parent=styles["Heading2"],
    fontSize=16,
    textColor=colors.HexColor("#004E89"),
    spaceAfter=12,
    spaceBefore=12,
    fontName="Helvetica-Bold",
)

subheading_style = ParagraphStyle(
    "CustomSubHeading",
    parent=styles["Heading3"],
    fontSize=13,
    textColor=colors.HexColor("#1B6CA8"),
    spaceAfter=8,
    fontName="Helvetica-Bold",
)

body_style = ParagraphStyle(
    "CustomBody",
    parent=styles["BodyText"],
    fontSize=10,
    alignment=TA_JUSTIFY,
    spaceAfter=8,
    leading=14,
)

# Contenido
content = []

# ============================================
# PORTADA
# ============================================
content.append(Spacer(1, 0.5 * inch))
content.append(Paragraph("👻 TRADING PHANTOM", title_style))
content.append(Spacer(1, 6))
content.append(
    Paragraph(
        "Enterprise-Grade Algorithmic Trading Platform with ML Intelligence",
        ParagraphStyle(
            "subtitle",
            parent=styles["Normal"],
            fontSize=14,
            textColor=colors.HexColor("#666666"),
            alignment=TA_CENTER,
            spaceAfter=12,
        ),
    )
)
content.append(Spacer(1, 0.2 * inch))

# Info de portada
portada_info = [
    ["Versión:", "1.1.0"],
    ["Fecha:", datetime.now().strftime("%B %d, %Y")],
    ["Licencia:", "MIT"],
    ["Lenguaje:", "Python 3.10+"],
    ["Plataforma:", "MetaTrader 5 | Windows"],
]
portada_table = Table(portada_info, colWidths=[2 * inch, 3 * inch])
portada_table.setStyle(
    TableStyle(
        [
            ("ALIGN", (0, 0), (0, -1), "RIGHT"),
            ("ALIGN", (1, 0), (1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#004E89")),
            (
                "ROWBACKGROUNDS",
                (0, 0),
                (-1, -1),
                [colors.white, colors.HexColor("#F0F0F0")],
            ),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
        ]
    )
)
content.append(portada_table)
content.append(Spacer(1, 0.3 * inch))

content.append(
    Paragraph(
        "<b>Un bot de trading completamente automatizado con inteligencia artificial, backtesting profesional "
        "y Knowledge Base para futuras IAs.</b>",
        ParagraphStyle(
            "desc",
            parent=styles["Normal"],
            fontSize=11,
            textColor=colors.HexColor("#333333"),
            alignment=TA_CENTER,
            spaceAfter=12,
            leading=14,
        ),
    )
)

content.append(PageBreak())

# ============================================
# TABLA DE CONTENIDOS
# ============================================
content.append(Paragraph("📋 Tabla de Contenidos", heading_style))
toc_items = [
    "1. Introducción",
    "2. Características principales",
    "3. Requisitos técnicos",
    "4. Instalación",
    "5. Estructura del proyecto",
    "6. Arquitectura y diseño",
    "7. Sistema de Machine Learning",
    "8. Knowledge Base",
    "9. API REST",
    "10. Backtesting",
    "11. Empaquetado",
    "12. Solución de problemas",
    "13. Roadmap",
]
for item in toc_items:
    content.append(Paragraph(item, body_style))
content.append(Spacer(1, 0.2 * inch))

content.append(PageBreak())

# ============================================
# INTRODUCCIÓN
# ============================================
content.append(Paragraph("1. Introducción", heading_style))
content.append(
    Paragraph(
        "<b>Trading Phantom</b> es una plataforma modular de trading algorítmico construida en Python, "
        "diseñada para operar en MetaTrader 5 con inteligencia artificial integrada. El proyecto combina "
        "automatización completa, machine learning avanzado, backtesting profesional y una interfaz "
        "web moderna en una solución empresarial.",
        body_style,
    )
)
content.append(Spacer(1, 0.1 * inch))

content.append(Paragraph("<b>Casos de uso:</b>", subheading_style))
use_cases = [
    "• <b>Traders profesionales:</b> Automatiza estrategias, backtesta y monitorea 24/7",
    "• <b>Analistas cuantitativos:</b> Experimenta con indicadores y ML sin código repetitivo",
    "• <b>Investigadores de IA:</b> Infraestructura lista para integrar LSTM, RL, Transformers",
    "• <b>Desarrolladores:</b> API REST + modularidad para crear bots personalizados",
    "• <b>Educación:</b> Aprende trading algorítmico con código profesional y documentado",
]
for uc in use_cases:
    content.append(Paragraph(uc, body_style))

content.append(Spacer(1, 0.2 * inch))
content.append(PageBreak())

# ============================================
# CARACTERÍSTICAS
# ============================================
content.append(Paragraph("2. Características Principales", heading_style))

features = [
    (
        "🤖 Bot de Trading Inteligente",
        "Loop automático configurable con indicadores técnicos (EMA, MACD, RSI), "
        "validación de riesgo, conexión MT5 y logging profesional.",
    ),
    (
        "📊 Machine Learning Integrado",
        "RandomForest entrenado con datos históricos, 7 indicadores como features, "
        "Knowledge Base que captura 8 tipos de aprendizaje.",
    ),
    (
        "🎨 UI Profesional",
        "Dashboard con KPIs en tiempo real, panel ML, logbox elegante, "
        "botón de shutdown con confirmación, diseño responsivo.",
    ),
    (
        "📈 Backtesting Visual",
        "Simulación numérica, gráficos interactivos, métricas detalladas "
        "(Sharpe, Drawdown, Win Rate), exportación de resultados.",
    ),
    (
        "🌐 API REST Completa",
        "20+ endpoints para control del bot, backtesting, ML, exportación de datos "
        "y acceso a Knowledge Base.",
    ),
    (
        "🐳 Docker & Escalabilidad",
        "docker-compose.yml con Postgres + Flask, base de datos persistente, "
        "healthchecks automatizados.",
    ),
    (
        "📦 Empaquetado Profesional",
        "EXE Windows con PyInstaller, instalador Windows con Inno Setup, "
        "self-contained sin dependencias externas.",
    ),
]

for feature_title, feature_desc in features:
    content.append(Paragraph(f"<b>{feature_title}</b>", subheading_style))
    content.append(Paragraph(feature_desc, body_style))
    content.append(Spacer(1, 0.08 * inch))

content.append(PageBreak())

# ============================================
# REQUISITOS
# ============================================
content.append(Paragraph("3. Requisitos Técnicos", heading_style))

req_table_data = [
    ["Requisito", "Versión", "Descripción"],
    ["Windows", "10 o superior", "Sistema operativo soportado"],
    ["Python", "3.10+", "Lenguaje de programación"],
    ["Git", "Opcional", "Para clonar repositorio"],
    ["MetaTrader 5", "Opcional", "Solo para operar en vivo"],
    ["Inno Setup", "Opcional", "Solo para crear instalador"],
]

req_table = Table(req_table_data, colWidths=[1.5 * inch, 1.5 * inch, 2.5 * inch])
req_table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#004E89")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [colors.white, colors.HexColor("#F5F5F5")],
            ),
        ]
    )
)
content.append(req_table)
content.append(Spacer(1, 0.2 * inch))

content.append(PageBreak())

# ============================================
# INSTALACIÓN
# ============================================
content.append(Paragraph("4. Instalación", heading_style))

content.append(Paragraph("Opción 1: Automática (Recomendado)", subheading_style))
content.append(
    Paragraph(
        "1. Abre <b>INSTALL.bat</b> (doble-click)<br/>"
        "   → Crea venv automáticamente<br/>"
        "   → Instala dependencias<br/>"
        "2. Abre <b>RUN.bat</b> (doble-click)<br/>"
        "   → Inicia servidor Flask<br/>"
        "   → Abre UI en http://127.0.0.1:5000",
        body_style,
    )
)
content.append(Spacer(1, 0.1 * inch))

content.append(Paragraph("Opción 2: Manual (Desarrollo)", subheading_style))
content.append(
    Paragraph(
        "python -m venv .venv<br/>"
        ".\\. venv\\Scripts\\Activate.ps1<br/>"
        "pip install -r requirements.txt<br/>"
        "pip install -r requirements-dev.txt<br/>"
        "python -m trading_phantom.main --debug",
        ParagraphStyle(
            "code",
            parent=styles["Normal"],
            fontSize=8,
            fontName="Courier",
            textColor=colors.HexColor("#333333"),
            leftIndent=20,
            spaceAfter=12,
            backColor=colors.HexColor("#F5F5F5"),
        ),
    )
)

content.append(Spacer(1, 0.2 * inch))
content.append(PageBreak())

# ============================================
# ESTRUCTURA
# ============================================
content.append(Paragraph("5. Estructura del Proyecto", heading_style))

content.append(
    Paragraph(
        "El proyecto sigue el patrón <b>src-layout</b>, organizando el código principal en "
        "src/trading_phantom/ con responsabilidades bien definidas:",
        body_style,
    )
)
content.append(Spacer(1, 0.1 * inch))

structure_items = [
    ("<b>src/trading_phantom/core/</b>", "Orquestación principal (Orchestrator)"),
    (
        "<b>src/trading_phantom/modules/</b>",
        "Strategy, RiskManager, Trader, DataLoader",
    ),
    (
        "<b>src/trading_phantom/analytics/</b>",
        "ML Pipeline, Knowledge Base, Transfer Learning",
    ),
    (
        "<b>src/trading_phantom/api/</b>",
        "REST API Blueprints (bot, backtest, analytics)",
    ),
    ("<b>src/trading_phantom/mt5/</b>", "Integración MetaTrader 5"),
    ("<b>src/trading_phantom/backtest/</b>", "Engine de backtesting"),
    ("<b>tests/</b>", "Tests unitarios e integración"),
    ("<b>docs/</b>", "Documentación profesional"),
    ("<b>scripts/</b>", "Scripts de desarrollo y empaquetado"),
]

for struct_name, struct_desc in structure_items:
    content.append(Paragraph(f"{struct_name}: {struct_desc}", body_style))
    content.append(Spacer(1, 0.06 * inch))

content.append(PageBreak())

# ============================================
# ARQUITECTURA
# ============================================
content.append(Paragraph("6. Arquitectura y Diseño", heading_style))

content.append(
    Paragraph(
        "Trading Phantom utiliza una arquitectura de <b>capas bien definidas</b> "
        "que facilita testing, escalabilidad y mantenimiento:",
        body_style,
    )
)
content.append(Spacer(1, 0.1 * inch))

arch_layers = [
    ("<b>Presentation Layer:</b>", "HTML/CSS/JS (Flask templates) - Dashboard y UI"),
    ("<b>API Layer:</b>", "Flask Blueprints - REST endpoints"),
    ("<b>Business Logic Layer:</b>", "Orchestrator, Strategy, ML Pipeline"),
    ("<b>Data Access Layer:</b>", "MT5Connector, Database, Cache"),
]

for arch_name, arch_desc in arch_layers:
    content.append(Paragraph(f"{arch_name} {arch_desc}", body_style))
    content.append(Spacer(1, 0.08 * inch))

content.append(Paragraph("<b>Patrones de Diseño Utilizados:</b>", subheading_style))
patterns = [
    "• Orchestrator Pattern - Coordina el flujo principal",
    "• Strategy Pattern - Estrategias intercambiables",
    "• Dependency Injection - Componentes desacoplados",
    "• Adapter Pattern - Adaptación a diferentes interfaces",
    "• Repository Pattern - Abstracción de acceso a datos",
]
for p in patterns:
    content.append(Paragraph(p, body_style))

content.append(Spacer(1, 0.2 * inch))
content.append(PageBreak())

# ============================================
# MACHINE LEARNING
# ============================================
content.append(Paragraph("7. Sistema de Machine Learning", heading_style))

content.append(
    Paragraph(
        "Trading Phantom integra un sistema de <b>ML modular y escalable</b> que aprende "
        "de los datos históricos de trading sin afectar la estrategia base.",
        body_style,
    )
)
content.append(Spacer(1, 0.1 * inch))

content.append(Paragraph("Componentes ML:", subheading_style))
ml_components = [
    ("<b>RandomForest Classifier:</b>", "Modelo principal de predicción"),
    (
        "<b>7 Features:</b>",
        "EMA, MACD, RSI, cambio precio, volumen, volatilidad, tendencia",
    ),
    ("<b>Database:</b>", "SQLite (local) o Postgres (producción)"),
    ("<b>Collector:</b>", "Ingesta automática de trades y backtests"),
]
for ml_comp, ml_desc in ml_components:
    content.append(Paragraph(f"{ml_comp} {ml_desc}", body_style))
    content.append(Spacer(1, 0.06 * inch))

content.append(Spacer(1, 0.1 * inch))
content.append(Paragraph("Flujo de ML:", subheading_style))
content.append(
    Paragraph(
        "1. <b>Recolecta de datos:</b> Bot ejecuta trades → auto-ingesta en DB<br/>"
        "2. <b>Entrenar modelo:</b> RandomForest.fit() con ≥30 trades<br/>"
        "3. <b>Activar ML:</b> config.yaml ml.enabled=true<br/>"
        "4. <b>Predicción:</b> Cada vela, ML valida señal con probabilidad",
        body_style,
    )
)

content.append(Spacer(1, 0.2 * inch))
content.append(PageBreak())

# ============================================
# KNOWLEDGE BASE
# ============================================
content.append(Paragraph("8. Knowledge Base", heading_style))

content.append(
    Paragraph(
        "<b>La Knowledge Base</b> es un sistema único que captura el aprendizaje completo "
        "del RandomForest y lo expone de forma modular para que futuras IAs "
        "(LSTM, RL, Transformers) puedan consumir sin reentrenar.",
        body_style,
    )
)
content.append(Spacer(1, 0.1 * inch))

content.append(Paragraph("8 Tipos de Conocimiento Almacenados:", subheading_style))

kb_data = [
    ["#", "Tipo", "Archivo", "Contenido"],
    ["1", "Feature Importance", "feature_importance.json", "Top 5 features ranking"],
    ["2", "Feature Embeddings", "feature_embeddings.json", "Mean, std, min, max"],
    ["3", "Correlation Matrix", "correlation_matrix.json", "Feature relationships"],
    ["4", "Decision Patterns", "decision_patterns.json", "Reglas del árbol"],
    [
        "5",
        "Performance Metrics",
        "performance_metrics.json",
        "Accuracy, precision, recall",
    ],
    ["6", "Training Data Stats", "feature_stats.json", "Distribución dataset"],
    ["7", "Trade Patterns", "winners_losers.json", "Análisis trades"],
    ["8", "Model Serialization", "random_forest.pkl", "Modelo guardado"],
]

kb_table = Table(kb_data, colWidths=[0.4 * inch, 1.3 * inch, 1.8 * inch, 1.5 * inch])
kb_table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#004E89")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [colors.white, colors.HexColor("#F5F5F5")],
            ),
        ]
    )
)
content.append(kb_table)
content.append(Spacer(1, 0.1 * inch))

content.append(
    Paragraph("<b>Ubicación:</b> src/trading_phantom/data/knowledge_base/", body_style)
)

content.append(Spacer(1, 0.2 * inch))
content.append(PageBreak())

# ============================================
# API REST
# ============================================
content.append(Paragraph("9. API REST", heading_style))

content.append(
    Paragraph(
        "Trading Phantom expone <b>20+ endpoints REST</b> para integración, "
        "automatización y acceso programático.",
        body_style,
    )
)
content.append(Spacer(1, 0.1 * inch))

content.append(Paragraph("Categorías de Endpoints:", subheading_style))

api_cats = [
    ("🤖 Bot", "/api/bot/start, /api/bot/stop, /api/bot/status"),
    ("📊 Backtest", "/api/backtest (POST/GET)"),
    ("🤖 ML", "/api/analytics/ml/train, /api/analytics/ml/predict"),
    ("💾 Exportación", "/api/analytics/export/trades, /api/analytics/export/backtests"),
    ("📚 Knowledge Base", "/api/knowledge/* (8 endpoints)"),
    ("📋 Logs", "/api/logs"),
]

for cat_name, cat_endpoints in api_cats:
    content.append(Paragraph(f"<b>{cat_name}:</b> {cat_endpoints}", body_style))
    content.append(Spacer(1, 0.06 * inch))

content.append(Spacer(1, 0.2 * inch))
content.append(PageBreak())

# ============================================
# BACKTESTING
# ============================================
content.append(Paragraph("10. Backtesting Visual", heading_style))

content.append(
    Paragraph(
        "El módulo de backtesting permite validar estrategias con datos históricos reales "
        "antes de operar en vivo.",
        body_style,
    )
)
content.append(Spacer(1, 0.1 * inch))

content.append(Paragraph("Características:", subheading_style))
backtest_features = [
    "✓ Simulación numérica completa",
    "✓ Gráficos interactivos (Equity curve, Drawdown)",
    "✓ Métricas profesionales (Sharpe, Sortino, Calmar, Max DD, Win Rate)",
    "✓ Exportación en JSON/CSV/Parquet",
    "✓ Comparación entre estrategias (A/B testing)",
    "✓ Análisis individual de trades",
]
for feat in backtest_features:
    content.append(Paragraph(feat, body_style))
    content.append(Spacer(1, 0.04 * inch))

content.append(Spacer(1, 0.2 * inch))
content.append(PageBreak())

# ============================================
# EMPAQUETADO
# ============================================
content.append(Paragraph("11. Empaquetado y Distribución", heading_style))

content.append(Paragraph("Generar ejecutable .exe:", subheading_style))
content.append(
    Paragraph(
        ".\\scripts\\build_exe.ps1          # Sin consola (usuario final)<br/>"
        ".\\scripts\\build_exe.ps1 -console # Con consola (debugging)",
        ParagraphStyle(
            "code",
            parent=styles["Normal"],
            fontSize=8,
            fontName="Courier",
            leftIndent=20,
            spaceAfter=8,
        ),
    )
)

content.append(Spacer(1, 0.1 * inch))
content.append(Paragraph("Crear instalador Windows:", subheading_style))
content.append(
    Paragraph(
        ".\\scripts\\build_installer.ps1<br/>"
        "→ Resultado: Setup-TradingPhantom-v1.1.0.exe",
        body_style,
    )
)

content.append(Spacer(1, 0.1 * inch))
content.append(
    Paragraph(
        "<b>Beneficios:</b> Self-contained (sin dependencias externas), "
        "autostart opcional, instalación limpia, fácil desinstalación.",
        body_style,
    )
)

content.append(Spacer(1, 0.2 * inch))
content.append(PageBreak())

# ============================================
# ROADMAP
# ============================================
content.append(Paragraph("12. Roadmap", heading_style))

content.append(Paragraph("<b>✅ Completado (v1.1.0)</b>", subheading_style))
completed = [
    "✓ Bot de trading con indicadores (EMA, MACD, RSI)",
    "✓ Backtesting visual con métricas",
    "✓ UI profesional con dashboard",
    "✓ ML RandomForest + Knowledge Base",
    "✓ 20+ REST API endpoints",
    "✓ Empaquetado .exe e instalador",
    "✓ Arquitectura modular escalable",
]
for item in completed:
    content.append(Paragraph(item, body_style))
    content.append(Spacer(1, 0.04 * inch))

content.append(Spacer(1, 0.1 * inch))
content.append(Paragraph("<b>🚀 Próximo (v1.2.0)</b>", subheading_style))
planned = [
    "□ LSTM para secuencias de precios",
    "□ Reinforcement Learning agent",
    "□ Ollama/DeepSeek integration",
    "□ Ensemble models (RF + LSTM + RL)",
    "□ Mobile app (React Native)",
]
for item in planned:
    content.append(Paragraph(item, body_style))
    content.append(Spacer(1, 0.04 * inch))

content.append(Spacer(1, 0.2 * inch))
content.append(PageBreak())

# ============================================
# CONCLUSIÓN
# ============================================
content.append(Paragraph("13. Conclusión", heading_style))

content.append(
    Paragraph(
        "<b>Trading Phantom</b> es una plataforma completa y profesional que demuestra "
        "cómo construir un bot de trading moderno con inteligencia artificial. ",
        body_style,
    )
)

content.append(Paragraph("El proyecto está diseñado para ser:", body_style))

conclusion_points = [
    "<b>Escalable:</b> Arquitectura modular lista para LSTM, RL, Transformers",
    "<b>Profesional:</b> UI moderna, API REST, backtesting visual",
    "<b>Educativo:</b> Código bien documentado y estructurado",
    "<b>Operacional:</b> Ready para producción con empaquetado profesional",
]
for point in conclusion_points:
    content.append(Paragraph(f"• {point}", body_style))
    content.append(Spacer(1, 0.06 * inch))

content.append(Spacer(1, 0.2 * inch))

content.append(
    Paragraph(
        "<b>Licencia:</b> MIT (libre para usar, modificar y distribuir)", body_style
    )
)

content.append(Spacer(1, 0.1 * inch))
content.append(
    Paragraph(
        "<b>GitHub:</b> https://github.com/blaspinto5/trading_phantom", body_style
    )
)

# ============================================
# PIE DE PÁGINA
# ============================================
content.append(Spacer(1, 0.3 * inch))
content.append(
    Paragraph(
        "___________________________________________________________________________",
        ParagraphStyle(
            "line",
            parent=styles["Normal"],
            fontSize=8,
            textColor=colors.HexColor("#CCCCCC"),
        ),
    )
)
content.append(Spacer(1, 0.05 * inch))
content.append(
    Paragraph(
        f"Trading Phantom Documentation | Generated {datetime.now().strftime('%B %d, %Y')} | v1.1.0 | MIT License",
        ParagraphStyle(
            "footer",
            parent=styles["Normal"],
            fontSize=8,
            textColor=colors.HexColor("#999999"),
            alignment=TA_CENTER,
        ),
    )
)

# ============================================
# GENERAR PDF
# ============================================
doc.build(content)
print(f"✅ PDF generado exitosamente: {pdf_path}")
print(f"📄 Tamaño: {os.path.getsize(pdf_path) / 1024:.1f} KB")
print(f"📍 Ubicación: {os.path.abspath(pdf_path)}")
