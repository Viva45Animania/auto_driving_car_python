from auto_driving_car.direction import Direction


def test_turning_left():
    assert Direction('N').left().value == 'W'
    assert Direction('W').left().value == 'S'
    assert Direction('S').left().value == 'E'
    assert Direction('E').left().value == 'N'

def test_turning_right():
    assert Direction('N').right().value == 'E'
    assert Direction('E').right().value == 'S'
    assert Direction('S').right().value == 'W'
    assert Direction('W').right().value == 'N'

def test_forward_offset():
    assert Direction('N').forward_offset() == (0, 1)
    assert Direction('E').forward_offset() == (1, 0)
    assert Direction('S').forward_offset() == (0, -1)
    assert Direction('W').forward_offset() == (-1, 0)

