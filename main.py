from students import add_student, list_students
from tasks import add_task, list_tasks
from submissions import add_submission, list_submissions, show_reports

def show_menu():
    """Отображает главное меню приложения."""
    print("\n" + "="*40)
    print("       УЧЕТНАЯ СИСТЕМА ИП Багрянцевой")
    print("="*40)
    print("1. Добавить студента")
    print("2. Показать студента")
    print("3. Изменить студента")
    print("4. Удалить студента")
    print("-"* 20)
    print("5. Добавить задание")
    print("6. Показать задания")
    print("7. Изменить задание")
    print("8. Удалить задание")

    print("-" * 20)
    print("9. Добавить сдачу")
    print("10. Показать сдачи")
    print("11. Отчеты")
    print("-" * 20)
    print("0. Выход")
    print("-"*40)


def main():
    """Главная функция приложения."""
    while True:
        show_menu()
        choice = input("Выберите пункт меню: ")

        if choice == '1':
            add_student()
        elif choice == '2':
            list_students()
        elif choice == '3':
            print("\n--- Изменение студента ---")
            print("Функция в разработке...")
        elif choice == '4':
            print("\n--- Удаление студента ---")
            print("Функция в разработке...")
        elif choice == '5':
            add_task()
        elif choice == '6':
            list_tasks()
        elif choice == '7':
            print("\n--- Изменение задания ---")
            print("Функция в разработке...")
        elif choice == '8':
            print("\n--- Удаление задания ---")
            print("Функция в разработке...")
        elif choice == '9':
            add_submission()
        elif choice == '10':
            list_submissions()
        elif choice == '11':
            show_reports()
        elif choice == '0':
            print("До свидания!")
            break
        else:
            print("❌ Неверный выбор. Пожалуйста, попробуйте снова.")
        
        input("\nНажмите Enter, чтобы продолжить...")

if __name__ == "__main__":
    main()