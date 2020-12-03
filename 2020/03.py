from pathlib import Path
from math import prod


class Map:
    def __init__(self, input_path: Path) -> None:
        with input_path.open() as f:
            self.map_lines = [line.strip() for line in f.readlines()]
        # Don't bother validating the input
        self.map_width = len(self.map_lines[0])
        self.map_height = len(self.map_lines)

    def is_tree_in_position(self, x: int, y: int) -> bool:
        return self.map_lines[y][x % self.map_width] == '#'

    def count_trees(self, slope_x: int, slope_y: int) -> int:
        x, y = slope_x, slope_y
        number_of_trees = 0
        while y < self.map_height:
            if self.is_tree_in_position(x, y):
                number_of_trees += 1
            x += slope_x
            y += slope_y
        return number_of_trees


# Part 1
area_map = Map(Path("input") / "03.txt")
print(area_map.count_trees(3, 1))

# Part 2
numbers_of_trees = [area_map.count_trees(*slope)
                    for slope in ((1,1), (3, 1), (5, 1), (7, 1), (1, 2))]
print(prod(numbers_of_trees))
