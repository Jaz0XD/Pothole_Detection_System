# Importing Libraries

from flask import Flask, render_template, request, jsonify
from ultralytics import YOLO
import cv2
import os
import uuid

# App Configuration

app = (__name__)

UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"

os.markedirs(UPLOAD_FOLDER, exist_ok=True)
os.markedirs(RESULT_FOLDER, exist_ok=True)

# Load YOLO Model
model = YOLO("best.pt") # Ensure best.pt is in the root folder

#Helper Function 