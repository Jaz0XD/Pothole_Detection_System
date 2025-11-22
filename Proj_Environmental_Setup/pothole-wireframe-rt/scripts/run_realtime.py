import cv2
import torch
from src.pipeline.capture.camera import Camera
from src.pipeline.preprocess.transforms import preprocess_frame
from src.pipeline.detection.yolov8_seg import YOLOv8Seg
from src.pipeline.depth.midas import MiDaS
from src.pipeline.fusion.pointcloud import create_point_cloud
from src.pipeline.reconstruction.mesh import generate_mesh
from src.pipeline.geometry.measurements import calculate_geometry
from src.pipeline.decision.engine import DecisionEngine
from src.pipeline.visualization.viewer import visualize_results

def run_realtime_detection():
    # Initialize camera
    camera = Camera()
    
    # Load models
    detection_model = YOLOv8Seg()
    depth_model = MiDaS()
    decision_engine = DecisionEngine()

    while True:
        # Capture frame
        frame = camera.get_frame()
        
        # Preprocess frame
        preprocessed_frame = preprocess_frame(frame)
        
        # Detect anomalies
        detections = detection_model.detect(preprocessed_frame)
        
        # Estimate depth
        depth_map = depth_model.estimate_depth(preprocessed_frame)
        
        # Create point cloud
        point_cloud = create_point_cloud(detections, depth_map)
        
        # Generate mesh
        mesh = generate_mesh(point_cloud)
        
        # Calculate geometry
        geometry = calculate_geometry(mesh)
        
        # Make decisions
        decision = decision_engine.make_decision(geometry)
        
        # Visualize results
        visualize_results(frame, detections, depth_map, mesh, decision)

        # Break loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_realtime_detection()