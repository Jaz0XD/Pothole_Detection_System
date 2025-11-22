# Contents of /pothole-wireframe-rt/pothole-wireframe-rt/src/pipeline/utils/config.py

import os

class Config:
    def __init__(self):
        # Camera configuration
        self.camera = {
            'width': 1280,
            'height': 720,
            'fps': 30,
            'device_index': 0  # Default camera index
        }

        # Model configuration
        self.models = {
            'yolo': {
                'weights_path': os.path.join('weights', 'yolo', 'yolov8_weights.pt'),
                'conf_threshold': 0.5,
                'iou_threshold': 0.4
            },
            'depth': {
                'midas_weights_path': os.path.join('weights', 'depth', 'midas_weights.pt'),
                'depthanything_weights_path': os.path.join('weights', 'depth', 'depthanything_weights.pt')
            }
        }

        # Processing configuration
        self.processing = {
            'resize': (640, 480),  # Resize dimensions for input
            'normalization': {
                'mean': [0.485, 0.456, 0.406],
                'std': [0.229, 0.224, 0.225]
            }
        }

        # Logging configuration
        self.logging = {
            'log_file': 'pipeline.log',
            'log_level': 'INFO'
        }

        # Output configuration
        self.output = {
            'results_dir': 'results',
            'visualization_dir': 'visualizations'
        }