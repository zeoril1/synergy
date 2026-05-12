print("Введите первый список чисел")
list1 = input().split()

print("Введите второй список чисел")
list2 = input().split()

common = []

for x in list1:
    if x in list2 and x not in common:
        common.append(x)

print(len(common))
