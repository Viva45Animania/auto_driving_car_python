from auto_driving_car.car import Car
from auto_driving_car.direction import Direction
from auto_driving_car.field import Field
from auto_driving_car.utils.validators import Validators
import pytest

field = Field(5, 5)  # Global test constant for field

def test_car_moves_forward_when_facing_north():
    car = Car(
        name='A',
        initial_position="1 2 N",
        commands="F",
        field=field
    )

    car.execute_next_command()

    assert car.x_axis == 1
    assert car.y_axis == 3
    assert car.direction.value == 'N'

def test_car_turns_left_and_right():
    car = Car(
        name='A',
        initial_position="1 1 N",
        commands="LRL",
        field=field
    )

    car.execute_next_command()  # L → W
    assert car.direction.value == 'W'

    car.execute_next_command()  # R → N
    assert car.direction.value == 'N'

    car.execute_next_command()  # L → W
    assert car.direction.value == 'W'

def test_car_executes_multiple_forward_commands():
    car = Car(
        name='B',
        initial_position="0 0 E",
        commands="FFF",
        field=field
    )

    car.execute_next_command()
    assert car.x_axis == 1 and car.y_axis == 0

    car.execute_next_command()
    assert car.x_axis == 2 and car.y_axis == 0

    car.execute_next_command()
    assert car.x_axis == 3 and car.y_axis == 0

def test_car_executes_full_command_sequence():
    car = Car(
        name='A',
        initial_position="1 2 N",
        commands="FFRFF",
        field=field
    )

    while car.commands:
        car.execute_next_command()

    assert (car.x_axis, car.y_axis) == (3, 4)
    assert car.direction.value == 'E'

def test_car_only_turns_without_moving():
    car = Car(
        name='B',
        initial_position="2 2 S",
        commands="LLRR",
        field=field
    )

    while car.commands:
        car.execute_next_command()

    assert (car.x_axis, car.y_axis) == (2, 2)
    assert car.direction.value == 'S'  # Ends up facing same direction

def test_car_multiple_out_of_bounds_moves_ignored():
    car = Car(
        name='C',
        initial_position="0 0 S",
        commands="FFFF",
        field=field
    )

    while car.commands:
        car.execute_next_command()

    assert (car.x_axis, car.y_axis) == (0, 0)
    assert car.direction.value == 'S'

def test_car_with_no_commands_does_nothing():
    car = Car(
        name='D',
        initial_position="3 3 E",
        commands="",
        field=field
    )

    car.execute_next_command()  # Should not crash

    assert (car.x_axis, car.y_axis) == (3, 3)
    assert car.direction.value == 'E'

# def test_car_does_not_move_after_collision_flag():
#     car = Car(
#         name='E',
#         initial_position="1 1 N",
#         commands="FF",
#         field=field
#     )

    # car.has_collided = True
    #
    # car.execute_next_command()
    # assert (car.x_axis, car.y_axis) == (1, 1)
    # assert car.commands == ['F','F']  # Command not consumed

def test_car_starts_at_border_facing_outward():
    car = Car(
        name='F',
        initial_position="4 4 N",  # Top-right corner of 5x5
        commands="F",              # Should be ignored
        field=field
    )

    car.execute_next_command()

    assert (car.x_axis, car.y_axis) == (4, 4)
    assert car.direction.value == 'N'

def test_car_raises_on_unknown_command():
    with pytest.raises(ValueError, match="Invalid command.*X"):
        Car(
            name='G',
            initial_position="1 1 N",
            commands="FX",  # 'X' is invalid
            field=field
        )

def test_car_does_not_change_state_on_invalid_command():
    with pytest.raises(ValueError, match="Invalid command.*X"):
        Car(
            name='H',
            initial_position="2 2 E",
            commands="X",  # invalid
            field=field
        )

def test_car_continues_after_failed_boundary_move():
    car = Car(
        name='I',
        initial_position="0 0 S",
        commands="FRF",  # F blocked, R should succeed, F moves east
        field=field
    )

    while car.commands:
        try:
            car.execute_next_command()
        except Exception:
            break

    assert (car.x_axis, car.y_axis) == (0, 0)
    assert car.direction.value == 'W'
