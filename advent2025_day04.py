import time
from typing import Iterable

from utils import BaseCoord as Coord
from utils import read_data


def calc_neighbors(grid: dict[Coord, int]):
    for coord in grid:
        grid[coord] = sum(x in grid for x in coord.neighbors())


def recalc_neighbors(grid: dict[Coord, int], removed: Iterable[Coord]):
    for pos in removed:
        for neighbor in pos.neighbors():
            if neighbor in grid:
                grid[neighbor] = max(grid[neighbor] - 1, 0)


def read_grid(raw_grid: str) -> dict[Coord, int]:
    grid = {}
    for y, line in enumerate(raw_grid.splitlines()):
        for x, char in enumerate(line):
            if char == "@":
                grid[Coord(x=x, y=y)] = 0
    calc_neighbors(grid)
    return grid


def main():
    grid = read_grid(read_data())
    can_remove = [k for k, v in grid.items() if v < 4]
    print(f"Part one: {len(can_remove)}")
    total_removed = 0
    while can_remove:
        total_removed += len(can_remove)
        [grid.pop(x) for x in can_remove]
        recalc_neighbors(grid, can_remove)
        can_remove = [k for k, v in grid.items() if v < 4]
    print(f"Part two: {total_removed}")


if __name__ == "__main__":
    timer_start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-timer_start}")
