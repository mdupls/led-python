import unittest
from effects.bounce import BounceEffect
from strip import Segment
from utils import OFF
import timeit

class TestRainbowWipeEffect(unittest.TestCase):
    def test_perf(self):
        n = 100000
        pixels = [OFF] * n
        segment = Segment(0, n)
        effect = BounceEffect(pixels, segment)

        # Test code for scenario two
        execution_time = timeit.timeit(effect.update, number=10)
        print(f"Time over 10 runs: {execution_time:.6f} seconds")

    def test_two_loops(self):
        n = 10
        pixels = [OFF] * n
        segment = Segment(0, n)
        effect = BounceEffect(pixels, segment)

        # Test code for scenario two
        execution_time = timeit.timeit(effect.update, number=2)
        print(f"Time over 10 runs: {execution_time:.6f} seconds")

if __name__ == '__main__':
    unittest.main()