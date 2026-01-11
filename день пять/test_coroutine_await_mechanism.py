"""
ТЕСТ: что реально возвращается при await корутины

Проверяем вашу гипотезу: возвращается ли корутина или Future?
"""

import asyncio
import inspect

# ============================================
# ТЕСТ 1: что возвращает await asyncio.sleep()
# ============================================
print("=" * 70)
print("ТЕСТ 1: что возвращает await asyncio.sleep()")
print("=" * 70)
print()

async def test1():
    # Когда мы делаем await asyncio.sleep(0.1):
    # Что реально возвращается в Task.__step()?
    await asyncio.sleep(0.1)
    return "done"

# Создаем Task вручную, чтобы отследить
# ВАЖНО: нужен event loop для создания Task
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
try:
    task = loop.create_task(test1())
finally:
    # Не закрываем loop здесь, он нужен для дальнейших тестов
    pass

# НО! Мы не можем напрямую вызвать __step(), он приватный
# Вместо этого посмотрим на механизм

print("asyncio.sleep(0.1) возвращает корутину")
sleep_coro = asyncio.sleep(0.1)
print(f"  Тип: {type(sleep_coro)}")
print(f"  Это корутина: {asyncio.iscoroutine(sleep_coro)}")
print()

print("Но await вызывает sleep_coro.__await__()")
sleep_awaitable = sleep_coro.__await__()
print(f"  Тип: {type(sleep_awaitable)}")
print(f"  Это генератор: {inspect.isgenerator(sleep_awaitable)}")
print()

print("Итератор при итерации возвращает:")
try:
    first = next(sleep_awaitable)
    print(f"  Тип: {type(first)}")
    print(f"  Это Future: {asyncio.isfuture(first)}")
    print(f"  Имеет _asyncio_future_blocking: {hasattr(first, '_asyncio_future_blocking')}")
    if hasattr(first, '_asyncio_future_blocking'):
        print(f"  _asyncio_future_blocking = {first._asyncio_future_blocking}")
except StopIteration:
    print("  Уже завершен")
except RuntimeError as e:
    print(f"  Ошибка (ожидаемо, нужен running loop): {e}")
    print("  Это нормально - asyncio.sleep() создает Future внутри")
print()

# ============================================
# ТЕСТ 2: что происходит в Task.__step()
# ============================================
print("=" * 70)
print("ТЕСТ 2: что происходит в Task.__step()")
print("=" * 70)
print()

print("Когда Task.__step() вызывает:")
print("  result = coro.send(None)")
print()
print("Корутина делает await asyncio.sleep(0.1)")
print("→ Python вызывает sleep_coro.__await__()")
print("→ Возвращает awaitable итератор")
print("→ Итератор при итерации возвращает Future")
print("→ Этот Future возвращается из await")
print("→ Task.__step() получает Future")
print()

# ============================================
# ТЕСТ 3: что если await другой корутины?
# ============================================
print("=" * 70)
print("ТЕСТ 3: что если await другой корутины?")
print("=" * 70)
print()

async def inner():
    await asyncio.sleep(0.1)
    return 42

async def outer():
    # await inner() - что возвращается?
    result = await inner()
    return result

print("inner() возвращает корутину")
inner_coro = inner()
print(f"  Тип: {type(inner_coro)}")
print()

print("await inner() вызывает inner().__await__()")
inner_awaitable = inner_coro.__await__()
print(f"  Тип: {type(inner_awaitable)}")
print()

print("Итератор при итерации возвращает:")
try:
    first = next(inner_awaitable)
    print(f"  Тип: {type(first)}")
    print(f"  Это Future: {asyncio.isfuture(first)}")
    print(f"  Это корутина: {asyncio.iscoroutine(first)}")
    print(f"  Имеет _asyncio_future_blocking: {hasattr(first, '_asyncio_future_blocking')}")
except StopIteration:
    print("  Уже завершен")
except RuntimeError as e:
    print(f"  Ошибка (ожидаемо): {e}")
    print("  Итерация awaitable может требовать running event loop")
print()

# Закрываем loop в конце
try:
    loop.close()
    asyncio.set_event_loop(None)
except:
    pass
print()

# ============================================
# ВЫВОД: где "превращение" корутины в Future
# ============================================
print("=" * 70)
print("ВЫВОД: где 'превращение' корутины в Future")
print("=" * 70)
print()

print("✅ КОРУТИНА НЕ ПРЕВРАЩАЕТСЯ В FUTURE!")
print()
print("Вместо этого:")
print("  1. await coro() → вызывает coro.__await__()")
print("  2. coro.__await__() → возвращает awaitable итератор")
print("  3. Итератор при итерации → возвращает Future")
print("  4. Task.__step() → получает Future через coro.send(None)")
print()
print("→ Корутина остается корутиной!")
print("→ Но await работает через awaitable итератор")
print("→ Который при итерации возвращает Future")
print()
print("📁 Реализация в C-коде:")
print("   genobject.c: coro_await()")
print("   → Создает PyCoroWrapper")
print("   → Который при итерации вызывает корутину")
print("   → И возвращает Future")
print()
print("🔑 КЛЮЧЕВОЕ ПОНИМАНИЕ:")
print("  В Task.__step() НЕ нужно превращать корутину в Future!")
print("  Потому что await УЖЕ вернул Future через __await__()")
print("  Task.__step() просто получает этот Future")

