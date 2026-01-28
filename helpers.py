def get_non_empty_input(prompt):
    """Запрашивает у пользователя непустую строку."""
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        print("Ошибка: ввод не может быть пустым. Попробуйте снова.")

def get_int_input(prompt, min_val=None):
    """Запрашивает у пользователя целое число."""
    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                print(f"Ошибка: значение должно быть не меньше {min_val}.")
                continue
            return value
        except ValueError:
            print("Ошибка: введите корректное целое число.")