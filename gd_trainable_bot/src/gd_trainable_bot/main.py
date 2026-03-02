from __future__ import annotations

import argparse
from pathlib import Path

from rich.console import Console

from gd_trainable_bot.modes.calibration import run_calibration
from gd_trainable_bot.modes.data_collection import run_data_collection
from gd_trainable_bot.modes.play_eval import run_play_eval
from gd_trainable_bot.modes.stats import run_stats
from gd_trainable_bot.modes.training import run_training
from gd_trainable_bot.utils.config import load_config


def interactive_menu(cfg: dict) -> None:
    console = Console()
    options = {
        "1": ("Calibration", run_calibration),
        "2": ("Data Collection", run_data_collection),
        "3": ("Training", run_training),
        "4": ("Play / Evaluation", run_play_eval),
        "5": ("Stats", run_stats),
    }
    while True:
        console.print("\n[bold cyan]gd_trainable_bot[/bold cyan]")
        for key, (label, _) in options.items():
            console.print(f"{key}. {label}")
        console.print("0. Salir")
        choice = input("Selecciona una opción: ").strip()
        if choice == "0":
            return
        item = options.get(choice)
        if not item:
            console.print("[red]Opción inválida[/red]")
            continue
        item[1](cfg)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bot entrenable para Geometry Dash")
    parser.add_argument("--config", default=str(Path("config") / "default.yaml"))
    parser.add_argument("--mode", choices=["menu", "calibration", "collect", "training", "play", "stats"], default="menu")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = load_config(args.config)

    mode_map = {
        "menu": interactive_menu,
        "calibration": run_calibration,
        "collect": run_data_collection,
        "training": run_training,
        "play": run_play_eval,
        "stats": run_stats,
    }
    fn = mode_map[args.mode]
    fn(cfg)


if __name__ == "__main__":
    main()
