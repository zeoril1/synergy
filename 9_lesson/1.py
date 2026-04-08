print("Введите количество чисел N")
n = int(input())

print("Введите числа через пробел")
numbers = input()
numbers = numbers.split(" ")

uniqueNumbers = []

for x in numbers:
    if x not in uniqueNumbers:
        uniqueNumbers.append(x)

print(len(uniqueNumbers))
