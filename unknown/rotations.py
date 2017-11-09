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
        for i, r in enumerate(self.rotations):
            if rotation < r:
                break
        else:
            r = 1 + self.rotations[0]
            i = len(self.rotations)

        prev = self.rotations[i - 1]
        if not i:
            prev -= 1

        width = r - prev
        ratio = (rotation - prev) / width
        assert 0 <= ratio < 1, str(ratio)
        if i:
            return i - 1, ratio
        return len(self.rotations) - 1, ratio
