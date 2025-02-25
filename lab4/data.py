from datetime import datetime, timedelta  # Импортируем нужные модули

# 1. тут я беру текущую дату и отнимаю 5 дней с помощью timedelta(days=5), потом просто вывожу обе даты.
current_date = datetime.now()  # Получаем текущую дату и время
new_date = current_date - timedelta(days=5)  # Отнимаем 5 дней
print("Текущая дата:", current_date.strftime("%Y-%m-%d"))
print("Дата 5 дней назад:", new_date.strftime("%Y-%m-%d"))
print("-" * 40)

# 2.  тут я считаю вчера, сегодня и завтра. Важный момент, что .date() я использовал чтобы убрать время и оставить только дату.
today = datetime.now().date()  # Получаем сегодняшнюю дату (без времени)
yesterday = today - timedelta(days=1)  # Вычисляем вчерашнюю дату
tomorrow = today + timedelta(days=1)  # Вычисляем завтрашнюю дату
print("Вчера:", yesterday)
print("Сегодня:", today)
print("Завтра:", tomorrow)
print("-" * 40)

# 3. здесь я убрал микросекунды из текущего времени, потому что .replace(microsecond=0) просто заменяет их на ноль.
current_time = datetime.now().replace(microsecond=0)  # Убираем микросекунды
print("Текущее время без микросекунд:", current_time)
print("-" * 40)

# 4. тут я создал две даты вручную и вычел их, после чего использовал .total_seconds(), чтобы получить разницу в секундах.
date1 = datetime(2024, 2, 20, 14, 30, 0)  # Пример первой даты
date2 = datetime(2024, 2, 25, 18, 45, 0)  # Пример второй даты
difference = (date2 - date1).total_seconds()  # Разница в секундах
print("Разница между датами в секундах:", difference)
