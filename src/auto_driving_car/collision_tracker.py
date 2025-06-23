
class CollisionTracker:
    def __init__(self):
        self.current_positions = {}
        self.next_positions = {}
        self.collided_cars = set()
        self.step = 0

    def reset(self):
        self.current_positions.clear()
        self.next_positions.clear()
        self.collided_cars.clear()
        self.step = 0

    def register_car(self, car):
        pos = car.current_position()
        if pos in self.current_positions:
            self._mark_collision(car, self.current_positions[pos], pos)
            return True
        self.current_positions[pos] = car
        return False

    def _mark_collision(self, car1, car2, position):
        car1.collide_with(car2.name, position, self.step)
        car2.collide_with(car1.name, position, self.step)
        self.collided_cars.add(car1.name)
        self.collided_cars.add(car2.name)

    def preview_move(self, car, next_position):
        if next_position not in self.next_positions:
            self.next_positions[next_position] = []
        self.next_positions[next_position].append(car)

    def resolve_collisions(self):
        for position, cars in self.next_positions.items():
            if len(cars) > 1:
                for car in cars:
                    others = [c.name for c in cars if c != car]
                    if others:
                        car.collide_with(others[0], position, self.step)
                        self.collided_cars.add(car.name)
            else:
                car = cars[0]
                old_pos = car.current_position()
                new_x, new_y = position
                car.x_axis, car.y_axis = new_x, new_y
                self.current_positions[position] = car
        self.next_positions.clear()
