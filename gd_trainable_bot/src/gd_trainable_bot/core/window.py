from __future__ import annotations

import ctypes
import ctypes.wintypes
from dataclasses import dataclass
from typing import Iterable


@dataclass
class WindowRect:
    left: int
    top: int
    right: int
    bottom: int

    @property
    def width(self) -> int:
        return self.right - self.left

    @property
    def height(self) -> int:
        return self.bottom - self.top


class WindowDetector:
    def __init__(self, title_keywords: Iterable[str]):
        self.title_keywords = [k.lower() for k in title_keywords]

    def find_geometry_dash_window(self) -> WindowRect | None:
        if not hasattr(ctypes, "windll"):
            return None

        user32 = ctypes.windll.user32
        windows: list[int] = []

        @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
        def enum_handler(hwnd, _lparam):
            if user32.IsWindowVisible(hwnd):
                length = user32.GetWindowTextLengthW(hwnd)
                if length > 0:
                    buff = ctypes.create_unicode_buffer(length + 1)
                    user32.GetWindowTextW(hwnd, buff, length + 1)
                    title = buff.value.lower()
                    if any(k in title for k in self.title_keywords):
                        windows.append(hwnd)
            return True

        user32.EnumWindows(enum_handler, 0)
        if not windows:
            return None

        rect = ctypes.wintypes.RECT()
        user32.GetWindowRect(windows[0], ctypes.byref(rect))
        return WindowRect(rect.left, rect.top, rect.right, rect.bottom)
