from auto_driving_car.direction import Direction
from auto_driving_car.field import Field
from auto_driving_car.utils.validators import Validators


class Car:
    def __init__(self, name: str, initial_position: str, commands: str, field: Field):
        self.name = name
        self.field = field
        self.has_collided = False
        self.collided_with = None
        self.collision_step = None
        self.command_pointer = 0

        try:
            x_str, y_str, dir_str = initial_position.strip().split()
            self.x_axis = int(x_str)
            self.y_axis = int(y_str)
            self.direction = Direction(dir_str)
        except Exception:
            raise ValueError(f"Invalid initial position for car {name}: {initial_position}")

        commands = commands.replace(" ", "")
        Validators.validate_commands(commands)
        self.commands = list(commands)

        if not self.field.is_within_bounds(self.x_axis, self.y_axis):
            raise RuntimeError("Initial position is out of field bounds")

        self._initial_position = (self.x_axis, self.y_axis, self.direction.value)
        self._initial_commands = list(self.commands)

    def execute_next_command(self, command=None):
        if command is None:
            if not self.commands:
                return
            command = self.commands.pop(0)

        if command == 'F':
            dx, dy = self.direction.forward_offset()
            next_x = self.x_axis + dx
            next_y = self.y_axis + dy

            if self.field.is_within_bounds(next_x, next_y):
                self.x_axis = next_x
                self.y_axis = next_y

        elif command == 'L':
            self.direction = self.direction.left()

        elif command == 'R':
            self.direction = self.direction.right()

    def current_position(self):
        return self.x_axis, self.y_axis

    def reset(self):
        self.x_axis, self.y_axis, dir_value = self._initial_position
        self.direction = Direction(dir_value)
        self.commands = list(self._initial_commands)

    def collide_with(self, other_car_name, position, step):
        self.has_collided = True
        self.collided_with = other_car_name
        self.collision_step = step
