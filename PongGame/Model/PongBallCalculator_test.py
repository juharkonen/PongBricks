import unittest   # The test framework
from Model.PongBallCalculator import PongBallCalculator, BALL_SPEED
from Model.ScreenGeometry import *

class Test_PongBallCalculator(unittest.TestCase):
    def test_update_state(self):
        state = PongBallCalculator()
        state.reset(math.pi / 4.0)
        state.update_state(0.5)
        
        sqrt_2 = math.sqrt(2)
        x_expected = SCREEN_CENTER_X + 0.5 * BALL_SPEED / sqrt_2
        y_expected = SCREEN_CENTER_Y + 0.5 * BALL_SPEED / sqrt_2

        self.assertAlmostEqual(state.x, x_expected, 2)
        self.assertAlmostEqual(state.y, y_expected, 2)
    
    def test_update_state_bounce(self):
        state = PongBallCalculator()
        angle = math.pi / 3.0
        state.reset(angle)
        delta_time = 1.5
        state.update_state(delta_time)

        x_expected = SCREEN_CENTER_X + delta_time * BALL_SPEED * math.cos(angle)
        # Bounce off top edge
        y_delta = delta_time * BALL_SPEED * math.sin(angle)
        y_expected = SCREEN_HEIGHT - (y_delta - SCREEN_HEIGHT / 2)
        self.assertAlmostEqual(state.x, x_expected, 2)
        self.assertAlmostEqual(state.y, y_expected, 2)

        state.reset_random()


if __name__ == '__main__':
    unittest.main()