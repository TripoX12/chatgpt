from __future__ import annotations

from dataclasses import dataclass

import cv2
import mss
import numpy as np

from gd_trainable_bot.core.window import WindowRect


@dataclass
class CaptureRegion:
    top: int
    left: int
    width: int
    height: int


class ScreenCapturer:
    def __init__(self, out_w: int, out_h: int):
        self.out_w = out_w
        self.out_h = out_h
        self.sct = mss.mss()

    def from_window(self, rect: WindowRect, top_ratio: float, bottom_ratio: float, left_ratio: float, right_ratio: float) -> CaptureRegion:
        w = rect.width
        h = rect.height
        top = rect.top + int(h * top_ratio)
        bottom = rect.top + int(h * bottom_ratio)
        left = rect.left + int(w * left_ratio)
        right = rect.left + int(w * right_ratio)
        return CaptureRegion(top=top, left=left, width=max(32, right - left), height=max(32, bottom - top))

    def capture_gray(self, region: CaptureRegion) -> np.ndarray:
        raw = np.array(self.sct.grab(region.__dict__))
        bgr = cv2.cvtColor(raw, cv2.COLOR_BGRA2BGR)
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        return cv2.resize(gray, (self.out_w, self.out_h), interpolation=cv2.INTER_AREA)
