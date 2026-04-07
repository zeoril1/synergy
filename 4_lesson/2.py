print("Введите пятизначное число")
number = input()
summ = float((int(number[3]) ** int(number[4])) * int(number[2]) / (int(number[0]) - int(number[1])))
print(summ)
