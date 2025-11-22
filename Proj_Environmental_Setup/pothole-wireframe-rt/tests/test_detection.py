import unittest
from src.pipeline.detection.yolov8_seg import YOLOv8Seg

class TestDetection(unittest.TestCase):

    def setUp(self):
        self.detector = YOLOv8Seg()

    def test_load_model(self):
        model_loaded = self.detector.load_model('path/to/weights')
        self.assertTrue(model_loaded, "Model should load successfully")

    def test_detect_potholes(self):
        test_image = 'path/to/test/image.jpg'
        detections = self.detector.detect(test_image)
        self.assertIsInstance(detections, list, "Detections should be a list")
        self.assertGreater(len(detections), 0, "There should be at least one detection")

    def test_segmentation_output(self):
        test_image = 'path/to/test/image.jpg'
        masks = self.detector.segment(test_image)
        self.assertIsInstance(masks, list, "Segmentation masks should be a list")
        self.assertGreater(len(masks), 0, "There should be at least one mask")

if __name__ == '__main__':
    unittest.main()