print("Введите минимальную сумму для вложения")
minimum = int(input())

print("Сумма у Майкла")
mike = int(input())

print("Сумма у Ивана")
ivan = int(input())

mikeCheck = mike >= minimum or False
ivanCheck = ivan >= minimum or False

if mikeCheck and ivanCheck:
    print(2)
elif mikeCheck:
    print("Mike")
elif ivanCheck:
    print("Ivan")
elif mike+ivan>=minimum:
    print(1)
else:
    print(0)