from pathlib import Path


OCCUPIED_SEAT = '#'
FREE_SEAT = 'L'
FLOOR = '.'
OUTSIDE = ''
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


class Seating:
    def __init__(self, rows: list[str]) -> None:
        self.rows = rows[:]

    def __eq__(self, other) -> bool:
        return all(a == b for a, b in zip(self.rows, other.rows))

    @property
    def height(self):
        return len(self.rows)

    @property
    def width(self):
        return len(self.rows[0])

    @property
    def number_of_occupied_seats(self) -> int:
        return sum(row.count(OCCUPIED_SEAT) for row in self.rows)

    def get_tile(self, x, y) -> str:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.rows[y][x]
        return OUTSIDE

    def get_neighbors(self, x, y) -> list[str]:
        return [self.get_tile(x + dx, y + dy) for dx, dy in DIRECTIONS]

    def evolve_tile(self, x, y) -> str:
        this_tile = self.get_tile(x, y)
        neighbors = self.get_neighbors(x, y)
        if this_tile == FREE_SEAT and neighbors.count(OCCUPIED_SEAT) == 0:
            return OCCUPIED_SEAT
        elif this_tile == OCCUPIED_SEAT and neighbors.count(OCCUPIED_SEAT) >= 4:
            return FREE_SEAT
        else:
            return this_tile

    def evolve(self):
        return self.__class__(
            [''.join(self.evolve_tile(x, y) for x in range(self.width))
             for y in range(self.height)]
        )


# Part 1
input_path = Path("input") / "11.txt"
with input_path.open() as f:
    initial_rows = [line.strip() for line in f]

previous_seating = None
seating = Seating(initial_rows)
while previous_seating is None or seating != previous_seating:
    previous_seating = seating
    seating = seating.evolve()

print(seating.number_of_occupied_seats)


# Part 2
class SeatingPart2(Seating):

    def get_visible_seats(self, x, y) -> list[str]:
        seats = []
        for dx, dy in DIRECTIONS:
            distance = 1
            while True:
                tile = self.get_tile(x + distance * dx, y + distance * dy)
                if tile == FLOOR:
                    distance += 1
                    continue
                elif tile == OUTSIDE:
                    break
                else:
                    seats.append(tile)
                    break
        return seats

    def evolve_tile(self, x, y) -> str:
        this_tile = self.get_tile(x, y)
        visible_seats = self.get_visible_seats(x, y)
        if this_tile == FREE_SEAT and visible_seats.count(OCCUPIED_SEAT) == 0:
            return OCCUPIED_SEAT
        elif this_tile == OCCUPIED_SEAT and visible_seats.count(OCCUPIED_SEAT) >= 5:
            return FREE_SEAT
        return this_tile


previous_seating = None
seating = SeatingPart2(initial_rows)
while previous_seating is None or seating != previous_seating:
    previous_seating = seating
    seating = seating.evolve()

print(seating.number_of_occupied_seats)
