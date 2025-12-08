import time
from itertools import combinations
from math import prod, sqrt
from typing import Self

from utils import BaseCoord3D, read_data


class Coord(BaseCoord3D):
    def straight_dist(self, other: Self) -> float:
        dx, dy, dz = self.x - other.x, self.y - other.y, self.z - other.z
        return sqrt(dx**2 + dy**2 + dz**2)

    @classmethod
    def from_raw(cls, raw: str) -> Self:
        x, y, z = (int(x) for x in raw.split(","))
        return cls(x=x, y=y, z=z)


def connect_circuits(points: set[Coord]) -> tuple[int, int]:
    circuits: set[frozenset[Coord]] = set()
    p1_answer = -1
    for i, (first, second) in enumerate(sorted(combinations(points, 2), key=lambda x: x[0].straight_dist(x[1]))):
        if i == 1000:
            p1_answer = prod(len(x) for x in sorted(circuits, key=lambda x: len(x), reverse=True)[:3])
        first_circuit = next(iter(x for x in circuits if first in x), None)
        second_circuit = next(iter(x for x in circuits if second in x), None)
        if not first_circuit and not second_circuit:
            circuits.add(frozenset({first, second}))
        elif first_circuit and not second_circuit:
            circuits.remove(first_circuit)
            circuits.add(first_circuit | {second})
        elif second_circuit and not first_circuit:
            circuits.remove(second_circuit)
            circuits.add(second_circuit | {first})
        elif first_circuit is second_circuit:
            continue
        else:
            circuits.remove(first_circuit)
            circuits.remove(second_circuit)
            circuits.add(first_circuit | second_circuit)
        if len(circuits) == 1 and len(next(iter(circuits))) == len(points):
            return p1_answer, first.x * second.x
    return p1_answer, -1


def main():
    points = {Coord.from_raw(x) for x in read_data().splitlines()}
    p1, p2 = connect_circuits(points)
    print(f"Part one: {p1}")
    print(f"Part two: {p2}")


if __name__ == "__main__":
    timer_start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-timer_start}")
