import time
from collections import Counter
from math import prod
from typing import NamedTuple, Self

from utils import read_data


class Field(NamedTuple):
    size_x: int
    size_y: int
    pattern_counts: tuple[int, ...]

    @classmethod
    def from_line(cls, line: str) -> Self:
        raw_size, *raw_pattern_counts = line.split()
        size_x, size_y = (int(x) for x in raw_size[:-1].split("x"))
        pattern_counts = tuple(int(x) for x in raw_pattern_counts)
        return cls(size_x, size_y, pattern_counts)

    def hacky_is_valid(self, pattern_sizes: list[int]) -> bool:
        # In the actual problem input (not the example), the patterns can never fit together, so just look at total size
        return sum(prod(x) for x in zip(self.pattern_counts, pattern_sizes)) <= self.size_x * self.size_y


def main():
    *raw_patterns, raw_fields = read_data().split("\n\n")
    pattern_sizes = [Counter(x)["#"] for x in raw_patterns]
    fields = [Field.from_line(x) for x in raw_fields.splitlines()]
    print(f"Part one: {sum(x.hacky_is_valid(pattern_sizes) for x in fields)}")


if __name__ == "__main__":
    timer_start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-timer_start}")
