pets = {}

petName = input("Введите имя питомца: ")
petType = input("Введите вид питомца: ")
petAge = int(input("Введите возраст питомца: "))
ownerName = input("Введите имя владельца: ")

pets[petName] = {
    "Вид питомца": petType,
    "Возраст питомца": petAge,
    "Имя владельца": ownerName
}

age = pets[petName]["Возраст питомца"]

if age % 10 == 1 and age % 100 != 11:
    years = "год"
elif 2 <= age % 10 <= 4 and not (12 <= age % 100 <= 14):
    years = "года"
else:
    years = "лет"

petInfo = list(pets.values())[0]

print(
    f'Это {petInfo["Вид питомца"]} по кличке "{petName}". '
    f'Возраст питомца: {petInfo["Возраст питомца"]} {years}. '
    f'Имя владельца: {petInfo["Имя владельца"]}'
)