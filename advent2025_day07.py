from collections import defaultdict

from utils import read_data
from utils import BaseCoord as Coord
import time


def read_grid(raw_grid: str) -> tuple[int, list[set[int]]]:
    first_line, *other_lines = raw_grid.splitlines()
    start_x = first_line.index("S")
    layers = [{i for i, x in enumerate(line) if x == "^"} for line in other_lines]
    # Filter out empty layers
    return start_x, [x for x in layers if x]

def propagate_layers(start_x: int, layers: list[set[int]]) -> int:
    active_columns = {start_x}
    total_splits = 0
    for layer in layers:
        splitters_hit = layer & active_columns
        total_splits += len(splitters_hit)
        active_columns -= splitters_hit
        active_columns |= set.union(*[{x-1, x+1} for x in splitters_hit])
    return total_splits

def quantum_layers(start_x: int, layers: list[set[int]]) -> int:
    timelines = defaultdict(int, {start_x: 1})
    for layer in layers:
        splitters_hit = layer & set(timelines.keys())
        for splitter in splitters_hit:
            magnitude_at_splitter = timelines.pop(splitter)
            timelines[splitter-1] += magnitude_at_splitter
            timelines[splitter+1] += magnitude_at_splitter
    return sum(timelines.values())


def main():
    start_x, layers = read_grid(read_data())
    print(f"Part one: {propagate_layers(start_x, layers)}")
    print(f"Part two: {quantum_layers(start_x, layers)}")


if __name__ == "__main__":
    timer_start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-timer_start}")
