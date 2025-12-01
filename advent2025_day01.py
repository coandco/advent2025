import time

from utils import read_data


def part_one(ops: list[int]) -> int:
    num_zeroes = 0
    cur_val = 50
    for op in ops:
        cur_val += op
        cur_val %= 100
        if cur_val == 0:
            num_zeroes += 1
    return num_zeroes


def part_two(ops: list[int]) -> int:
    num_zeroes = 0
    cur_val = 50
    for op in ops:
        # make an array of all the numbers the op covers, filter it down to just the zeroes, and count it
        zeroes_in_op = sum(1 for x in range(cur_val, cur_val + op, op // abs(op)) if x % 100 == 0)
        num_zeroes += zeroes_in_op
        cur_val += op
        cur_val %= 100
    return num_zeroes


def main():
    # Change L/R to -/+ before converting each line to an int so I don't have to do special processing
    ops = [int(x.translate(str.maketrans("LR", "-+"))) for x in read_data().splitlines()]
    print(f"Part one: {part_one(ops)}")
    print(f"Part two: {part_two(ops)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
