import psycopg2
from db import get_connection
from queries import ADD_STUDENT, GET_ALL_STUDENTS, GET_STUDENT_BY_ID, UPDATE_STUDENT, DELETE_STUDENT
from helpers import get_non_empty_input, get_int_input

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

def edit_student():
    """Редактирует данные существующего студента."""
    print("\n--- Изменение студента ---")
    student_id = get_int_input("Введите ID студента для изменения: ", min_val=1)

    conn = get_connection()
    if not conn: return

    try:
        with conn.cursor() as cur:
            cur.execute(GET_STUDENT_BY_ID, (student_id,))
            student = cur.fetchone()
            if not student:
                print(f"❌ Студент с ID {student_id} не найден.")
                return

            print(f"Текущие данные: Имя='{student[1]}', Группа='{student[2]}', Активен={student[4]}")

            new_name = input(f"Введите новое имя (текущее: '{student[1]}'): ").strip()
            new_group = input(f"Введите новую группу (текущая: '{student[2]}'): ").strip()
            is_active_input = input(f"Студент активен? (y/n, текущее: {'y' if student[4] else 'n'}): ").strip().lower()
            new_is_active = is_active_input == 'y'

            final_name = new_name if new_name else student[1]
            final_group = new_group if new_group else student[2]
            
            cur.execute(UPDATE_STUDENT, (final_name, final_group, new_is_active, student_id))
            conn.commit()
            print(f"✅ Данные студента с ID {student_id} обновлены.")

    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Ошибка при обновлении студента: {e}")
    finally:
        conn.close()

def delete_student():
    """Удаляет студента из БД (каскадно удаляет все его сдачи)."""
    print("\n--- Удаление студента ---")
    student_id = get_int_input("Введите ID студента для удаления: ", min_val=1)
    
    conn = get_connection()
    if not conn: return
    try:
        with conn.cursor() as cur:
            cur.execute(GET_STUDENT_BY_ID, (student_id,))
            if not cur.fetchone():
                print(f"❌ Студент с ID {student_id} не найден.")
                return
            
            confirm = input(f"Вы уверены, что хотите удалить студента с ID {student_id}? (y/n): ").lower()
            if confirm != 'y':
                print("Удаление отменено.")
                return

            cur.execute(DELETE_STUDENT, (student_id,))
            conn.commit()
            print(f"✅ Студент с ID {student_id} и все его сдачи удалены.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Ошибка при удалении студента: {e}")
    finally:
        conn.close()