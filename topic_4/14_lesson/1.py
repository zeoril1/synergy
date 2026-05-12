myList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

def showList(listData, index=0):
    if index >= len(listData):
        print("Конец списка")
        return

    print(listData[index])

    showList(listData, index + 1)


showList(myList)