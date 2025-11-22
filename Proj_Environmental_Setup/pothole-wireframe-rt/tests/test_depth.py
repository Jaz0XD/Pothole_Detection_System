import pytest
from src.pipeline.depth.midas import MiDaS
from src.pipeline.depth.depthanything_v2 import DepthAnythingV2

def test_midas_depth_estimation():
    model = MiDaS()
    input_image = "path/to/test/image.jpg"  # Replace with actual test image path
    depth_map = model.predict(input_image)
    
    assert depth_map is not None
    assert depth_map.shape[0] > 0
    assert depth_map.shape[1] > 0

def test_depthanything_v2_estimation():
    model = DepthAnythingV2()
    input_image = "path/to/test/image.jpg"  # Replace with actual test image path
    depth_map = model.predict(input_image)
    
    assert depth_map is not None
    assert depth_map.shape[0] > 0
    assert depth_map.shape[1] > 0

# Additional tests can be added as needed for edge cases and performance.