# Lab 02: Attacking Diffie-Hellman

In Lab 01 you built a Diffie-Hellman key exchange. This time you are the
eavesdropper.

You have intercepted nine key exchanges. For each one you know the public
values only:

| symbol | meaning |
|---|---|
| g | the generator |
| n | the modulus |
| A | Alice's public value, g^a mod n |
| B | Bob's public value, g^b mod n |

Your program must recover the shared key g^(ab) mod n whenever the parameters
allow it, and report **cannot determine** when they do not. Scenario 1 reuses
the first test case from Lab 01, with numbers small enough to trace on paper;
work it by hand before you write any code. The other eight exchanges use 64-bit
parameters of differing quality. Some are easy, some take real work, and at
least one is beyond reach for any laptop. Deciding which is which is part of the
assignment.

## Files

- `skeleton.py` is the only file you edit. It holds a toolkit of stub functions
  with hints, plus a driver that runs every scenario.
- `scenarios.py` supplies the data. Do not edit it. It exposes
  `get_scenarios()` and `check(scenario_id, key)`, which tells you whether a
  candidate key is right without revealing the answer.

## Running

```
python3 skeleton.py
```

Each scenario prints one line, either

```
Scenario 3: key = 7125552715819496214  PASSED (0.01 s)
```

or

```
Scenario 4: cannot determine            (0.02 s)
```

followed by a summary count.

## Advice

Fill in the toolkit from the top down and test each piece on small numbers you
can check by hand before pointing it at the scenarios. Start with `fermat_test`,
the naive primality test, and try it on 561 before moving to Miller-Rabin; the
docstring says why. Giving up is a legitimate
answer when the math says so, but your code should decide that quickly rather
than running for an hour. In your write-up, explain for each scenario what
weakness you exploited or why no attack was possible.
