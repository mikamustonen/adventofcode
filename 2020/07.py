import re
from pathlib import Path


def parse_contents(input_path: Path) -> dict[str, dict[str, int]]:
    result = {}
    with input_path.open() as f:
        for line in f:
            container, _, contents = line.partition(" bags contain ")
            contents = re.findall(r"(\d+) ([\s\w]+) bag", contents)
            result[container] = {y: int(x) for x, y in contents}
    return result


def can_contain(what: str, container: str, rules: dict) -> bool:
    return (any(item == what for item in rules[container]) or
            any(can_contain(what, item, rules) for item in rules[container]))


def number_of_contents(container: str, rules: dict) -> int:
    return sum(number * (number_of_contents(item, rules) + 1)
               for item, number in rules[container].items())


nesting_rules = parse_contents(Path("input") / "07.txt")
print(sum(can_contain('shiny gold', container, nesting_rules) for container in nesting_rules))
print(number_of_contents('shiny gold', nesting_rules))
