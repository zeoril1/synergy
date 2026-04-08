print("Введите количество вводимых чисел от 1 до 10000")
sumNumbers = int(input())

numbers = []
i=0

while i < sumNumbers:
    i = i + 1
    print("Введите %i число" % i)
    numbers.append(int(input()))

print(numbers[::-1])