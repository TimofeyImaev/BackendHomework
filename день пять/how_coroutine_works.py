"""
ОБЪЯСНЕНИЕ: Как работает generator-based корутина внутри asyncio

1. @types.coroutine создает генератор с флагом CO_ITERABLE_COROUTINE
2. yield from "разворачивает" другую корутину или Future
3. Task.__step() вручную управляет генератором через .send() и .throw()
4. Когда генератор возвращает значение, оно становится результатом Task
"""

import asyncio
from types import coroutine as types_coroutine
import inspect

# ============================================
# ШАГ 1: Создание generator-based корутины
# ============================================
@types_coroutine
def simple_coro():
    print("  → simple_coro: началась")
    # yield from приостанавливает выполнение и ждет результат
    result = yield from asyncio.sleep(0.1)
    print(f"  → simple_coro: получила {result}")
    return "done"

# Когда мы вызываем функцию, получаем ГЕНЕРАТОР
gen = simple_coro()
print(f"Тип simple_coro(): {type(gen)}")
print(f"Это генератор? {inspect.isgenerator(gen)}")
print(f"Это корутина для asyncio? {asyncio.iscoroutine(gen)}")
print()

# ============================================
# ШАГ 2: Как Task управляет генератором
# ============================================
print("=== Как Task управляет генератором ===")

# Вручную показываем, как Task.__step() работает:
def manual_step_demo():
    gen = simple_coro()
    print("1. Запускаем генератор: gen.send(None)")
    try:
        # Первый вызов - запускает генератор до первого yield
        result = gen.send(None)
        print(f"   Получили: {result} (это Future от asyncio.sleep)")
        
        # В реальности Task ждет, пока Future завершится,
        # затем вызывает gen.send(future.result())
        # Для демонстрации просто показываем структуру:
        print("2. Task ждет завершения Future...")
        print("3. Когда Future готов, Task вызывает: gen.send(future.result())")
        
    except StopIteration as e:
        print(f"   Генератор завершился с результатом: {e.value}")

manual_step_demo()
print()

# ============================================
# ШАГ 3: Реальный пример с asyncio
# ============================================
print("=== Реальный пример с asyncio ===")

@types_coroutine
def inner():
    print("inner: началась")
    yield from asyncio.sleep(0.1)
    print("inner: завершилась")
    return 42

@types_coroutine
def outer():
    print("outer: началась")
    # yield from автоматически "разворачивает" inner()
    # Task будет управлять обеими корутинами
    result = yield from inner()
    print(f"outer: получила {result}")
    return result

# ensure_future() умеет работать с generator-based корутинами
# Он создает обертку, которая превращает генератор в корутину
task = asyncio.ensure_future(outer())

# Запускаем event loop
result = asyncio.get_event_loop().run_until_complete(task)
print(f"Итоговый результат: {result}")

