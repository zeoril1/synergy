print("Введите первое число")
firstNumber = int(input())

print("Введите второе число")
secondNumber = int(input())

result = ""

while firstNumber <= secondNumber:
    if firstNumber % 2 == 0:
        result = result + str(firstNumber) + " "
    firstNumber = firstNumber + 1

print(result)
