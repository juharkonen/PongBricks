import math

arm_r1 = 10
arm_r2 = 12
motor2_x = 3#2
motor1_calibration_angle_degrees = math.degrees(1.5*math.pi - math.asin(1/4))
motor2_calibration_angle_degrees = math.degrees(math.pi - math.asin(1/3))

"""
screen coordinates: origin in bottom left, one unit is one stud (20 LDU)
motor coordinates: origin on motor 1 axle
"""
class ScreenCalculator:

    @staticmethod
    def screen_to_motor_coordinates(x_screen, y_screen):
        return x_screen - 9, y_screen + 3

    @staticmethod
    def distance(x, y, a, b):
        dx = x - a
        dy = y - b
        return math.sqrt(dx*dx + dy*dy)

    @staticmethod
    def calculate_angle(x, y, a, b):
        r1 = arm_r1
        r2 = arm_r2
        r3 = ScreenCalculator.distance(x, y, a, b)
        denominator = r1*r1 + r3*r3 - r2*r2
        nominator = 2 * r1 * r3
        gamma = math.acos(denominator / nominator)
        beta = math.acos((x - a) / r3)
        return beta, gamma

    @staticmethod
    def get_motor_angles(x_screen, y_screen):
        # Get motor coordinates
        x, y = ScreenCalculator.screen_to_motor_coordinates(x_screen, y_screen)
        m1_beta, m1_gamma = ScreenCalculator.calculate_angle(x, y, 0, 0)
        m2_beta, m2_gamma = ScreenCalculator.calculate_angle(x, y, motor2_x, 0)
        return math.degrees(m1_beta + m1_gamma), math.degrees(m2_beta - m2_gamma)


    
