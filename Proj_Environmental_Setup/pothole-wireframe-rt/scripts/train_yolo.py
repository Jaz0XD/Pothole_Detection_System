import os
import yaml
import torch
from ultralytics import YOLO
from pathlib import Path

def load_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def train_yolo_model(config):
    model = YOLO(config['model']['path'])
    model.train(data=config['dataset']['path'], epochs=config['training']['epochs'])

def main():
    # Load configuration
    config_path = Path(__file__).parent.parent / 'configs' / 'detection_yolov8.yaml'
    config = load_config(config_path)

    # Train the YOLO model
    train_yolo_model(config)

if __name__ == "__main__":
    main()