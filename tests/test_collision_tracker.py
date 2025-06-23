from auto_driving_car.car import Car
from auto_driving_car.field import Field
from auto_driving_car.collision_tracker import CollisionTracker

field = Field(10, 10)

def test_register_single_car_has_no_collision():
    car = Car(name="A", initial_position="0 0 N", commands="", field=field)
    tracker = CollisionTracker()

    collided = tracker.register_car(car)

    assert not collided
    assert not car.has_collided

def test_collision_detected_when_two_cars_occupy_same_position():
    car1 = Car(name="A", initial_position="1 1 N", commands="", field=field)
    car2 = Car(name="B", initial_position="1 1 N", commands="", field=field)

    tracker = CollisionTracker()
    tracker.register_car(car1)
    collided = tracker.register_car(car2)

    assert collided
    assert car1.has_collided
    assert car2.has_collided

def test_no_collision_when_cars_in_different_positions():
    car1 = Car(name="A", initial_position="1 1 N", commands="", field=field)
    car2 = Car(name="B", initial_position="2 2 N", commands="", field=field)

    tracker = CollisionTracker()
    tracker.register_car(car1)
    collided = tracker.register_car(car2)

    assert not collided
    assert not car1.has_collided
    assert not car2.has_collided


def test_reset_clears_all_positions():
    car = Car(name="A", initial_position="0 0 N", commands="", field=field)
    tracker = CollisionTracker()

    tracker.register_car(car)
    tracker.reset()

    assert tracker.current_positions == {}
    assert tracker.next_positions == {}
    assert tracker.collided_cars == set()
    assert tracker.step == 0
