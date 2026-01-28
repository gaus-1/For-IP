import psycopg2
from db import get_connection
from queries import ADD_STUDENT, GET_ALL_STUDENTS
from helpers import get_non_empty_input

def add_student():
    """Добавляет нового студента в БД."""
    print("\n--- Добавление студента ---")
    name = get_non_empty_input("Введите имя студента: ")
    group = get_non_empty_input("Введите название группы: ")
    
    conn = get_connection()
    if not conn: return
    try:
        with conn.cursor() as cur:
            cur.execute(ADD_STUDENT, (name, group))
            student_id = cur.fetchone()[0]
            conn.commit()
            print(f"✅ Студент '{name}' добавлен с ID: {student_id}")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Ошибка при добавлении студента: {e}")
    finally:
        conn.close()

def list_students():
    """Выводит список всех студентов."""
    print("\n--- Список студентов ---")
    conn = get_connection()
    if not conn: return
    try:
        with conn.cursor() as cur:
            cur.execute(GET_ALL_STUDENTS)
            students = cur.fetchall()
            if not students:
                print("Студенты не найдены.")
                return
            print(f"{'ID':<5}{'Имя':<25}{'Группа':<15}{'Активен':<10}{'Дата создания'}")
            print("-" * 70)
            for row in students:
                print(f"{row[0]:<5}{row[1]:<25}{row[2]:<15}{row[3]:<10}{row[4]}")
    except psycopg2.Error as e:
        print(f"❌ Ошибка при получении списка студентов: {e}")
    finally:
        conn.close()