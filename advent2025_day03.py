from utils import read_data
import time


def leftmost_largest(digits: list[int]) -> tuple[int, int]:
    max_digit = min_pos = -1
    for i, digit in enumerate(digits):
        if digit > max_digit:
            min_pos, max_digit = i, int(digit)
        if max_digit == 9:
            break
    return min_pos, max_digit


def largest_joltage(bank: list[int], num_batteries: int = 2) -> int:
    final_digits = []
    pos = 0
    for i in range(1, num_batteries + 1):
        # Start at the previous position and leave room for the rest of the batteries
        newpos, digit = leftmost_largest(bank[pos : len(bank) - (num_batteries - i)])
        final_digits.append(digit)
        # Advance our position past the newly-found leftmost largest digit
        pos = pos + newpos + 1
    # Cheeky/lazy way to assemble/stitch the digits together
    return int("".join(str(x) for x in final_digits))


def main():
    banks = [[int(x) for x in line] for line in read_data().splitlines()]
    print(f"Part one: {sum(largest_joltage(x, num_batteries=2) for x in banks)}")
    print(f"Part two: {sum(largest_joltage(x, num_batteries=12) for x in banks)}")


if __name__ == "__main__":
    timer_start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-timer_start}")
