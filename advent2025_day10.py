from collections import deque
from typing import NamedTuple, Self

from utils import read_data
import time
import re

DESIRED_REGEX = re.compile(r'^\[(?P<desired>[#.]+)]')
BUTTONS_REGEX = re.compile(r'\((?P<button>[0-9,]+)\)')
JOLTAGE_REGEX = re.compile(r'\{(?P<joltages>[0-9,]+)}')


class Machine(NamedTuple):
    desired: tuple[bool, ...]
    buttons: tuple[tuple[int, ...], ...]
    joltages: tuple[int, ...]

    @classmethod
    def from_line(cls, line: str) -> Self:
        desired = tuple(x == "#" for x in DESIRED_REGEX.search(line).group("desired"))
        buttons = tuple(tuple(int(num) for num in x.split(",")) for x in BUTTONS_REGEX.findall(line))
        joltages = tuple(int(x) for x in JOLTAGE_REGEX.search(line).group('joltages').split(","))
        return cls(desired, buttons, joltages)

    def push_button(self, num: int, cur_state: tuple[bool, ...]) -> tuple[bool, ...]:
        if num >= len(self.buttons):
            raise Exception(f"Unknown button {num}.  This machine has {len(self.buttons)} buttons (zero-indexed).")
        return tuple(not x if i in self.buttons[num] else x for i, x in enumerate(cur_state))

    def __repr__(self) -> str:
        desired = ''.join("#" if x else "." for x in self.desired)
        buttons = " ".join(f"({','.join(str(num) for num in x)})" for x in self.buttons)
        joltages = ",".join(str(x) for x in self.joltages)
        return f"[{desired}] {buttons} {{{joltages}}}"

def start_machine(machine: Machine) -> int:
    queue = deque([((False,) * len(machine.desired), (i,)) for i in range(len(machine.buttons))])
    while queue:
        before_state, presses = queue.popleft()
        after_state = machine.push_button(presses[-1], before_state)
        if after_state == machine.desired:
            return len(presses)
        queue.extend((after_state, presses + (i,)) for i in range(len(machine.buttons)) if not i in presses)
    return -1

TEST_DATA = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""


def main():
    machines = [Machine.from_line(x) for x in read_data().splitlines()]
    print(f"Part one: {sum(start_machine(x) for x in machines)}")


if __name__ == "__main__":
    timer_start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-timer_start}")
