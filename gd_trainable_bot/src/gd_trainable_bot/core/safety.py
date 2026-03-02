from __future__ import annotations

import threading

from pynput import keyboard

from gd_trainable_bot.core.input import ControlState


class SafetyController:
    def __init__(self, emergency_key: str = "f8", pause_key: str = "f9"):
        self.state = ControlState()
        self.emergency_key = emergency_key.lower()
        self.pause_key = pause_key.lower()
        self._listener: keyboard.Listener | None = None
        self._lock = threading.Lock()

    def start(self) -> None:
        def on_press(key):
            key_name = getattr(key, "name", None) or getattr(key, "char", "")
            key_name = str(key_name).lower()
            with self._lock:
                if key_name == self.emergency_key:
                    self.state.stop = True
                if key_name == self.pause_key:
                    self.state.paused = not self.state.paused

        self._listener = keyboard.Listener(on_press=on_press)
        self._listener.daemon = True
        self._listener.start()

    def stop(self) -> None:
        if self._listener:
            self._listener.stop()
