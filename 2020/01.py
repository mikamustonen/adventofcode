from pathlib import Path


input_path = Path("input") / "01.txt"

with input_path.open() as f:
    numbers = set(int(line) for line in f)

# Part 1: Find two entries that sum to 2020 and multiply them
for x in numbers:
    y = 2020 - x
    # If (x, y) is a solution then (y, x) is too, so ignore the cases x > y
    if x < y and y in numbers:
        print(f"{x} x {y} = {x * y}")

# Part 2: Find three entries that sum to 2020 and multiply them
for x in numbers:
    for y in numbers:
        z = 2020 - x - y
        # Consider only ordered triplets because of the symmetry of the solution
        if x < y < z and z in numbers:
            print(f"{x} x {y} x {z} = {x * y * z}")
