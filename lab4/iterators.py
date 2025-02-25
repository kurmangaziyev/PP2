from datetime import datetime, timedelta  

# 1. Генератор квадратов чисел до N
def square_generator(n):
    for i in range(1, n + 1):
        yield i ** 2

# 2. Генератор чётных чисел до N
def even_numbers(n):
    for i in range(0, n + 1, 2):
        yield i

# 3. Генератор чисел, делящихся на 3 и 4
def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

# 4. Генератор квадратов от a до b
def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2

# 5. Генератор обратного отсчёта
def countdown(n):
    for i in range(n, -1, -1):
        yield i

# Компактные тесты
if __name__ == "__main__":
    print("Квадраты до 5:", list(square_generator(5)))
    n = int(input("Введите N для чётных чисел: "))
    print("Чётные числа:", ", ".join(map(str, even_numbers(n))))
    n = int(input("Введите N для чисел, делящихся на 3 и 4: "))
    print("Числа, делящиеся на 3 и 4:", list(divisible_by_3_and_4(n)))
    print("Квадраты от 3 до 7:", list(squares(3, 7)))
    print("Обратный отсчёт от 10:", list(countdown(10)))
