# depthanything_v2.py

import torch
import torch.nn.functional as F
from torchvision import transforms

class DepthAnythingV2:
    def __init__(self, model_path):
        self.model = self.load_model(model_path)
        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
        ])

    def load_model(self, model_path):
        model = torch.load(model_path)
        model.eval()
        return model

    def predict_depth(self, image):
        image = self.transform(image).unsqueeze(0)  # Add batch dimension
        with torch.no_grad():
            depth_map = self.model(image)
        return depth_map.squeeze(0)  # Remove batch dimension

    def post_process_depth(self, depth_map):
        depth_map = F.interpolate(depth_map.unsqueeze(0), size=(480, 640), mode='bilinear', align_corners=False)
        return depth_map.squeeze(0)  # Remove batch dimension

# Example usage:
# depth_model = DepthAnythingV2('path/to/depthanything_model.pth')
# depth_map = depth_model.predict_depth(input_image)
# processed_depth_map = depth_model.post_process_depth(depth_map)