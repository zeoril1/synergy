# Класс Касса
class CashRegister:
    def __init__(self, money=0):
        self.money = money

    def topUp(self, amount):
        self.money += amount
        print(f"Касса пополнена на {amount}. Текущая сумма: {self.money}")

    def count1000(self):
        print(f"Количество целых тысяч в кассе: {self.money // 1000}")

    def takeAway(self, amount):

        if amount > self.money:
            raise ValueError("Недостаточно денег в кассе!")

        self.money -= amount
        print(f"Из кассы забрали {amount}. Остаток: {self.money}")


cash = CashRegister(5000)

cash.topUp(123456)

cash.count1000()

cash.takeAway(54321)

cash.count1000()