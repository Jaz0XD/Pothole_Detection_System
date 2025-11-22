import time
import numpy as np
import cv2
from src.pipeline.detection.yolov8_seg import YOLOv8Seg
from src.pipeline.depth.midas import MiDaS
from src.pipeline.reconstruction.mesh import generate_mesh
from src.pipeline.geometry.measurements import calculate_geometry

def benchmark_detection_pipeline(video_source=0, num_frames=100):
    # Initialize models
    yolo_model = YOLOv8Seg()
    depth_model = MiDaS()

    # Start video capture
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print("Error: Could not open video source.")
        return

    frame_times = []
    geometry_results = []

    for _ in range(num_frames):
        start_time = time.time()

        # Capture frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Detection
        masks = yolo_model.detect(frame)

        # Depth estimation
        depth_map = depth_model.estimate_depth(frame)

        # Generate mesh
        mesh = generate_mesh(masks, depth_map)

        # Calculate geometry
        geometry = calculate_geometry(mesh)
        geometry_results.append(geometry)

        # Calculate frame processing time
        frame_time = time.time() - start_time
        frame_times.append(frame_time)

        # Display results (optional)
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release video capture
    cap.release()
    cv2.destroyAllWindows()

    # Calculate average processing time
    avg_time = np.mean(frame_times)
    print(f"Average processing time per frame: {avg_time:.4f} seconds")
    print(f"Geometry results: {geometry_results}")

if __name__ == "__main__":
    benchmark_detection_pipeline()