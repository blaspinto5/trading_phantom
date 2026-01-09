# 📚 Documentación Trading Phantom v1.1.0

Bienvenido a la documentación completa de **Trading Phantom**, una plataforma empresarial de trading algorítmico con inteligencia artificial.

---

## 📖 Archivos de Documentación

### 1. **README.md** (46 KB - 2000+ líneas)
**La guía más completa del proyecto**

Contiene:
- ✅ Características principales (8 secciones)
- ✅ Instalación (3 opciones diferentes)
- ✅ Estructura del proyecto (árbol completo)
- ✅ Arquitectura y diseño (patrones, flujos)
- ✅ Sistema ML y Knowledge Base explicado
- ✅ API REST documentada (20+ endpoints con ejemplos JSON)
- ✅ Backtesting visual
- ✅ Empaquetado y distribución
- ✅ Testing y CI/CD
- ✅ Solución de problemas (10+ escenarios)
- ✅ Contribuciones y roadmap

**Cuándo leer:** Primero, para entender todo el proyecto

**Tiempo estimado:** 30-45 minutos de lectura

---

### 2. **ARCHIVOS_Y_FUNCIONES.md** (25 KB - 700+ líneas)
**Listado detallado de cada archivo del proyecto**

Contiene:
- 📁 **Archivos raíz** - main.py, webapp.py, requirements.txt, etc (11 archivos)
- 🔧 **Scripts** - INSTALL, RUN, BUILD_EXE, BUILD_INSTALLER (6 scripts)
- 🔄 **core/** - orchestrator.py (orquestador principal)
- 💼 **modules/** - strategy, risk_manager, trader, data_loader (4 módulos)
- 🤖 **analytics/** - ML, Knowledge Base, Transfer Learning (5 módulos)
- 🌐 **api/** - REST endpoints (5 blueprints)
- 💹 **mt5/** - Conector MetaTrader 5
- 📊 **backtest/** - Engine de backtesting
- 🎨 **static/** - CSS styling (400+ líneas)
- 📄 **templates/** - HTML (index.html, ml_info.html)
- 🧪 **tests/** - Tests unitarios e integración
- 📚 **docs/** - Documentación adicional

**Cada archivo tiene:**
- Tipo de archivo
- Función específica
- Responsabilidades detalladas
- Métodos principales
- Parámetros que usa
- Output que genera

**Cuándo leer:** Cuando necesites entender QUÉ HACE cada archivo específico

**Tiempo estimado:** 20-30 minutos de lectura (o búsqueda rápida)

---

### 3. **Trading_Phantom_Documentation.pdf** (19 KB)
**Documentación profesional en PDF imprimible**

Contiene:
- 📄 Portada profesional
- 📋 Tabla de contenidos
- 📖 13 secciones completas:
  1. Introducción
  2. Características principales
  3. Requisitos técnicos
  4. Instalación
  5. Estructura del proyecto
  6. Arquitectura y diseño
  7. Machine Learning
  8. Knowledge Base (8 tipos)
  9. API REST
  10. Backtesting
  11. Empaquetado
  12. Solución de problemas
  13. Roadmap y conclusiones

**Características:**
- ✅ Tablas formateadas
- ✅ Colores corporativos (azul/naranja)
- ✅ Imprimible en excelente calidad
- ✅ A4 profesional
- ✅ Pie de página con metadata

**Cuándo leer:** Para imprimir, compartir o leer offline

**Tiempo estimado:** 20-30 minutos de lectura

---

### 4. **generate_pdf.py** (23 KB)
**Script que genera el PDF automáticamente**

Contiene:
- 🔧 Configuración de reportlab
- 📄 Estructura completa del PDF
- 🎨 Estilos profesionales
- 📊 Tablas y formatos

**Cómo usar:**
```powershell
pip install reportlab
python documentacion/generate_pdf.py
```

**Cuándo usar:** Cuando actualices la documentación y necesites regenerar el PDF

---

## 🎯 Guía de Lectura Recomendada

### Para **nuevos usuarios** (45 minutos):
1. Lee: README.md (Introducción + Instalación + Primera ejecución)
2. Ve: Dashboard en http://127.0.0.1:5000
3. Prueba: Backtesting básico
4. Leer: Sección de ML + Knowledge Base del README

### Para **desarrolladores** (2 horas):
1. Lee: README.md (Estructura + Arquitectura)
2. Lee: ARCHIVOS_Y_FUNCIONES.md (cada módulo)
3. Explorar: Código fuente (src/trading_phantom/)
4. Prueba: Tests unitarios (`python -m pytest`)
5. Experimenta: Modifica strategy.py y entrena modelo

### Para **investors/shareholders** (30 minutos):
1. Lee: README.md (¿Qué es + Características + Roadmap)
2. Mira: PDF (más profesional)
3. Ejecuta: Bot demo
4. Pregunta: Cualquier duda técnica

### Para **presentaciones** (20 minutos):
1. Imprime: PDF
2. Abre: Dashboard en pantalla
3. Ejecuta: Bot live demo
4. Refiere a: README.md para preguntas técnicas

---

## 📊 Estadísticas de Documentación

| Documento | Tamaño | Líneas | Tiempo Lectura | Tipo |
|-----------|--------|--------|----------------|------|
| README.md | 46 KB | 2000+ | 30-45 min | Guía completa |
| ARCHIVOS_Y_FUNCIONES.md | 25 KB | 700+ | 20-30 min | Referencia |
| Trading_Phantom_Documentation.pdf | 19 KB | N/A | 20-30 min | PDF profesional |
| **TOTAL** | **90 KB** | **2700+** | **1-2 horas** | Completa |

---

## 🔍 Búsqueda Rápida

### "¿Cómo instalo Trading Phantom?"
→ README.md → Sección "Instalación rápida"

### "¿Qué hace el archivo X?"
→ ARCHIVOS_Y_FUNCIONES.md → Busca el nombre del archivo

### "¿Cómo uso la API?"
→ README.md → Sección "API REST"

### "¿Qué es la Knowledge Base?"
→ README.md → Sección "Sistema de ML y Knowledge Base"

### "¿Cómo entreno el modelo ML?"
→ README.md → Sección "ML Training paso a paso"

### "¿Tengo un error. Qué hago?"
→ README.md → Sección "Solución de problemas"

### "¿Cuál es el roadmap?"
→ README.md → Sección "Roadmap"

### "Necesito imprimir documentación"
→ Trading_Phantom_Documentation.pdf

---

## 🚀 Próximos Pasos

### Después de leer la documentación:

1. **Instalar:**
   ```powershell
   .\INSTALL.bat
   .\RUN.bat
   ```

2. **Ejecutar backtesting:**
   - Accede a http://127.0.0.1:5000
   - Click en "Backtest"
   - Selecciona parámetros y ejecuta

3. **Entrenar ML (opcional):**
   ```powershell
   python scripts/ml_train.py
   ```

4. **Explorar API:**
   - GET http://127.0.0.1:5000/api/bot/status
   - POST http://127.0.0.1:5000/api/backtest
   - GET http://127.0.0.1:5000/api/knowledge/summary

5. **Revisar código:**
   - src/trading_phantom/core/orchestrator.py (inicio)
   - src/trading_phantom/modules/strategy.py (indicadores)
   - src/trading_phantom/analytics/ml_pipeline.py (ML)

---

## 📞 Soporte y Contacto

- **GitHub Issues:** https://github.com/blaspinto5/trading_phantom/issues
- **Documentación técnica:** Lee ARCHIVOS_Y_FUNCIONES.md
- **Código fuente:** Explore src/trading_phantom/
- **Logs:** Revise logs/ durante ejecución

---

## 📝 Versión y Licencia

- **Versión:** 1.1.0
- **Fecha:** Enero 2026
- **Licencia:** MIT (libre para usar y modificar)
- **Maintainer:** Peruano Pinto

---

<div align="center">

**¡Bienvenido a Trading Phantom!**

Esperamos que disfrutes del proyecto.
Si tienes preguntas, consulta la documentación arriba.

**[README.md](README.md) • [ARCHIVOS_Y_FUNCIONES.md](ARCHIVOS_Y_FUNCIONES.md) • [PDF](Trading_Phantom_Documentation.pdf)**

---

Made with ❤️ by the Trading Phantom community

</div>
