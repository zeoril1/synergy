import collections

pets = {
    1: {
        "Мухтар": {
            "Вид питомца": "Собака",
            "Возраст питомца": 9,
            "Имя владельца": "Павел"
        }
    },
    2: {
        "Каа": {
            "Вид питомца": "желторотый питон",
            "Возраст питомца": 19,
            "Имя владельца": "Саша"
        }
    }
}


def getPet(petId):
    return pets[petId] if petId in pets.keys() else False


def getSuffix(age):
    if age % 10 == 1 and age % 100 != 11:
        return "год"
    elif 2 <= age % 10 <= 4 and not (12 <= age % 100 <= 14):
        return "года"
    else:
        return "лет"


def petsList():
    for petId, petData in pets.items():
        petName = list(petData.keys())[0]
        petInfo = petData[petName]

        print(f"ID питомца: {petId}")
        print(
            f'Это {petInfo["Вид питомца"]} по кличке "{petName}". '
            f'Возраст питомца: {petInfo["Возраст питомца"]} '
            f'{getSuffix(petInfo["Возраст питомца"])}. '
            f'Имя владельца: {petInfo["Имя владельца"]}'
        )
        print()


def create():
    last = collections.deque(pets, maxlen=1)[0]

    petName = input("Введите имя питомца: ")
    petType = input("Введите вид питомца: ")
    petAge = int(input("Введите возраст питомца: "))
    ownerName = input("Введите имя владельца: ")

    pets[last + 1] = {
        petName: {
            "Вид питомца": petType,
            "Возраст питомца": petAge,
            "Имя владельца": ownerName
        }
    }

    print("Запись успешно создана!")


def read():
    petId = int(input("Введите ID питомца: "))

    pet = getPet(petId)

    if pet is False:
        print("Питомец не найден!")
        return

    petName = list(pet.keys())[0]
    petInfo = pet[petName]

    print(
        f'Это {petInfo["Вид питомца"]} по кличке "{petName}". '
        f'Возраст питомца: {petInfo["Возраст питомца"]} '
        f'{getSuffix(petInfo["Возраст питомца"])}. '
        f'Имя владельца: {petInfo["Имя владельца"]}'
    )


def update():
    petId = int(input("Введите ID питомца: "))

    pet = getPet(petId)

    if pet is False:
        print("Питомец не найден!")
        return

    petName = list(pet.keys())[0]

    newPetName = input("Введите новое имя питомца: ")
    newPetType = input("Введите новый вид питомца: ")
    newPetAge = int(input("Введите новый возраст питомца: "))
    newOwnerName = input("Введите новое имя владельца: ")

    pets[petId] = {
        newPetName: {
            "Вид питомца": newPetType,
            "Возраст питомца": newPetAge,
            "Имя владельца": newOwnerName
        }
    }

    print("Информация обновлена!")


def delete():
    petId = int(input("Введите ID питомца: "))

    if petId in pets.keys():
        del pets[petId]
        print("Запись удалена!")
    else:
        print("Питомец не найден!")


command = ""

while command != "stop":
    command = input(
        "\nВведите команду (create, read, update, delete, list, stop): "
    )

    if command == "create":
        create()

    elif command == "read":
        read()

    elif command == "update":
        update()

    elif command == "delete":
        delete()

    elif command == "list":
        petsList()

    elif command == "stop":
        print("Работа программы завершена.")

    else:
        print("Неизвестная команда!")