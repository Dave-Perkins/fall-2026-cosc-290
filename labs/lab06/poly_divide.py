"""
Polynomial long division mod a prime, shown step by step.

Coefficients are listed highest degree first, so

    3 1 4 1 5 0 0 0 0   means   3x^8 + x^7 + 4x^6 + x^5 + 5x^4

Usage:
    python3 poly_divide.py 3 1 4 1 5 0 0 0 0 --by 1 3 5 8 1
    python3 poly_divide.py --mod 13 3 1 4 --by 2 5

The dividend comes first, then --by and the divisor.  The modulus is 11
unless --mod says otherwise.  The program prints every subtraction, then the
quotient and the remainder.
"""

import argparse
import sys


def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def term(coef, power):
    """ One term, such as 3x^2, x, or 5. """
    if power == 0:
        return str(coef)
    x = "x" if power == 1 else f"x^{power}"
    return x if coef == 1 else f"{coef}{x}"


def poly(coeffs):
    """ The polynomial written out, zero terms omitted: 3x^2 + x + 5. """
    n = len(coeffs)
    terms = [term(c, n - 1 - i) for i, c in enumerate(coeffs) if c != 0]
    return " + ".join(terms) if terms else "0"


def both(coeffs):
    """ The polynomial and its coefficient list side by side. """
    return f"{poly(coeffs)}    [{' '.join(str(c) for c in coeffs)}]"


def long_division(num, den, p, name="G(x)"):
    """
    Divide num by den mod p, printing each step.  Returns (quotient, remainder).
    The remainder has len(den) - 1 coefficients, leading zeros kept.
    """
    num = [c % p for c in num]
    den = [c % p for c in den]
    while den and den[0] == 0:
        den = den[1:]
    if not den:
        raise ValueError("division by the zero polynomial")

    print(f"Long division of {poly(num)} by {name} = {poly(den)}, mod {p}:")
    lead_inv = pow(den[0], p - 2, p)          # inverse of the leading coefficient
    if den[0] != 1:
        print(f"  the leading coefficient of {name} is {den[0]}; its inverse mod {p} "
              f"is {lead_inv}, since {den[0]} * {lead_inv} = {den[0] * lead_inv} "
              f"= {den[0] * lead_inv % p} (mod {p})")

    work = list(num)
    quotient = []
    steps = len(work) - len(den) + 1
    if steps <= 0:
        print(f"  the degree of {poly(num)} is already below the degree of {name}: nothing to do")
        quotient = [0]
        remainder = [0] * (len(den) - 1 - len(work)) + work
    else:
        for i in range(steps):
            deg = len(work) - 1 - i
            coef = work[i]
            factor = (coef * lead_inv) % p
            quotient.append(factor)
            if coef == 0:
                print(f"  x^{deg} term is 0, nothing to subtract")
                continue
            shift = deg - (len(den) - 1)
            multiple = [(factor * c) % p for c in den] + [0] * shift
            if den[0] == 1:
                how = f"{term(factor, shift)} * {name}"
            else:
                how = f"{coef} * {lead_inv} = {factor}, so {term(factor, shift)} * {name}"
            print(f"  leading term {term(coef, deg)}: subtract {how} = {poly(multiple)}")
            for j in range(len(den)):
                work[i + j] = (work[i + j] - factor * den[j]) % p
            print(f"      leaves {both(work[i + 1:])}")
        remainder = work[len(work) - (len(den) - 1):]

    print(f"quotient q(x) = {both(quotient)}")
    print(f"remainder r(x) = {both(remainder)}")
    return quotient, remainder


def main():
    ap = argparse.ArgumentParser(description="Polynomial long division mod a prime, step by step.")
    ap.add_argument("dividend", nargs="+", type=int, metavar="c",
                    help="coefficients of the dividend, highest degree first")
    ap.add_argument("--by", nargs="+", type=int, required=True, metavar="c",
                    help="coefficients of the divisor, highest degree first")
    ap.add_argument("--mod", type=int, default=11, help="the prime modulus (default 11)")
    args = ap.parse_args()

    p = args.mod
    if not is_prime(p):
        sys.exit(f"error: {p} is not prime")
    if any(not 0 <= c < p for c in args.dividend + args.by):
        sys.exit(f"error: coefficients must be from 0 to {p - 1}")
    if all(c == 0 for c in args.by):
        sys.exit("error: cannot divide by 0")
    long_division(args.dividend, args.by, p)


if __name__ == "__main__":
    main()
