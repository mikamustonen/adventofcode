from pathlib import Path
from string import ascii_lowercase
from typing import List


def read_blank_separated_file(path: Path) -> List[List[str]]:
    with path.open() as f:
        chunks = f.read().strip().split("\n\n")
    return [chunk.split("\n") for chunk in chunks]


def combine_group_answers(answers: List[str]) -> str:
    return ''.join(c for c in ascii_lowercase if any(c in answer for answer in answers))


def combine_group_answers_corrected(answers: List[str]) -> str:
    return ''.join(c for c in ascii_lowercase if all(c in answer for answer in answers))


# Part 1
groups_data = read_blank_separated_file(Path("input") / "06.txt")
print(sum(len(combine_group_answers(group)) for group in groups_data))

# Part 2
print(sum(len(combine_group_answers_corrected(group)) for group in groups_data))
