from data_pipeline_takehome.tasks.task_decorator import task

word_cache_limit = 6
permutations_cache: dict[str, list[str]] = {}
cache_hits = {"hits": 0, "misses": 0, "total": 0}


# @timer(label="permutations")
@task(failure_rate=0.01)
def permutations(word: str, use_cache=True):
    if len(word) == 0:
        return []
    if len(word) == 1:
        return [word]

    chars = list(word)
    chars.sort()
    sorted_word = "".join(chars)
    cache_hits["total"] += 1
    if use_cache and sorted_word in permutations_cache:
        cache_hits["hits"] += 1
        return permutations_cache[sorted_word]

    cache_hits["misses"] += 1

    perms = []
    for i in range(len(sorted_word)):
        first_char = chars[i]
        tail = chars.copy()

        # Swap the first and ith character, then remove the first char
        tail[i] = chars[0]
        tail.pop(0)

        tail_perms = permutations("".join(tail))

        for tail_perm in tail_perms:
            perms.append(first_char + tail_perm)

    if use_cache and len(word) <= word_cache_limit:
        permutations_cache[sorted_word] = perms

    return perms
