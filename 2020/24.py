from pathlib import Path


def parse_line(line: str) -> list[str]:
    result = []
    i = 0
    while i < len(line):
        if line[i] in 'ns':
            result.append(line[i:i+2])
            i += 2
        else:
            result.append(line[i])
            i += 1
    return result


input_path = Path("input") / "24.txt"
with input_path.open() as f:
    instructions = [parse_line(line.strip()) for line in f]

# The coordinate system: x axis points east, y axis points northeast
directions = {'e': (1, 0), 'w': (-1, 0), 'ne': (0, 1), 'nw': (-1, 1), 'se': (1, -1), 'sw': (0, -1)}

# Part 1
black_tiles = set()
for instruction in instructions:
    x, y = 0, 0
    for step in instruction:
        dx, dy = directions[step]
        x += dx
        y += dy
    if (x, y) in black_tiles:
        black_tiles.remove((x, y))
    else:
        black_tiles.add((x, y))

print(len(black_tiles))


# Part 2
def neighbors(x: int, y: int) -> list[tuple[int, int]]:
    return [(x + dx, y + dy) for dx, dy in directions.values()]


def tiles_next_day(black_tiles: set[tuple[int, int]]) -> set[tuple[int, int]]:

    tiles_to_track = set()
    for tile in black_tiles:
        tiles_to_track.add(tile)
        tiles_to_track.update(set(neighbors(*tile)))

    result = set()
    for tile in tiles_to_track:
        black_neighbors = sum((x, y) in black_tiles for x, y in neighbors(*tile))
        if (tile in black_tiles and black_neighbors == 1) or black_neighbors == 2:
            result.add(tile)

    return result


for day in range(1, 101):
    black_tiles = tiles_next_day(black_tiles)
    print(f"Day {day}: {len(black_tiles)}")
