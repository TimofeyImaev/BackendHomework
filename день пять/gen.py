from types import coroutine
import asyncio

def simple_generator():
    print("Шаг 1")
    yield 1
    print("Шаг 2")
    yield 2
    print("Шаг 3")
    return "Готово"

# Использование:
gen = simple_generator()
print(next(gen))  # "Шаг 1", затем 1
print(next(gen))  # "Шаг 2", затем 2
try:
    print(next(gen))  # "Шаг 3", затем StopIteration: Готово
except StopIteration as e:
    print(f"Результат: {e.value}")  # "Результат: Готово"





# Создаем обычный генератор
def my_generator():
    print("Генератор: начали")
    # yield приостанавливает выполнение
    value = yield "первый yield"
    print(f"Генератор: получили {value}")
    return "завершено"

# Делаем из него корутину
coro_func = coroutine(my_generator)

async def main():
    print("Main: начали")
    
    # Получаем корутин-объект
    coro = coro_func()
    
    # Вручную управляем корутиной (так делает Task)
    try:
        # Первый шаг - запускаем до первого yield
        result = coro.send(None)
        print(f"Main: получили {result}")
        
        # Второй шаг - продолжаем с значением
        result = coro.send("второе значение")
    except StopIteration as e:
        print(f"Main: корутина завершилась с результатом: {e.value}")

# Запускаем event loop
asyncio.run(main())




