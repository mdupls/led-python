import unittest
from unittest.mock import MagicMock, patch
from effects.cycle_single_color import run
from utils import OFF

class DummyNP:
    def __init__(self, n):
        self.data = [(0,0,0,0)] * n
        self.write_calls = 0
    def __setitem__(self, idx, val):
        self.data[idx] = val
    def __getitem__(self, idx):
        return self.data[idx]
    def __len__(self):
        return len(self.data)
    def write(self):
        self.write_calls += 1

class DummyCh:
    def __init__(self, n):
        self.np = DummyNP(n)

class TestYourFunctionOrClass(unittest.TestCase):
    def test_scenario_one(self):
        ch = DummyCh(5)
        color = (1,2,3,4)
        cycles = 3

        run(ch, cycles, color)
        
        assert ch.np.write_calls == len(ch.np) * cycles + 1

        for i in range(len(ch.np)):
            assert ch.np[i] == OFF

    def test_scenario_two(self):
        # Test code for scenario two
        pass

if __name__ == '__main__':
    unittest.main()