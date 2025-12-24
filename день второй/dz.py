from functools import wraps

def limit_calls(max_calls: int):
    if max_calls <= 0:
        raise ValueError("max_calls must be positive")
    
    def decorator(func):
        calls_count = 0
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal calls_count
            if calls_count >= max_calls:
                raise RuntimeError(f"Function {func.__name__} exceeded maximum calls limit ({max_calls})")
            calls_count += 1
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator

@limit_calls(2)
def sum(a: int, b: int):
    return a + b

print(sum(1, 2))
print(sum(1, 2))
print(sum(1, 2))