import cv2
import numpy as np
import yaml

def load_camera_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def calibrate_camera(camera_index=0, config_path='configs/camera.yaml'):
    config = load_camera_config(config_path)
    chessboard_size = tuple(config['chessboard_size'])
    frame_size = tuple(config['frame_size'])
    
    # Prepare object points
    objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    cap = cv2.VideoCapture(camera_index)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

        if ret:
            objpoints.append(objp)
            imgpoints.append(corners)

            # Draw and display the corners
            cv2.drawChessboardCorners(frame, chessboard_size, corners, ret)

        cv2.imshow('Calibration', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Calibrate the camera
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, frame_size, None, None)

    # Save the calibration results
    calibration_data = {
        'camera_matrix': mtx.tolist(),
        'dist_coeffs': dist.tolist()
    }

    with open('camera_calibration.yaml', 'w') as file:
        yaml.dump(calibration_data, file)

if __name__ == "__main__":
    calibrate_camera()