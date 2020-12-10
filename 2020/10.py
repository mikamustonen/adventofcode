from collections import defaultdict
from pathlib import Path


# Part 1
input_path = Path("input") / "10.txt"
with input_path.open() as f:
    adapters = sorted(int(line) for line in f)
adapters = [0] + adapters + [adapters[-1] + 3]  # include wall outlet and the device

diffs = [x - y for x, y in zip(adapters[1:], adapters[:-1])]
number_of_diffs_1 = sum(diff == 1 for diff in diffs)
number_of_diffs_3 = sum(diff == 3 for diff in diffs)
print(f"{number_of_diffs_1} x {number_of_diffs_3} = {number_of_diffs_1 * number_of_diffs_3}")

# Part 2
# Construct a distribution of different ways of producing different joltages
distribution = defaultdict(lambda: 0)
distribution[0] = 1  # the wall outlet
for adapter in adapters[1:]:
    distribution[adapter] = sum(distribution[adapter - i] for i in range(4))

print(distribution[adapters[-1]])
