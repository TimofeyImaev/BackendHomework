def inner():
    yield 1
    return "inner done"

def outer():
    result = yield from inner()  # ← здесь gi_yieldfrom указывает на inner()
    yield result

gen_outer = outer()
print(gen_outer.gi_yieldfrom)  # None - еще не начали yield from
print(next(gen_outer))
print(gen_outer.gi_yieldfrom)  # <generator object inner at ...> - сейчас ждем inner
print(gen_outer.gi_running)
print(gen_outer.gi_code)