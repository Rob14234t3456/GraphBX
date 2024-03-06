from math import log2, ceil


def bit_size(n):
    # calculates number of bits before final nonzero bit in binary representation
    if n == 0:
        return 0
    else:
        return ceil(log2(n)) + 1


def hamming_distance(a: int, b: int):
    # given two integers, calculates hamming distance of their binary forms
    n = max(bit_size(a), bit_size(b))
    distance = 0
    for i in reversed(range(n)):
        # first, check if ith place bit differs
        distance += (a >= 2 ** i) != (b >= 2 ** i)

        # then set up remaining bit place calculations
        a -= (2 ** i) * (a >= 2 ** i)
        b -= (2 ** i) * (b >= 2 ** i)
    return distance


def combinations(s: list, k: int):
    # generator function
    # yields all k-combinations of s
    ...


def permutations(s: list, k: int):
    # generator function
    # yields all k-permutations of s
    if k == 1:
        for i in range(len(s)):
            yield [s[i]]
    else:
        for i in range(len(s)):
            for perm in permutations([e for e in s if e != s[i]], k - 1):
                yield [s[i], *perm]
