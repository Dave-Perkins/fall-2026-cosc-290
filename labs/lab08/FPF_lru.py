from math import factorial
from time import perf_counter
from functools import lru_cache

def counted(f):                 # 1. takes a function as its argument
    def wrapper(n):             # 2. a new function, defined inside; it can see f
        wrapper.calls += 1      # 3. increment the attribute .calls
        return f(n)             # 4. then call the original
    wrapper.calls = 0           # 5. attach a counter to the new function
    return wrapper              # 6. hand the new function back

def fpf(n):
    if n == 1:
        return 0
    elif n == 2:
        return 1
    return (n - 1) * (fpf(n - 1) + fpf(n - 2))

# lru_cache is a decorator from the standard library.  lru_cache(maxsize=None)
# builds the decorator; applying it to fpf returns a wrapper that remembers
# every result, so each value of n is computed only once.
fpf = lru_cache(maxsize=None)(fpf)
cached = fpf                    # keep a handle on this wrapper to ask it for statistics later

fpf = counted(fpf)              # wrap again, so every call (cache hit or miss) is counted

n = 30
start = perf_counter()
result = fpf(n)
elapsed = perf_counter() - start
print(f"fpf({n}) = {result}")
print(f"fpf({n}) / {n}! = {result / factorial(n)}")
print(f"{fpf.calls} calls, took {round(elapsed, 5)} seconds")
print(cached.cache_info())      # misses = times the body ran, hits = answers from memory
