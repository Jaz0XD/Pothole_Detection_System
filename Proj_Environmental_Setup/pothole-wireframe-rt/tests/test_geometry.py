import unittest
from src.pipeline.geometry.measurements import calculate_area, calculate_perimeter, calculate_volume

class TestGeometryCalculations(unittest.TestCase):

    def test_calculate_area(self):
        # Test for a rectangle
        length = 5
        width = 3
        expected_area = 15
        self.assertEqual(calculate_area(length, width), expected_area)

        # Test for a circle
        radius = 3
        expected_area_circle = 28.27  # Approximation of π * r^2
        self.assertAlmostEqual(calculate_area(radius=radius), expected_area_circle, places=2)

    def test_calculate_perimeter(self):
        # Test for a rectangle
        length = 5
        width = 3
        expected_perimeter = 16
        self.assertEqual(calculate_perimeter(length, width), expected_perimeter)

        # Test for a circle
        radius = 3
        expected_perimeter_circle = 18.85  # Approximation of 2 * π * r
        self.assertAlmostEqual(calculate_perimeter(radius=radius), expected_perimeter_circle, places=2)

    def test_calculate_volume(self):
        # Test for a rectangular prism
        length = 5
        width = 3
        height = 2
        expected_volume = 30
        self.assertEqual(calculate_volume(length, width, height), expected_volume)

        # Test for a cylinder
        radius = 3
        height = 5
        expected_volume_cylinder = 28.27 * height  # π * r^2 * h
        self.assertAlmostEqual(calculate_volume(radius=radius, height=height), expected_volume_cylinder, places=2)

if __name__ == '__main__':
    unittest.main()