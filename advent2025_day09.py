import time
from itertools import combinations, pairwise
from typing import Iterable, Self

from utils import BaseCoord, read_data


class Coord(BaseCoord):
    @classmethod
    def from_str(cls, raw: str) -> Self:
        x, y = raw.split(",")
        return cls(x=int(x), y=int(y))

    def x_range(self, other: Self) -> range:
        return range(min(self.x, other.x), max(self.x, other.x) + 1)

    def y_range(self, other: Self) -> range:
        return range(min(self.y, other.y), max(self.y, other.y) + 1)

    def area(self, other: Self) -> int:
        # The +1s are because the area includes the points themselves
        dx, dy = abs(self.x - other.x) + 1, abs(self.y - other.y) + 1
        return dx * dy

    def line_intersects(self, other: Self, point1: Self, point2: Self) -> bool:
        is_right = min(point1.x, point2.x) >= max(self.x, other.x)
        is_left = max(point1.x, point2.x) <= min(self.x, other.x)
        is_below = min(point1.y, point2.y) >= max(self.y, other.y)
        is_above = max(point1.y, point2.y) <= min(self.y, other.y)
        if all(x is False for x in (is_right, is_left, is_below, is_above)):
            return True
        return False

    def points_in_area(self, other: Self) -> Iterable[Self]:
        for y in self.y_range(other):
            for x in self.x_range(other):
                yield Coord(x=x, y=y)

    def line_between(self, other: Self) -> Iterable[Self]:
        if self.x == other.x:
            yield from (Coord(x=self.x, y=y) for y in self.y_range(other))
        elif self.y == other.y:
            yield from (Coord(x=x, y=self.y) for x in self.x_range(other))
        else:
            raise Exception("Points not in a straight line!")


def get_lines(points: list[Coord]) -> list[tuple[Coord, Coord]]:
    return sorted(pairwise(points + [points[0]]), key=lambda x: x[0].distance(x[1]), reverse=True)


def check_combo_lines(area_one: Coord, area_two: Coord, lines: list[tuple[Coord, Coord]]) -> bool:
    for line_one, line_two in lines:
        if area_one.line_intersects(area_two, line_one, line_two):
            return False
    return True


def compress_points(points: list[Coord]) -> tuple[dict[int, int], dict[int, int], list[Coord]]:
    x_mapping = {x: i for i, x in enumerate(sorted({point.x for point in points}))}
    y_mapping = {x: i for i, x in enumerate(sorted({point.y for point in points}))}
    new_points = [Coord(x=x_mapping[point.x], y=y_mapping[point.y]) for point in points]
    return {v: k for k, v in x_mapping.items()}, {v: k for k, v in y_mapping.items()}, new_points


def get_green_tiles(points: list[Coord]) -> set[Coord]:
    green_tiles: set[Coord] = set()
    # Set up a sliding window, going through the points by pairs after advancing one of the iterators by one
    for first, second in pairwise(points + [points[0]]):
        green_tiles.update(first.line_between(second))
    # Now that we have the boundary, do a flood fill of the inside
    # First, find a pixel with the leftmost x
    pixel = next(iter(x for x in sorted(points, key=lambda x: x.x)))
    # Then, go right until you see an empty spot.  That spot will be inside.
    while pixel in green_tiles:
        pixel += Coord(x=1, y=0)
    # Now that we have an inner pixel, flood fill
    to_fill = [pixel]
    while to_fill:
        cur = to_fill.pop()
        for neighbor in cur.cardinal_neighbors():
            if neighbor not in green_tiles:
                to_fill.append(neighbor)
                green_tiles.add(neighbor)
    return green_tiles


def check_combo_greentiles(first: Coord, second: Coord, green_tiles: set[Coord]) -> bool:
    return all(x in green_tiles for x in first.points_in_area(second))


def solve_p2_compression(points: list[Coord]) -> int:
    x_map, y_map, compressed_points = compress_points(points)
    biggest_rectangles = sorted(combinations(compressed_points, r=2), key=lambda x: x[0].area(x[1]), reverse=True)
    green_tiles = get_green_tiles(compressed_points)
    first, second = None, None
    for first, second in biggest_rectangles:
        if check_combo_greentiles(first, second, green_tiles):
            break
    # Once we have our max points, we re-expand them so we can get the actual area
    real_first, real_second = Coord(x=x_map[first.x], y=y_map[first.y]), Coord(x=x_map[second.x], y=y_map[second.y])
    return real_first.area(real_second)


def solve_p2_lines(points: list[Coord], biggest_rectangles: list[tuple[Coord, Coord]]) -> int:
    lines = get_lines(points)
    biggest_rectangles = sorted(combinations(points, r=2), key=lambda x: x[0].area(x[1]), reverse=True)
    first, second = None, None
    for first, second in biggest_rectangles:
        if check_combo_lines(first, second, lines):
            break
    return first.area(second)


def main():
    points: list[Coord] = [Coord.from_str(line) for line in read_data().splitlines()]
    biggest_rectangles = sorted(combinations(points, r=2), key=lambda x: x[0].area(x[1]), reverse=True)
    max_area = biggest_rectangles[0][0].area(biggest_rectangles[0][1])
    print(f"Part one: {max_area}")
    print(f"Part two: {solve_p2_lines(points, biggest_rectangles)}")


if __name__ == "__main__":
    timer_start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-timer_start}")
