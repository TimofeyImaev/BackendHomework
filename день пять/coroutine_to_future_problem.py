"""
ПРОБЛЕМА: что происходит когда await возвращает корутину?

Вы правы! Когда мы делаем:
  await asyncio.sleep(1)

asyncio.sleep(1) возвращает КОРУТИНУ, а не Future!
Но в Task.__step() проверяется только _asyncio_future_blocking.

Где же корутина превращается в Future?
"""

import asyncio
import inspect

# ============================================
# ПРОБЛЕМА: await возвращает корутину
# ============================================
print("=" * 70)
print("ПРОБЛЕМА: await возвращает корутину")
print("=" * 70)
print()

async def inner():
    await asyncio.sleep(0.1)
    return 42

async def outer():
    # Когда мы делаем await inner():
    # inner() возвращает КОРУТИНУ, а не Future!
    result = await inner()
    return result

# Проверяем
inner_coro = inner()
print(f"inner() тип: {type(inner_coro)}")
print(f"Это корутина: {asyncio.iscoroutine(inner_coro)}")
print(f"Это Future: {asyncio.isfuture(inner_coro)}")
print()

# ============================================
# РЕШЕНИЕ: корутина имеет __await__()
# ============================================
print("=" * 70)
print("РЕШЕНИЕ: корутина имеет __await__()")
print("=" * 70)
print()

print("Когда Python видит: await inner()")
print("Он НЕ вызывает inner() напрямую!")
print("Он вызывает: inner().__await__()")
print()

# Проверяем __await__()
awaitable = inner_coro.__await__()
print(f"inner().__await__() тип: {type(awaitable)}")
print(f"Это генератор: {inspect.isgenerator(awaitable)}")
print()

# ============================================
# КАК ЭТО РАБОТАЕТ: корутина.__await__()
# ============================================
print("=" * 70)
print("КАК ЭТО РАБОТАЕТ: корутина.__await__()")
print("=" * 70)
print()

print("1. Python компилятор:")
print("   'await inner()' → байт-код GET_AWAITABLE")
print()
print("2. Интерпретатор (ceval.c):")
print("   GET_AWAITABLE → _PyEval_GetAwaitable()")
print("   → Вызывает inner().__await__()")
print()
print("3. Корутина.__await__() (C-код):")
print("   → Возвращает awaitable итератор")
print("   → Это НЕ сама корутина!")
print()
print("4. Task.__step() вызывает:")
print("   result = coro.send(None)")
print("   → Получает результат из awaitable итератора")
print("   → Это может быть Future или другая корутина")
print()

# ============================================
# ПРОВЕРКА: что возвращает корутина при await
# ============================================
print("=" * 70)
print("ПРОВЕРКА: что возвращает корутина при await")
print("=" * 70)
print()

async def test_coro():
    # Когда мы делаем await asyncio.sleep(1):
    # asyncio.sleep(1) возвращает корутину
    # Но await вызывает sleep_coro.__await__()
    # Который возвращает Future!
    await asyncio.sleep(0.1)
    return "done"

# Создаем корутину
test = test_coro()

# Получаем awaitable итератор
awaitable_iter = test.__await__()

print("test_coro() тип:", type(test))
print("test_coro().__await__() тип:", type(awaitable_iter))
print()

# Пробуем получить первый элемент
# ВАЖНО: итерация awaitable может требовать event loop
try:
    first = awaitable_iter.__next__()
    print(f"Первый элемент awaitable: {type(first)}")
    print(f"Это Future: {asyncio.isfuture(first)}")
    print(f"Это корутина: {asyncio.iscoroutine(first)}")
    print(f"Имеет _asyncio_future_blocking: {hasattr(first, '_asyncio_future_blocking')}")
except StopIteration:
    print("awaitable уже завершен")
except RuntimeError as e:
    print(f"Ошибка (ожидаемо): {e}")
    print("Итерация awaitable может требовать running event loop")
print()

# ============================================
# КЛЮЧ: asyncio.sleep() возвращает корутину
# ============================================
print("=" * 70)
print("КЛЮЧ: asyncio.sleep() возвращает корутину")
print("=" * 70)
print()

# ВАЖНО: asyncio.sleep() требует event loop для создания Future
# Поэтому создаем loop для демонстрации
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

