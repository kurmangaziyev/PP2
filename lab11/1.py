import psycopg2
import csv
from psycopg2 import sql
import re

# Параметры подключения к базе данных
DB_NAME = "phonebook1_db"
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
            
            # Создание функции для поиска по паттерну
            cur.execute("""
                CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
                RETURNS TABLE(first_name VARCHAR, last_name VARCHAR, email VARCHAR, phone_number VARCHAR) AS $$
                BEGIN
                    RETURN QUERY
                    SELECT c.first_name, c.last_name, c.email, p.phone_number
                    FROM contacts c
                    JOIN phones p ON c.id = p.contact_id
                    WHERE c.first_name ILIKE '%' || pattern || '%' OR c.last_name ILIKE '%' || pattern || '%' OR p.phone_number LIKE '%' || pattern || '%';
                END;
                $$ LANGUAGE plpgsql;
            """)
            
            # Процедура для вставки нового пользователя
            cur.execute("""
                CREATE OR REPLACE PROCEDURE insert_user(name VARCHAR, phone VARCHAR)
                LANGUAGE plpgsql AS $$
                BEGIN
                    IF EXISTS (SELECT 1 FROM contacts c JOIN phones p ON c.id = p.contact_id WHERE p.phone_number = phone) THEN
                        UPDATE phones SET phone_number = phone WHERE contact_id = (SELECT id FROM contacts c JOIN phones p ON c.id = p.contact_id WHERE p.phone_number = phone);
                    ELSE
                        INSERT INTO contacts (first_name, last_name) VALUES (name, ' ') RETURNING id INTO contact_id;
                        INSERT INTO phones (contact_id, phone_number) VALUES (contact_id, phone);
                    END IF;
                END;
                $$;
            """)
            
            # Процедура для вставки нескольких пользователей
            cur.execute("""
                CREATE OR REPLACE PROCEDURE insert_multiple_users(users TEXT[])
                LANGUAGE plpgsql AS $$
                DECLARE
                    user_record TEXT;
                    user_name VARCHAR;
                    user_phone VARCHAR;
                BEGIN
                    FOREACH user_record IN ARRAY users
                    LOOP
                        user_name := split_part(user_record, ',', 1);
                        user_phone := split_part(user_record, ',', 2);
                        PERFORM insert_user(user_name, user_phone);
                    END LOOP;
                END;
                $$;
            """)

            # Процедура для удаления контакта по имени или номеру телефона
            cur.execute("""
                CREATE OR REPLACE PROCEDURE delete_contact(search_term TEXT)
                LANGUAGE plpgsql AS $$
                BEGIN
                    DELETE FROM contacts WHERE id IN (
                        SELECT c.id
                        FROM contacts c
                        JOIN phones p ON c.id = p.contact_id
                        WHERE c.first_name ILIKE '%' || search_term || '%' OR c.last_name ILIKE '%' || search_term || '%' OR p.phone_number LIKE '%' || search_term || '%'
                    );
                END;
                $$;
            """)

            conn.commit()
            print("Таблицы и функции успешно созданы")
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
        phone_number = input("Введите номер телефона: ")
        
        conn = create_connection()
        if conn:
            cur = conn.cursor()
            
            # Вставка контакта
            cur.execute("""
                INSERT INTO contacts (first_name, last_name)
                VALUES (%s, %s) RETURNING id;
            """, (first_name, last_name))
            
            contact_id = cur.fetchone()[0]
            
            # Вставка телефона
            cur.execute("""
                INSERT INTO phones (contact_id, phone_number)
                VALUES (%s, %s);
            """, (contact_id, phone_number))
            
            conn.commit()
            print(f"Контакт {first_name} {last_name} успешно добавлен")
            cur.close()
            conn.close()
    except Exception as e:
        print(f"Ошибка при добавлении контакта: {e}")

def query_contacts():
    """Поиск контактов с различными фильтрами"""
    pattern = input("Введите паттерн для поиска: ")
    
    conn = create_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM search_contacts(%s);", (pattern,))
        contacts = cur.fetchall()
        
        if contacts:
            print("Найденные контакты:")
            for contact in contacts:
                print(f"{contact[0]} {contact[1]} | {contact[2]} | {contact[3]}")
        else:
            print("Контакты не найдены")
        cur.close()
        conn.close()

def delete_contact():
    """Удаление контакта по имени или номеру телефона"""
    search_term = input("Введите имя, фамилию или номер телефона для удаления: ")
    
    conn = create_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("CALL delete_contact(%s);", (search_term,))
        conn.commit()
        print("Контакт успешно удален")
        cur.close()
        conn.close()

def main():
    # Создаем таблицы и функции
    create_tables()
    
    while True:
        print("\nТелефонная книга:")
        print("1. Добавить контакт вручную")
        print("2. Поиск контактов")
        print("3. Удалить контакт")
        print("0. Выход")
        
        try:
            choice = int(input("Выберите действие: "))
            
            if choice == 1:
                insert_contact_from_console()
            elif choice == 2:
                query_contacts()
            elif choice == 3:
                delete_contact()
            elif choice == 0:
                print("Программа завершена")
                break
            else:
                print("Неверный выбор")
        except ValueError:
            print("Пожалуйста, введите число")

if __name__ == "__main__":
    main()
