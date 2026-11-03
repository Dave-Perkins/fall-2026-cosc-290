from math import factorial
from time import perf_counter

def counted(f):                 # 1. takes a function as its argument
    def wrapper(n):             # 2. a new function, defined inside; it can see f
        wrapper.calls += 1      # 3. do the bookkeeping
        return f(n)             # 4. then call the original
    wrapper.calls = 0           # 5. attach a counter to the new function
    return wrapper              # 6. hand the new function back

@counted                        # same as writing  fpf = counted(fpf)  after the def
def fpf(n):                     # so the name fpf now refers to wrapper, not to this body
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
print(f"{fpf.calls} calls, took {round(elapsed, 2)} seconds")
