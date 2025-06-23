class Field:
    def __init__(self, width: int, height: int):
        self.width=width
        self.height=height

    def is_within_bounds(self, inputwidth: int, inputheight: int) -> bool:
        within = 0<=inputwidth < self.width and 0<=inputheight < self.height
        return within

    def is_outside_bounds(self, inputwidth: int, inputheight: int) -> bool:
        outside = not self.is_within_bounds(inputwidth, inputheight)
        return outside