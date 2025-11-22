# Setup Instructions for Real-Time Pothole Detection System

## Prerequisites

Before setting up the project, ensure that you have the following installed on your system:

- **Operating System**: Ubuntu 20.04/22.04 (recommended) or Windows 10/11 (optional)
- **Python**: Version 3.10 or higher
- **Anaconda**: For managing the Python environment
- **CUDA Toolkit**: If using a GPU for acceleration

## Environment Setup

1. **Clone the Repository**

   Clone the project repository from GitHub (or your source) to your local machine:

   ```bash
   git clone <repository-url>
   cd pothole-wireframe-rt
   ```

2. **Create a Conda Environment**

   Create a new conda environment for the project:

   ```bash
   conda create -n pothole_env python=3.10
   conda activate pothole_env
   ```

3. **Install Required Packages**

   Install the necessary Python packages using pip:

   ```bash
   pip install ultralytics
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   pip install opencv-python
   pip install open3d
   pip install matplotlib numpy scipy
   ```

4. **Install Additional Dependencies**

   If you have an `environment.yml` file, you can also install dependencies using:

   ```bash
   conda env update --file environment.yml
   ```

## Configuration

1. **Camera Configuration**

   Edit the `configs/camera.yaml` file to set up your camera parameters, such as resolution and frame rate.

2. **Dataset Configuration**

   Update the `configs/dataset.yaml` file to specify the paths to your dataset, including raw images and annotations.

3. **Model Configuration**

   Adjust the model settings in `configs/detection_yolov8.yaml` and `configs/depth_midas.yaml` as needed for your specific use case.

## Running the Application

To run the real-time pothole detection application, execute the following command:

```bash
python src/app.py
```

## Testing

To run the unit tests for the project, use the following command:

```bash
pytest tests/
```

## Additional Notes

- Ensure that your camera is connected and recognized by the system before running the application.
- For optimal performance, it is recommended to use a machine with a dedicated GPU.
- Refer to the `README.md` file for more detailed information about the project and its components.

This setup guide provides a comprehensive overview of the steps required to get the real-time pothole detection system up and running.