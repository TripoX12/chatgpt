from __future__ import annotations

from rich.console import Console

from gd_trainable_bot.core.capture import ScreenCapturer
from gd_trainable_bot.core.input import InputController
from gd_trainable_bot.core.window import WindowDetector


def run_calibration(cfg: dict) -> None:
    console = Console()
    detector = WindowDetector(cfg["window"]["title_keywords"])
    rect = detector.find_geometry_dash_window()
    if rect is None:
        console.print("[red]No se encontró ventana de Geometry Dash.[/red]")
        return

    cap = ScreenCapturer(cfg["window"]["frame_width"], cfg["window"]["frame_height"])
    crop = cap.from_window(rect, **cfg["window"]["capture"])
    frame = cap.capture_gray(crop)
    console.print(f"[green]Ventana detectada:[/green] {rect}")
    console.print(f"[green]Región de captura:[/green] {crop}")
    console.print(f"[green]Frame OK:[/green] shape={frame.shape}")

    answer = input("¿Enviar un salto de prueba (space)? [s/N]: ").strip().lower()
    if answer == "s":
        InputController(cfg["control"]["jump_key"]).jump()
        console.print("[yellow]Salto enviado.[/yellow]")
