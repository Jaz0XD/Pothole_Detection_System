# API Documentation for Real-Time Pothole Detection System

## Overview

This document provides an overview of the API endpoints and functionalities available in the Real-Time Wireframe-Based Pothole Detection and Avoidance System. The system utilizes a monocular camera for capturing road images, detecting potholes, estimating depth, and generating 3D wireframe meshes.

## API Endpoints

### 1. Capture

- **Endpoint:** `/api/capture/start`
  - **Method:** POST
  - **Description:** Starts the video capture from the monocular camera.
  - **Request Body:** None
  - **Response:**
    - **200 OK:** Capture started successfully.
    - **500 Internal Server Error:** Failed to start capture.

- **Endpoint:** `/api/capture/stop`
  - **Method:** POST
  - **Description:** Stops the video capture.
  - **Request Body:** None
  - **Response:**
    - **200 OK:** Capture stopped successfully.
    - **500 Internal Server Error:** Failed to stop capture.

### 2. Detection

- **Endpoint:** `/api/detection`
  - **Method:** GET
  - **Description:** Processes the latest captured frame to detect potholes and road anomalies.
  - **Response:**
    - **200 OK:** Detection results returned.
      - **Body:**
        - `detections`: List of detected anomalies with coordinates and confidence scores.
    - **204 No Content:** No anomalies detected.

### 3. Depth Estimation

- **Endpoint:** `/api/depth`
  - **Method:** GET
  - **Description:** Estimates depth from the latest captured frame.
  - **Response:**
    - **200 OK:** Depth estimation results returned.
      - **Body:**
        - `depth_map`: Array representing the depth of each pixel.
    - **204 No Content:** Depth estimation not available.

### 4. 3D Reconstruction

- **Endpoint:** `/api/reconstruction`
  - **Method:** POST
  - **Description:** Generates a 3D mesh from the detected anomalies and depth data.
  - **Request Body:**
    - `detections`: List of detected anomalies.
    - `depth_map`: Depth data.
  - **Response:**
    - **200 OK:** 3D mesh generated successfully.
      - **Body:**
        - `mesh`: URL to the generated mesh file.
    - **400 Bad Request:** Invalid input data.

### 5. Decision Engine

- **Endpoint:** `/api/decision`
  - **Method:** POST
  - **Description:** Triggers decision-making based on detected anomalies.
  - **Request Body:**
    - `detections`: List of detected anomalies.
  - **Response:**
    - **200 OK:** Decision made successfully.
      - **Body:**
        - `action`: Recommended action (e.g., slow down, avoid).
    - **500 Internal Server Error:** Failed to process decision.

## Error Handling

All API endpoints will return appropriate HTTP status codes to indicate success or failure. In case of errors, the response body will include a message detailing the error.

## Conclusion

This API documentation outlines the key functionalities of the Real-Time Pothole Detection and Avoidance System. For further details on implementation and usage, refer to the project's README and setup documentation.