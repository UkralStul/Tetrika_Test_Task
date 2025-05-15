import unittest
import sys
from task2 import get_result

def run_task_tests(task_module_name, task_description):
    """Запускает тесты для указанного модуля задачи."""
    print(f"--- Запуск тестов для: {task_description} ---")
    loader = unittest.TestLoader()
    try:
        suite = loader.discover(start_dir=task_module_name, pattern='test_*.py')
    except ImportError:
        print(f"Не удалось найти или импортировать тесты из модуля {task_module_name}.")
        print("Убедитесь, что структура проекта верна и есть __init__.py в папке задачи.")
        return False

    if suite.countTestCases() == 0:
        print(f"Тесты не найдены в {task_module_name}.")
        return False

    runner = unittest.TextTestRunner(verbosity=1, stream=sys.stdout)  # verbosity=1 для краткого вывода
    result = runner.run(suite)

    if result.wasSuccessful():
        print(f"Тесты к заданию '{task_description}' прошли успешно!\n")
        return True
    else:
        print(f"Тесты к заданию '{task_description}' НЕ ПРОШЛИ.\n")
        print("--- Детали ошибок/провалов: ---")
        for failure in result.failures:
            print(f"Провал: {failure[0]}")
            print(failure[1])
        for error in result.errors:
            print(f"Ошибка: {error[0]}")
            print(error[1])
        print("-------------------------------\n")
        return False


if __name__ == "__main__":
    # Получаем результат отдельно для второго задания
    # get_result()

    tasks_to_test = [
        ("task1", "Задача 1 (Декоратор @strict)"),
        ("task3", "Задача 3 (Интервалы)"),
    ]

    all_tasks_passed = True
    final_results = []

    for task_module, task_desc in tasks_to_test:
        passed = run_task_tests(task_module, task_desc)
        if not passed:
            all_tasks_passed = False
        final_results.append(f"{task_desc}: {'УСПЕШНО' if passed else 'ПРОВАЛ'}")

    print("\n--- Общий итог тестирования ---")
    for res_line in final_results:
        print(res_line)

    if all_tasks_passed:
        print("\nВсе тесты для всех выбранных заданий прошли успешно!")
        sys.exit(0)
    else:
        print("\nНекоторые тесты не пройдены.")
        sys.exit(1)