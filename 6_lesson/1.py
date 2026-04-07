print("Введите количество вводимых символов")
number = int(input())

i = 0
summ = 0

while i < number:
    i = i + 1
    print("введите %i целое число:" % i)
    if int(input()) == 0:
        summ = summ + 1

print(summ)
