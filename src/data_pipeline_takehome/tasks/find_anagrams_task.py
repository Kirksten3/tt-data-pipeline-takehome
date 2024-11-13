import os
from typing import Dict, List

from data_pipeline_takehome.resources.gcs import load_file_or_backup
from data_pipeline_takehome.tasks.task_decorator import task
from data_pipeline_takehome.utilities.tasks import ConfigurationManager


def find_anagrams(permutations: List[str], dictionary: Dict[str, str]) -> List[str]:
    return list({p.lower(): True for p in permutations if p.lower() in dictionary})


@task(failure_rate=0.1)
def task_find_anagrams(
    config: ConfigurationManager, permutations: List[str]
) -> List[str]:
    config.logger.info("Loading dictionary.")
    dictionary = load_file_or_backup(
        os.getenv("GCS_BUCKET"),
        "english_dictionary.json",
        "src/data_pipeline_takehome/resources/english_dictionary.json",
    )
    if dictionary is not None:
        config.logger.info("Dictionary Loaded.")
    return find_anagrams(permutations, dictionary)
