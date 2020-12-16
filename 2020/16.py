from math import prod
from pathlib import Path


# Part 1
input_file = Path("input") / "16.txt"
with input_file.open() as f:
    rules_section, your_ticket_section, tickets_section = f.read().split("\n\n")

rules = []
all_valid_ranges = []
for line in rules_section.strip().split("\n"):
    field_name, _, rule = line.strip().partition(":")
    valid_ranges = [tuple(int(x) for x in string.split("-")) for string in rule.split(" or ")]
    rules.append((field_name, valid_ranges))
    all_valid_ranges.extend(valid_ranges)

my_ticket = [int(x) for x in your_ticket_section.split("\n")[1].strip().split(",")]
nearby_tickets = [tuple(int(x) for x in line.split(",")) for line in tickets_section.strip().split("\n")[1:]]

sum_of_invalid_fields = sum(field
                            for ticket in nearby_tickets
                            for field in ticket
                            if not any(a <= field <= b for a, b in all_valid_ranges))

print(sum_of_invalid_fields)


# Part 2
def is_ticket_valid(ticket: tuple[int]) -> bool:
    for field in ticket:
        if not any(a <= field <= b for a, b in all_valid_ranges):
            return False
    return True


valid_tickets = [ticket for ticket in nearby_tickets if is_ticket_valid(ticket)]

field_names = [name for name, _ in rules]

# For each field, figure out the possible options
number_of_fields = len(valid_tickets[0])
field_name_options = []
for i in range(number_of_fields):
    options = set()
    for field_name, valid_ranges in rules:
        if all(any(a <= ticket[i] <= b for a, b in valid_ranges) for ticket in valid_tickets):
            options.add(field_name)
    field_name_options.append(options)

# Figure out the combination of options that must be valid by process of elimination
ticket_fields = {}
while len(ticket_fields) < number_of_fields:
    for i, options in enumerate(field_name_options):
        remaining_options = options - ticket_fields.keys()
        if len(remaining_options) == 1:
            (found_field,) = remaining_options
            if found_field not in ticket_fields:
                ticket_fields[found_field] = i

print(prod(my_ticket[i] for name, i in ticket_fields.items() if name.startswith("departure")))
