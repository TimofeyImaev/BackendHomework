import time

def decorator(func):
    def wrapper(s: str):
        s = ''.join(sorted(s.strip()))
        return func(s)
    return wrapper

@decorator
def fun(s: str):
    return s

def write_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        answer = func(*args, **kwargs)
        end_time = time.time()
        print(end_time - start_time)
        return answer
    return wrapper

@write_time
def sortstr(strings):
    answer = []
    for s in strings:
        answer.append(fun(s))
    return answer

with open("tests/3", "r") as f:
    strings = f.readlines()
    sortstr(strings)
    # for i in sortstr(strings):
    #     print(i)