from auto_driving_car.car import Car
from auto_driving_car.field import Field
from auto_driving_car.collision_tracker import CollisionTracker


class Simulator:
    def __init__(self, field: Field, cars: list[Car]):
        if not cars:
            raise ValueError("No cars to simulate")
        self.field = field
        self.cars = cars
        self.collision_tracker = CollisionTracker()

    def run(self):
        if not self.cars:
            raise ValueError("No cars to simulate")

        self.collision_tracker.reset()

        max_steps = max(len(car.commands) for car in self.cars)
        for step in range(max_steps):
            self.collision_tracker.step = step
            next_positions = {}
            collision = False

            for car in self.cars:
                if step < len(car.commands):
                    command = car.commands[step]

                    if command == "F":
                        dx, dy = car.direction.forward_offset()
                        next_x = car.x_axis + dx
                        next_y = car.y_axis + dy

                        if self.field.is_within_bounds(next_x, next_y):
                            next_positions.setdefault((next_x, next_y), []).append(car)
                        else:
                            car.execute_next_command(command)
                    else:
                        car.execute_next_command(command)

            for pos, cars_at_pos in next_positions.items():
                if len(cars_at_pos) > 1:
                    for car in cars_at_pos:
                        for other_car in cars_at_pos:
                            if car != other_car:
                                self.collision_tracker._mark_collision(car, other_car, pos)
                    collision = True
                else:
                    car = cars_at_pos[0]
                    car.execute_next_command("F")
            if collision:
                print("After simulation, the result is:")
                for car in self.cars:
                    if hasattr(car, 'collided_with') and car.collided_with:
                        print(
                            f"- {car.name}, collides with {car.collided_with} at {car.current_position()} at step {car.collision_step}\n"
                        )
                break

        results = {}
        for car in self.cars:
            result = {
                "position": car.current_position(),
                "direction": car.direction.value
            }

            if hasattr(car, 'collided_with') and car.collided_with is not None:
                result["collided"] = True
                result["collided_with"] = car.collided_with
                result["collision_step"] = car.collision_step

            results[car.name] = result

        return results