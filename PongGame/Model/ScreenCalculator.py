import math

class ScreenCalculator:
    x = 0
    y = 0
    motor1_x = 0
    motor1_y = 0
    motor2_x = 2
    motor2_y = 0
    motor1_start_angle = 1.5*math.pi - math.asin(1/3)
    motor2_start_angle = math.pi - math.asin(0.5)

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
        r1 = 10
        r2 = 12
        r3 = ScreenCalculator.distance(x, y, a, b)
        denominator = r1*r1 + r3*r3 - r2*r2
        nominator = 2 * r1 * r3
        gamma = math.acos(denominator / nominator)
        beta = math.acos((x - a) / r3)
        return beta + gamma

    @staticmethod
    def get_motor_angles(x_screen, y_screen):
        # Get motor coordinates
        

        # Repeat for motor 1 and 2
        # Calculate r3
        # Calculate gamma
        # Calculate angle
        return 0, 0


    
