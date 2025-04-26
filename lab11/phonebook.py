import psycopg2
import csv
from psycopg2 import sql
import os

# Параметры подключения к базе данных
DB_NAME = "phonebook_db"
DB_USER = "bmk"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"

def create_connection():
    """Создает подключение к базе данных PostgreSQL"""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except psycopg2.Error as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        return None

def create_tables():
    """Создает необходимые таблицы для телефонной книги"""
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            
            # Создание таблицы для контактов
            cur.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    email VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Создание таблицы для телефонов
            cur.execute("""
                CREATE TABLE IF NOT EXISTS phones (
                    id SERIAL PRIMARY KEY,
                    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
                    phone_number VARCHAR(20) NOT NULL,
                    phone_type VARCHAR(20) DEFAULT 'mobile'
                );
            """)
            
            conn.commit()
            print("Таблицы успешно созданы")
        except psycopg2.Error as e:
            print(f"Ошибка при создании таблиц: {e}")
        finally:
            cur.close()
            conn.close()

def insert_contact_from_console():
    """Вставка данных о контакте из консоли"""
    try:
        first_name = input("Введите имя: ")
        last_name = input("Введите фамилию: ")
        email = input("Введите email (необязательно): ")
        phone_number = input("Введите номер телефона: ")
        phone_type = input("Введите тип телефона (по умолчанию 'mobile'): ") or "mobile"
        
        conn = create_connection()
        if conn:
            cur = conn.cursor()
            
            # Вставка контакта
            cur.execute("""
                INSERT INTO contacts (first_name, last_name, email)
                VALUES (%s, %s, %s) RETURNING id;
            """, (first_name, last_name, email))
            
            contact_id = cur.fetchone()[0]
            
            # Вставка телефона
            cur.execute("""
                INSERT INTO phones (contact_id, phone_number, phone_type)
                VALUES (%s, %s, %s);
            """, (contact_id, phone_number, phone_type))
            
            conn.commit()
            print(f"Контакт {first_name} {last_name} успешно добавлен")
            cur.close()
            conn.close()
    except Exception as e:
        print(f"Ошибка при добавлении контакта: {e}")

def insert_contacts_from_csv(file_path):
    """Загрузка контактов из CSV файла"""
    try:
        conn = create_connection()
        if conn:
            cur = conn.cursor()
            
            with open(file_path, mode='r', encoding='utf-8') as csvfile:
                csv_reader = csv.DictReader(csvfile)
                
                for row in csv_reader:
                    # Вставка контакта
                    cur.execute("""
                        INSERT INTO contacts (first_name, last_name, email)
                        VALUES (%s, %s, %s) RETURNING id;
                    """, (row.get('first_name'), row.get('last_name'), row.get('email')))
                    
                    contact_id = cur.fetchone()[0]
                    
                    # Вставка телефона
                    cur.execute("""
                        INSERT INTO phones (contact_id, phone_number, phone_type)
                        VALUES (%s, %s, %s);
                    """, (contact_id, row.get('phone_number'), row.get('phone_type', 'mobile')))
            
            conn.commit()
            print("Контакты из CSV успешно загружены")
            cur.close()
            conn.close()
    except Exception as e:
        print(f"Ошибка при загрузке контактов из CSV: {e}")

