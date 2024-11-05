import json

from data_pipeline_takehome.tasks.permutations_task import permutations
from data_pipeline_takehome.tasks.task_decorator import task

with open("src/data_pipeline_takehome/resources/english_dictionary.json") as file:
    english_dictionary = json.load(file)


@task(failure_rate=0.1)
def find_anagrams(word: str):
    perms = ["".join(p) for p in permutations(word)]
    anagrams = {}
    for p in perms:
        p_lower = p.lower()
        if p_lower in english_dictionary:
            anagrams[p_lower] = True

    return list(anagrams)
