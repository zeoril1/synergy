def getFactorial(number):
    factorial = 1

    for i in range(1, number + 1):
        factorial *= i

    return factorial


userNumber = int(input("Введите натуральное число: "))

mainFactorial = getFactorial(userNumber)

factorialList = []

for i in range(mainFactorial, 0, -1):
    factorialList.append(getFactorial(i))

print("Факториал числа:", mainFactorial)
print("Список факториалов:", factorialList)