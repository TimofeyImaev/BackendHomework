"""
await с вложенными корутинами - аналогично yield from

Показываем, как await "раскрывает" вложенные корутины
так же, как yield from раскрывает вложенные генераторы.
"""

import asyncio
import time

# ============================================
# ВЛОЖЕННЫЕ КОРУТИНЫ БЕЗ await
# ============================================
print("=" * 70)
print("ВЛОЖЕННЫЕ КОРУТИНЫ БЕЗ await")
print("=" * 70)
print()

async def inner():
    print(f"  [{time.time():.2f}] inner: await sleep(0.1)")
    await asyncio.sleep(0.1)
    print(f"  [{time.time():.2f}] inner: await sleep(0.1)")
    await asyncio.sleep(0.1)
    print(f"  [{time.time():.2f}] inner: return 'inner_done'")
    return "inner_done"

async def middle():
    print(f"[{time.time():.2f}] middle: await inner()")
    result = await inner()  # ← Раскрывает inner
    print(f"[{time.time():.2f}] middle: получил '{result}'")
    print(f"[{time.time():.2f}] middle: await sleep(0.1)")
    await asyncio.sleep(0.1)
    print(f"[{time.time():.2f}] middle: return 'middle_done'")
    return "middle_done"

async def outer():
    print(f"[{time.time():.2f}] outer: await middle()")
    result = await middle()  # ← Раскрывает middle (который уже раскрыл inner)
    print(f"[{time.time():.2f}] outer: получил '{result}'")
    print(f"[{time.time():.2f}] outer: await sleep(0.1)")
    await asyncio.sleep(0.1)
    print(f"[{time.time():.2f}] outer: return 'outer_done'")
    return "outer_done"

print("Запускаем вложенные корутины:")
print()
result = asyncio.run(outer())
print(f"Итоговый результат: {result}")
print()
print("→ Все await'ы выполняются последовательно!")
print("→ Три корутины превратились в один поток")
print("→ await 'раскрыл' вложенность")
print()

# ============================================
# КАК await "РАСКРЫВАЕТ" ВЛОЖЕННОСТЬ
# ============================================
print("=" * 70)
print("КАК await 'РАСКРЫВАЕТ' ВЛОЖЕННОСТЬ")
print("=" * 70)
print()

print("await работает примерно так:")
print()
print("async def outer():")
print("    result = await middle()  # Раскрывается в:")
print()
print("    # Эквивалентно (упрощенно):")
print("    # 1. Вызываем middle()")
print("    # 2. Получаем корутину")
print("    # 3. Выполняем её до завершения")
print("    # 4. Все await'ы из middle выполняются последовательно")
print("    # 5. Все await'ы из inner (вызванного из middle) тоже")
print("    # 6. Получаем результат")
print()
print("→ await 'раскрывает' вложенность")
print("→ Все await'ы выполняются в одном потоке")
print("→ Последовательно, один за другим")
print()

# ============================================
# ДЕМОНСТРАЦИЯ: три уровня вложенности
# ============================================
print("=" * 70)
print("ДЕМОНСТРАЦИЯ: три уровня вложенности")
print("=" * 70)
print()

async def level1():
    """Первый уровень"""
    print("    [level1] await sleep(0.1)")
    await asyncio.sleep(0.1)
    print("    [level1] await sleep(0.1)")
    await asyncio.sleep(0.1)
    print("    [level1] return 'level1_done'")
    return 'level1_done'

async def level2():
    """Второй уровень"""
    print("  [level2] await level1()")
    result = await level1()
    print(f"  [level2] получил: {result}")
    print("  [level2] await sleep(0.1)")
    await asyncio.sleep(0.1)
    print("  [level2] return 'level2_done'")
    return 'level2_done'

async def level3():
    """Третий уровень"""
    print("[level3] await level2()")
    result = await level2()
    print(f"[level3] получил: {result}")
    print("[level3] await sleep(0.1)")
    await asyncio.sleep(0.1)
    print("[level3] return 'level3_done'")
    return 'level3_done'

print("Структура:")
print("  level3()")
print("    await level2()")
print("      await level1()")
print("        await sleep(0.1), sleep(0.1)")
print("      await sleep(0.1)")
print("    await sleep(0.1)")
print()

print("Когда мы делаем await, это превращается в:")
print("  level3() → один поток с await'ами:")
print("    await sleep(0.1)  # из level1")
print("    await sleep(0.1)  # из level1")
print("    await sleep(0.1)  # из level2")
print("    await sleep(0.1)  # из level3")
print()

