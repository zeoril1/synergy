class Transport:
    def __init__(self, name, maxSpeed, mileage):
        self.name = name
        self.maxSpeed = maxSpeed
        self.mileage = mileage


class Autobus(Transport):
    pass


bus = Autobus("Renaul Logan", 180, 12)

print(
    f"Название автомобиля: {bus.name} "
    f"Скорость: {bus.maxSpeed} "
    f"Пробег: {bus.mileage}"
)