def update_contact():
    """Обновление данных контакта"""
    try:
        search_term = input("Введите имя или фамилию контакта для обновления: ")
        
        conn = create_connection()
        if conn:
            cur = conn.cursor()
            
            # Поиск контакта
            cur.execute("""
                SELECT c.id, c.first_name, c.last_name, c.email, p.phone_number, p.phone_type
                FROM contacts c
                JOIN phones p ON c.id = p.contact_id
                WHERE c.first_name ILIKE %s OR c.last_name ILIKE %s
            """, (f'%{search_term}%', f'%{search_term}%'))
            
            contacts = cur.fetchall()
            
            if not contacts:
                print("Контакты не найдены")
                return
            
            print("\nНайденные контакты:")
            for i, contact in enumerate(contacts):
                print(f"{i+1}. {contact[1]} {contact[2]}, Email: {contact[3]}, Телефон: {contact[4]} ({contact[5]})")
            
            try:
                choice = int(input("\nВыберите номер контакта для обновления: ")) - 1
                contact_id = contacts[choice][0]
                
                print("\nЧто вы хотите обновить?")
                print("1. Имя")
                print("2. Фамилию")
                print("3. Email")
                print("4. Номер телефона")
                
                update_choice = int(input("Введите ваш выбор: "))
                
                if update_choice == 1:
                    new_value = input("Введите новое имя: ")
                    cur.execute("""
                        UPDATE contacts SET first_name = %s WHERE id = %s
                    """, (new_value, contact_id))
                elif update_choice == 2:
                    new_value = input("Введите новую фамилию: ")
                    cur.execute("""
                        UPDATE contacts SET last_name = %s WHERE id = %s
                    """, (new_value, contact_id))
                elif update_choice == 3:
                    new_value = input("Введите новый email: ")
                    cur.execute("""
                        UPDATE contacts SET email = %s WHERE id = %s
                    """, (new_value, contact_id))
                elif update_choice == 4:
                    new_value = input("Введите новый номер телефона: ")
                    cur.execute("""
                        UPDATE phones SET phone_number = %s 
                        WHERE contact_id = %s
                    """, (new_value, contact_id))
                
                conn.commit()
                print("Контакт успешно обновлен")
            except (ValueError, IndexError):
                print("Неверный выбор")
            
            cur.close()
            conn.close()
    except Exception as e:
        print(f"Ошибка при обновлении контакта: {e}")

def query_contacts():
    """Поиск контактов с различными фильтрами"""
    try:
        print("\nПоиск контактов:")
        print("1. По имени или фамилии")
        print("2. По номеру телефона")
        print("3. По email")
        print("4. Вывести все контакты")
        
        search_choice = int(input("Выберите тип поиска: "))
        
        conn = create_connection()
        if conn:
            cur = conn.cursor()
            
            if search_choice == 1:
                search_term = input("Введите имя или фамилию: ")
                cur.execute("""
                    SELECT c.first_name, c.last_name, c.email, p.phone_number, p.phone_type
                    FROM contacts c
                    JOIN phones p ON c.id = p.contact_id
                    WHERE c.first_name ILIKE %s OR c.last_name ILIKE %s
                """, (f'%{search_term}%', f'%{search_term}%'))
            elif search_choice == 2:
                search_term = input("Введите номер телефона: ")
                cur.execute("""
                    SELECT c.first_name, c.last_name, c.email, p.phone_number, p.phone_type
                    FROM contacts c
                    JOIN phones p ON c.id = p.contact_id
                    WHERE p.phone_number LIKE %s
                """, (f'%{search_term}%',))
            elif search_choice == 3:
                search_term = input("Введите email: ")
                cur.execute("""
                    SELECT c.first_name, c.last_name, c.email, p.phone_number, p.phone_type
                    FROM contacts c
                    JOIN phones p ON c.id = p.contact_id
                    WHERE c.email ILIKE %s
                """, (f'%{search_term}%',))
            elif search_choice == 4:
                cur.execute("""
                    SELECT c.first_name, c.last_name, c.email, p.phone_number, p.phone_type
                    FROM contacts c
                    JOIN phones p ON c.id = p.contact_id
                    ORDER BY c.last_name, c.first_name
                """)
            else:
                print("Неверный выбор")
                return
            
            contacts = cur.fetchall()
            
            if contacts:
                print("\nНайденные контакты:")
                print("Имя | Фамилия | Email | Телефон | Тип")
                print("-" * 80)
                for contact in contacts:
                    print(f"{contact[0]} | {contact[1]} | {contact[2]} | {contact[3]} | {contact[4]}")
            else:
                print("Контакты не найдены")
            
            cur.close()
            conn.close()
    except Exception as e:
        print(f"Ошибка при поиске контактов: {e}")

