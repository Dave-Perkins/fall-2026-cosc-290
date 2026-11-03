from math import factorial
from time import perf_counter

def fpf(n):
    # Build up from the bottom: a and b hold fpf(k - 2) and fpf(k - 1).
    # Same recurrence as before, but each value is computed once, in order,
    # with no recursion and no cache.
    if n == 1:
        return 0
    a, b = 0, 1                 # fpf(1), fpf(2)
    for k in range(3, n + 1):
        a, b = b, (k - 1) * (a + b)
    return b

n = 400
start = perf_counter()
result = fpf(n)
elapsed = perf_counter() - start
print(f"fpf({n}) = {result}")
print(f"fpf({n}) / {n}! = {result / factorial(n)}")
print(f"{max(n - 2, 0)} loop steps, took {round(elapsed, 5)} seconds")