try:
    sleep_coro = asyncio.sleep(0.1)
    print(f"asyncio.sleep(0.1) тип: {type(sleep_coro)}")
    print(f"Это корутина: {asyncio.iscoroutine(sleep_coro)}")
    print(f"Это Future: {asyncio.isfuture(sleep_coro)}")  # ← Показываем isfuture
    print()

    # Но когда мы делаем await, вызывается __await__()
    sleep_awaitable = sleep_coro.__await__()
    print(f"sleep_coro.__await__() тип: {type(sleep_awaitable)}")
    print()

    # Получаем первый элемент
    try:
        sleep_result = sleep_awaitable.__next__()
        print(f"Первый элемент: {type(sleep_result)}")
        print(f"Это Future: {asyncio.isfuture(sleep_result)}")  # ← ВОТ ГДЕ ПРОВЕРКА!
        print(f"Имеет _asyncio_future_blocking: {hasattr(sleep_result, '_asyncio_future_blocking')}")
        if hasattr(sleep_result, '_asyncio_future_blocking'):
            print(f"_asyncio_future_blocking = {sleep_result._asyncio_future_blocking}")
        
        # Показываем, как Task.__step() проверяет это
        print()
        print("В Task.__step() (tasks.py:334):")
        blocking = getattr(sleep_result, '_asyncio_future_blocking', None)
        print(f"  blocking = getattr(result, '_asyncio_future_blocking', None)")
        print(f"  blocking = {blocking}")
        if blocking is not None:
            print(f"  → Это Future! Обрабатываем через add_done_callback()")
        else:
            print(f"  → Это НЕ Future, будет ошибка")
            
    except StopIteration:
        print("awaitable уже завершен")
    except RuntimeError as e:
        print(f"Ошибка при итерации: {e}")
        print("Это нормально - asyncio.sleep() создает Future внутри, который требует running loop")
        print()
        print("НО! Мы можем показать проверку isfuture на простом Future:")
        print()
        # Показываем на простом Future
        simple_future = loop.create_future()
        print(f"simple_future тип: {type(simple_future)}")
        print(f"Это Future: {asyncio.isfuture(simple_future)}")  # ← Показываем isfuture
        print(f"Имеет _asyncio_future_blocking: {hasattr(simple_future, '_asyncio_future_blocking')}")
        if hasattr(simple_future, '_asyncio_future_blocking'):
            print(f"_asyncio_future_blocking = {simple_future._asyncio_future_blocking}")
        print()
        print("Как работает isfuture() (base_futures.py:13-21):")
        print("  def isfuture(obj):")
        print("      return (hasattr(obj.__class__, '_asyncio_future_blocking') and")
        print("              obj._asyncio_future_blocking is not None)")
        print()
        print(f"  Проверка simple_future:")
        print(f"    hasattr(simple_future.__class__, '_asyncio_future_blocking') = {hasattr(simple_future.__class__, '_asyncio_future_blocking')}")
        print(f"    simple_future._asyncio_future_blocking = {getattr(simple_future, '_asyncio_future_blocking', 'НЕТ')}")
        print()
        print("Сравнение с корутиной:")
        print(f"  sleep_coro это Future: {asyncio.isfuture(sleep_coro)}")
        print(f"  simple_future это Future: {asyncio.isfuture(simple_future)}")
        print()
        print("В Task.__step() (tasks.py:334):")
        blocking = getattr(simple_future, '_asyncio_future_blocking', None)
        print(f"  blocking = getattr(result, '_asyncio_future_blocking', None)")
        print(f"  blocking = {blocking}")
        if blocking is not None:
            print(f"  → Это Future! Обрабатываем через add_done_callback()")
        else:
            print(f"  → Это НЕ Future, будет ошибка")
        print()
        print("→ isfuture() проверяет наличие _asyncio_future_blocking")
        print("→ Task.__step() использует это для определения Future")
finally:
    loop.close()
    asyncio.set_event_loop(None)
print()

# ============================================
# ВЫВОД: где корутина превращается в Future
# ============================================
print("=" * 70)
print("ВЫВОД: где корутина превращается в Future")
print("=" * 70)
print()

print("✅ КОРУТИНА НЕ ПРЕВРАЩАЕТСЯ В FUTURE!")
print()
print("Вместо этого:")
print("  1. await coro() вызывает coro.__await__()")
print("  2. coro.__await__() возвращает awaitable итератор")
print("  3. Итератор при итерации возвращает Future")
print("  4. Task.__step() получает этот Future")
print()
print("→ Корутина остается корутиной!")
print("→ Но await работает через awaitable итератор")
print("→ Который возвращает Future при итерации")
print()

print("📁 Код корутины.__await__() находится в C-коде:")
print("   genobject.c: coro_await()")
print("   → Создает PyCoroWrapper")
print("   → Который при итерации вызывает корутину")
print("   → И возвращает Future")
print()

print("🔑 КЛЮЧЕВОЕ ПОНИМАНИЕ:")
print("  await coro() НЕ возвращает корутину напрямую!")
print("  await coro() вызывает coro.__await__()")
print("  Который возвращает итератор")
print("  Итератор при итерации возвращает Future")
print("  Task.__step() получает этот Future")

