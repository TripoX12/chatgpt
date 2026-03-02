from __future__ import annotations

import time
from dataclasses import dataclass

from pynput.keyboard import Controller, Key


@dataclass
class ControlState:
    paused: bool = False
    stop: bool = False


class InputController:
    def __init__(self, jump_key: str = "space"):
        self.keyboard = Controller()
        self.jump_key = Key.space if jump_key.lower() == "space" else jump_key

    def jump(self, hold_ms: int = 35) -> None:
        self.keyboard.press(self.jump_key)
        time.sleep(hold_ms / 1000)
        self.keyboard.release(self.jump_key)
