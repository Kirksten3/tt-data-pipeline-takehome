from typing import List
from .task_decorator import task

cache = {}


def permutations(word: str) -> List[str]:
    global cache
    if len(word) == 0:
        return []
    if len(word) == 1:
        return [word]

    chars = sorted(list(word))
    sort_word = "".join(chars)
    if sort_word in cache:
        return cache[sort_word]

    perms = set()
    for i in range(len(chars)):
        first_char = chars[i]
        tail = chars.copy()

        # Swap the first and ith character, then remove the first char
        tail[i] = chars[0]
        tail.pop(0)

        tail_perms = permutations("".join(tail))

        for tail_perm in tail_perms:
            perms.add(first_char + tail_perm)

        cache[sort_word] = perms

    return list(perms)


@task(failure_rate=0.01)
def task_permutations(word: str) -> List[str]:
    return list(permutations(word))
