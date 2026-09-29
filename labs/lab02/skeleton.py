"""
Lab 02: Attacking Diffie-Hellman

You have eavesdropped on nine Diffie-Hellman key exchanges.  For each one you
know the public values g, n, A = g^a mod n and B = g^b mod n, and nothing else.
Recover the shared key g^(ab) mod n whenever the parameters are weak enough to
allow it, and say "cannot determine" when they are not.  Scenario 1 is small
enough to work by hand; do that first and use it to test each function.

Run with:

    python3 skeleton.py

Edit only this file.  scenarios.py supplies the data and a hash-based checker.

The functions below are a toolkit.  Fill them in from the top down; each one is
useful on its own, and attack() at the bottom puts them together.  You may use
Python's built-in pow(x, y, m) for fast modular exponentiation, and pow(x, -1, m)
for a modular inverse.
"""

from __future__ import annotations

import random
import time
from math import gcd, isqrt, lcm

import scenarios
from scenarios import Scenario

# If a prime factor of ord(g) is larger than this, baby-step giant-step would
# need more than about 2^20 table entries.  Treat such scenarios as out of reach.
BSGS_LIMIT = 1 << 40


def fermat_test(n: int, rounds: int = 20) -> bool:
    """
    The naive primality test.  Return True if n passes `rounds` trials of
    Fermat's little theorem, False if any trial proves n composite.

    Fermat's little theorem says that if n is prime, then a^(n-1) = 1 (mod n)
    for every a not divisible by n.  So pick a random base a with 2 <= a <= n-2
    and compute a^(n-1) mod n.  If the result is not 1, n is certainly composite.
    If it is 1, try another base.  After `rounds` bases have all returned 1,
    call n a probable prime.

    Warm-up: 561 = 3 * 11 * 17 is composite.  Check by hand (with pow) that
    2^560, 5^560 and 7^560 are all 1 mod 561, so those bases say "prime".  In
    fact every base coprime to 561 does; such numbers are called Carmichael
    numbers and there are infinitely many.  Random bases still catch 561, but
    only when they happen to share a factor with it, which is really a lucky
    trial division.  For a Carmichael number with large prime factors that luck
    never comes.  Once you see the problem, read the docstring for
    is_probable_prime.
    """
    raise NotImplementedError


def is_probable_prime(n: int) -> bool:
    """
    Return True if n is (almost certainly) prime.

    Trial division up to sqrt(n) is far too slow for 64-bit n: sqrt(2^64) is
    about four billion.  Use the Miller-Rabin test instead.  Write n - 1 as
    2^s * d with d odd; then for each base a in a fixed list, compute
    x = a^d mod n and square it up to s - 1 times.  If x never hits 1 or n - 1
    in the right way, n is composite.  With the bases 2, 3, 5, ..., 37 the test
    is exact for every n below 3.3 * 10^24.

    Miller-Rabin is the Fermat test with one extra check: it looks at the
    square roots taken on the way to a^(n-1), not just the final value.
    """
    raise NotImplementedError


def factor(n: int) -> dict[int, int]:
    """
    Return the prime factorization of n as a dictionary {prime: exponent}.

    Suggested approach:
      1. Trial-divide by small primes (up to about 10^5) to strip small factors.
      2. If what remains passes is_probable_prime, record it and stop.
      3. Otherwise split it with Pollard's rho method: iterate x -> x^2 + c mod n
         from two starting points at different speeds and take gcd(x - y, n)
         until it is a nontrivial factor.  Recurse on both pieces.
    Pollard rho finds a 32-bit factor of a 64-bit number in about 2^16 steps.
    """
    raise NotImplementedError


def carmichael_lambda(n_factors: dict[int, int]) -> int:
    """
    Return lambda(n), the exponent of the group of units mod n, given the
    factorization of n.

    Every unit x satisfies x^lambda(n) = 1 (mod n), so the order of any
    generator divides lambda(n).  For a prime p, lambda(p) = p - 1.  For a
    product of distinct primes, lambda(n) = lcm(p - 1 for each prime p).
    (For a prime power p^e with p odd, use (p - 1) * p^(e - 1).)
    """
    raise NotImplementedError


