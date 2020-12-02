import re
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class PasswordEntry:
    min_times: int
    max_times: int
    character: str
    password: str


def parse_input(input_path: Path) -> List[PasswordEntry]:
    results = []
    entry_format = re.compile(r'(?P<min_times>\d+)-(?P<max_times>\d+) (?P<character>.): (?P<password>.+)')

    with input_path.open() as f:
        for line in f:
            parsed_line = entry_format.search(line.strip()).groupdict()
            results.append(PasswordEntry(
                min_times=int(parsed_line['min_times']),
                max_times=int(parsed_line['max_times']),
                character=parsed_line['character'],
                password=parsed_line['password']
            ))

    return results


def is_valid(entry: PasswordEntry) -> bool:
    number_of_occurrences = len([character for character in entry.password if character == entry.character])
    return entry.min_times <= number_of_occurrences <= entry.max_times


def is_valid_new_rules(entry: PasswordEntry) -> bool:
    # Re-interpreted rules: min_times and max_times are actually one-based string positions
    # in exactly one of which the character must appear
    return len([position
                for position in [entry.min_times, entry.max_times]
                if entry.character == entry.password[position - 1]]) == 1


# Part 1
password_data = parse_input(Path("input") / "02.txt")
total_number_of_passwords = len(password_data)
number_of_valid_passwords = sum(is_valid(entry) for entry in password_data)
print(f"{number_of_valid_passwords}/{total_number_of_passwords} passwords valid")

# Part 2
number_of_valid_passwords = sum(is_valid_new_rules(entry) for entry in password_data)
print(f"{number_of_valid_passwords}/{total_number_of_passwords} passwords valid according to the new rules")
