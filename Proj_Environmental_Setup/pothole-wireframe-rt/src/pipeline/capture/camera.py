import cv2

class Camera:
    def __init__(self, camera_index=0, width=640, height=480):
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.cap = None

    def initialize(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

    def capture_frame(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                return frame
        return None

    def release(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def __del__(self):
        self.release()