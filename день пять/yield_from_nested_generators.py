"""
КАК yield from работает с вложенными генераторами

Вы правы! yield from "раскрывает" вложенные генераторы.
Три вложенных генератора превращаются в один с множеством остановок.
"""

import inspect

# ============================================
# ВЛОЖЕННЫЕ ГЕНЕРАТОРЫ БЕЗ yield from
# ============================================
print("=" * 70)
print("ВЛОЖЕННЫЕ ГЕНЕРАТОРЫ БЕЗ yield from")
print("=" * 70)
print()

def inner():
    print("  inner: yield 1")
    yield 1
    print("  inner: yield 2")
    yield 2
    print("  inner: return 'done'")
    return "done"

def middle():
    print("middle: создаю inner")
    gen = inner()
    print("middle: yield из inner")
    yield from gen
    print("middle: yield 3")
    yield 3
    print("middle: return")
    return "middle_done"

def outer():
    print("outer: создаю middle")
    gen = middle()
    print("outer: yield из middle")
    yield from gen
    print("outer: yield 4")
    yield 4
    print("outer: return")
    return "outer_done"

print("Создаем генератор:")
gen = outer()
print(f"Тип: {type(gen)}")
print()

print("Итерация:")
try:
    print(f"next(gen) = {next(gen)}")
    print(f"next(gen) = {next(gen)}")
    print(f"next(gen) = {next(gen)}")
    print(f"next(gen) = {next(gen)}")
    next(gen)  # Должен вызвать StopIteration
except StopIteration as e:
    print(f"StopIteration: {e.value}")
print()

# ============================================
# КАК yield from "РАСКРЫВАЕТ" ВЛОЖЕННОСТЬ
# ============================================
print("=" * 70)
print("КАК yield from 'РАСКРЫВАЕТ' ВЛОЖЕННОСТЬ")
print("=" * 70)
print()

print("yield from работает примерно так:")
print()
print("def outer():")
print("    gen = middle()")
print("    yield from gen  # Раскрывается в:")
print()
print("    # Эквивалентно:")
print("    for value in gen:")
print("        yield value")
print()
print("Но на самом деле yield from делает больше:")
print("  1. Передает значения из inner → middle → outer")
print("  2. Передает значения в обратном направлении (gen.send())")
print("  3. Обрабатывает StopIteration с return значением")
print()

# ============================================
# ДЕМОНСТРАЦИЯ: три уровня вложенности
# ============================================
print("=" * 70)
print("ДЕМОНСТРАЦИЯ: три уровня вложенности")
print("=" * 70)
print()

def level1():
    """Первый уровень"""
    print("  [level1] yield 'a'")
    yield 'a'
    print("  [level1] yield 'b'")
    yield 'b'
    print("  [level1] return 'level1_done'")
    return 'level1_done'

def level2():
    """Второй уровень"""
    print("[level2] yield from level1()")
    result = yield from level1()
    print(f"[level2] получил из level1: {result}")
    print("[level2] yield 'c'")
    yield 'c'
    print("[level2] return 'level2_done'")
    return 'level2_done'

def level3():
    """Третий уровень"""
    print("level3: yield from level2()")
    result = yield from level2()
    print(f"level3: получил из level2: {result}")
    print("level3: yield 'd'")
    yield 'd'
    print("level3: return 'level3_done'")
    return 'level3_done'

print("Создаем генератор с тремя уровнями:")
gen = level3()
print()

print("Итерация (все yield'ы выполняются последовательно):")
values = []
try:
    while True:
        value = next(gen)
        values.append(value)
        print(f"  Получено: {value}")
except StopIteration as e:
    print(f"  StopIteration: {e.value}")
    values.append(f"return={e.value}")

print()
print(f"Все значения: {values}")
print()
print("→ Три вложенных генератора превратились в один!")
print("→ Все yield'ы выполняются последовательно")
print("→ yield from 'раскрыл' вложенность")
print()

