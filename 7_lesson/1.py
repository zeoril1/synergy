print("Введите строку")
inputString = str(input())

if inputString == inputString[::-1]:
    print("yes")
else:
    print("no")