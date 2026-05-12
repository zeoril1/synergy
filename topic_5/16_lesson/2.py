class Turtle:
    def __init__(self, x=0, y=0, s=1):
        self.x = x
        self.y = y
        self.s = s

    def goUp(self):
        self.y += self.s

    def goDown(self):
        self.y -= self.s

    def goLeft(self):
        self.x -= self.s

    def goRight(self):
        self.x += self.s

    def evolve(self):
        self.s += 1

    def degrade(self):

        if self.s - 1 <= 0:
            raise ValueError("Шаг не может быть меньше или равен 0!")

        self.s -= 1

    def countMoves(self, x2, y2):

        distanceX = abs(x2 - self.x)
        distanceY = abs(y2 - self.y)

        movesX = distanceX // self.s
        movesY = distanceY // self.s

        if distanceX % self.s != 0:
            movesX += 1

        if distanceY % self.s != 0:
            movesY += 1

        return movesX + movesY


turtle = Turtle(0, 0, 2)

print(f"Позиция черепашки: x = {turtle.x}, y = {turtle.y}")

turtle.goUp()

print(f"Позиция черепашки: x = {turtle.x}, y = {turtle.y}")

turtle.goRight()

print(f"Позиция черепашки: x = {turtle.x}, y = {turtle.y}")

turtle.evolve()

print(f"Новый шаг: {turtle.s}")

turtle.goLeft()

print(f"Позиция черепашки: x = {turtle.x}, y = {turtle.y}")

turtle.goDown()
print(f"Позиция черепашки: x = {turtle.x}, y = {turtle.y}")

turtle.degrade()

print(f"Новый шаг: {turtle.s}")

turtle.degrade()
print(f"Новый шаг: {turtle.s}")

print("Минимальное количество ходов:",
      turtle.countMoves(10, 7))