# gd_trainable_bot (Windows)

Proyecto local y entrenable para jugar **Geometry Dash real** por captura de pantalla + simulación de teclado.

## Qué hace esta primera versión

- Detecta la ventana de Geometry Dash por título.
- Captura la región de juego en tiempo real.
- Toma decisiones binarias: `jump` / `no jump`.
- Puede ejecutar partidas automáticas.
- Guarda datos por intento para reentrenar.
- Entrena un modelo supervisado local (`RandomForest`) y guarda checkpoints.
- Carga el último modelo (alias `best_model.joblib`) para jugar/evaluar.
- Registra métricas históricas para comparar evolución.

> Enfoque elegido: **híbrido y realista**.
> 1) Heurística simple para empezar sin datos.
> 2) Recolección de dataset en partidas reales.
> 3) Entrenamiento supervisado incremental con checkpoints persistentes.
> Esto permite funcionar desde el día 1 y mejorar con el tiempo sin depender de cloud.

---

## Estructura

- `src/gd_trainable_bot/` código principal
- `config/default.yaml` configuración central
- `data/raw/` intentos recolectados (`npz`)
- `data/processed/` estadísticas y derivados
- `checkpoints/` modelos entrenados
- `logs/` espacio para logs
- `scripts/` instalador y lanzadores para Windows

---

## Requisitos (Windows)

1. Windows 10/11
2. Python 3.10+
3. Geometry Dash instalado y ejecutándose en ventana visible.

---

## Instalación (fácil)

1. Abre **CMD** dentro de la carpeta `gd_trainable_bot`.
2. Ejecuta:

```bat
scripts\install_windows.bat
```

Esto crea `.venv`, instala dependencias y el comando `gd-bot`.

---

## Uso rápido (sin programar)

### Opción A: menú interactivo

```bat
scripts\run_menu.bat
```

Verás estas opciones:
1. Calibration
2. Data Collection
3. Training
4. Play / Evaluation
5. Stats

### Opción B: ejecutar modo directo

```bat
scripts\run_mode.bat calibration
scripts\run_mode.bat collect
scripts\run_mode.bat training
scripts\run_mode.bat play
scripts\run_mode.bat stats
```

---

## Flujo recomendado (primera semana)

1. **Calibration**
   - valida detección de ventana,
   - valida captura,
   - prueba envío de salto.
2. **Data Collection** (varias sesiones)
   - recolecta intentos automáticos.
3. **Training**
   - entrena checkpoint local.
4. **Play / Evaluation**
   - compara rendimiento contra histórico.
5. **Stats**
   - revisa evolución.

Repite 2→3→4 para mejorar progresivamente.

---

## Seguridad y control

- **F8**: parada de emergencia.
- **F9**: pausa/reanudar.
- Si no encuentra la ventana del juego, no envía inputs.

---

## Configuración rápida

Edita `config/default.yaml`:

- `window.title_keywords`: títulos para detectar Geometry Dash.
- `window.capture.*_ratio`: recorte de área útil.
- `control.jump_key`: tecla de salto (por defecto `space`).
- `collection.attempts_per_run`: cantidad de intentos por sesión.
- `training.*`: hiperparámetros del modelo.

---

## Qué mejorar después (roadmap)

1. Detector de muerte/avance más robusto por visión (HUD/progreso).
2. Features temporales (stack de frames o diferencia entre frames).
3. Política con red neuronal ligera (PyTorch local).
4. Entrenamiento online por lotes al terminar cada sesión.
5. Perfil por nivel (modelos separados por mapa).

---

## Nota legal y práctica

Uso experimental local en tu PC. Respeta términos del juego/plataforma. Este proyecto evita técnicas invasivas (inyección de memoria/mods) y usa solo visión + input simulado.
