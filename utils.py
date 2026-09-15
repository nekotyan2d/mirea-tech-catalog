def input_int(prompt: str) -> int:
    while True:
        raw_value = input(prompt)
        try:
            return int(raw_value)
        except ValueError:
            print("Некорректный ввод, введите целое число.")


def input_float(prompt: str) -> float:
    while True:
        raw_value = input(prompt)
        try:
            return float(raw_value)
        except ValueError:
            print("Некорректный ввод, введите число.")