# ============================================
# ЭКВИВАЛЕНТ: что происходит внутри
# ============================================
print("=" * 70)
print("ЭКВИВАЛЕНТ: что происходит внутри")
print("=" * 70)
print()

print("level3() с yield from level2():")
print()
print("Эквивалентно (упрощенно):")
print()
print("def level3_equivalent():")
print("    gen2 = level2()")
print("    while True:")
print("        try:")
print("            value = next(gen2)  # Получаем из level2")
print("            yield value         # Отдаем наружу")
print("        except StopIteration as e:")
print("            result = e.value    # Получаем return значение")
print("            break")
print("    yield 'd'")
print("    return 'level3_done'")
print()
print("→ yield from автоматически делает эту работу")
print("→ Передает значения туда-обратно")
print("→ Обрабатывает StopIteration")
print()

# ============================================
# ПЕРЕДАЧА ЗНАЧЕНИЙ: gen.send(value)
# ============================================
print("=" * 70)
print("ПЕРЕДАЧА ЗНАЧЕНИЙ: gen.send(value)")
print("=" * 70)
print()

def receiver():
    """Генератор, который получает значения"""
    print("  receiver: жду значение")
    val1 = yield "ready1"
    print(f"  receiver: получил {val1}")
    val2 = yield "ready2"
    print(f"  receiver: получил {val2}")
    return f"got {val1} and {val2}"

def delegator():
    """Генератор, который делегирует через yield from"""
    print("delegator: yield from receiver()")
    result = yield from receiver()
    print(f"delegator: получил результат {result}")
    return result

print("Демонстрация передачи значений:")
gen = delegator()
print()

# Первый next() запускает генератор
print("next(gen):")
value = next(gen)
print(f"  Получено: {value}")
print()

# send() передает значение в receiver через delegator
print("gen.send('hello'):")
value = gen.send('hello')
print(f"  Получено: {value}")
print()

# Еще один send()
print("gen.send('world'):")
try:
    value = gen.send('world')
except StopIteration as e:
    print(f"  StopIteration: {e.value}")
print()

print("→ yield from передает значения через все уровни!")
print("→ 'hello' прошло через delegator → receiver")
print("→ 'world' прошло через delegator → receiver")
print()

# ============================================
# СРАВНЕНИЕ: yield from vs await
# ============================================
print("=" * 70)
print("СРАВНЕНИЕ: yield from vs await")
print("=" * 70)
print()

print("yield from с вложенными генераторами:")
print("  level3 → level2 → level1")
print("  → Все yield'ы выполняются последовательно")
print("  → Три генератора = один с множеством остановок")
print()
print("await с вложенными корутинами:")
print("  outer → middle → inner")
print("  → Работает ТАК ЖЕ!")
print("  → await 'раскрывает' вложенность")
print("  → Все await'ы выполняются последовательно")
print()
print("→ await работает как yield from для корутин")
print("→ Оба 'раскрывают' вложенность")
print("→ Оба превращают вложенные вызовы в один поток")
print()

# ============================================
# ВЫВОД
# ============================================
print("=" * 70)
print("ВЫВОД")
print("=" * 70)
print()

print("✅ yield from 'раскрывает' вложенные генераторы")
print("   - Три вложенных генератора → один с множеством yield")
print("   - Все yield'ы выполняются последовательно")
print("   - Значения передаются через все уровни")
print()
print("✅ await работает ТАК ЖЕ")
print("   - Три вложенные корутины → один поток выполнения")
print("   - Все await'ы выполняются последовательно")
print("   - await 'раскрывает' вложенность как yield from")
print()
print("🔑 КЛЮЧЕВОЕ ПОНИМАНИЕ:")
print("   yield from и await 'раскрывают' вложенность")
print("   Вложенные вызовы превращаются в один поток")
print("   С множеством точек остановки (yield/await)")































