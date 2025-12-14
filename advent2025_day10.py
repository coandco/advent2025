from collections import deque
from typing import NamedTuple, Self

from utils import read_data
import time
import re

DESIRED_REGEX = re.compile(r'^\[(?P<desired>[#.]+)]')
BUTTONS_REGEX = re.compile(r'\((?P<button>[0-9,]+)\)')
JOLTAGE_REGEX = re.compile(r'\{(?P<joltages>[0-9,]+)}')


class Machine(NamedTuple):
    num_lights: int
    desired: int
    buttons: tuple[int, ...]
    joltages: tuple[int, ...]

    @classmethod
    def from_line(cls, line: str) -> Self:
        raw_desired = DESIRED_REGEX.search(line).group("desired")
        desired = int(f"{''.join('1' if x == '#' else '0' for x in raw_desired)}", 2)
        num_lights = len(raw_desired)
        raw_buttons = [[int(num) for num in x.split(",")] for x in BUTTONS_REGEX.findall(line)]
        buttons = tuple(sum(1 << (num_lights-x-1) for x in button) for button in raw_buttons)
        joltages = tuple(int(x) for x in JOLTAGE_REGEX.search(line).group('joltages').split(","))
        return cls(num_lights, desired, buttons, joltages)

    def start(self) -> int:
        queue: deque[tuple[int, tuple[int, ...]]] = deque([(0, (i,)) for i in range(len(self.buttons))])
        while queue:
            before_state, presses = queue.popleft()
            after_state = before_state ^ self.buttons[presses[-1]]
            if after_state == self.desired:
                return len(presses)
            queue.extend((after_state, presses + (i,)) for i in range(len(self.buttons)) if not i in presses)
        return -1

    def __repr__(self) -> str:
        desired = f"{self.desired:0{self.num_lights}b}".translate(str.maketrans('10', '#.'))
        buttons = " ".join(f"({x:0{self.num_lights}b})" for x in self.buttons)
        joltages = ",".join(str(x) for x in self.joltages)
        return f"[{desired}] {buttons} {{{joltages}}}"


TEST_DATA = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""


def main():
    machines = [Machine.from_line(x) for x in read_data().splitlines()]
    print(f"Part one: {sum(x.start() for x in machines)}")


if __name__ == "__main__":
    timer_start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-timer_start}")
