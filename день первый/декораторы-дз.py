from functools import wraps


def logi(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"func {func.__name__} args {args} kwargs {kwargs}")
        return func(*args, **kwargs)
    return wrapper

@logi
def add(a, b):
    return a + b

print(add(1, 2))