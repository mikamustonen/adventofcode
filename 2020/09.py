from pathlib import Path


# Part 1
input_path = Path("input") / "09.txt"
with input_path.open() as f:
    data = [int(x) for x in f]

preamble_length = 25

for i, value in enumerate(data[preamble_length:]):
    window = data[i:i+preamble_length]
    allowed_inputs = set(x + y for x in window for y in window)
    if value not in allowed_inputs:
        print(value)
        break

# Part 2
for start in range(len(data)):
    for end in range(start + 2, len(data)):
        window = data[start:end]
        total = sum(window)
        if total == value:
            print(min(window) + max(window))
        elif total > value:
            break  # optimization: break from the inner loop