print("Запускаем:")
start = time.time()
result = asyncio.run(level3())
elapsed = time.time() - start
print(f"Результат: {result}")
print(f"Время: {elapsed:.2f} сек (последовательно: 0.1 + 0.1 + 0.1 + 0.1 = 0.4)")
print()
print("→ Все await'ы выполняются последовательно!")
print("→ Три корутины превратились в один поток")
print("→ await 'раскрыл' вложенность")
print()

# ============================================
# СРАВНЕНИЕ: yield from vs await
# ============================================
print("=" * 70)
print("СРАВНЕНИЕ: yield from vs await")
print("=" * 70)
print()

print("yield from с генераторами:")
print("  def outer():")
print("      yield from middle()")
print("        yield from inner()")
print("          yield 1, 2, 3")
print("  → Все yield'ы выполняются последовательно")
print("  → Один генератор с множеством yield")
print()
print("await с корутинами:")
print("  async def outer():")
print("      await middle()")
print("        await inner()")
print("          await sleep(0.1), sleep(0.1)")
print("  → Все await'ы выполняются последовательно")
print("  → Один поток с множеством await")
print()
print("→ Оба 'раскрывают' вложенность!")
print("→ Оба превращают вложенные вызовы в один поток")
print()

# ============================================
# ПЕРЕДАЧА ЗНАЧЕНИЙ: через await
# ============================================
print("=" * 70)
print("ПЕРЕДАЧА ЗНАЧЕНИЙ: через await")
print("=" * 70)
print()

async def receiver():
    """Корутина, которая получает значения через await"""
    print("  receiver: await sleep(0.1)")
    await asyncio.sleep(0.1)
    val1 = "hello"  # В реальности это может быть результат await
    print(f"  receiver: получил {val1}")
    
    print("  receiver: await sleep(0.1)")
    await asyncio.sleep(0.1)
    val2 = "world"
    print(f"  receiver: получил {val2}")
    
    return f"got {val1} and {val2}"

async def delegator():
    """Корутина, которая делегирует через await"""
    print("delegator: await receiver()")
    result = await receiver()
    print(f"delegator: получил результат {result}")
    return result

print("Демонстрация передачи значений:")
print()
result = asyncio.run(delegator())
print(f"Итоговый результат: {result}")
print()
print("→ await передает значения через все уровни!")
print("→ Результаты проходят через delegator → receiver")
print("→ await 'раскрывает' вложенность и передает значения")
print()

# ============================================
# ЭКВИВАЛЕНТ: что происходит внутри
# ============================================
print("=" * 70)
print("ЭКВИВАЛЕНТ: что происходит внутри")
print("=" * 70)
print()

print("async def outer():")
print("    result = await middle()")
print()
print("Эквивалентно (упрощенно):")
print()
print("async def outer_equivalent():")
print("    coro = middle()")
print("    # Task.__step() вызывает coro.send(None)")
print("    # Корутина выполняется до следующего await")
print("    # Если middle делает await inner(), то:")
print("    #   - inner() выполняется до завершения")
print("    #   - Все await'ы из inner выполняются последовательно")
print("    #   - middle продолжается")
print("    #   - Все await'ы из middle выполняются последовательно")
print("    #   - outer продолжается")
print("    result = <результат middle>")
print("    await sleep(0.1)")
print("    return 'outer_done'")
print()
print("→ await автоматически делает эту работу")
print("→ 'Раскрывает' вложенность")
print("→ Превращает вложенные корутины в один поток")
print()

# ============================================
# ВЫВОД
# ============================================
print("=" * 70)
print("ВЫВОД")
print("=" * 70)
print()

print("✅ await 'раскрывает' вложенные корутины")
print("   - Три уровня → один поток")
print("   - Все await'ы выполняются последовательно")
print("   - Множество точек остановки в одном потоке")
print()
print("✅ await работает как yield from")
print("   - Оба 'раскрывают' вложенность")
print("   - Оба превращают вложенные вызовы в один поток")
print("   - Оба выполняют все точки остановки последовательно")
print()
print("🔑 КЛЮЧЕВОЕ ПОНИМАНИЕ:")
print("   await = yield from для корутин")
print("   Вложенные корутины → один поток с множеством await")
print("   Это и есть 'раскрытие' вложенности!")































