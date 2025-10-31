# Pothole Detection System

A real-time wireframe pothole detection system for autonomous vehicles to slow down or avoid potholes and speed bumps on Indian roads.

This project detects and highlights road irregularities (potholes and speed bumps) in live video streams or recorded footage, drawing wireframe overlays and issuing alerts that an autonomous vehicle stack can use to react (slow down, avoid, or re-route).

---

## Table of Contents

- [Key features](#key-features)
- [Technologies](#technologies)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Real-time webcam / camera feed](#real-time-webcam--camera-feed)
  - [Run on video file](#run-on-video-file)
  - [Process images or folder of images](#process-images-or-folder-of-images)
- [Training (overview)](#training-overview)
- [Evaluation](#evaluation)
- [Project structure](#project-structure)
- [Tips for best results](#tips-for-best-results)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

---

## Key features

- Real-time detection of potholes and speed bumps using computer vision / deep learning.
- Wireframe overlay visualization to highlight the detected road defects.
- Alerts/messages suitable for integration with vehicle control modules (e.g., send slow-down command).
- Works on live camera streams, recorded video, and images.
- Designed with Indian road conditions in mind (uneven surfaces, varied lighting, occlusions).

---

## Technologies

The system is built with widely used open-source tools (examples — your repo may target a specific library):

- Python 3.8+
- OpenCV (for video/image capture and visualization)
- A deep-learning library (TensorFlow or PyTorch) for detection model(s)
- NumPy, scikit-learn (utilities)
- Optionally: CUDA/cuDNN for GPU acceleration

(Adjust the exact library names/versions to match the code in this repository.)

---

## Requirements

- Python 3.8 or newer
- pip
- (Optional) NVIDIA GPU with CUDA for faster inference/training

A minimal dependencies list is expected to be in requirements.txt — install it with:

```bash
pip install -r requirements.txt
```

If you use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate    # macOS / Linux
venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Jaz0XD/Pothole_Detection_System.git
cd Pothole_Detection_System
```

2. Install dependencies (see Requirements).

3. Download or place pre-trained model weights in the appropriate folder (e.g., `weights/` or as specified by the config). If this repository includes pretrained weights, follow the file/README instructions for their location.

---

## Usage

Note: Replace filenames/paths and CLI options below with the actual script names and flags in the repository.

### Real-time webcam / camera feed

Run the detector on a connected camera (webcam / vehicle camera):

```bash
python detect.py --source 0 --weights weights/latest.pth --display wireframe --save_output output/live_output.mp4
```

- --source: camera index (0) or a video RTSP/HTTP stream URL
- --weights: path to model weights
- --display: visualization mode (e.g., wireframe, boxes)
- --save_output: optional path to save annotated video

Expected result: a window showing live feed with potholes/speed bumps highlighted with wireframes and alert text. If integrated, alerts can be published to a message queue or socket.

### Run on a video file

```bash
python detect.py --source data/test_video.mp4 --weights weights/latest.pth --save_output output/annotated_video.mp4
```

### Process images or folder of images

```bash
python detect.py --source data/images/ --weights weights/latest.pth --output_dir output/images
```

Single image:

```bash
python detect.py --source data/images/sample.jpg --weights weights/latest.pth
```

---

## Training (overview)

If you want to train your own model:

1. Prepare dataset
   - Place labeled images and annotations in the `dataset/` folder.
   - Use a consistent annotation format (COCO, Pascal VOC, YOLO txt, etc.). See `dataset/README.md` (if present) for the required format.

2. Configure training
   - Edit `configs/train_config.yaml` (or the config file in the repo) to set dataset paths, hyperparameters, model architecture, and training epochs.

3. Start training:

```bash
python train.py --config configs/train_config.yaml --weights ''   # start training from scratch
```

To fine-tune from existing weights:

```bash
python train.py --config configs/train_config.yaml --weights weights/pretrained.pth
```

4. Checkpoints and logs
   - Checkpoints are saved to `weights/` by default.
   - Training logs (loss, metrics) can be written to `runs/` for visualization in TensorBoard.

---

## Evaluation

Use the evaluation script to compute detection metrics:

```bash
python evaluate.py --weights weights/best.pth --dataset dataset/val/
```

Common metrics:
- Precision / Recall
- mAP (mean Average Precision)
- Inference FPS (frames per second) — important for real-time use

---

## Project structure

A typical project layout (adjust to match repository contents):

- data/ or dataset/ — example videos / images and annotations
- weights/ — pretrained and saved model checkpoints
- src/ or pothole_detection/ — source code (detection, utils, models)
- detect.py — script to run detection on video/image/webcam
- train.py — training script
- evaluate.py — evaluation script
- requirements.txt — python dependencies
- README.md — this file

---

## Tips for best results

- Use a wide variety of training images that represent real Indian road scenarios: day/night, wet/dry, various occlusions, different vehicle speeds and camera heights.
- Perform data augmentation (brightness, contrast, perspective) to make the model robust.
- If you deploy on vehicle hardware, optimize the model (pruning, quantization) and test inference speed on the target device.
- Calibrate the camera and cropping: detection performance changes with mounting height and field of view.

---

## Contributing

Contributions are welcome! Contributions may include:

- Improving detection accuracy
- Adding support for more input sources (ROS topics, CAN bus integration)
- Improving the visualization and alerting logic
- Adding documentation, tests, and CI

To contribute:

1. Fork the repo
2. Create a feature branch: git checkout -b feature/my-change
3. Make changes and add tests if applicable
4. Open a pull request describing your changes

Please follow the code style used in the repository and add clear commit messages.

---

## License

This repository does not include an explicit license file. If you are the repo owner, add a LICENSE file (MIT, Apache-2.0, etc.). If you are a contributor, check the repository license before contributing.

---

## Contact

Project owner / maintainer: Jaz0XD

For questions, issues, or feature requests, please open an issue on the repository: https://github.com/Jaz0XD/Pothole_Detection_System/issues

---

## Acknowledgements

Thank you to all open-source libraries and datasets that make building real-time computer vision systems possible (OpenCV, PyTorch/TensorFlow, and the community datasets and annotation tools).

If you'd like, I can:
- Generate a minimal requirements.txt from the repository files,
- Draft an example command set tailored to the actual scripts present in the repo,
- Or create a CONTRIBUTING.md and issue / PR templates.
