from __future__ import annotations

import time
from pathlib import Path

from rich.console import Console

from gd_trainable_bot.core.capture import ScreenCapturer
from gd_trainable_bot.core.input import InputController
from gd_trainable_bot.core.safety import SafetyController
from gd_trainable_bot.core.window import WindowDetector
from gd_trainable_bot.ml.agent import HybridAgent
from gd_trainable_bot.ml.dataset import DatasetManager, StatsTracker
from gd_trainable_bot.utils.io import utc_stamp


def run_data_collection(cfg: dict) -> None:
    console = Console()
    detector = WindowDetector(cfg["window"]["title_keywords"])
    rect = detector.find_geometry_dash_window()
    if rect is None:
        console.print("[red]No se encontró Geometry Dash. Abortando.[/red]")
        return

    cap = ScreenCapturer(cfg["window"]["frame_width"], cfg["window"]["frame_height"])
    region = cap.from_window(rect, **cfg["window"]["capture"])
    input_ctrl = InputController(cfg["control"]["jump_key"])
    safety = SafetyController(cfg["control"]["emergency_stop_key"], cfg["control"]["pause_resume_key"])
    safety.start()

    manager = DatasetManager(Path(cfg["paths"]["raw_data_dir"]), Path(cfg["paths"]["processed_data_dir"]))
    stats = StatsTracker(Path(cfg["paths"]["stats_file"]))
    agent = HybridAgent()

    attempts = cfg["collection"]["attempts_per_run"]
    tick = cfg["runtime"]["tick_ms"] / 1000

    console.print("[cyan]Recolectando datos... F8=stop, F9=pause[/cyan]")
    for i in range(attempts):
        if safety.state.stop:
            break

        samples = []
        start = time.time()
        for step in range(3000):
            while safety.state.paused and not safety.state.stop:
                time.sleep(0.1)
            if safety.state.stop:
                break

            frame = cap.capture_gray(region)
            decision = agent.heuristic(frame)
            if decision.action == 1:
                input_ctrl.jump()

            samples.append({"features": agent.featurize(frame).tolist(), "action": decision.action})
            time.sleep(tick)

            if step > 60 and decision.confidence < 0.58:
                break

        duration = time.time() - start
        progress = len(samples)
        summary = {
            "attempt_id": f"{utc_stamp()}_{i}",
            "duration_sec": round(duration, 2),
            "death_point": progress,
            "distance_metric": progress,
            "timestamp": utc_stamp(),
        }
        out_path = manager.write_attempt(samples, summary)
        stats.append({"mode": "collection", "attempt": i + 1, **summary, "file": str(out_path)})
        console.print(f"Intento {i + 1}/{attempts}: {progress} ticks guardados")

    safety.stop()
    console.print("[green]Recolección finalizada.[/green]")
