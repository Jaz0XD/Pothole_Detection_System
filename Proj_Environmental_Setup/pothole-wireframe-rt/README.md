# Real-Time Wireframe-Based Pothole Detection and Avoidance System

## Overview
This project aims to develop a low-cost, camera-only real-time pothole detection and avoidance system suitable for autonomous vehicles and road maintenance. The system utilizes a monocular camera to capture road images, processes these images to detect potholes and other anomalies, estimates depth, and generates 3D wireframe meshes for accurate geometry analysis.

## Project Structure
The project is organized into several directories and files, each serving a specific purpose:

- **src/**: Contains the main application code.
  - **app.py**: Main entry point for the application.
  - **pipeline/**: Implements the detection pipeline.
    - **capture/**: Handles video frame capture from the camera.
    - **preprocess/**: Contains preprocessing functions for image normalization and resizing.
    - **detection/**: Implements the YOLOv8 segmentation model for pothole detection.
    - **depth/**: Contains depth estimation models (MiDaS and DepthAnything V2).
    - **fusion/**: Integrates depth data with detected anomalies to create point clouds.
    - **reconstruction/**: Generates 3D meshes from point clouds.
    - **geometry/**: Includes functions for calculating geometric properties.
    - **decision/**: Implements decision-making logic for speed adjustments and avoidance maneuvers.
    - **visualization/**: Provides functions for visualizing detected potholes and generated meshes.
    - **io/**: Handles logging and exporting results.
    - **utils/**: Contains utility functions and configuration settings.
  - **types/**: Defines custom types used in the project.

- **configs/**: Contains configuration files for various components of the system.
- **scripts/**: Includes scripts for running the pipeline, calibrating the camera, downloading weights, training the YOLO model, and benchmarking.
- **notebooks/**: Jupyter notebooks for exploratory data analysis and model evaluation.
- **data/**: Directories for storing raw, processed images, and annotations.
- **weights/**: Directories for storing model weights for YOLO and depth estimation.
- **tests/**: Contains unit tests for various components of the project.
- **docs/**: Documentation files for system architecture, API, and setup instructions.
- **.vscode/**: Configuration files for the Visual Studio Code environment.
- **.gitignore**: Specifies files and directories to be ignored by Git.
- **environment.yml**: Lists dependencies for the project in a conda environment.
- **requirements.txt**: Lists Python packages required for the project.
- **pyproject.toml**: Contains project metadata and dependencies for Python packaging.
- **LICENSE**: Licensing information for the project.

## Getting Started
To set up the project environment, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd pothole-wireframe-rt
   ```

2. Create and activate the conda environment:
   ```
   conda env create -f environment.yml
   conda activate pothole_env
   ```

3. Install additional requirements:
   ```
   pip install -r requirements.txt
   ```

4. Configure the camera settings in `configs/camera.yaml`.

5. Run the real-time detection pipeline:
   ```
   python scripts/run_realtime.py
   ```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.