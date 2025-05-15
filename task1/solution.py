import inspect
from functools import wraps  # Для сохранения метаданных оборачиваемой функции


def strict(func):
    sig = inspect.signature(func)
    func_annotations = func.__annotations__

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            bound_arguments = sig.bind(*args, **kwargs)
        except TypeError as e:
            raise TypeError(f"Ошибка вызова функции: {e}") from e

        for name, value in bound_arguments.arguments.items():
            if name in func_annotations:
                expected_type = func_annotations[name]
                actual_type = type(value)

                if actual_type is not expected_type:
                    raise TypeError(
                        f"Аргумент '{name}' имеет некорректный тип: "
                        f"ожидался {expected_type.__name__}, получен {actual_type.__name__}"
                    )
        return func(*args, **kwargs)

    return wrapper