from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier


@dataclass
class AgentDecision:
    action: int
    confidence: float


class HybridAgent:
    """Agente híbrido:
    1) Heurística simple basada en borde frontal
    2) Si hay modelo entrenado, usa modelo supervisado
    """

    def __init__(self, model_path: Path | None = None, n_estimators: int = 200, max_depth: int = 12):
        self.model_path = model_path
        self.model = None
        self.clf_params = {"n_estimators": n_estimators, "max_depth": max_depth, "random_state": 42}

    def load_if_exists(self) -> bool:
        if self.model_path and self.model_path.exists():
            self.model = joblib.load(self.model_path)
            return True
        return False

    def featurize(self, frame: np.ndarray) -> np.ndarray:
        edges = np.abs(np.diff(frame.astype(np.float32), axis=1))
        edge_signal = edges[:, -40:].mean()
        lower_lane = frame[int(frame.shape[0] * 0.65):, :].mean()
        return np.array([frame.mean(), frame.std(), edge_signal, lower_lane], dtype=np.float32)

    def heuristic(self, frame: np.ndarray) -> AgentDecision:
        feat = self.featurize(frame)
        action = 1 if feat[2] > 17.5 else 0
        confidence = min(0.95, max(0.55, feat[2] / 40))
        return AgentDecision(action=action, confidence=float(confidence))

    def act(self, frame: np.ndarray) -> AgentDecision:
        x = self.featurize(frame).reshape(1, -1)
        if self.model is None:
            return self.heuristic(frame)
        proba = self.model.predict_proba(x)[0]
        action = int(np.argmax(proba))
        return AgentDecision(action=action, confidence=float(proba[action]))

    def train(self, x: np.ndarray, y: np.ndarray) -> dict[str, float]:
        model = RandomForestClassifier(**self.clf_params)
        model.fit(x, y)
        self.model = model
        return {"train_accuracy": float(model.score(x, y))}

    def save(self) -> None:
        if self.model_path is None or self.model is None:
            return
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, self.model_path)
