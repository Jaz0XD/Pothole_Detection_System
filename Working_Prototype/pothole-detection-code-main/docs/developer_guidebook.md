# Pothole Detection Prototype Guidebook

## 1. Purpose

This repository is a Python-based pothole detection prototype for an RC car workflow. It combines:

- live video capture from a webcam, video file, or ESP32-CAM stream
- pothole detection using either a heuristic detector or YOLO
- monocular depth estimation
- geometric approximation of pothole distance, width, length, and depth
- a small telemetry dashboard
- optional pseudo-label capture for online learning
- optional serial output to a motor-control microcontroller

This document is both:

- a developer guide for starting and understanding the project
- a practical manual outline for an end-user/operator document

## 2. Current Codebase Summary

The main runtime entry point is [app.py](D:\PERSONAL\RGCET\FINAL YEAR PROJECT\Working_Prototype\pothole-detection-code-main\app.py), which forwards into [src/pothole_detection/app.py](D:\PERSONAL\RGCET\FINAL YEAR PROJECT\Working_Prototype\pothole-detection-code-main\src\pothole_detection\app.py).

Core subsystems:

- `vision.capture`: opens the video source
- `models.detector`: heuristic or YOLO pothole detection
- `models.depth`: proxy, MiDaS, Depth Anything, or hybrid depth estimation
- `vision.wireframe`: depth-based wireframe overlay and severity scoring inputs
- `vision.geometry`: approximates real-world distance and pothole dimensions
- `control.policy`: converts severity into `CRUISE`, `SLOW`, or `AVOID`
- `control.serial_bridge`: sends commands to a serial-connected controller
- `dashboard.server`: exposes telemetry over HTTP
- `learning.online`: stores high-confidence detections as pseudo-labeled samples

## 3. Prerequisites

### Software

- Python 3.10 or newer
- `pip`
- OpenCV-compatible camera drivers if using a webcam
- Arduino IDE if you want to flash the ESP32 motor controller sketch

### Optional ML/runtime dependencies

The project package only declares base dependencies:

- `numpy`
- `opencv-python`

Extra features require manual installation:

- `pyserial` for serial communication
- `torch` and `torchvision` for MiDaS
- `ultralytics` for YOLO training and YOLO inference
- `transformers` and `pillow` for Depth Anything

### Hardware

Depending on the mode you want:

- laptop webcam, or
- USB camera, or
- ESP32-CAM streaming over Wi-Fi

For vehicle actuation:

- a motor-control ESP32 or Arduino-compatible board
- USB serial connection to the laptop
- motor driver / Adafruit Motor Shield hardware as expected by the current `.ino` sketch

## 4. Project Structure

```text
app.py
pyproject.toml
datasets/
docs/
esp32/
scripts/
src/pothole_detection/
```

Important files:

- [README.md](D:\PERSONAL\RGCET\FINAL YEAR PROJECT\Working_Prototype\pothole-detection-code-main\README.md)
- [docs/architecture.md](D:\PERSONAL\RGCET\FINAL YEAR PROJECT\Working_Prototype\pothole-detection-code-main\docs\architecture.md)
- [src/pothole_detection/config/default.toml](D:\PERSONAL\RGCET\FINAL YEAR PROJECT\Working_Prototype\pothole-detection-code-main\src\pothole_detection\config\default.toml)
- [src/pothole_detection/models/detector.py](D:\PERSONAL\RGCET\FINAL YEAR PROJECT\Working_Prototype\pothole-detection-code-main\src\pothole_detection\models\detector.py)
- [src/pothole_detection/models/depth.py](D:\PERSONAL\RGCET\FINAL YEAR PROJECT\Working_Prototype\pothole-detection-code-main\src\pothole_detection\models\depth.py)
- [src/pothole_detection/dashboard/server.py](D:\PERSONAL\RGCET\FINAL YEAR PROJECT\Working_Prototype\pothole-detection-code-main\src\pothole_detection\dashboard\server.py)
- [esp32/esp32_rc_car/esp32_rc_car.ino](D:\PERSONAL\RGCET\FINAL YEAR PROJECT\Working_Prototype\pothole-detection-code-main\esp32\esp32_rc_car\esp32_rc_car.ino)

## 5. How to Start the Project

### Step 1: Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Step 2: Install the package

```powershell
pip install -e .
```

### Step 3: Install optional dependencies based on your use case

For dashboard + heuristic detection only:

```powershell
pip install pyserial
```

For YOLO and depth models:

```powershell
pip install ultralytics pyserial torch torchvision transformers pillow
```

### Step 4: Initialize the dataset folders

```powershell
python scripts\init_dataset.py
```

This creates the YOLO-style dataset layout under `datasets/pothole_yolo`.

### Step 5: Start the runtime

For the default heuristic pipeline using your local webcam:

```powershell
python app.py --source 0
```

For a saved video:

