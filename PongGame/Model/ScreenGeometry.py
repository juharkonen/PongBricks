import math

SCREEN_WIDTH = 20.0
SCREEN_HEIGHT = 13.0

BALL_ARM_R1 = 10.0
BALL_ARM_R2 = 12.0

BALL_MOTOR2_X = 4.0

SCREEN_TO_MOTOR1_OFFSET_X = -8.0
SCREEN_TO_MOTOR1_OFFSET_Y = 4.5

BALL_GEAR_RATIO = 40.0 / 8.0
BALL_GEAR_SIGN = 1.0

BALL_SPEED = 5
# Increment ball speed by 10% of initial speed on hit
BALL_SPEED_HIT_INCREMENT = 0.1 * BALL_SPEED

# Paddles
PADDLE_HEIGHT = 3.0
PADDLE_HALF_HEIGHT = PADDLE_HEIGHT / 2.0
PADDLE_RANGE_Y = SCREEN_HEIGHT - PADDLE_HEIGHT
# Paddle can move 0.5 units outside range
PADDLE_EDGE_HEIGHT = 0.5
PADDLE_HALF_RANGE_Y = PADDLE_RANGE_Y / 2.0
PADDLE_ARM1 = 6.0
PADDLE_ARM2 = 10.0
PADDLE_MOTOR_X = 6.0
PADDLE_MOTOR_Y = -4.0
PADDLE_GEAR_RATIO = 3.0

PADDLE_SPEED = 4.0
AUTOPLAY_PADDLE_SPEED = PADDLE_SPEED / 1.0
# How much paddle impacts ball y speed if paddle moves during hit
PADDLE_BALL_SPEED_IMPULSE = 0.3