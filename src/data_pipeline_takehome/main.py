import argparse
import json
import time

from data_pipeline_takehome.tasks.filter_input_task import filter_input
from data_pipeline_takehome.tasks.find_anagrams_task import find_anagrams
from data_pipeline_takehome.tasks.get_words_task import get_words


def anagram_analysis_pipeline(text_input: str):
    start = time.perf_counter()

    filtered_input = filter_input(text_input)
    words = get_words(filtered_input)

    all_anagrams = []
    for word in words:
        print(f"Finding anagrams for {word}")
        anagrams = find_anagrams(word)
        all_anagrams += anagrams

    anagram_counts = {}
    for anagram in all_anagrams:
        if anagram not in anagram_counts:
            anagram_counts[anagram] = 0
        anagram_counts[anagram] += 1

    end = time.perf_counter()
    print(f"Text processing took {(end - start) * 1000}ms")

    return {"runtime": (end - start) * 1000, "anagram_counts": anagram_counts}


with open("src/data_pipeline_takehome/resources/test_cases.json") as file:
    test_cases = json.load(file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the data pipeline with a specified test case.")
    parser.add_argument(
        "--test-case",
        type=str,
        default="small",
        choices=[*test_cases, "all"],
        help="Specify which test case to run. Default is 'small'.",
    )
    args = parser.parse_args()

    test_cases_to_run = []

    if args.test_case == "all":
        test_cases_to_run = test_cases.items()
    else:
        test_cases_to_run = [(args.test_case, test_cases[args.test_case])]

    for case_name, test_case in test_cases_to_run:
        print(f"Running test case: {case_name}")
        result = anagram_analysis_pipeline(test_case["text"])
        print(json.dumps(result, indent=2))
        assert (
            result["runtime"] < test_case["expected"]["runtime"]
        ), f"Runtime {result['runtime']} exceeds expected {test_case['expected']['runtime']}"
        for anagram, count in test_case["expected"]["anagram_counts"].items():
            assert anagram in result["anagram_counts"], f"Anagram '{anagram}' not found in result"
            assert (
                result["anagram_counts"][anagram] == count
            ), f"Anagram '{anagram}' count {result['anagram_counts'][anagram]} differs from expected {count}"