```powershell
python app.py --source path\to\video.mp4
```

For an ESP32-CAM stream:

```powershell
python app.py --source http://192.168.4.1:81/stream
```

## 6. Supported Runtime Modes

### A. Heuristic pothole detection

Default configuration:

- `detection.mode = "heuristic"`
- `depth.mode = "proxy"`

This mode is easiest to start because it does not require YOLO weights.

Run:

```powershell
python app.py --source 0
```

### B. YOLO-based pothole detection

Before using this mode you need:

- a trained `.pt` model
- `ultralytics` installed
- config changed so `detection.mode = "yolo"`

Run:

```powershell
python app.py --source 0 --model-path runs\detect\train\weights\best.pt
```

Important: if `detection.mode` stays as `"heuristic"`, passing `--model-path` alone does not activate YOLO.

### C. Telemetry-only mode

This disables the OpenCV display window while keeping telemetry output active.

```powershell
python app.py --source 0 --telemetry-only
```

### D. Detection-disabled mode

This keeps the app alive, sends cruise commands, and updates telemetry without running pothole inference.

```powershell
python app.py --source 0 --disable-detection --telemetry-only
```

### E. Output recording

To save the annotated result video:

```powershell
python app.py --source 0 --save-output artifacts\run.mp4
```

## 7. Command-Line Options

Supported options from the runtime:

- `--source`: camera index, video file path, or stream URL
- `--config`: custom TOML config path
- `--model-path`: YOLO weights path
- `--serial-port`: serial port for motor controller
- `--baudrate`: serial baudrate, default `115200`
- `--save-output`: output annotated video file
- `--telemetry-only`: disable preview window
- `--disable-detection`: skip pothole inference

Example:

```powershell
python app.py --source 0 --config src\pothole_detection\config\default.toml --serial-port COM5 --baudrate 115200
```

## 8. How the Project Functions Internally

The runtime loop in `src/pothole_detection/app.py` works like this:

1. load configuration from TOML
2. initialize dataset folders
3. open video source
4. build detector and depth estimator
5. start dashboard server
6. read each frame
7. run detection and depth estimation if enabled
8. compute geometry and severity
9. choose a vehicle command
10. write telemetry JSON
11. optionally write dashboard preview image
12. optionally send serial command to the controller
13. show the annotated frame unless telemetry-only mode is active

Severity mapping:

- low score: `none` or `minor`
- medium score: `moderate`
- high score: `severe`

Vehicle action mapping:

- `none` or `minor` -> `CRUISE`
- `moderate` -> `SLOW`
- `severe` -> `AVOID`

## 9. Dashboard

If dashboard support is enabled in config, the app starts an HTTP server at:

```text
http://127.0.0.1:8765
```

The dashboard shows:

- detection status
- commanded vehicle speed
- pothole distance
- severity
- estimated width, length, and depth
- online-learning sample count
- FPS and detection count

Runtime state is written to:

- `artifacts/dashboard/state.json`

Optional frame snapshot is written to:

- `artifacts/dashboard/frame.jpg`

## 10. Configuration

Main configuration file:

- [src/pothole_detection/config/default.toml](D:\PERSONAL\RGCET\FINAL YEAR PROJECT\Working_Prototype\pothole-detection-code-main\src\pothole_detection\config\default.toml)

Key sections:

- `[video]`: display and frame size
- `[camera]`: field of view, mount height, tilt, depth scaling
- `[runtime]`: detection enabled and max detections
- `[detection]`: `heuristic` or `yolo`, thresholds, classes
- `[depth]`: `proxy`, `midas`, `depthanything`, or `hybrid`
- `[severity]`: score thresholds
- `[control]`: cruise/slow/avoid speeds and send interval
- `[dataset]`: dataset root and image extension
- `[online_learning]`: pseudo-label capture and retraining controls
- `[dashboard]`: dashboard host, port, preview behavior, telemetry file paths

Recommended first-run settings:

- keep `detection.mode = "heuristic"`
- keep `depth.mode = "proxy"`
- keep `dashboard.enabled = true`
- keep `online_learning.auto_retrain = false`

## 11. Training Workflow

The repository supports YOLO-format training data in:

```text
datasets/pothole_yolo/
  images/train
  images/val
  images/test
  images/pseudo
  labels/train
  labels/val
  labels/test
  labels/pseudo
```

YOLO label format:

```text
class_id x_center y_center width height
```

Typical training command:

```powershell
yolo task=detect mode=train model=yolov8n.pt data=datasets\pothole_yolo\data.yaml epochs=50 imgsz=640
```

After training, update the config to `detection.mode = "yolo"` and run with `--model-path`.

## 12. Online Learning / Pseudo Labels

If `online_learning.enabled = true` and `capture_enabled = true`, the app periodically stores high-confidence detections into:

- `datasets/pothole_yolo/images/pseudo`
- `datasets/pothole_yolo/labels/pseudo`

