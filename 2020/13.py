from pathlib import Path
from math import gcd, prod


# Part 1
input_path = Path("input") / "13.txt"
with input_path.open() as f:
    earliest_time = int(f.readline())
    bus_ids = [int(x) for x in f.readline().split(',') if x != 'x']

# tuple: (bus id, waiting time)
options = [(bus_id, 0 if earliest_time % bus_id == 0 else bus_id - earliest_time % bus_id) for bus_id in bus_ids]
best_option = sorted(options, key=lambda x: x[1])[0]
print(best_option[0] * best_option[1])

# Part 2
with input_path.open() as f:
    f.readline()  # ignored
    buses = [(i, int(x)) for i, x in enumerate(f.readline().split(',')) if x != 'x']  # (offset, bus_id)

# This is a congruence system: We want to find the smallest timestamp x so that
#     (x + offset) mod bus_id == 0   for all buses
# which is equivalent to
#     x mod bus_id = (bus_id - offset) mod bus_id

# Check that the bus IDs are pairwise coprime
if any(gcd(a, b) != 1 for a in bus_ids for b in bus_ids if a != b):
    raise SystemExit("The bus IDs are not pairwise coprime. Implement a different algorithm.")

# This
a = [(bus_id - offset) % bus_id for offset, bus_id in buses]
m = [bus_id for _, bus_id in buses]

# Solve the congruence system using the Chinese remainder theorem
product_of_ms = prod(m)
b = [product_of_ms // m_i for m_i in m]
result = sum(a_i * pow(b_i, -1, m_i) * b_i for a_i, b_i, m_i in zip(a, b, m)) % product_of_ms

print(result)
