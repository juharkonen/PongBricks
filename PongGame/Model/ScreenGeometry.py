
import math
#from Model.ScreenCalculator import ScreenCalculator
SCREEN_WIDTH = 20.0
SCREEN_HEIGHT = 14.0

BALL_ARM_R1 = 10
BALL_ARM_R2 = 12

BALL_MOTOR2_X = 3

SCREEN_TO_MOTOR1_OFFSET_X = -9
SCREEN_TO_MOTOR1_OFFSET_Y = 4

BALL_GEAR_RATIO = 40.0 / 8.0
BALL_GEAR_SIGN = -1

#MOTOR1_CALIBRATION_ANGLE_DEGREES, MOTOR2_CALIBRATION_ANGLE_DEGREES = ScreenCalculator.get_motor_angles(SCREEN_WIDTH/2, SCREEN_HEIGHT)
MOTOR1_CALIBRATION_ANGLE_DEGREES = 270.0 - math.degrees(math.asin(1/4.0))
MOTOR2_CALIBRATION_ANGLE_DEGREES = 180 - math.degrees(math.asin(1/BALL_MOTOR2_X))

# Paddles
PADDLE_RANGE_Y = 11
PADDLE_ARM1 = 6
PADDLE_ARM2 = 10
PADDLE_MOTOR_X = 6
PADDLE_MOTOR_Y = -4
PADDLE_GEAR_RATIO = 3