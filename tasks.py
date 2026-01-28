import psycopg2
from db import get_connection
from queries import ADD_TASK, GET_ALL_TASKS, GET_TASK_BY_ID, UPDATE_TASK, DELETE_TASK
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
    print("\n--- Список заданий ---")
    conn = get_connection()
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

def edit_task():
    """Редактирует данные существующего задания."""
    print("\n--- Изменение задания ---")
    task_id = get_int_input("Введите ID задания для изменения: ", min_val=1)

    conn = get_connection()
    if not conn: return

    try:
        with conn.cursor() as cur:
            cur.execute(GET_TASK_BY_ID, (task_id,))
            task = cur.fetchone()
            if not task:
                print(f"❌ Задание с ID {task_id} не найдено.")
                return

            print(f"Текущие данные: Название='{task[1]}', Макс. балл={task[2]}, В архиве={task[4]}")
            
            new_title = input(f"Введите новое название (текущее: '{task[1]}'): ").strip()
            new_max_score_str = input(f"Введите новый макс. балл (текущий: '{task[2]}'): ").strip()
            is_active_input = input(f"Задание в архиве? (y/n, текущее: {'y' if task[4] else 'n'}): ").strip().lower()
            
            final_title = new_title if new_title else task[1]
            final_is_archived = is_active_input == 'y'
            
            if new_max_score_str:
                try:
                    new_max_score = int(new_max_score_str)
                    if new_max_score < 0:
                        print("❌ Макс. балл не может быть отрицательным.")
                        return
                    if new_max_score < task[2]:
                        print("❌ Ошибка: Нельзя понизить максимальный балл, так как существуют сдачи с более высоким баллом.")
                        return
                    final_max_score = new_max_score
                except ValueError:
                    print("❌ Некорректный ввод для макс. балла.")
                    return
            else:
                final_max_score = task[2]

            cur.execute(UPDATE_TASK, (final_title, final_max_score, final_is_archived, task_id))
            conn.commit()
            print(f"✅ Данные задания с ID {task_id} обновлены.")

    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Ошибка при обновлении задания: {e}")
    finally:
        conn.close()

def delete_task():
    """Удаляет задание из БД (каскадно удаляет все связанные сдачи)."""
    print("\n--- Удаление задания ---")
    task_id = get_int_input("Введите ID задания для удаления: ", min_val=1)
    
    conn = get_connection()
    if not conn: return
    try:
        with conn.cursor() as cur:
            cur.execute(GET_TASK_BY_ID, (task_id,))
            if not cur.fetchone():
                print(f"❌ Задание с ID {task_id} не найдено.")
                return
            
            confirm = input(f"Вы уверены, что хотите удалить задание с ID {task_id}? (y/n): ").lower()
            if confirm != 'y':
                print("Удаление отменено.")
                return

            cur.execute(DELETE_TASK, (task_id,))
            conn.commit()
            print(f"✅ Задание с ID {task_id} и все связанные сдачи удалены.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Ошибка при удалении задания: {e}")
    finally:
        conn.close()