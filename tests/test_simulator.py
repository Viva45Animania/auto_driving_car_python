from auto_driving_car.simulator import Simulator
from auto_driving_car.field import Field
from auto_driving_car.car import Car
import pytest

field = Field(5, 5)

""" one car simulation """
def test_simulator_runs_one_car_with_movement():
    car = Car(name="A", initial_position="1 2 N", commands="FFRFF", field=field)
    sim = Simulator(field=field, cars=[car])
    result = sim.run()

    assert result["A"] == {
        "position": (3, 4),
        "direction": "E"
    }

def test_simulator_car_hits_boundary_and_stays():
    car = Car(name="A", initial_position="4 4 N", commands="FFF", field=field)
    sim = Simulator(field=field, cars=[car])
    result = sim.run()

    assert result["A"] == {
        "position": (4, 4),  # Can't go beyond edge
        "direction": "N"
    }

def test_simulator_does_nothing_when_no_commands():
    car = Car(name="A", initial_position="0 0 W", commands="", field=field)
    sim = Simulator(field=field, cars=[car])
    result = sim.run()

    assert result["A"] == {
        "position": (0, 0),
        "direction": "W"
    }

def test_simulator_raises_error_for_invalid_car():
    with pytest.raises(RuntimeError, match="out of field bounds"):
        car = Car(name="A", initial_position="6 6 E", commands="F", field=field)
        Simulator(field=field, cars=[car])

def test_simulator_all_out_of_bounds_commands_ignored():
    car = Car(name="A", initial_position="0 0 S", commands="FFFF", field=field)
    sim = Simulator(field=field, cars=[car])
    result = sim.run()

    assert result["A"] == {
        "position": (0, 0),
        "direction": "S"
    }

# def test_simulator_raises_on_unknown_car_command():
#     car = Car(name="A", initial_position="1 1 N", commands="FX", field=field)
#     with pytest.raises(ValueError, match="Unknown command: X"):
#         Simulator(field=field, cars=[car])

def test_simulator_trims_whitespace_commands():
    car = Car(name="A", initial_position="2 2 E", commands=" F F R F  ", field=field)
    sim = Simulator(field=field, cars=[car])
    result = sim.run()

    assert result["A"] == {
        "position": (4, 1),
        "direction": "S"
    }

def test_simulator_car_turns_but_does_not_move():
    car = Car(name="A", initial_position="0 0 N", commands="RRRR", field=field)  # Full rotation
    sim = Simulator(field=field, cars=[car])
    result = sim.run()

    assert result["A"] == {
        "position": (0, 0),
        "direction": "N"
    }

def test_simulator_car_ignores_bad_move_but_processes_rest():
    car = Car(name="A", initial_position="0 0 S", commands="FFRFF", field=field)
    sim = Simulator(field=field, cars=[car])
    result = sim.run()

    assert result["A"] == {
        "position": (0, 0),  # Moved after turning right to East
        "direction": "W"
    }

def test_simulator_raises_on_empty_car_list():
    with pytest.raises(ValueError, match="No cars to simulate"):
        Simulator(field=field, cars=[])

def test_simulator_double_run_resets_or_preserves_state():
    car = Car(name="A", initial_position="1 2 N", commands="FF", field=field)
    sim = Simulator(field=field, cars=[car])

    result_1 = sim.run()
    result_2 = sim.run()  # This depends on design decision

    assert result_1 == result_2  # or assert a clear expectation


""" multiple cars simulation """
def test_simulation_two_cars_follow_commands_to_completion_without_collision():
    car_a = Car(name="A", initial_position="1 2 N", commands="FF", field=field)
    car_b = Car(name="B", initial_position="0 0 E", commands="FF", field=field)

    sim = Simulator(field=field, cars=[car_a, car_b])
    result = sim.run()

    assert result["A"] == {"position": (1, 4), "direction": "N"}
    assert result["B"] == {"position": (2, 0), "direction": "E"}

def test_simulation_multiple_cars_do_not_collide_with_independent_paths():
    car1 = Car(name="A", initial_position="0 0 N", commands="FF", field=field)
    car2 = Car(name="B", initial_position="2 2 E", commands="FF", field=field)

    simulator = Simulator(field=field, cars=[car1, car2])
    result = simulator.run()

    assert result["A"]["position"] == (0, 2)
    assert result["A"]["direction"] == "N"

    assert result["B"]["position"] == (4, 2)
    assert result["B"]["direction"] == "E"

def test_simulation_car_with_shorter_command_sequence():
    car1 = Car(name="A", initial_position="0 0 N", commands="F", field=field)
    car2 = Car(name="B", initial_position="1 0 N", commands="FFF", field=field)

    simulator = Simulator(field=field, cars=[car1, car2])
    result = simulator.run()

    assert result["A"]["position"] == (0, 1)
    assert result["B"]["position"] == (1, 3)

def test_simulation_cars_start_same_spot_different_directions_no_collision():
    car1 = Car(name="A", initial_position="3 3 N", commands="F", field=field)
    car2 = Car(name="B", initial_position="3 3 S", commands="F", field=field)

    simulator = Simulator(field=field, cars=[car1, car2])
    result = simulator.run()

    assert result["A"]["position"] == (3, 4)
    assert result["B"]["position"] == (3, 2)

# def test_simulation_detects_collision_between_two_cars():
#     car1 = Car(name="A", initial_position="1 1 E", commands="F", field=field)
#     car2 = Car(name="B", initial_position="2 1 W", commands="F", field=field)
#
#     sim = Simulator(field=field, cars=[car1, car2])
#     result = sim.run()
#
#     assert result["A"]["collided"] is True
#     assert result["B"]["collided"] is True
#     assert result["A"]["position"] == (1, 1)
#     assert result["B"]["position"] == (2, 1)
#
# def test_simulation_runs_without_collision_for_separate_paths():
#     car1 = Car(name="A", initial_position="0 0 N", commands="FF", field=field)
#     car2 = Car(name="B", initial_position="4 4 S", commands="FF", field=field)
#
#     sim = Simulator(field=field, cars=[car1, car2])
#     result = sim.run()
#
#     assert result["A"]["collided"] is False
#     assert result["B"]["collided"] is False
#
# def test_simulation_stops_on_collision_midway():
#     car1 = Car(name="A", initial_position="1 1 N", commands="FFF", field=field)
#     car2 = Car(name="B", initial_position="1 4 S", commands="FFF", field=field)
#
#     sim = Simulator(field=field, cars=[car1, car2])
#     result = sim.run()
#
#     # They meet at (1,2) after 2 moves
#     assert result["A"]["collided"]
#     assert result["B"]["collided"]
#     assert result["A"]["position"] == (1, 2)
#     assert result["B"]["position"] == (1, 3)


