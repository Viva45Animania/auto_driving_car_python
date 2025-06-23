from auto_driving_car.field import Field

def test_car_is_within_bounds():
    field = Field(5, 5)

    assert field.is_within_bounds(0, 0) is True
    assert field.is_within_bounds(4, 4) is True
    assert field.is_within_bounds(0, 4) is True
    assert field.is_within_bounds(4, 0) is True
    assert field.is_within_bounds(5, 4) is False
    assert field.is_within_bounds(4, 5) is False
    assert field.is_within_bounds(-1, 0) is False
    assert field.is_within_bounds(0, -1) is False

def test_car_is_outside_bounds():
    field = Field(5, 5)

    assert field.is_outside_bounds(0, 0) is False
    assert field.is_outside_bounds(4, 4) is False
    assert field.is_outside_bounds(0, 4) is False
    assert field.is_outside_bounds(4, 0) is False
    assert field.is_outside_bounds(5, 4) is True
    assert field.is_outside_bounds(4, 5) is True
    assert field.is_outside_bounds(-1, 0) is True
    assert field.is_outside_bounds(0, -1) is True
    assert field.is_outside_bounds(6, 0) is True
    assert field.is_outside_bounds(0, 6) is True


