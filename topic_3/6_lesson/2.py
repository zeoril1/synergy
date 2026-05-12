print("Введите натуральное число меньше или равное 2 миллиардам")
number = int(input())

summ = 0

if number < 2000000001:
    for i in range(number):
        if not number % (i + 1):
            print(i+1)
            summ = summ + 1
    print(summ)
else:
    print("Число больше 2 миллиардов")
