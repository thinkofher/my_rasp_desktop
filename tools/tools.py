from string import ascii_uppercase, digits
from random import choice


def random_key(length):
    key = ''.join(
        choice((ascii_uppercase + digits)) for _ in range(length)
    )
    return key
