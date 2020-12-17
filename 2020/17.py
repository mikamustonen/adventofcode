from pathlib import Path


input_file = Path("input") / "17.txt"
active_cubes = set()
with input_file.open() as f:
    for y, line in enumerate(f):
        for x, character in enumerate(line):
            if character == '#':
                active_cubes.add((x, y, 0))


# Part 1
def next_cycle(cubes: set[tuple[int, int, int]]) -> set[tuple[int, int, int]]:
    new_active_cubes = set()
    x_min = min(cube[0] for cube in cubes) - 1
    x_max = max(cube[0] for cube in cubes) + 1
    y_min = min(cube[1] for cube in cubes) - 1
    y_max = max(cube[1] for cube in cubes) + 1
    z_min = min(cube[2] for cube in cubes) - 1
    z_max = max(cube[2] for cube in cubes) + 1
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            for z in range(z_min, z_max + 1):
                number_of_neigbors = sum(1 for x1, y1, z1 in (cubes - {(x, y, z)})
                                         if abs(x - x1) <= 1 and abs(y - y1) <= 1 and abs(z - z1) <= 1
                                         )
                is_active = (x, y, z) in cubes
                if (is_active and 2 <= number_of_neigbors <= 3) or (not is_active and number_of_neigbors == 3):
                    new_active_cubes.add((x, y, z))

    return new_active_cubes


for i in range(6):
    active_cubes = next_cycle(active_cubes)

print(len(active_cubes))


# Part 2
def next_cycle_4d(cubes: set[tuple[int, int, int, int]]) -> set[tuple[int, int, int, int]]:
    new_active_cubes = set()
    x_min = min(cube[0] for cube in cubes) - 1
    x_max = max(cube[0] for cube in cubes) + 1
    y_min = min(cube[1] for cube in cubes) - 1
    y_max = max(cube[1] for cube in cubes) + 1
    z_min = min(cube[2] for cube in cubes) - 1
    z_max = max(cube[2] for cube in cubes) + 1
    w_min = min(cube[3] for cube in cubes) - 1
    w_max = max(cube[3] for cube in cubes) + 1
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            for z in range(z_min, z_max + 1):
                for w in range(w_min, w_max + 1):
                    number_of_neigbors = sum(1 for x1, y1, z1, w1 in (cubes - {(x, y, z, w)})
                                             if abs(x - x1) <= 1 and abs(y - y1) <= 1 and abs(z - z1) <= 1 and abs(w - w1) <= 1
                                             )
                    is_active = (x, y, z, w) in cubes
                    if (is_active and 2 <= number_of_neigbors <= 3) or (not is_active and number_of_neigbors == 3):
                        new_active_cubes.add((x, y, z, w))

    return new_active_cubes


active_cubes = set()
with input_file.open() as f:
    for y, line in enumerate(f):
        for x, character in enumerate(line):
            if character == '#':
                active_cubes.add((x, y, 0, 0))

for i in range(6):
    active_cubes = next_cycle_4d(active_cubes)

print(len(active_cubes))
