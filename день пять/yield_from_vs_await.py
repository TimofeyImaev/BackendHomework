"""
ОБЪЯСНЕНИЕ: Разница между yield from и await

Короткий ответ: НЕТ, это не только тип возвращаемого значения!

Основные различия:
1. yield from - для генераторов и generator-based корутин
2. await - для нативных корутин (async def)
3. Разный механизм работы под капотом
4. Разная интеграция с event loop
"""

import asyncio
import inspect
from types import coroutine as types_coroutine

# ============================================
# 1. yield from - работает с генераторами
# ============================================
def simple_generator():
    """Обычный генератор"""
    yield 1
    yield 2
    return "done"

def generator_with_yield_from():
    """Генератор, использующий yield from"""
    result = yield from simple_generator()
    return result

print("=== 1. yield from с генераторами ===")
gen = generator_with_yield_from()
print(f"Тип: {type(gen)}")
print(f"Это генератор: {inspect.isgenerator(gen)}")
print(f"Это корутина: {asyncio.iscoroutine(gen)}")

# Вручную управляем генератором
try:
    print(f"send(None): {gen.send(None)}")  # 1
    print(f"send(None): {gen.send(None)}")  # 2
    gen.send(None)  # StopIteration с "done"
except StopIteration as e:
    print(f"Результат: {e.value}")
print()

# ============================================
# 2. yield from - работает с generator-based корутинами
# ============================================
@types_coroutine
def generator_based_coro():
    """Generator-based корутина (старый стиль)"""
    yield from asyncio.sleep(0.1)
    return 42

@types_coroutine
def outer_with_yield_from():
    """Использует yield from для generator-based корутины"""
    result = yield from generator_based_coro()
    return result

print("=== 2. yield from с generator-based корутинами ===")
gen_coro = outer_with_yield_from()
print(f"Тип: {type(gen_coro)}")
print(f"Это генератор: {inspect.isgenerator(gen_coro)}")
print(f"Это корутина: {asyncio.iscoroutine(gen_coro)}")
print()

# ============================================
# 3. await - работает только с нативными корутинами
# ============================================
async def native_coro():
    """Нативная корутина (современный стиль)"""
    await asyncio.sleep(0.1)
    return 42

async def outer_with_await():
    """Использует await для нативной корутины"""
    result = await native_coro()
    return result

print("=== 3. await с нативными корутинами ===")
native_coro_obj = outer_with_await()
print(f"Тип: {type(native_coro_obj)}")
print(f"Это генератор: {inspect.isgenerator(native_coro_obj)}")
print(f"Это корутина: {asyncio.iscoroutine(native_coro_obj)}")
print()

# ============================================
# 4. КЛЮЧЕВОЕ РАЗЛИЧИЕ: Механизм работы
# ============================================
print("=== 4. Как они работают под капотом ===")

# yield from использует:
# - gen.send(value) для передачи значений
# - StopIteration для возврата результата
# - Работает синхронно в текущем контексте

# await использует:
# - coro.__await__() для получения awaitable итератора
# - Работает через event loop
# - Может приостановить выполнение и вернуть управление в event loop

def demonstrate_yield_from_mechanism():
    """Показываем, как работает yield from"""
    def inner():
        val = yield 1
        return val + 10
    
    def outer():
        # yield from автоматически:
        # 1. Передает значения из inner наружу
        # 2. Передает значения извне в inner
        result = yield from inner()
        return result
    
    gen = outer()
    # Первый send запускает до первого yield
    print(f"yield from: первый send -> {gen.send(None)}")  # 1
    # Второй send передает значение в inner и получает результат
    try:
        result = gen.send(5)  # Передаем 5 в inner, получаем результат
    except StopIteration as e:
        print(f"yield from: результат -> {e.value}")  # 15

demonstrate_yield_from_mechanism()
print()

# ============================================
# 5. НЕСОВМЕСТИМОСТЬ: нельзя смешивать
# ============================================
print("=== 5. Несовместимость ===")

# ❌ НЕ РАБОТАЕТ:
# async def bad():
#     result = yield from native_coro()  # SyntaxError!

# ❌ НЕ РАБОТАЕТ:
# @types_coroutine
# def bad2():
#     result = await native_coro()  # SyntaxError!

print("yield from можно использовать только в генераторах")
print("await можно использовать только в async def функциях")
print()

# ============================================
# 6. Интеграция с event loop
# ============================================
print("=== 6. Интеграция с event loop ===")

async def demonstrate_await_with_loop():
    """await интегрирован с event loop"""
    print("await автоматически:")
    print("1. Приостанавливает текущую корутину")
    print("2. Возвращает управление в event loop")
    print("3. Event loop может выполнить другие задачи")
    print("4. Когда awaitable готов, корутина продолжается")
    
    # await создает "точку приостановки"
    await asyncio.sleep(0.1)
    print("Корутина продолжена после await")

print("yield from работает синхронно - не возвращает управление в loop")
print("await работает асинхронно - возвращает управление в loop")
print()

# ============================================
# ВЫВОД
# ============================================
print("=== ВЫВОД ===")
print("yield from и await НЕ отличаются только типом!")
print()
print("yield from:")
print("  - Для генераторов и generator-based корутин")
print("  - Работает синхронно (не возвращает управление в loop)")
print("  - Использует gen.send() и StopIteration")
print("  - Может передавать значения туда-обратно")
print()
print("await:")
print("  - Для нативных корутин (async def)")
print("  - Работает асинхронно (возвращает управление в loop)")
print("  - Использует coro.__await__() и event loop")
print("  - Интегрирован с планировщиком задач")
print()
print("Они работают на разных уровнях абстракции!")




























