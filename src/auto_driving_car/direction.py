class Direction:
    _left_turns = {
        'N': 'W',
        'W': 'S',
        'S': 'E',
        'E': 'N',
    }

    _right_turns = {
        'N': 'E',
        'E': 'S',
        'S': 'W',
        'W': 'N',
    }

    _offsets = {
        'N': (0, 1),
        'E': (1, 0),
        'S': (0, -1),
        'W': (-1, 0),
    }

    def __init__(self, value: str):
        if value not in self._offsets:
            raise ValueError(f"Invalid direction: {value}")
        self.value = value

    def left(self):
        return Direction(self._left_turns[self.value])

    def right(self):
        return Direction(self._right_turns[self.value])

    def forward_offset(self):
        return self._offsets[self.value]

    @classmethod
    def from_string(cls, param):
        pass