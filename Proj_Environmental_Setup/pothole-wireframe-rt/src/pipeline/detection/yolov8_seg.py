import torch
import cv2
import numpy as np
from ultralytics import YOLO

class YOLOv8Segmentation:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def preprocess(self, frame):
        # Resize and normalize the frame
        frame_resized = cv2.resize(frame, (640, 640))
        frame_normalized = frame_resized / 255.0
        return frame_normalized

    def detect(self, frame):
        # Preprocess the frame
        processed_frame = self.preprocess(frame)

        # Perform inference
        results = self.model(processed_frame)

        # Extract masks and bounding boxes
        masks = results[0].masks.xy
        boxes = results[0].boxes.xyxy

        return masks, boxes

    def draw_masks(self, frame, masks):
        for mask in masks:
            mask = mask.cpu().numpy().astype(np.uint8)
            color = (0, 255, 0)  # Green color for masks
            frame[mask > 0] = color
        return frame

    def run(self, video_source=0):
        cap = cv2.VideoCapture(video_source)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            masks, boxes = self.detect(frame)
            frame_with_masks = self.draw_masks(frame, masks)

            cv2.imshow('Pothole Detection', frame_with_masks)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    model_path = 'weights/yolo/best.pt'  # Path to the YOLOv8 model weights
    yolo_segmentation = YOLOv8Segmentation(model_path)
    yolo_segmentation.run()