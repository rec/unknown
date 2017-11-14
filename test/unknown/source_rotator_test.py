import unittest
# from unknown import source_rotator
# from . import mocks


class MockOutput:
    results = []

    def writeframes(self, frame):
        self.results += [frame]


class RotateSourcesTest(unittest.TestCase):
    def test_rotate_dc(self):

        pass
