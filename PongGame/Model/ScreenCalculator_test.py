from ScreenCalculator import ScreenCalculator    # The code to test
import unittest   # The test framework
import math

class Test_ScreenCalculator(unittest.TestCase):
    calculator = ScreenCalculator()

    def test_motor1_start_angle(self):
        self.assertAlmostEqual(ScreenCalculator.motor1_start_angle, 1.5 * math.pi - 0.3398, 4)

    def test_motor2_start_angle(self):
        self.assertAlmostEqual(ScreenCalculator.motor2_start_angle, math.pi - 0.5236, 4)

    def test_screen_to_motor_coordinates_origin(self):
        self.assertEqual(ScreenCalculator.screen_to_motor_coordinates(0, 0), (-9,3))
        self.assertEqual(ScreenCalculator.screen_to_motor_coordinates(9, 1), (0,4))

    def test_distance(self):
        self.assertAlmostEqual(ScreenCalculator.distance(-9, 3, 2, 0), 11.40, 2)

    def test_calculate_angle(self):
        self.assertAlmostEqual(ScreenCalculator.calculate_angle(-9, 3, 0, 0), 2.7828, 5)

    def test_get_motor_angles(self):
        self.assertEqual(ScreenCalculator.get_motor_angles(0, 0), (0,0))

if __name__ == '__main__':
    unittest.main()