from math import factorial
from time import perf_counter

def fpf(n):
    if n == 1:
        return 0
    elif n == 2:
        return 1
    return (n - 1) * (fpf(n - 1) + fpf(n - 2))

n = 30
start = perf_counter()
result = fpf(n)
elapsed = perf_counter() - start
print(f"fpf({n}) = {result}")
print(f"fpf({n}) / {n}! = {result / factorial(n)}")
print(f"took {round(elapsed, 2)} seconds")
