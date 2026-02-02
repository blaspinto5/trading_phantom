# ⚡ Quick Start - Trading Phantom

## 🚀 Instalación (30 segundos)

### Opción 1: Doble-click (Más fácil)
1. **Windows Explorer**: Ve a la carpeta del proyecto
2. **Doble-click**: `INSTALL.bat`
3. **Espera**: ~1-2 minutos mientras instala
4. **Responde**: ¿Ejecutar ahora? Presiona `s` + Enter

### Opción 2: PowerShell
```powershell
.\INSTALL.ps1
```

Eso es todo. ✅

---

## ▶️ Ejecutar la aplicación

### Opción 1: Doble-click (Más fácil)
- **Doble-click**: `RUN.bat`
- La aplicación se abre en http://127.0.0.1:5000

### Opción 2: PowerShell
```powershell
.\RUN.ps1
```

---

## 📊 ¿Qué puedo hacer?

Una vez que abra la aplicación:

### 🤖 Bot Trading
- Inicia el bot automático
- Conecta con MetaTrader 5
- Ejecuta órdenes en tiempo real

### 📈 Backtesting
- Prueba estrategias con datos históricos
- Visualiza resultados interactivamente
- Calcula métricas (Sharpe, DrawDown, etc)

### 📊 Logs y monitoreo
- Ve logs en tiempo real
- Monitorea estado del bot
- Accede a histórico de operaciones

---

## 🆘 Problemas?

### "Python no encontrado"
→ Descarga desde: https://www.python.org/downloads/ (3.10+)

### "El puerto 5000 está en uso"
→ Edita `src/trading_phantom/webapp.py` línea ~195 y cambia el puerto

### "MetaTrader 5 no se conecta"
→ Abre MetaTrader 5 antes de iniciar el bot

### ¿Más ayuda?
→ Ver: `docs/QUICKSTART.md` (guía detallada)

---

## 📚 Documentación completa

- **docs/README.md** — Guía completa con todos los detalles
- **docs/QUICKSTART.md** — Instalación paso a paso (5 min)
- **docs/API.md** — Endpoints REST con ejemplos
- **docs/ARCHITECTURE.md** — Diseño técnico y patrones
- **CONTRIBUTING.md** — Cómo contribuir al proyecto
- **CHANGELOG.md** — Historial de cambios

---

## 🎯 Próximos pasos

1. ✅ **Instalar**: `INSTALL.bat` o `INSTALL.ps1`
2. ✅ **Ejecutar**: `RUN.bat` o `RUN.ps1`
3. 📖 **Leer**: Ver documentación en `docs/`
4. 🤖 **Explorar**: Prueba el bot o backtesting
5. 🔧 **Configurar**: Edita `src/trading_phantom/config/config.yaml`

---

**¿Listo?** 🚀

```
Opción 1 (recomendado): Doble-click INSTALL.bat
Opción 2: .\INSTALL.ps1 en PowerShell
```

**Preguntas?** Ver `docs/QUICKSTART.md`
