import random
import sys

# This may come in handy...
from fermat import miller_rabin, fermat

# If you use a recursive implementation of `mod_exp` or extended-euclid,
# you recurse once for every bit in the number.
# If your number is more than 1000 bits, you'll exceed python's recursion limit.
# Here we raise the limit so the tests can run without any issue.
# Can you implement `mod_exp` and extended-euclid without recursion?
sys.setrecursionlimit(4000)

# When trying to find a relatively prime e for (p-1) * (q-1)
# use this list of 25 primes
# If none of these work, throw an exception (and let the instructors know!)
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


# Implement this function
def ext_euclid(a: int, b: int) -> tuple[int, int, int]:
    """
    The Extended Euclid algorithm
    Returns x, y , d such that:
    - d = GCD(a, b)
    - ax + by = d

    Note: a must be greater than b
    """
    if b == 0:
        return 1, 0, a
    x, y, d = ext_euclid(b, a % b)
    return y, x - (a//b)*y, d


# Implement this function
def generate_large_prime(bits=512) -> int:
    """
    Generate a random prime number with the specified bit length.
    Use random.getrandbits(bits) to generate a random number of the
     specified bit length.
    """
    while True:
        x = random.getrandbits(bits)
        k = 20
        if fermat(x, k) == "prime":
            return x


# Implement this function
def generate_key_pairs(bits: int) -> tuple[int, int, int]:
    """
    Generate RSA public and private key pairs.
    Return N, e, d
    - N must be the product of two random prime numbers p and q
    - e and d must be multiplicative inverses mod (p-1)(q-1)
    """
    p = generate_large_prime(bits)
    q = generate_large_prime(bits)
    while q == p:
        q = generate_large_prime(bits)
    N = p * q
    i = (p-1)*(q-1)
    e = 2
    d = 0
    for prime in primes:
        x, y, gcd = ext_euclid(i, prime)
        if gcd == 1:
            e = prime
            d = y
            break
    if d < 0:
        d = i + d
    return N, e, d
