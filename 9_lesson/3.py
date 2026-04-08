print("Введите числа через пробел")
numbers = input().split()

seen = []

for x in numbers:
    if x in seen:
        print("YES")
    else:
        print("NO")
        seen.append(x)
