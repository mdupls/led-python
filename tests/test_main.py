import unittest
from unittest.mock import MagicMock, patch
import main

class DummyNP:
    def __init__(self, n):
        self.data = [(0,0,0,0)] * n
        self.calls = []
    def __setitem__(self, idx, val):
        self.data[idx] = val
    def __getitem__(self, idx):
        return self.data[idx]
    def __len__(self):
        return len(self.data)
    def write(self):
        self.calls.append('write')

class DummyCh:
    def __init__(self, n):
        self.np = DummyNP(n)
        self.zero_data = [(0,0,0,0)] * n

class TestMain(unittest.TestCase):
    def test_rand_color(self):
        color = main.rand_color()
        self.assertEqual(len(color), 4)
        self.assertTrue(0 <= color[0] <= 255)
        self.assertTrue(0 <= color[1] <= 255)
        self.assertTrue(0 <= color[2] <= 255)
        self.assertTrue(0 <= color[3] <= 127)

    def test_clear(self):
        ch = DummyCh(5)
        ch.np.data = [(1,2,3,4)] * 5
        main.clear(ch)
        self.assertEqual(ch.np.data, ch.zero_data)

    @patch('main.sleep', return_value=None)
    def test_solid_color(self, _):
        ch = DummyCh(3)
        color = (1,2,3,4)
        main.solid_color(ch, 0, color)
        self.assertEqual(ch.np.data, ch.zero_data)
        self.assertIn('write', ch.np.calls)

    def test_hsv_to_rgb(self):
        # Test black, white, and a color
        self.assertEqual(main.hsv_to_rgb(0, 0, 0, 0), (0, 0, 0, 0))
        self.assertEqual(main.hsv_to_rgb(0, 0, 1, 0), (255, 255, 255, 0))
        rgb = main.hsv_to_rgb(0.5, 1, 1, 0)
        self.assertEqual(len(rgb), 4)

if __name__ == '__main__':
    unittest.main()