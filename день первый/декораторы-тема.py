"""
Домашнее задание: Декораторы в Python

Декораторы - это мощный инструмент Python, позволяющий модифицировать поведение функций
без изменения их исходного кода. В этом файле представлены примеры и задания по декораторам.
"""


# Пример 1: Простой декоратор
def simple_decorator(func):
    """
    Простой декоратор, который выводит сообщение до и после вызова функции.
    """
    def wrapper(*args, **kwargs):
        print(f"Функция {func.__name__} была вызвана")
        result = func(*args, **kwargs)
        print(f"Функция {func.__name__} завершила выполнение")
        return result
    return wrapper


@simple_decorator
def greet(name):
    """Пример функции с декоратором"""
    print(f"Привет, {name}!")
    return f"Приветствие для {name}"


# Пример 2: Декоратор с параметрами
def repeat(times):
    """
    Декоратор с параметрами, который повторяет выполнение функции указанное количество раз.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                result = func(*args, **kwargs)
                results.append(result)
            return results
        return wrapper
    return decorator


@repeat(times=3)
def say_hello():
    """Функция, которая будет вызвана 3 раза"""
    print("Привет!")
    return "hello"


# Пример 3: Декоратор для измерения времени выполнения
import time
from functools import wraps


def measure_time(func):
    """
    Декоратор для измерения времени выполнения функции.
    """
    @wraps(func)  # Сохраняет метаданные оригинальной функции
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Функция {func.__name__} выполнена за {execution_time:.4f} секунд")
        return result
    return wrapper


@measure_time
def slow_function():
    """Пример функции с измерением времени выполнения"""
    time.sleep(1)
    return "Готово!"


# ============================================================================
# ТЕСТИРОВАНИЕ ПРИМЕРОВ:
# ============================================================================

if __name__ == "__main__":
    print("=" * 50)
    print("Тестирование примеров декораторов")
    print("=" * 50)
    
    # Тест простого декоратора
    print("\n1. Тест simple_decorator:")
    greet("Иван")
    
    # Тест декоратора с параметрами
    print("\n2. Тест repeat decorator:")
    results = say_hello()
    
    # Тест декоратора измерения времени
    print("\n3. Тест measure_time decorator:")
    slow_function()

