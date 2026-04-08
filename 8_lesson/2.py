print("Введите количество вводимых чисел от 1 до 100 000")
sumNumbers = int(input())
print("Введите числа через , от 1 до 1 000 000 000")
numbers = str(input())

numbers = numbers.split(",")
newNumbers = []
i=0

while i < sumNumbers:
    if i == sumNumbers - 1:
        newNumbers.append(numbers[0])
    else:
        newNumbers.append(numbers[i+1])
    i = i + 1
print(newNumbers)

