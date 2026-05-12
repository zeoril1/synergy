import random

def createMatrix(rowsCount, colsCount):
    matrix = []

    for i in range(rowsCount):
        row = []

        for j in range(colsCount):
            row.append(random.randint(-50, 150))

        matrix.append(row)

    return matrix


def addMatrix(matrixOne, matrixTwo):
    resultMatrix = []

    for i in range(len(matrixOne)):
        row = []

        for j in range(len(matrixOne[i])):
            row.append(matrixOne[i][j] + matrixTwo[i][j])

        resultMatrix.append(row)

    return resultMatrix


rowsCount = 10
colsCount = 10

matrixOne = createMatrix(rowsCount, colsCount)
matrixTwo = createMatrix(rowsCount, colsCount)

matrixThree = addMatrix(matrixOne, matrixTwo)

print("Матрица 1:")
for row in matrixOne:
    print(row)

print("\nМатрица 2:")
for row in matrixTwo:
    print(row)

print("\nМатрица 3 (сумма):")
for row in matrixThree:
    print(row)