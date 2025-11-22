from flask import Flask
from pipeline.capture.camera import Camera
from pipeline.preprocess.transforms import preprocess_frame
from pipeline.detection.yolov8_seg import detect_potholes
from pipeline.depth.midas import estimate_depth
from pipeline.fusion.pointcloud import create_pointcloud
from pipeline.reconstruction.mesh import generate_mesh
from pipeline.geometry.measurements import calculate_geometry
from pipeline.decision.engine import DecisionEngine
from pipeline.visualization.viewer import visualize_results
from pipeline.io.logger import Logger

app = Flask(__name__)

# Initialize components
camera = Camera()
logger = Logger()
decision_engine = DecisionEngine()

@app.route('/start', methods=['GET'])
def start_detection():
    logger.log("Starting real-time pothole detection.")
    while True:
        frame = camera.capture_frame()
        preprocessed_frame = preprocess_frame(frame)
        pothole_masks = detect_potholes(preprocessed_frame)
        depth_map = estimate_depth(preprocessed_frame)
        pointcloud = create_pointcloud(pothole_masks, depth_map)
        mesh = generate_mesh(pointcloud)
        geometry = calculate_geometry(mesh)
        decision = decision_engine.make_decision(geometry)
        visualize_results(frame, pothole_masks, mesh)

        if decision['action'] == 'slow_down':
            logger.log("Action: Slow down.")
        elif decision['action'] == 'avoid':
            logger.log("Action: Avoid obstacle.")

    return "Detection started."

if __name__ == '__main__':
    app.run(debug=True)