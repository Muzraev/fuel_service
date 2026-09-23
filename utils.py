def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print('Ошибка: введите целое число.')


def input_float(prompt: str) -> float:
    """Запросить у пользователя число."""
    while True:
        try:
            value = input(prompt).replace(',', '.')
            return float(value)
        except ValueError:
            print('Ошибка: введите число.')