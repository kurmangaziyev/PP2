import math  # Подключаем модуль математики, потому что мы тут серьёзные ребята 🤓

def degrees_to_radians(degree):
    """Функция переводит градусы в радианы по формуле: радианы = градусы × (π / 180)"""
    return degree * (math.pi / 180)

# Спрашиваем у пользователя, сколько градусов надо перевести
degree = float(input("🔥 Введите угол в градусах: "))

# Вызываем функцию и переводим градусы в радианы
radian = degrees_to_radians(degree)

# Красиво выводим результат с 6 знаками после запятой
print(f"🎯 Угол в радианах: {radian:.6f} 🔥")