def delete_contact():
    """Удаление контакта по имени пользователя или номеру телефона"""
    try:
        print("\nУдаление контакта:")
        print("1. По имени или фамилии")
        print("2. По номеру телефона")
        
        delete_choice = int(input("Выберите способ удаления: "))
        
        conn = create_connection()
        if conn:
            cur = conn.cursor()
            
            if delete_choice == 1:
                search_term = input("Введите имя или фамилию: ")
                cur.execute("""
                    SELECT c.id, c.first_name, c.last_name, p.phone_number
                    FROM contacts c
                    JOIN phones p ON c.id = p.contact_id
                    WHERE c.first_name ILIKE %s OR c.last_name ILIKE %s
                """, (f'%{search_term}%', f'%{search_term}%'))
            elif delete_choice == 2:
                search_term = input("Введите номер телефона: ")
                cur.execute("""
                    SELECT c.id, c.first_name, c.last_name, p.phone_number
                    FROM contacts c
                    JOIN phones p ON c.id = p.contact_id
                    WHERE p.phone_number LIKE %s
                """, (f'%{search_term}%',))
            else:
                print("Неверный выбор")
                return
            
            contacts = cur.fetchall()
            
            if not contacts:
                print("Контакты не найдены")
                return
            
            print("\nНайденные контакты:")
            for i, contact in enumerate(contacts):
                print(f"{i+1}. {contact[1]} {contact[2]}, Телефон: {contact[3]}")
            
            try:
                choice = int(input("\nВыберите номер контакта для удаления (0 для отмены): "))
                if choice == 0:
                    print("Удаление отменено")
                    return
                    
                contact_id = contacts[choice-1][0]
                
                # Удаление контакта (каскадно удалит и связанные телефоны)
                cur.execute("""
                    DELETE FROM contacts WHERE id = %s
                """, (contact_id,))
                
                conn.commit()
                print("Контакт успешно удален")
            except (ValueError, IndexError):
                print("Неверный выбор")
            
            cur.close()
            conn.close()
    except Exception as e:
        print(f"Ошибка при удалении контакта: {e}")

def create_sample_csv():
    """Создает пример CSV файла с контактами"""
    try:
        file_path = "sample_contacts.csv"
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['first_name', 'last_name', 'email', 'phone_number', 'phone_type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerow({
                'first_name': 'Иван', 
                'last_name': 'Иванов', 
                'email': 'ivan@example.com', 
                'phone_number': '+7 999 123 4567', 
                'phone_type': 'mobile'
            })
            writer.writerow({
                'first_name': 'Мария', 
                'last_name': 'Петрова', 
                'email': 'maria@example.com', 
                'phone_number': '+7 999 765 4321', 
                'phone_type': 'work'
            })
            writer.writerow({
                'first_name': 'Алексей', 
                'last_name': 'Сидоров', 
                'email': 'alex@example.com', 
                'phone_number': '+7 999 555 1234', 
                'phone_type': 'home'
            })
        
        print(f"Пример CSV файла создан: {file_path}")
        return file_path
    except Exception as e:
        print(f"Ошибка при создании примера CSV файла: {e}")
        return None

def main():
    # Создаем таблицы
    create_tables()
    
    while True:
        print("\nТелефонная книга:")
        print("1. Добавить контакт вручную")
        print("2. Загрузить контакты из CSV")
        print("3. Обновить данные контакта")
        print("4. Поиск контактов")
        print("5. Удалить контакт")
        print("6. Создать пример CSV файла")
        print("0. Выход")
        
        try:
            choice = int(input("Выберите действие: "))
            
            if choice == 1:
                insert_contact_from_console()
            elif choice == 2:
                file_path = input("Введите путь к CSV файлу: ")
                insert_contacts_from_csv(file_path)
            elif choice == 3:
                update_contact()
            elif choice == 4:
                query_contacts()
            elif choice == 5:
                delete_contact()
            elif choice == 6:
                create_sample_csv()
            elif choice == 0:
                print("Программа завершена")
                break
            else:
                print("Неверный выбор")
        except ValueError:
            print("Пожалуйста, введите число")

if __name__ == "__main__":
    main()