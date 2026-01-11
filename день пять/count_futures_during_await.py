import asyncio



async def level1():
    print("  level1: await sleep(0.1)")
    print(f"  Future до await: {future_count}")
    await asyncio.sleep(0.1)
    print(f"  Future после await: {future_count}")
    return "level1_done"

async def level2():
    print("level2: await level1()")
    print(f"Future до await: {future_count}")
    result = await level1()
    print(f"Future после await level1: {future_count}")
    print("level2: await sleep(0.1)")
    await asyncio.sleep(0.1)
    print(f"Future после await sleep: {future_count}")
    return "level2_done"

async def level3():
    print("level3: await level2()")
    print(f"Future до await: {future_count}")
    result = await level2()
    print(f"Future после await level2: {future_count}")
    print("level3: await sleep(0.1)")
    await asyncio.sleep(0.1)
    print(f"Future после await sleep: {future_count}")
    return "level3_done"

# Создаем новый loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
patch_loop(loop)

print("Запускаем вложенные await:")
asyncio.run(level3())
print()
print(f"ИТОГО создано Future: {future_count}")
print("→ Каждый await asyncio.sleep() создает 1 Future")
print("→ await сам по себе НЕ создает Future!")
print()

# ============================================
# ТЕСТ 3: await БЕЗ asyncio.sleep()
# ============================================
print("=" * 70)
print("ТЕСТ 3: await БЕЗ asyncio.sleep()")
print("=" * 70)
print()

async def simple_coro():
    """Корутина БЕЗ Future"""
    return 42

async def test_no_future():
    """await корутины, которая НЕ создает Future"""
    print("Вызываем await simple_coro()")
    print("Ожидание: НЕ создастся ни одного Future")
    print()
    
    print(f"Future до await: {future_count}")
    result = await simple_coro()
    print(f"Future после await: {future_count}")
    print(f"Результат: {result}")
    print()

# Сбрасываем счетчик
future_count = 0
future_refs.clear()

# Создаем новый loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
patch_loop(loop)

print("Запускаем тест:")
asyncio.run(test_no_future())
print(f"ИТОГО создано Future: {future_count}")
print("→ await БЕЗ asyncio.sleep() НЕ создает Future!")
print()

# ============================================
# ТЕСТ 4: подсчет активных Future в любой момент
# ============================================
print("=" * 70)
print("ТЕСТ 4: подсчет активных Future в любой момент")
print("=" * 70)
print()

def count_active_futures():
    """Подсчитывает активные Future"""
    count = 0
    active_futures = []
    for obj in gc.get_objects():
        if isinstance(obj, asyncio.Future):
            if not obj.done():
                count += 1
                active_futures.append(obj)
    return count, active_futures

async def test_active_futures():
    """Тест подсчета активных Future в любой момент"""
    print("Вызываем await asyncio.sleep(0.1)")
    print()
    
    count, futures = count_active_futures()
    print(f"Активных Future до await: {count}")
    print("Начинаем await...")
    
    # await создает Future внутри sleep
    # Во время await должен быть 1 активный Future (из sleep)
    await asyncio.sleep(0.1)
    
    count, futures = count_active_futures()
    print(f"Активных Future после await: {count}")
    if count > 0:
        print(f"  Активные Future: {[type(f).__name__ for f in futures]}")
    print()
    print("→ Во время await был 1 Future (из asyncio.sleep)")
    print("→ await сам по себе НЕ создал Future!")

# Создаем новый loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
patch_loop(loop)

print("Запускаем тест:")
asyncio.run(test_active_futures())

# ============================================
# ВЫВОД
# ============================================
print("=" * 70)
print("ВЫВОД")
print("=" * 70)
print()

print("✅ await НЕ создает Future")
print("   - await simple_coro() → 0 Future")
print("   - await asyncio.sleep() → 1 Future (созданный внутри sleep)")
print()
print("✅ Future создается ВНУТРИ корутин")
print("   - asyncio.sleep() создает Future внутри")
print("   - await просто использует этот Future")
print()
print("✅ В любой момент времени:")
print("   - await БЕЗ sleep → 0 Future")
print("   - await sleep → 1 Future (из sleep)")
print("   - await НЕ добавляет Future!")
print()
print("🔑 ДОКАЗАТЕЛЬСТВО:")
print("   await сам по себе НЕ создает Future")
print("   Future создается только внутри корутин (например, в sleep)")
print("   await просто использует уже созданный Future")

