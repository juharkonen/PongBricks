from ScreenCalculator import ScreenCalculator
from Model.ScreenGeometry import *
   # The code to test
import unittest   # The test framework
import math

class Test_ScreenCalculator(unittest.TestCase):
    calculator = ScreenCalculator()

    def test_motor1_start_angle(self):
        motor1_offset = math.degrees(math.asin(1/4))
        self.assertAlmostEqual(MOTOR1_CALIBRATION_ANGLE_DEGREES, 270 - motor1_offset, 2)

    def test_motor2_start_angle(self):
        motor1_offset = math.degrees(math.asin(1/3))
        self.assertAlmostEqual(MOTOR2_CALIBRATION_ANGLE_DEGREES, 180 - motor1_offset, 2)

    def test_screen_to_motor_coordinates_origin(self):
        self.assertEqual(ScreenCalculator.screen_to_motor_coordinates(0, 0), (SCREEN_TO_MOTOR1_OFFSET_X,SCREEN_TO_MOTOR1_OFFSET_Y))
        #self.assertEqual(ScreenCalculator.screen_to_motor_coordinates(9, 1), (0,4))

    def test_distance(self):
        self.assertAlmostEqual(ScreenCalculator.distance(-9, 3, 2, 0), 11.40, 2)

    def test_calculate_angle(self):
        ScreenCalculator.get_motor_angles(11, 10)
        self.assertAlmostEqual(ScreenCalculator.calculate_angle(
            SCREEN_TO_MOTOR1_OFFSET_X, SCREEN_TO_MOTOR1_OFFSET_Y, 0, 0), 4.146, 2)

    def test_get_motor_angles(self):
        # calculate angle at bottom left
        motor2_x_distance = SCREEN_TO_MOTOR1_OFFSET_X - MOTOR2_X
        motor2_r3_sqr = motor2_x_distance*motor2_x_distance + SCREEN_TO_MOTOR1_OFFSET_Y*SCREEN_TO_MOTOR1_OFFSET_Y
        motor2_r3 = math.sqrt(motor2_r3_sqr)
        d = ARM_R1*ARM_R1 + motor2_r3_sqr - ARM_R2*ARM_R2
        n = 2 * ARM_R1 * motor2_r3
        gamma = math.acos(d / n)
        beta = math.acos((SCREEN_TO_MOTOR1_OFFSET_X - MOTOR2_X) / motor2_r3)
        alpha = beta - gamma

        motor1_angle, motor2_angle = ScreenCalculator.get_motor_angles(0, 0)

        #self.assertAlmostEqual(motor1_angle, math.degrees(4.146), 1)
        self.assertAlmostEqual(motor2_angle, math.degrees(alpha), 2)

if __name__ == '__main__':
    unittest.main()