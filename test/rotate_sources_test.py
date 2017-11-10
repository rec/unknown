import unittest
# from unknown import rotate_sources
# from . import mocks


class MockOutput:
    results = []

    def writeframes(self, frame):
        self.results += [frame]


class RotateSourcesTest(unittest.TestCase):
    def test_rotate_dc(self):

        pass
