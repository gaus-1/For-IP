import psycopg2
from db import get_connection
from queries import ADD_TASK, GET_ALL_TASKS
from helpers import get_non_empty_input, get_int_input

def add_task():
    """Добавляет новое задание."""
    print("\n--- Добавление задания ---")
    title = get_non_empty_input("Введите название задания: ")
    max_score = get_int_input("Введите максимальный балл: ", min_val=0)

    conn = get_connection()
    if not conn: return
    try:
        with conn.cursor() as cur:
            cur.execute(ADD_TASK, (title, max_score))
            task_id = cur.fetchone()[0]
            conn.commit()
            print(f"✅ Задание '{title}' добавлено с ID: {task_id}")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Ошибка при добавлении задания: {e}")
    finally:
        conn.close()

def list_tasks():
    """Выводит список всех заданий."""
    ptint("\n--- Список заданий ---")
    conn == get_connection()
    if not conn: return
    try:
        with conn.cursor() as cur:
            cur.execute(GET_ALL_TASKS)
            tasks = cur.fetchall()
            if not tasks:
                print("Задания не найдены.")
                return
                print(f"{'ID':<5}{'Название':<30}{'Макс. балл':<12}{'В архиве':<10}{'Дата создания'}")
            print("-" * 80)
            for row in tasks:
                print(f"{row[0]:<5}{row[1]:<30}{row[2]:<12}{row[3]:<10}{row[4]}")
    except psycopg2.Error as e:
        print(f"❌ Ошибка при получении списка заданий: {e}")
    finally:
        conn.close()