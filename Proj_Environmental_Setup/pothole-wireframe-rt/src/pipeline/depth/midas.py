import torch
import torch.nn.functional as F
from torchvision.transforms import Normalize
import numpy as np

class MiDaSDepthEstimator:
    def __init__(self, model_type='DPT_Large'):
        self.model_type = model_type
        self.model = self.load_model(model_type)
        self.transform = self.get_transform()

    def load_model(self, model_type):
        if model_type == 'DPT_Large':
            model = torch.hub.load("intel-isl/MiDaS", "DPT_Large", pretrained=True)
        elif model_type == 'DPT_Hybrid':
            model = torch.hub.load("intel-isl/MiDaS", "DPT_Hybrid", pretrained=True)
        else:
            raise ValueError("Invalid model type. Choose 'DPT_Large' or 'DPT_Hybrid'.")
        model.eval()
        return model

    def get_transform(self):
        return Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])

    def predict_depth(self, image):
        with torch.no_grad():
            input_tensor = self.transform(image).unsqueeze(0)
            depth_map = self.model(input_tensor)
            depth_map = F.interpolate(depth_map.unsqueeze(1), size=image.shape[:2], mode='bilinear', align_corners=False)
            return depth_map.squeeze().cpu().numpy()

# Example usage:
# depth_estimator = MiDaSDepthEstimator()
# depth_map = depth_estimator.predict_depth(input_image)