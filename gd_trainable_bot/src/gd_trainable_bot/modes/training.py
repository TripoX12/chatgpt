from __future__ import annotations

from pathlib import Path

from rich.console import Console
from sklearn.model_selection import train_test_split

from gd_trainable_bot.ml.agent import HybridAgent
from gd_trainable_bot.ml.dataset import DatasetManager, StatsTracker
from gd_trainable_bot.utils.io import utc_stamp


def run_training(cfg: dict) -> None:
    console = Console()
    manager = DatasetManager(Path(cfg["paths"]["raw_data_dir"]), Path(cfg["paths"]["processed_data_dir"]))
    x, y = manager.load_all()
    if len(y) < 100:
        console.print("[red]Datos insuficientes. Recolecta más intentos.[/red]")
        return

    x_train, x_val, y_train, y_val = train_test_split(
        x, y, test_size=cfg["training"]["test_split"], random_state=cfg["training"]["random_state"]
    )

    ckpt = Path(cfg["paths"]["checkpoints_dir"]) / f"model_{utc_stamp()}.joblib"
    agent = HybridAgent(model_path=ckpt, n_estimators=cfg["training"]["n_estimators"], max_depth=cfg["training"]["max_depth"])
    train_metrics = agent.train(x_train, y_train)
    val_acc = agent.model.score(x_val, y_val)
    agent.save()

    best_alias = Path(cfg["paths"]["checkpoints_dir"]) / "best_model.joblib"
    best_alias.write_bytes(ckpt.read_bytes())

    stats = StatsTracker(Path(cfg["paths"]["stats_file"]))
    stats.append(
        {
            "mode": "training",
            "timestamp": utc_stamp(),
            "samples": int(len(y)),
            "train_accuracy": train_metrics["train_accuracy"],
            "val_accuracy": float(val_acc),
            "checkpoint": str(ckpt),
        }
    )

    console.print(f"[green]Entrenamiento completado.[/green] val_acc={val_acc:.3f}")
    console.print(f"Checkpoint: {ckpt}")
