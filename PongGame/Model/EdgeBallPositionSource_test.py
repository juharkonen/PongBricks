from EdgeBallPositionSource import EdgeBallPositionSource, START_DURATION, TIME_PER_EDGE, SCREEN_WIDTH, SCREEN_HEIGHT
import unittest   # The test framework
import math

class Test_EdgeBallPositionSource(unittest.TestCase):
    positionSource = EdgeBallPositionSource()
    def test_get_screen_position_begin_start(self):
        self.positionSource.reset_time()
        self.positionSource.set_start_position(2, 3)

        x, y = self.positionSource.get_screen_position(0)
        self.assertAlmostEqual(x, 2, 4)
        self.assertAlmostEqual(y, 3, 4)

    def test_get_screen_position_end_start(self):
        self.positionSource.reset_time()
        self.positionSource.set_start_position(2, 3)

        x, y = self.positionSource.get_screen_position(2)
        self.assertAlmostEqual(x, 0, 4)
        self.assertAlmostEqual(y, 0, 4)

    def test_get_screen_position_after_start(self):
        self.positionSource.reset_time()
        self.positionSource.set_start_position(2, 3)


        # Halfway left edge
        x, y = self.positionSource.get_screen_position(START_DURATION + 0.5 * TIME_PER_EDGE)
        self.assertAlmostEqual(x, 0, 4)
        self.assertAlmostEqual(y, 6, 4)

        # Top left
        x, y = self.positionSource.get_screen_position(0.5 * TIME_PER_EDGE)
        self.assertAlmostEqual(x, 0, 4)
        self.assertAlmostEqual(y, SCREEN_HEIGHT, 4)

        # Top right
        x, y = self.positionSource.get_screen_position(TIME_PER_EDGE)
        self.assertAlmostEqual(x, SCREEN_WIDTH, 4)
        self.assertAlmostEqual(y, SCREEN_HEIGHT, 4)

        # Bottom right
        x, y = self.positionSource.get_screen_position(TIME_PER_EDGE)
        self.assertAlmostEqual(x, SCREEN_WIDTH, 4)
        self.assertAlmostEqual(y, 0, 4)

        # Bottom left
        x, y = self.positionSource.get_screen_position(TIME_PER_EDGE)
        self.assertAlmostEqual(x, 0, 4)
        self.assertAlmostEqual(y, 0, 4)

if __name__ == '__main__':
    unittest.main()