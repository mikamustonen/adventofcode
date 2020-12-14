import re
from collections import defaultdict
from pathlib import Path


# Part 1
input_path = Path("input") / "14.txt"
with input_path.open() as f:
    instructions = [line.strip() for line in f]

memory = defaultdict(lambda: 0)
and_mask, or_mask = 0, 0

for instruction in instructions:
    if instruction.startswith("mask"):
        mask = instruction.removeprefix("mask = ")
        and_mask = int(mask.replace('1', '0').replace('X', '1'), base=2)
        or_mask = int(mask.replace('X', '0'), base=2)
    elif instruction.startswith("mem"):
        matcher = re.match(r"mem\[(\d+)\] = (\d+)", instruction)
        address, value = matcher.groups()
        memory[int(address)] = int(value) & and_mask | or_mask

print(sum(x for _, x in memory.items()))


# Part 2
def generate_floating_options(address: str):
    if 'X' in address:
        yield from generate_floating_options(address.replace('X', '0', 1))
        yield from generate_floating_options(address.replace('X', '1', 1))
    else:
        yield address


memory = defaultdict(lambda: 0)
and_mask, or_mask = 0, 0
floating_masks = []

for instruction in instructions:
    if instruction.startswith("mask"):
        mask = instruction.removeprefix("mask = ")
        or_mask = int(mask.replace('X', '0'), base=2)
        and_mask = int(mask.replace('0', '1').replace('X', '0'), base=2)
        floating_masks = [int(x, base=2) for x in generate_floating_options(mask)]
    elif instruction.startswith("mem"):
        matcher = re.match(r"mem\[(\d+)\] = (\d+)", instruction)
        address, value = [int(x) for x in matcher.groups()]
        base_address = address & and_mask | or_mask
        for a in floating_masks:
            memory[base_address | a] = value

print(sum(x for _, x in memory.items()))
