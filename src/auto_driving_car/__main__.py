from auto_driving_car.field import Field
from auto_driving_car.car import Car
from auto_driving_car.simulator import Simulator
from auto_driving_car.utils.validators import Validators

cars = []
field = None

def main():
    global field, cars
    print("Welcome to Auto Driving Car Simulation!")
    print("Please enter the width and height of the simulation field in x y format (e.g. '1 1'):")

    try:
        width, height = map(int, input("> ").strip().split())
        field = Field(width, height)
        print(f"You have created a field of {width} x {height}.")
    except ValueError:
        print("Invalid field size. Please enter two integers.")
        return

    while True:
        print("\nPlease choose from the following options:")
        print("[1] Add a car to field")
        print("[2] Run simulation")
        choice = input("> ").strip()

        if choice == "1":
            add_car()
        elif choice == "2":
            run_simulation()
        else:
            print("Invalid choice. Please select 1 or 2.")

def add_car():
    global cars
    try:
        print("Please enter the name of the car:")
        name = input("> ").strip().upper()

        if any(car.name == name for car in cars):
            print(f"Car name '{name}' already exists. Please choose a unique name.")
            return

        print(f"Please enter initial position of car {name} in x y Direction format (e.g. '1 2 N'):")
        position = input("> ").strip().upper()

        print(f"Please enter the commands for car {name}: (e.g. 'FFLR'):")
        commands = input("> ").strip().replace(" ", "")

        Validators.validate_commands(commands)

        new_car = Car(name=name, initial_position=position, commands=commands, field=field)
        cars.append(new_car)

        print(f"\nCar '{new_car.name}' added successfully.")
        display_current_cars()

    except Exception as e:
        print(f"Failed to add car: {e}")

def display_current_cars():
    print("\nYour current list of cars are:")
    for car in cars:
        print(f"- {car.name}, ({car.x_axis}, {car.y_axis}) {car.direction.value}, {''.join(car.commands)}")


def run_simulation():
    global cars, field

    if not cars:
        print("No cars were added. Please add at least one car before running the simulation.")
        return

    display_current_cars()

    print("\nRunning simulation...\n")
    simulator = Simulator(field=field, cars=cars)
    results = simulator.run()

    print("After simulation, the result is:")
    for car in cars:
        result = results[car.name]
        print(f"- {car.name}, {result['position']} {result['direction']}")

    post_simulation_menu()

    # Post-simulation menu
def post_simulation_menu():
    global cars
    while True:
        print("\nPlease choose from the following options:")
        print("[1] Start over")
        print("[2] Exit")
        next_choice = input("> ").strip()

        if next_choice == "1":
            print("\nRestarting simulation...\n")
            cars = []
            main()
            return
        elif next_choice == "2":
            print("\nThank you for running the simulation. Goodbye!")
            exit()
        else:
            print("Invalid option. Please choose 1 or 2.")

if __name__ == "__main__":
    main()
