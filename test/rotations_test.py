import unittest
from unknown.rotations import Rotations

ROT2 = Rotations([0, 1 / 2])
ROT3 = Rotations([0, 1 / 3, 2 / 3])
ROT3_OFF = Rotations([0.25, 0.50])


class RotationsTest(unittest.TestCase):
    def do_test(self, rotations, rotation, index, ratio):
        i2, r2 = rotations.find(rotation)
        self.assertEqual(i2, index)
        print(i2, r2)
        self.assertAlmostEqual(r2, ratio)

    def test_two(self):
        self.do_test(ROT2, 0, 0, 0)
        self.do_test(ROT2, 0.20, 0, 0.40)
        self.do_test(ROT2, 0.40, 0, 0.8)
        self.do_test(ROT2, 0.49, 0, 0.98)
        self.do_test(ROT2, 0.50, -1, 0)
        self.do_test(ROT2, 0.70, -1, 0.40)
        self.do_test(ROT2, 0.99, -1, 0.98)

    def test_three(self):
        self.do_test(ROT3, 0, 0, 0)
        self.do_test(ROT3, 0.20, 0, 0.6)
        self.do_test(ROT3, 0.40, 1, 0.20)
        self.do_test(ROT3, 0.49, 1, 0.47)
        self.do_test(ROT3, 0.50, 1, 0.50)
        self.do_test(ROT3, 0.70, -1, 0.10)
        self.do_test(ROT3, 0.99, -1, 0.97)

    def test_three_offset(self):
        self.do_test(ROT3_OFF, 0, -1, 2 / 3)
        self.do_test(ROT3_OFF, 0.20, -1, 14 / 15)
        self.do_test(ROT3_OFF, 0.40, 0, 0.60)
        self.do_test(ROT3_OFF, 0.49, 0, 0.96)
        self.do_test(ROT3_OFF, 0.50, 1, 0.00)
        self.do_test(ROT3_OFF, 0.70, 2, 4 / 15)
        self.do_test(ROT3_OFF, 0.99, 2, 49 / 75)
