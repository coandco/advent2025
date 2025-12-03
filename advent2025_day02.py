import time
from math import floor
from typing import Iterable

from utils import read_data


def repeats(startval: int, num_repeats: int) -> Iterable[int]:
    curval = startval
    start_len = len(str(curval))
    while len(str(curval)) == start_len:
        yield int(f"{curval}" * num_repeats)
        curval += 1


def invalids_in_range(span: range) -> Iterable[tuple[int, int]]:
    start_str = str(span.start)
    stop_len = len(str(span.stop - 1))
    seen_repeats = set()
    # This checks all the possible lengths, e.g. it checks 2, 3, and 4 if the range is 10-1000
    for num_digits in range(len(start_str), stop_len + 1):
        # Check longer repeat lengths first to make sure double repeats don't get eaten by seen_repeats
        for repeat_length in reversed(range(1, floor(stop_len / 2) + 1)):
            # We only test lengths that divide evenly into the number of digits, and there has to be at least 2 repeats
            if num_digits % repeat_length != 0 or num_digits // repeat_length < 2:
                continue
            # For the smallest number of digits we can start testing for repeats based on the start of the range
            # If we're at a larger number of digits, we start where it rolls over, e.g. 10000 for a 5-length number
            test_start = int(start_str[:repeat_length]) if num_digits == len(start_str) else pow(10, repeat_length - 1)
            for to_test in repeats(test_start, num_digits // repeat_length):
                if to_test < span.start or to_test in seen_repeats:
                    continue
                if to_test >= span.stop:
                    break
                seen_repeats.add(to_test)
                yield to_test, num_digits // repeat_length


def double_repeats(spans: list[range]) -> Iterable[int]:
    for span in spans:
        yield from (x[0] for x in invalids_in_range(span) if x[1] == 2)


def all_repeats(spans: list[range]) -> Iterable[int]:
    for span in spans:
        yield from (x[0] for x in invalids_in_range(span))


def main():
    range_strs = [x.split("-") for x in read_data().split(",")]
    ranges = [range(int(x[0]), int(x[1]) + 1) for x in range_strs]
    print(f"Part one: {sum(double_repeats(ranges))}")
    print(f"Part two: {sum(all_repeats(ranges))}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
