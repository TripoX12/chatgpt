from __future__ import annotations

from pathlib import Path

from rich.console import Console
from rich.table import Table

from gd_trainable_bot.ml.dataset import StatsTracker


def run_stats(cfg: dict) -> None:
    console = Console()
    tracker = StatsTracker(Path(cfg["paths"]["stats_file"]))
    payload = tracker.read()
    sessions = payload.get("sessions", [])
    if not sessions:
        console.print("[yellow]Aún no hay estadísticas.[/yellow]")
        return

    table = Table(title="Resumen de sesiones")
    table.add_column("Modo")
    table.add_column("Timestamp")
    table.add_column("Best")
    table.add_column("Avg/Val")
    table.add_column("Checkpoint/Archivo")

    for s in sessions[-15:]:
        best = str(s.get("best_score", s.get("death_point", "-")))
        avg = str(round(s.get("avg_score", s.get("val_accuracy", 0.0)), 3))
        cp = s.get("checkpoint", s.get("file", s.get("model", "-")))
        table.add_row(s.get("mode", "-"), s.get("timestamp", "-"), best, avg, cp)

    console.print(table)
