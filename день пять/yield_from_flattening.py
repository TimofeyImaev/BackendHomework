"""
ДОКАЗАТЕЛЬСТВО: yield from превращает вложенные генераторы в один

Вы АБСОЛЮТНО ПРАВЫ!
Три вложенных генератора превращаются в один с кучей остановок.
"""

# ============================================
# ДОКАЗАТЕЛЬСТВО: вложенность "раскрывается"
# ============================================
print("=" * 70)
print("ДОКАЗАТЕЛЬСТВО: вложенность 'раскрывается'")
print("=" * 70)
print()

def inner():
    yield 1
    yield 2
    yield 3
    return "inner_done"

def middle():
    yield from inner()  # ← Раскрывает inner
    yield 4
    yield 5
    return "middle_done"

def outer():
    yield from middle()  # ← Раскрывает middle (который уже раскрыл inner)
    yield 6
    yield 7
    return "outer_done"

print("Структура:")
print("  outer()")
print("    yield from middle()")
print("      yield from inner()")
print("        yield 1, 2, 3")
print("      yield 4, 5")
print("    yield 6, 7")
print()

print("Когда мы делаем yield from, это превращается в:")
print("  outer() → один генератор с yield'ами:")
print("    yield 1  # из inner")
print("    yield 2  # из inner")
print("    yield 3  # из inner")
print("    yield 4  # из middle")
print("    yield 5  # из middle")
print("    yield 6  # из outer")
print("    yield 7  # из outer")
print()

print("Демонстрация:")
gen = outer()
values = []
try:
    while True:
        value = next(gen)
        values.append(value)
        print(f"  Получено: {value}")
except StopIteration as e:
    print(f"  StopIteration: {e.value}")

print()
print(f"Все значения подряд: {values}")
print("→ Все yield'ы из всех уровней выполняются последовательно!")
print("→ Вложенность 'раскрыта' в один поток")
print()

# ============================================
# ЭКВИВАЛЕНТ: что делает yield from
# ============================================
print("=" * 70)
print("ЭКВИВАЛЕНТ: что делает yield from")
print("=" * 70)
print()

print("def outer():")
print("    yield from middle()")
print()
print("Эквивалентно (упрощенно):")
print()
print("def outer_equivalent():")
print("    gen = middle()")
print("    while True:")
print("        try:")
print("            value = next(gen)  # Получаем из middle")
print("            yield value        # Отдаем наружу")
print("        except StopIteration as e:")
print("            result = e.value   # Получаем return")
print("            break")
print("    yield 6")
print("    yield 7")
print("    return 'outer_done'")
print()
print("→ yield from автоматически делает эту работу")
print("→ 'Раскрывает' вложенность")
print("→ Превращает вложенные генераторы в один поток")
print()

# ============================================
# ТРИ УРОВНЯ: полная демонстрация
# ============================================
print("=" * 70)
print("ТРИ УРОВНЯ: полная демонстрация")
print("=" * 70)
print()

def level1():
    print("    [level1] yield 'a'")
    yield 'a'
    print("    [level1] yield 'b'")
    yield 'b'
    print("    [level1] return")
    return 'level1_done'

def level2():
    print("  [level2] yield from level1()")
    result = yield from level1()
    print(f"  [level2] получил: {result}")
    print("  [level2] yield 'c'")
    yield 'c'
    print("  [level2] return")
    return 'level2_done'

def level3():
    print("[level3] yield from level2()")
    result = yield from level2()
    print(f"[level3] получил: {result}")
    print("[level3] yield 'd'")
    yield 'd'
    print("[level3] return")
    return 'level3_done'

print("Запускаем три уровня:")
gen = level3()
print()

print("Итерация (все выполняется последовательно):")
values = []
try:
    while True:
        value = next(gen)
        values.append(value)
        print(f"  → Получено: {value}")
except StopIteration as e:
    print(f"  → StopIteration: {e.value}")

print()
print(f"Все значения: {values}")
print()
print("→ Три генератора превратились в один!")
print("→ Все yield'ы выполняются последовательно")
print("→ Вложенность полностью 'раскрыта'")
print()

# ============================================
# СРАВНЕНИЕ: с await
# ============================================
print("=" * 70)
print("СРАВНЕНИЕ: с await")
print("=" * 70)
print()

print("await работает ТАК ЖЕ:")
print()
print("async def level1():")
print("    await asyncio.sleep(0.1)  # yield точка")
print("    await asyncio.sleep(0.1)  # yield точка")
print()
print("async def level2():")
print("    await level1()  # 'раскрывает' level1")
print("    await asyncio.sleep(0.1)  # yield точка")
print()
print("async def level3():")
print("    await level2()  # 'раскрывает' level2 (который уже раскрыл level1)")
print("    await asyncio.sleep(0.1)  # yield точка")
print()
print("→ Все await'ы выполняются последовательно")
print("→ Три корутины превращаются в один поток")
print("→ С множеством точек остановки (await)")
print()

# ============================================
# ВЫВОД
# ============================================
print("=" * 70)
print("ВЫВОД")
print("=" * 70)
print()

print("✅ yield from 'раскрывает' вложенные генераторы")
print("   - Три уровня → один генератор")
print("   - Все yield'ы выполняются последовательно")
print("   - Множество точек остановки в одном потоке")
print()
print("✅ await работает ТАК ЖЕ")
print("   - Три уровня корутин → один поток")
print("   - Все await'ы выполняются последовательно")
print("   - Множество точек остановки")
print()
print("🔑 КЛЮЧЕВОЕ ПОНИМАНИЕ:")
print("   yield from и await 'раскрывают' вложенность")
print("   Вложенные вызовы → один поток с множеством остановок")
print("   Это и есть 'раскрытие' вложенности!")



























