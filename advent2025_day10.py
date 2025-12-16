from collections import defaultdict
from functools import cache
from itertools import combinations
from math import inf
from typing import NamedTuple, Self
from functools import reduce
from operator import xor

from utils import read_data
import time
import re

DESIRED_REGEX = re.compile(r'^\[(?P<desired>[#.]+)]')
BUTTONS_REGEX = re.compile(r'\((?P<button>[0-9,]+)\)')
JOLTAGE_REGEX = re.compile(r'\{(?P<joltages>[0-9,]+)}')


class Machine(NamedTuple):
    raw_desired: tuple[bool, ...]
    raw_buttons: tuple[tuple[bool, ...], ...]
    joltages: tuple[int, ...]

    @classmethod
    def from_line(cls, line: str) -> Self:
        raw_desired = tuple(x == "#" for x in DESIRED_REGEX.search(line).group("desired"))
        raw_buttons = tuple(tuple(int(num) for num in x.split(",")) for x in BUTTONS_REGEX.findall(line))
        raw_buttons = tuple(tuple(num in x for num in range(len(raw_desired))) for x in raw_buttons)
        joltages = tuple(int(x) for x in JOLTAGE_REGEX.search(line).group('joltages').split(","))
        return cls(raw_desired, raw_buttons, joltages)

    @property
    def num_lights(self) -> int:
        return len(self.raw_desired)

    @property
    @cache
    def buttons(self) -> tuple[int, ...]:
        return tuple(int(''.join('1' if x else '0' for x in button), 2) for button in self.raw_buttons)

    @property
    @cache
    def desired(self) -> int:
        return int(f"{''.join('1' if x else '0' for x in self.raw_desired)}", 2)

    @property
    @cache
    def patterns(self):
        patterns: dict[int, list[tuple[int, ...]]] = defaultdict(list)
        for pat_length in range(0, len(self.buttons) + 1):
            for combo in combinations(range(len(self.buttons)), r=pat_length):
                result = reduce(xor, (0,) + tuple(self.buttons[x] for x in combo))
                patterns[result].append(combo)
        return patterns

    @cache
    def buttons_joltage(self, buttons: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(sum(x) for x in zip((0,) * self.num_lights, *(self.raw_buttons[i] for i in buttons)))

    def start(self):
        return min(len(x) for x in self.patterns[self.desired])

    @cache
    def calc_joltage_step(self, target: tuple[int, ...]) -> int | None:
        # If our target is all zeroes, we're done, return 0
        if not any(target):
            return 0
        # The final pattern is equal to the parity of the joltage
        target_pattern = int("".join("1" if x % 2 else "0" for x in target), 2)
        # For each possible combination of buttons to hit the target pattern, calculate the joltage from pushing them
        min_presses = inf
        for combo in self.patterns[target_pattern]:
            buttons_joltage = self.buttons_joltage(combo)
            # If this is a valid combo, subtracting it from target will result in no negative numbers
            after_joltage = [x[0] - x[1] for x in zip(target, buttons_joltage)]
            if any(x < 0 for x in after_joltage):
                continue
            # At this point all the target levels should be even, so we can divide them by half and recurse
            half_joltage_presses = self.calc_joltage_step(tuple(x // 2 for x in after_joltage))
            min_presses = min(min_presses, len(combo) + (2 * half_joltage_presses))
        return min_presses


    def set_joltages(self) -> int:
        return self.calc_joltage_step(self.joltages)

    def __repr__(self) -> str:
        desired = f"{''.join('#' if x else '.' for x in self.raw_desired)}"
        buttons = " ".join(f"({','.join(str(i) for i, v in enumerate(x) if v)})" for x in self.raw_buttons)
        joltages = ",".join(str(x) for x in self.joltages)
        return f"[{desired}] {buttons} {{{joltages}}}"


def my_main():
    machines = [Machine.from_line(x) for x in read_data().splitlines()]
    print(f"Part one: {sum(x.start() for x in machines)}")
    print(f"Part two: {sum(x.set_joltages() for x in machines)}")


if __name__ == "__main__":
    timer_start = time.monotonic()
    my_main()
    print(f"Time: {time.monotonic()-timer_start}")
