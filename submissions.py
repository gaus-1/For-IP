import psycopg2
from db import get_connection
from queries import (
    GET_STUDENT_BY_ID, GET_TASK_BY_ID, ADD_OR_UPDATE_SUBMISSION, GET_ALL_SUBMISSIONS,
    REPORT_AVG_SCORE, REPORT_TOP_STUDENTS, REPORT_NO_SUBMISSIONS
)
from helpers import get_int_input

def add_submission():
    """Добавляет или обновляет сдачу студента по заданию."""
    print("\n--- Добавление сдачи ---")
    
    student_id = get_int_input("Введите ID студента: ", min_val=1)
    task_id = get_int_input("Введите ID задания: ", min_val=1)
    
    conn = get_connection()
    if not conn: return

    try:
        with conn.cursor() as cur:
            cur.execute(GET_STUDENT_BY_ID, (student_id,))
            student = cur.fetchone()
            if not student or not student[4]:
                print(f"❌ Ошибка: Студент с ID {student_id} не найден или неактивен.")
                return

            cur.execute(GET_TASK_BY_ID, (task_id,))
            task = cur.fetchone()
            if not task or task[4]:
                print(f"❌ Ошибка: Задание с ID {task_id} не найдено или в архиве.")
                return
            
            max_score = task[2]
            print(f"Максимальный балл за задание: {max_score}")
            score = get_int_input(f"Введите балл студента (0-{max_score}): ", min_val=0, max_val=max_score)
            comment = input("Введите комментарий (необязательно): ").strip()

            cur.execute(ADD_OR_UPDATE_SUBMISSION, (student_id, task_id, score, comment))
            conn.commit()
            print(f"✅ Сдача для студента '{student[1]}' по заданию '{task[1]}' успешно записана!")

    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Ошибка базы данных при добавлении сдачи: {e}")
    finally:
        conn.close()

def list_submissions():
    """Выводит список всех сдач с JOIN."""
    print("\n--- Список всех сдач ---")
    conn = get_connection()
    if not conn: return
    try:
        with conn.cursor() as cur:
            cur.execute(GET_ALL_SUBMISSIONS)
            submissions = cur.fetchall()
            if not submissions:
                print("Сдач пока нет.")
                return
            
            print(f"{'ID сдачи':<10}{'Студент':<20}{'Группа':<15}{'Задание':<25}{'Балл':<7}{'Дата сдачи'}")
            print("-" * 100)
            for row in submissions:
                print(f"{row[0]:<10}{row[1]:<20}{row[2]:<15}{row[3]:<25}{row[4]:<7}{row[5]}")
                if row[6]:
                    print(f"{' ':>15}Комментарий: {row[6]}")

    except psycopg2.Error as e:
        print(f"❌ Ошибка при получении списка сдач: {e}")
    finally:
        conn.close()

def show_average_score_report():
    """Отчет: средний балл по студентам."""
    print("\n--- Отчет: средний балл по студентам ---")
    conn = get_connection()
    if not conn: return
    try:
        with conn.cursor() as cur:
            cur.execute(REPORT_AVG_SCORE)
            results = cur.fetchall()
            if not results:
                print("Нет данных для отчета.")
                return
            print(f"{'ID':<5}{'Студент':<25}{'Группа':<15}{'Средний балл':<15}{'Кол-во сдач'}")
            print("-" * 75)
            for row in results:
                print(f"{row[0]:<5}{row[1]:<25}{row[2]:<15}{row[3]:<15.2f}{row[4]}")
    except psycopg2.Error as e:
        print(f"❌ Ошибка при生成 отчета: {e}")
    finally:
        conn.close()

def show_top_students_report():
    """Отчет: топ-5 студентов по сумме баллов."""
    print("\n--- Отчет: топ-5 студентов по сумме баллов ---")
    conn = get_connection()
    if not conn: return
    try:
        with conn.cursor() as cur:
            cur.execute(REPORT_TOP_STUDENTS)
            results = cur.fetchall()
            if not results:
                print("Нет данных для отчета.")
                return
            print(f"{'ID':<5}{'Студент':<25}{'Группа':<15}{'Сумма баллов':<15}{'Кол-во сдач'}")
            print("-" * 75)
            for row in results:
                print(f"{row[0]:<5}{row[1]:<25}{row[2]:<15}{row[3]:<15}{row[4]}")
    except psycopg2.Error as e:
        print(f"❌ Ошибка при生成 отчета: {e}")
    finally:
        conn.close()

def show_no_submissions_report():
    """Отчет: студенты без сдач."""
    print("\n--- Отчет: студенты без сдач ---")
    conn = get_connection()
    if not conn: return
    try:
        with conn.cursor() as cur:
            cur.execute(REPORT_NO_SUBMISSIONS)
            results = cur.fetchall()
            if not results:
                print("Все студенты сдали хотя бы одно задание.")
                return
            print(f"{'ID':<5}{'Студент':<25}{'Группа':<15}")
            print("-" * 45)
            for row in results:
                print(f"{row[0]:<5}{row[1]:<25}{row[2]:<15}")
    except psycopg2.Error as e:
        print(f"❌ Ошибка при生成 отчета: {e}")
    finally:
        conn.close()

def show_reports():
    """Меню для выбора отчета."""
    print("\n--- Отчеты ---")
    print("1. Средний балл по студентам")
    print("2. Топ-5 студентов по сумме баллов")
    print("3. Студенты без сдач")
    choice = input("Выберите отчет: ")
    if choice == '1':
        show_average_score_report()
    elif choice == '2':
        show_top_students_report()
    elif choice == '3':
        show_no_submissions_report()
    else:
        print("Неверный выбор.")