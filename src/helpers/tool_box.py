import random


def random_id(max_length: int = 3) -> int:
    length = random.randint(1, max_length)
    return random.randint(1, (10**length - 1))


def random_string(max_length: int = 5) -> str:
    length = random.randint(1, max_length)
    return "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=length))
