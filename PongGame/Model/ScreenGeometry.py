import math

BALL_DIAMETER = 2.0
BALL_RADIUS = BALL_DIAMETER / 2.0

# Ball is always at least BALL_RADIUS distance from edges
SCREEN_WIDTH = 22
SCREEN_HEIGHT = 14
SCREEN_MOVABLE_LEFT = BALL_RADIUS
SCREEN_MOVABLE_RIGHT = SCREEN_WIDTH - BALL_RADIUS
SCREEN_MOVABLE_BOTTOM = BALL_RADIUS
SCREEN_MOVABLE_TOP = SCREEN_HEIGHT - BALL_RADIUS
SCREEN_CENTER_X = SCREEN_WIDTH / 2.0
SCREEN_CENTER_Y = SCREEN_HEIGHT / 2.0

BALL_ARM_R1 = 9.0
BALL_ARM_R2 = 12.0

# Ball motor 2 axle position in motor coordinates (relative to ball motor 1), aka distance between ball motors
BALL_MOTOR2_X = 5.0

# Ball motor 1 axle pivot distance from screen bottom left
SCREEN_TO_MOTOR1_OFFSET_X = -8.5
SCREEN_TO_MOTOR1_OFFSET_Y = 3.5

BALL_GEARS = [8, 40]

BALL_SPEED = 5
# Increment ball speed by 10% of initial speed on hit
BALL_SPEED_HIT_INCREMENT = 0.1 * BALL_SPEED

# Paddles
PADDLE_HEIGHT = 3.0
PADDLE_HALF_HEIGHT = PADDLE_HEIGHT / 2.0
PADDLE_EDGE_THICKNESS = 0.5
PADDLE_HEIGHT_WITH_THICKNESS = PADDLE_HEIGHT + 2.0 * PADDLE_EDGE_THICKNESS

# Paddle origin is where arm is attached to the paddle (half a stud offset from screen y)
SCREEN_TO_PADDLE_Y_OFFSET = 0.5
PADDLE_RANGE_Y = SCREEN_HEIGHT - PADDLE_HEIGHT_WITH_THICKNESS
PADDLE_CENTER_Y = PADDLE_RANGE_Y / 2.0
PADDLE_ARM1 = 6.0
PADDLE_ARM2 = 10.0
# Paddle motor axle distance from paddle pivot
PADDLE_MOTOR_X = 6.0
PADDLE_MOTOR_Y = -3.5
PADDLE_GEARS = [12, 36]

PADDLE_SPEED = 4.0
AUTOPLAY_PADDLE_SPEED = PADDLE_SPEED / 1.0
# How much paddle impacts ball y speed if paddle moves during hit
PADDLE_BALL_SPEED_IMPULSE = 0.3
