from __future__ import annotations

from pathlib import Path

import numpy as np

from gd_trainable_bot.utils.io import ensure_dir, load_json, save_json, utc_stamp


class DatasetManager:
    def __init__(self, raw_dir: Path, processed_dir: Path):
        self.raw_dir = ensure_dir(raw_dir)
        self.processed_dir = ensure_dir(processed_dir)

    def write_attempt(self, samples: list[dict], summary: dict) -> Path:
        run_id = utc_stamp()
        out = self.raw_dir / f"attempt_{run_id}.npz"
        x = np.array([s["features"] for s in samples], dtype=np.float32)
        y = np.array([s["action"] for s in samples], dtype=np.int64)
        np.savez_compressed(out, x=x, y=y, summary=summary)
        return out

    def load_all(self) -> tuple[np.ndarray, np.ndarray]:
        files = sorted(self.raw_dir.glob("attempt_*.npz"))
        if not files:
            return np.empty((0, 4), dtype=np.float32), np.empty((0,), dtype=np.int64)
        xs = []
        ys = []
        for f in files:
            data = np.load(f, allow_pickle=True)
            xs.append(data["x"])
            ys.append(data["y"])
        return np.vstack(xs), np.hstack(ys)


class StatsTracker:
    def __init__(self, stats_file: Path):
        self.stats_file = stats_file

    def append(self, session: dict) -> None:
        payload = load_json(self.stats_file, default={"sessions": []})
        payload.setdefault("sessions", []).append(session)
        save_json(self.stats_file, payload)

    def read(self) -> dict:
        return load_json(self.stats_file, default={"sessions": []})
