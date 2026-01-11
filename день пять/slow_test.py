import asyncio
from types import coroutine as types_coroutine
import inspect

# ============================================
# ОБЪЯСНЕНИЕ: Как работает generator-based корутина
# ============================================
# В старом Python (до 3.5) использовали @asyncio.coroutine + yield from
# В Python 3.8+ asyncio.coroutine удален, но можно использовать types.coroutine
# 
# ПРОБЛЕМА: types.coroutine создает генератор, а не корутину для asyncio!
# create_task() проверяет iscoroutine() и отклоняет генераторы
# 
# РЕШЕНИЕ: Используем ensure_future() вместо create_task()
# ensure_future() умеет работать с генераторами через обертку

# Создаем generator-based корутину (старый стиль)
@types_coroutine
def inner():
    print("inner: началась")
    # yield from работает с Future или другой корутиной
    # asyncio.sleep() возвращает корутину, yield from ее "разворачивает"
    yield from asyncio.sleep(1)
    print("inner: завершилась")
    return 42

@types_coroutine  
def outer():
    print("outer: началась")
    # yield from другой корутины (тоже @coroutine!)
    result = yield from inner()  # НЕТ АВТОМАТИЧЕСКОГО TASK!
    print(f"outer: получила {result}")
    return result

# Запускаем
loop = asyncio.get_event_loop()

# ДИАГНОСТИКА: Проверяем, что у нас получилось
inner_obj = inner()
outer_obj = outer()
print(f"inner() тип: {type(inner_obj)}")
print(f"inner() это генератор? {inspect.isgenerator(inner_obj)}")
print(f"inner() это корутина? {asyncio.iscoroutine(inner_obj)}")
print(f"outer() тип: {type(outer_obj)}")
print(f"outer() это генератор? {inspect.isgenerator(outer_obj)}")
print(f"outer() это корутина? {asyncio.iscoroutine(outer_obj)}")
print()

# ВАЖНО: create_task() НЕ РАБОТАЕТ с generator-based корутинами!
# Он проверяет iscoroutine() и выбрасывает TypeError
# 
# РЕШЕНИЕ: Используем ensure_future() - он умеет оборачивать генераторы
# ensure_future() создает Task для корутин или оборачивает генератор
task = asyncio.ensure_future(outer())  # ← Работает с генераторами!

print(f"task создан: {type(task)}")
print()

result = loop.run_until_complete(task)
print(f"Итог: {result}")