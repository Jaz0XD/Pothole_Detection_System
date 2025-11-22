import os
import requests

def download_weights(weights_url, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    response = requests.get(weights_url)
    if response.status_code == 200:
        weight_file_path = os.path.join(save_dir, os.path.basename(weights_url))
        with open(weight_file_path, 'wb') as f:
            f.write(response.content)
        print(f"Weights downloaded and saved to {weight_file_path}")
    else:
        print(f"Failed to download weights from {weights_url}. Status code: {response.status_code}")

if __name__ == "__main__":
    # Example URLs for YOLO and Depth model weights
    yolo_weights_url = "https://example.com/path/to/yolo_weights.pt"
    depth_weights_url = "https://example.com/path/to/depth_weights.pt"

    # Directories to save weights
    yolo_weights_dir = "../weights/yolo"
    depth_weights_dir = "../weights/depth"

    # Download weights
    download_weights(yolo_weights_url, yolo_weights_dir)
    download_weights(depth_weights_url, depth_weights_dir)