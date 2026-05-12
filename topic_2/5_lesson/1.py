print("Введите число")
number = input()
number = int(number)

if number != 0:
    if number % 2:
        remainderDiv = "нечетное "
    else:
        remainderDiv = "четное "

    if number < 0:
        rationalNumber = "Отрицательное "
    else:
        rationalNumber = "Положительное "

    print(rationalNumber+remainderDiv+"число")
else:
    print("нулевое число")