This is a pseudo-label collection mechanism, not proof of correctness. Review those samples before using them for retraining.

Automatic retraining exists in code, but it is disabled by default. That is the safer configuration.

## 13. ESP32 / RC Car Integration Notes

The repository contains an Arduino sketch at:

- [esp32/esp32_rc_car/esp32_rc_car.ino](D:\PERSONAL\RGCET\FINAL YEAR PROJECT\Working_Prototype\pothole-detection-code-main\esp32\esp32_rc_car\esp32_rc_car.ino)

### Important mismatch in the current implementation

The Python app and the Arduino sketch are not yet protocol-compatible.

Python serial behavior:

- default baudrate is `115200`
- sends lines like:
  - `CRUISE speed=55`
  - `SLOW speed=30`
  - `AVOID dir=right speed=24`

Arduino sketch behavior:

- uses `Serial.begin(9600)`
- accepts:
  - `F`
  - `B`
  - `L`
  - `R`
  - `S`
  - `STOP`

Result:

- telemetry and perception can run
- serial output can print in mock mode if `--serial-port` is omitted
- full RC-car actuation will not work correctly until the command protocol is aligned

### Recommended fix direction

Choose one of these:

1. change Python to emit `F/L/R/S/STOP` and use `9600`
2. change the Arduino sketch to parse `CRUISE/SLOW/AVOID` at `115200`

Until that is done, treat the serial-control portion as prototype/incomplete.

## 14. Known Limitations

- Default detection is heuristic, not a trained pothole detector.
- Distance/width/length/depth values are approximate and depend heavily on camera calibration.
- `depth.mode = "proxy"` is a synthetic depth approximation, not real metric depth.
- YOLO mode is only active when both config and `--model-path` are set correctly.
- Auto-retraining can reinforce bad pseudo labels if used carelessly.
- Current motor-control serial protocol is inconsistent with the shipped Arduino sketch.

## 15. Troubleshooting

### App says dependency is missing

Install project and optional dependencies:

```powershell
pip install -e .
pip install ultralytics pyserial torch torchvision transformers pillow
```

### Camera cannot be opened

- verify camera index
- close other applications using the camera
- test a video file first
- verify the ESP32-CAM stream URL is reachable

### Dashboard does not update

- confirm `dashboard.enabled = true`
- open `http://127.0.0.1:8765`
- check whether `artifacts/dashboard/state.json` is being created

### YOLO does not run

- install `ultralytics`
- ensure `detection.mode = "yolo"`
- pass a valid `--model-path`

### Serial commands are not moving the car

- verify COM port
- verify baudrate
- verify Python and Arduino are using the same command protocol

## 16. Recommended Developer Workflow

For a clean demo path:

1. run with webcam and heuristic mode first
2. verify dashboard output
3. verify pseudo-label capture folders are created
4. train or obtain YOLO weights
5. switch to YOLO mode
6. only then integrate serial hardware control
7. align the Python-to-ESP32 serial protocol before vehicle tests

## 17. What a User Manual Document Should Contain

If you want to produce a formal user manual for this project, include these sections:

### Mandatory sections

- document title, version, author, and date
- project overview and objective
- target users
- hardware requirements
- software requirements
- installation steps
- startup procedure
- operating modes
- configuration instructions
- dashboard usage
- dataset/training instructions if the audience includes developers
- safety notes for RC-car operation
- troubleshooting
- maintenance/update process
- known limitations
- contact or support details

### Strongly recommended sections

- system architecture diagram
- hardware connection diagram
- screenshots of the dashboard
- sample commands
- expected outputs
- serial communication notes
- FAQ
- glossary of terms

## 18. Suggested User Manual Template

Use this outline for a final `.docx`, `.pdf`, or report document:

1. Introduction
2. System Overview
3. Hardware Components
4. Software Installation
5. Folder Structure
6. Configuration
7. How to Start the Application
8. How to Run with Webcam
9. How to Run with ESP32-CAM
10. How to Use the Dashboard
11. How Detection Decisions Work
12. How to Train or Replace the YOLO Model
13. How to Collect Pseudo Labels
14. How to Connect the RC Car Controller
15. Troubleshooting
16. Known Issues and Limitations
17. Safety Instructions
18. Appendix

## 19. Suggested Short Operator Instructions

For a non-developer operator, the shortest usable runbook is:

1. activate the virtual environment
2. start the app with `python app.py --source 0`
3. open `http://127.0.0.1:8765`
4. watch detection status and severity
5. press `q` in the OpenCV window to stop

## 20. Final Assessment

This codebase is a workable prototype for:

- pothole visualization
- telemetry demonstration
- experimental geometry estimation
- future RC-car automation

It is not yet a complete end-to-end autonomous RC-car system because the current serial-control protocol between Python and the Arduino/ESP32 sketch is inconsistent.
