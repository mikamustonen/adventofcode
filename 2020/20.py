from dataclasses import dataclass
from math import prod, isqrt
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class OrientedTile:
    """A tile locked in a particular orientation"""
    id: int
    top: str
    right: str
    bottom: str
    left: str
    interior: tuple[str]


@dataclass(frozen=True)
class Tile:
    """All possible orientations of a tile"""
    id: int
    orientations: tuple[OrientedTile]


class Board:
    """A board that is filled in order from the top left corner row by row"""
    def __init__(self, size: int):
        self.size: int = size
        row = [None for _ in range(size)]
        self.slots: list[list[Optional[OrientedTile]]] = [row[:] for _ in range(size)]
        self.x: int = 0
        self.y: int = 0

    def place(self, orientation: OrientedTile) -> bool:
        if self.x > 0:
            required_left = self.slots[self.y][self.x - 1].right
            if orientation.left != required_left:
                return False
        if self.y > 0:
            required_top = self.slots[self.y - 1][self.x].bottom
            if orientation.top != required_top:
                return False
        self.slots[self.y][self.x] = orientation
        self.x += 1
        if self.x == self.size:
            self.y += 1
            self.x = 0
        return True

    def remove_last(self) -> None:
        self.slots[self.y][self.x] = None
        self.x -= 1
        if self.x < 0:
            self.y -= 1
            self.x = self.size - 1

    @property
    def checksum(self) -> int:
        return prod(self.slots[y][x].id for x, y in [(0, 0), (0, -1), (-1, 0), (-1, -1)])

    def __str__(self):
        result = ""
        for line in self.slots:
            for tile in line:
                if tile:
                    result = result + " " + str(tile.id)
                else:
                    result = result + " None"
            result = result + "\n"
        return result

    @property
    def image(self) -> list[str]:
        result = []
        for tile_row in self.slots:
            for i in range(len(tile_row[0].interior)):
                result.append(''.join(tile.interior[i] for tile in tile_row))
        return result


def rotate(tile: OrientedTile) -> OrientedTile:
    """Produces a version of the tile rotated 90 degrees clockwise"""
    size = len(tile.interior)
    rotated_interior = tuple(''.join(tile.interior[y][x] for y in reversed(range(size)))
                             for x in range(size))
    return OrientedTile(
        id=tile.id,
        top=tile.left[::-1],
        right=tile.top,
        bottom=tile.right[::-1],
        left=tile.bottom,
        interior=rotated_interior
    )


def mirror(tile: OrientedTile) -> OrientedTile:
    return OrientedTile(
        id=tile.id,
        top=tile.top[::-1],
        right=tile.left,
        bottom=tile.bottom[::-1],
        left=tile.right,
        interior=tuple(line[::-1] for line in tile.interior)
    )


def orientations(tile: OrientedTile) -> Tile:
    """Produce rotated and mirrored versions of the tile"""
    flipped_tile = mirror(tile)
    versions = []
    new_tile = tile
    for _ in range(4):
        new_tile = rotate(new_tile)
        flipped_tile = rotate(flipped_tile)
        versions.append(new_tile)
        versions.append(flipped_tile)

    return Tile(id=tile.id, orientations=tuple(versions))


def parse_input(file: Path) -> set[Tile]:
    tiles = set()
    with file.open() as f:
        for section in f.read().split('\n\n'):
            lines = section.split('\n')
            id = int(lines[0].removeprefix('Tile ').removesuffix(':'))
            contents = [line.strip() for line in lines[1:] if line]
            top = contents[0]
            bottom = contents[-1]
            left = ''.join(row[0] for row in contents)
            right = ''.join(row[-1] for row in contents)
            interior = tuple(row[1:-1] for row in contents[1:-1])
            tile = OrientedTile(id=id, top=top, right=right, bottom=bottom, left=left, interior=interior)
            tiles.add(orientations(tile))
    return tiles


def solve(board: Board, available_tiles: set[Tile]) -> Optional[Board]:
    """Recursive solver; Given a partially filled board, returns the solved board
    or None if not possible."""
    if not available_tiles:
        return board  # no more tiles left -- success!
    for tile in available_tiles:
        remaining_tiles = available_tiles - {tile}
        for orientation in tile.orientations:
            did_fit = board.place(orientation)
            if did_fit:
                solution = solve(board, remaining_tiles)
                if solution:
                    return solution
                board.remove_last()
    return None  # tried every option, nothing worked


# Part 1
tileset = parse_input(Path("input") / "20.txt")
board = Board(isqrt(len(tileset)))
solution = solve(board, tileset)
print(solution.checksum)


# Part 2
monster_stencil = ["                  # ",
                   "#    ##    ##    ###",
                   " #  #  #  #  #  #   "]


def count_monsters(tile: OrientedTile) -> int:
    number_of_monsters = 0
    monster = ''.join(monster_stencil)
    monster_height = len(monster_stencil)
    monster_width = len(monster_stencil[0])
    size = len(tile.interior)
    for y in range(size - monster_height):
        window_lines = tile.interior[y:y+monster_height]
        for x in range(size - monster_width):
            window = ''.join(line[x:x+monster_width] for line in window_lines)
            if all(x == '#' for x, y in zip(window, monster) if y == "#"):
                number_of_monsters += 1
    return number_of_monsters


full_image = OrientedTile(interior=tuple(solution.image), top="", bottom="", left="", right="", id=0)
full_image_orientations = orientations(full_image)

monster_size = sum(line.count('#') for line in monster_stencil)
number_of_waves = sum(line.count('#') for line in full_image.interior)
for image in full_image_orientations.orientations:
    count = count_monsters(image)
    if count > 0:
        # Assume no overlapping sea monsters
        print(number_of_waves - count * monster_size)
