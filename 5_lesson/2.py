print("Введите слово на латинице")
word = input()

a = word.count('a') or False
e = word.count('e') or False
i = word.count('i') or False
o = word.count('o') or False
u = word.count('u') or False

sumVowel = a + e + i + o + u

print("Гласных:", sumVowel)
print("Согласных:", len(word)-sumVowel)

print("\na:", a)
print("e:", e)
print("i:", i)
print("o:", o)
print("u:", u)