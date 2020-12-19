import re
from pathlib import Path


# Part 1
def convert_to_regex(rule_number: int) -> str:
    rule = rules[rule_number]
    if type(rule) == str:
        return rule
    options = [''.join(convert_to_regex(x) for x in option) for option in rule]
    if len(options) > 1:
        return '(' + '|'.join(options) + ')'
    return options[0]


input_path = Path("input") / "19.txt"

with input_path.open() as f:
    rules_section, messages_section = f.read().split("\n\n")
    rules = {}
    for line in rules_section.strip().split("\n"):
        rule_number, rule = line.split(": ")
        if rule.startswith('"'):
            rules[int(rule_number)] = rule.removeprefix('"').removesuffix('"')
        else:
            rules[int(rule_number)] = [[int(x) for x in subrule.split()] for subrule in rule.split(" | ")]
    messages = [line.strip() for line in messages_section.strip().split("\n")]

pattern = convert_to_regex(0)
print(sum(re.fullmatch(pattern, message) is not None for message in messages))


# Part 2
def convert_to_regex_part2(rule_number: int) -> str:
    # Special cases
    if rule_number == 8:
        return convert_to_regex_part2(42) + "+"
    elif rule_number == 11:
        a, b = convert_to_regex_part2(42), convert_to_regex_part2(31)
        return '(' + '|'.join((i*a + i*b) for i in range(1, 10)) + ')'

    rule = rules[rule_number]
    if type(rule) == str:
        return rule
    options = []
    for option in rule:
        options.append(''.join(convert_to_regex_part2(x) for x in option))
    if len(options) > 1:
        return '(' + '|'.join(options) + ')'
    return options[0]


pattern = convert_to_regex_part2(0)
print(sum(re.fullmatch(pattern, message) is not None for message in messages))
