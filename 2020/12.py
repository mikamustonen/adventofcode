from pathlib import Path


input_path = Path("input") / "12.txt"
with input_path.open() as f:
    instructions = [(line[0], int(line.strip()[1:])) for line in f]

# Part 1
# The coordinate system choice: x right, y down
x, y = 0, 0
directions = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}
dx, dy = directions['E']  # current direction

for instruction, amount in instructions:
    if instruction == 'F':
        x, y = x + amount * dx, y + amount * dy
    elif instruction == 'L':
        for i in range(amount // 90):
            dx, dy = dy, -dx
    elif instruction == 'R':
        for i in range(amount // 90):
            dx, dy = -dy, dx
    else:
        translate_x, translate_y = directions[instruction]
        x, y = x + amount * translate_x, y + amount * translate_y

print (abs(x) + abs(y))

# Part 2
x, y = 0, 0
dx, dy = 10, -1  # waypoint

for instruction, amount in instructions:
    if instruction == 'F':
        x += dx * amount
        y += dy * amount
    elif instruction == 'L':
        for i in range(amount // 90):
            dx, dy = dy, -dx
    elif instruction == 'R':
        for i in range(amount // 90):
            dx, dy = -dy, dx
    else:
        translate_x, translate_y = directions[instruction]
        dx, dy = dx + amount * translate_x, dy + amount * translate_y

print (abs(x) + abs(y))
