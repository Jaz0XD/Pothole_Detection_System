import unittest
from src.pipeline.pipeline import Pipeline

class TestPipeline(unittest.TestCase):

    def setUp(self):
        self.pipeline = Pipeline()

    def test_capture(self):
        frames = self.pipeline.capture_frames()
        self.assertIsNotNone(frames)
        self.assertGreater(len(frames), 0)

    def test_preprocess(self):
        processed_frames = self.pipeline.preprocess_frames()
        self.assertIsNotNone(processed_frames)
        self.assertGreater(len(processed_frames), 0)

    def test_detection(self):
        detections = self.pipeline.detect_anomalies()
        self.assertIsNotNone(detections)
        self.assertGreater(len(detections), 0)

    def test_depth_estimation(self):
        depth_map = self.pipeline.estimate_depth()
        self.assertIsNotNone(depth_map)

    def test_reconstruction(self):
        mesh = self.pipeline.reconstruct_mesh()
        self.assertIsNotNone(mesh)

    def test_decision_engine(self):
        decision = self.pipeline.make_decision()
        self.assertIn(decision, ['slow_down', 'avoid', 'continue'])

if __name__ == '__main__':
    unittest.main()