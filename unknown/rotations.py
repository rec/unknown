class Rotations:
    def __init__(self, rotations):
        self.rotations = list(rotations)

        if len(rotations) < 2:
            raise ValueError('There need to be at least two rotations')

        if not all(0 <= r <= 1 for r in self.rotations):
            raise ValueError('All rotations must be between 0 and 1')

        for i, r in enumerate(self.rotations):
            if i and self.rotations[i - 1] > r:
                raise ValueError('Rotations must be in non-decreasing order')

    def find(self, rotation):
        rotation = rotation % 1

        # Find the first index greater than rotation.
        for i, r in enumerate(self.rotations):
            if r > rotation:
                break
        else:
            i = 0

        r1, r2 = self.rotations[i - 1], self.rotations[i]
        width = (r2 - r1) % 1
        consumed = (rotation - r1) % 1
        ratio = consumed / width
        assert 0 <= ratio < 1, str(ratio)
        return i - 1, ratio
