print("Введите максимальную массу лодки (m):")
m = int(input())

print("Введите количество рыбаков (n):")
n = int(input())

weights = []

i = 0
while i < n:
    i = i + 1
    print("Введите вес %i-го рыбака:" % i)
    weights.append(int(input()))

weights.sort()

left = 0
right = n - 1
boats = 0

while left <= right:
    if weights[left] + weights[right] <= m:
        left += 1
    right -= 1
    boats += 1

print(boats)
