"""
Reed-Solomon error correction over the integers mod 11, correcting one error.

A message is k symbols, each an integer from 0 to 10.  The codeword is the
message followed by 2 parity symbols, n = k + 2 symbols in all, with
n <= 10 (so k <= 8).

Symbols are the coefficients of a polynomial, first symbol first:

    3 1 4 1 5  means  3x^4 + 1x^3 + 4x^2 + 1x + 5

so "position i" is the coefficient of x^i, and the LAST symbol is position 0.

The generator polynomial g(x) = (x - a)(x - a^2), with a = 2, has
roots a and a^2.  Encoding makes the codeword T(x) a multiple of g(x), so
T(a) = T(a^2) = 0.  If an error e(x) = M * x^i is added at position i, the
two syndromes S1 = r(a) and S2 = r(a^2) depend only on the error:

    S1 = M * a^i        S2 = M * (a^i)^2

so S2 / S1 = a^i tells where the error is, and S1 / a^i tells what it is.

Usage (after copying this file to rs.py):
    python3 rs.py encode 3 1 4 1 5              (k symbols -> codeword)
    python3 rs.py decode 3 1 4 1 5 2 10         (codeword with up to 1 error -> message)

Fill in the five functions marked pass.  The generator polynomial, the
polynomial long division, and main() are finished.
"""

import sys

P = 11                  # the prime modulus; symbols are 0 .. P-1
ALPHA = 2               # a primitive root mod P: its powers 2^0 .. 2^9 are all different
T = 1                   # errors we can correct
PARITY = 2 * T          # number of parity symbols appended to every message
MAX_N = P - 1           # a codeword can be no longer than this


# ---------------------------------------------------------------------------
# Arithmetic mod P and polynomial helpers (given)
#
# A polynomial is a list of coefficients, highest degree first:
#     [3, 1, 4, 1, 5]  is  3x^4 + 1x^3 + 4x^2 + 1x + 5
# ---------------------------------------------------------------------------

def inverse(a):
    """ The inverse of a mod P. """
    return pow(a, P - 2, P)


def poly_eval(poly, x):
    """ The value of the polynomial at x, mod P. """
    result = 0
    for coefficient in poly:
        result = (result * x + coefficient) % P
    return result


def poly_mul(a, b):
    """ The product ab of the two given polynomials, mod P. """
    product = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            product[i + j] = (product[i + j] + ai * bj) % P
    return product


# ---------------------------------------------------------------------------
# Encoding (generator and poly_remainder are given; encode is for you to do)
# ---------------------------------------------------------------------------

def generator():
    """ g(x) = (x - a)(x - a^2) mod P, as a list of 3 coefficients. """
    g = [1]
    for j in range(1, PARITY + 1):
        root = pow(ALPHA, j, P)
        g = poly_mul(g, [1, (-root) % P])
    return g


def poly_remainder(num, den):
    """
    The remainder when num is divided by den, mod P, by long division.
    Returned as a list of len(den) - 1 coefficients (leading zeros kept).
    """
    num = list(num)
    lead_inv = inverse(den[0])
    for i in range(len(num) - len(den) + 1):
        factor = (num[i] * lead_inv) % P
        if factor != 0:
            for j in range(len(den)):
                num[i + j] = (num[i + j] - factor * den[j]) % P
    return num[len(num) - (len(den) - 1):]


def encode(message):
    """
    The codeword for a message: the message followed by PARITY parity symbols,
    chosen so that the whole codeword is divisible by g(x).
    """
    pass   


# ---------------------------------------------------------------------------
# Decoding (TODO)
# ---------------------------------------------------------------------------

def syndromes(received):
    """ [S1, S2] where S_j is the received polynomial evaluated at a^j. """
    pass   


def locate_error(S, n):
    """
    The position of the error, from the syndromes of an n-symbol received
    word that is known to have at least one error (S is not all zero).

    One error M at position i gives S1 = M * X and S2 = M * X^2 with
    X = a^i, so X = S2 / S1.  The position is the i with a^i = X.
    (Equivalently, i is the root of the error locator L(x) = 1 - X x at
    x = a^(-i).)  Returns None when no position fits: more than one error.
    """
    pass   


def error_value(S, position):
    """ The error value M at the given position: M = S1 / a^position. """
    pass   


def decode(received):
    """
    Fix up to one error.  Returns (corrected codeword, message, position,
    value), with position and value None when there was no error, or
    returns None when there is more than one error.
    """
    pass   


# ---------------------------------------------------------------------------
# Command-line interface (no need to edit below this line)
# ---------------------------------------------------------------------------

def parse_symbols(words, low, high):
    """ The words as ints from 0 to P-1; there must be low..high of them. """
    try:
        symbols = [int(w) for w in words]
    except ValueError:
        print(f"error: symbols must be integers, got {' '.join(words)}")
        sys.exit(1)
    if any(s < 0 or s >= P for s in symbols):
        print(f"error: symbols must be from 0 to {P - 1}, got {' '.join(words)}")
        sys.exit(1)
    if not low <= len(symbols) <= high:
        print(f"error: expected {low} to {high} symbols, got {len(symbols)}")
        sys.exit(1)
    return symbols


def show(symbols):
    return " ".join(str(s) for s in symbols)


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("encode", "decode"):
        print(f"usage: python3 rs.py encode <1 to {MAX_N - PARITY} symbols>")
        print(f"       python3 rs.py decode <{PARITY + 1} to {MAX_N} symbols>")
        print(f"       (each symbol is an integer from 0 to {P - 1})")
        sys.exit(1)
    command, words = sys.argv[1], sys.argv[2:]

    if command == "encode":
        message = parse_symbols(words, 1, MAX_N - PARITY)
        codeword = encode(message)
        print("message: ", show(message))
        print("codeword:", show(codeword))
    else:
        received = parse_symbols(words, PARITY + 1, MAX_N)
        print("received: ", show(received))
        print("syndromes:", show(syndromes(received)))
        result = decode(received)
        if result is None:
            print(f"decoding failed: more than {T} error")
            sys.exit(0)
        corrected, message, position, value = result
        if position is None:
            print("no error detected")
        else:
            print(f"error at position x^{position} (value {value}), subtracted")
        print("corrected:", show(corrected))
        print("message:  ", show(message))


main()
