from __future__ import annotations

import time
from pathlib import Path

from rich.console import Console

from gd_trainable_bot.core.capture import ScreenCapturer
from gd_trainable_bot.core.input import InputController
from gd_trainable_bot.core.safety import SafetyController
from gd_trainable_bot.core.window import WindowDetector
from gd_trainable_bot.ml.agent import HybridAgent
from gd_trainable_bot.ml.dataset import StatsTracker
from gd_trainable_bot.utils.io import utc_stamp


def run_play_eval(cfg: dict) -> None:
    console = Console()
    detector = WindowDetector(cfg["window"]["title_keywords"])
    rect = detector.find_geometry_dash_window()
    if rect is None:
        console.print("[red]No se detectó Geometry Dash.[/red]")
        return

    best_model = Path(cfg["paths"]["checkpoints_dir"]) / "best_model.joblib"
    agent = HybridAgent(model_path=best_model)
    loaded = agent.load_if_exists()
    if not loaded:
        console.print("[yellow]No hay modelo entrenado: usando heurística base.[/yellow]")

    cap = ScreenCapturer(cfg["window"]["frame_width"], cfg["window"]["frame_height"])
    region = cap.from_window(rect, **cfg["window"]["capture"])
    input_ctrl = InputController(cfg["control"]["jump_key"])
    safety = SafetyController(cfg["control"]["emergency_stop_key"], cfg["control"]["pause_resume_key"])
    safety.start()

    scores = []
    for attempt in range(10):
        if safety.state.stop:
            break
        ticks = 0
        for _ in range(4000):
            while safety.state.paused and not safety.state.stop:
                time.sleep(0.1)
            if safety.state.stop:
                break
            frame = cap.capture_gray(region)
            decision = agent.act(frame)
            if decision.action == 1:
                input_ctrl.jump()
            ticks += 1
            time.sleep(cfg["runtime"]["tick_ms"] / 1000)
            if ticks > 60 and decision.confidence < 0.55:
                break
        scores.append(ticks)
        console.print(f"Intento {attempt + 1}: score={ticks}")

    safety.stop()
    if scores:
        session = {
            "mode": "play_eval",
            "timestamp": utc_stamp(),
            "attempts": len(scores),
            "best_score": max(scores),
            "avg_score": sum(scores) / len(scores),
            "model": str(best_model if loaded else "heuristic"),
        }
        StatsTracker(Path(cfg["paths"]["stats_file"])).append(session)
        console.print(f"[green]Mejor score:[/green] {session['best_score']}")