def element_order(g: int, n: int, multiple: int) -> int:
    """
    Return the multiplicative order of g mod n, the smallest k > 0 with
    g^k = 1 (mod n), given some known multiple of it (lambda(n) works).

    Start with m = multiple.  For each prime p dividing m, keep replacing m
    by m / p as long as g^(m/p) = 1 (mod n).  What remains is the order.
    """
    raise NotImplementedError


def baby_step_giant_step(g: int, h: int, n: int, order: int) -> int | None:
    """
    Solve g^x = h (mod n) for 0 <= x < order, or return None if no solution.

    Let m = ceil(sqrt(order)).  Any x can be written as x = i*m + j with
    0 <= i, j < m.  Baby steps: store g^j -> j for every j in a dictionary.
    Giant steps: compute h * (g^(-m))^i for i = 0, 1, 2, ... and stop when the
    value appears in the dictionary.  Then x = i*m + j.

    This costs about sqrt(order) time and memory, which is fine when order is
    a few billion and hopeless when order is near 2^63.
    """
    raise NotImplementedError


def crt(residues: list[int], moduli: list[int]) -> int:
    """
    Chinese Remainder Theorem: return x with x = residues[i] (mod moduli[i])
    for every i.  The moduli are pairwise coprime.  The answer is unique mod
    the product of the moduli.
    """
    raise NotImplementedError


def pohlig_hellman(g: int, h: int, n: int, order_factors: dict[int, int]) -> int | None:
    """
    Solve g^x = h (mod n) when the order of g has the factorization
    order_factors = {p: e, ...}.  Return x mod ord(g), or None on failure.

    Idea: the hard problem splits into one small problem per prime power p^e
    dividing the order.  For each p^e:
      * project into the subgroup of order p^e by raising g and h to the power
        ord(g) / p^e;
      * find x mod p^e one base-p digit at a time, where each digit is a
        discrete log in a subgroup of order p (use baby_step_giant_step);
    then glue the results together with crt().

    The whole attack costs about sqrt(largest prime factor of ord(g)), so
    what matters is not the size of n but the size of the largest prime
    dividing the order of g.
    """
    raise NotImplementedError


def attack(s: Scenario) -> int | None:
    """
    Return the shared key g^(ab) mod n, or None if it is out of reach.

    Suggested ladder.  Try each rung on every scenario before moving on:
      1. Brute force: try a = 0, 1, 2, ... until g^a = A.  Works when g has a
         small order, which you can only tell by trying.
      2. Factor n to get lambda(n), then find ord(g) and factor that.
      3. If the largest prime factor of ord(g) exceeds BSGS_LIMIT, give up.
      4. Otherwise run pohlig_hellman(g, A, n, ...) to recover a mod ord(g).
         Then the shared key is pow(B, a, n).
    Note that recovering a only mod ord(g) is enough, because B lies in the
    subgroup generated by g.
    """
    return None


def main() -> None:
    solved = 0
    total_start = time.perf_counter()
    for s in scenarios.get_scenarios():
        start = time.perf_counter()
        key = attack(s)
        elapsed = time.perf_counter() - start
        if key is None:
            print(f"Scenario {s.id}: cannot determine            ({elapsed:.2f} s)")
        elif scenarios.check(s.id, key):
            solved += 1
            print(f"Scenario {s.id}: key = {key:<20} PASSED ({elapsed:.2f} s)")
        else:
            print(f"Scenario {s.id}: key = {key:<20} FAILED ({elapsed:.2f} s)")
    total = time.perf_counter() - total_start
    print(f"\nRecovered {solved} of {len(scenarios.SCENARIOS)} keys in {total:.2f} s")


main()
