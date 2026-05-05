from __future__ import annotations

import cv2


def open_video_source(source: str):
    parsed = int(source) if source.isdigit() else source
    cap = cv2.VideoCapture(parsed)
    if not cap.isOpened():
        raise RuntimeError(f"Unable to open video source: {source}")
    return cap

