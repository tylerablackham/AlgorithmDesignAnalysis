import pytest
from byu_pytest_utils import max_score

from fermat import mod_exp, fermat, miller_rabin

mod_exp_args = [
    (2, 10, 17, 4),
    (3, 7, 13, 3),
    (5, 20, 23, 12),
    (7, 13, 19, 7),
    (10, 24, 345, 100),
    (123, 23, 13, 11),
]


@max_score(10)
def test_mod_exp() -> None:
    for x, y, N, expected in mod_exp_args:
        assert mod_exp(x, y, N) == expected


prime_args = [17, 7520681183, 7263570389, 8993337217, 1320230501, 4955627707, 1095542699, 4505853973, 3176051033,
              6620550763, 2175869827, 565873182758780452445419697353, 529711114181889655730813410547,
              600873118804270914899076141007, 414831830449457057686418708951, 307982960434844707438032183853]


@max_score(5)
def test_primes_fermat() -> None:
    """This function tests multiple known prime numbers to verify that your fermat
    primality tests return 'prime'"""
    for N in prime_args:
        call = fermat(N, 100)
        assert call == "prime"


@max_score(10)
def test_primes_miller_rabin() -> None:
    """This function tests multiple known prime numbers to verify that your
    miller_rabin primality tests return 'prime'"""
    for N in prime_args:
        call = miller_rabin(N, 100)
        assert call == "prime"


composite_args = [24, 255, 6349202, 123456789, 248239522935, 593872957829392,
                  409359300583028201801840123]


@max_score(5)
def test_composites_fermat() -> None:
    """This function tests multiple known composite numbers to verify that your fermat
    primality tests return 'composite'"""
    for N in composite_args:
        call = fermat(N, 100)
        assert call == "composite"


@max_score(10)
def test_composites_miller_rabin() -> None:
    """This function tests multiple known composite numbers to verify that your
    miller_rabin primality tests return 'composite'"""
    for N in composite_args:
        call = miller_rabin(N, 100)
        assert call == "composite"
