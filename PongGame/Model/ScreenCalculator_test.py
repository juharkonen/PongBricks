from ScreenCalculator import (ScreenCalculator, motor2_calibration_angle_degrees,
                              motor1_calibration_angle_degrees, motor2_x, arm_r1, arm_r2)
   # The code to test
import unittest   # The test framework
import math

class Test_ScreenCalculator(unittest.TestCase):
    calculator = ScreenCalculator()

    def test_motor1_start_angle(self):
        motor1_offset = math.degrees(math.asin(1/4))
        self.assertAlmostEqual(motor1_calibration_angle_degrees, 270 - motor1_offset, 2)

    def test_motor2_start_angle(self):
        motor1_offset = math.degrees(math.asin(1/3))
        self.assertAlmostEqual(motor2_calibration_angle_degrees, 180 - motor1_offset, 2)

    def test_screen_to_motor_coordinates_origin(self):
        self.assertEqual(ScreenCalculator.screen_to_motor_coordinates(0, 0), (-9,3))
        self.assertEqual(ScreenCalculator.screen_to_motor_coordinates(9, 1), (0,4))

    def test_distance(self):
        self.assertAlmostEqual(ScreenCalculator.distance(-9, 3, 2, 0), 11.40, 2)

    def test_calculate_angle(self):
        ScreenCalculator.get_motor_angles(11, 10)
        self.assertAlmostEqual(ScreenCalculator.calculate_angle(-9, 3, 0, 0), 4.146, 2)

    def test_get_motor_angles(self):
        motor2_x_distance = -9 - motor2_x
        motor2_r3_sqr = motor2_x_distance*motor2_x_distance + 3*3
        motor2_r3 = math.sqrt(motor2_r3_sqr)
        d = arm_r1*arm_r1 + motor2_r3_sqr - arm_r2*arm_r2
        n = 2 * arm_r1 * motor2_r3
        gamma = math.acos(d / n)
        beta = math.acos((-9 - 3) / motor2_r3)
        alpha = gamma + beta

        motor1_angle, motor2_angle = ScreenCalculator.get_motor_angles(0, 0)

        self.assertAlmostEqual(motor1_angle, math.degrees(4.146), 1)
        self.assertAlmostEqual(motor2_angle, math.degrees(alpha), 2)

if __name__ == '__main__':
    unittest.main()