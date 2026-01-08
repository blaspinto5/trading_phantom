## 🚀 BACKTESTING PARALELO - QUICK START

### ⚡ Ejecutar en paralelo SEGURO:

**Terminal 1 (Bot en vivo):**
```bash
python main.py --debug
```

**Terminal 2 (Backtesting paralelo):**
```bash
python run_backtest_parallel.py
# O directo:
python backtest_advanced_model.py
python backtest_improved_strategy.py
```

**Resultado:**
- ✅ Bot sigue operando
- ✅ Backtesting se ejecuta en paralelo
- ✅ Sin conflictos
- ✅ Sin interferencia

---

### 🔍 ¿Es seguro?

| Aspecto | Estado |
|---------|--------|
| **Conflicto BD** | ❌ NO (backtest es READ-ONLY) |
| **Modelo ML** | ❌ NO (cada proceso carga su copia) |
| **CPU** | ✅ Soportado |
| **RAM** | ✅ Suficiente |
| **Archivos** | ❌ NO (outputs diferentes) |

---

### 📊 Opciones:

1. **Backtesting básico:**
   ```bash
   python backtest_advanced_model.py
   ```

2. **Backtesting mejorado:**
   ```bash
   python backtest_improved_strategy.py
   ```

3. **Ambos simultáneamente:**
   ```bash
   python run_backtest_parallel.py
   # Selecciona opción 3
   ```

4. **Validar modelo:**
   ```bash
   python scripts/ml_train_advanced.py --no-save
   ```

---

### ⏱️ Cuándo ejecutar

- ✅ **Después de 48h:** Bot validado → Backtesting paralelo OK
- ❌ **Ahora:** Bot recién iniciado → Primero monitorea vivo
- ✅ **Día 3+:** Totalmente seguro

---

### 📈 Tiempo

- Backtesting: ~5-10 segundos
- Bot: Contínuo (no afectado)
- Total: Sin delay adicional

---

**Status:** SEGURO EJECUTAR EN PARALELO ✅
