"""Camera sensor abstraction with graceful fallback."""

from __future__ import annotations

from visionforall.core.events import Frame


class CameraSensor:
    """Capture frame from webcam when opencv is available."""

    def capture_frame(self) -> Frame:
        try:
            import cv2  # type: ignore

            cam = cv2.VideoCapture(0)
            ok, _frame = cam.read()
            cam.release()
            if ok:
                return Frame(source="camera:0", payload=_frame)
        except Exception:
            pass
        return Frame(source="mock-camera")
