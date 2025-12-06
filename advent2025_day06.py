import time
from itertools import groupby
from math import prod

from utils import read_data


def main():
    *raw_lines, ops = read_data().splitlines()
    raw_columns = zip(*raw_lines)
    grouped_columns = [list(g) for k, g in groupby(raw_columns, key=lambda x: any(c != " " for c in x)) if k]
    grouped_row_ints = [[int("".join(row)) for row in zip(*x)] for x in grouped_columns]
    ops = [op.strip() for op in ops.split()]
    opcodes = {"+": sum, "*": prod}
    p1_total = sum(opcodes[ops[i]](x) for i, x in enumerate(grouped_row_ints))
    print(f"Part one: {p1_total}")
    grouped_col_ints = [[int("".join(column)) for column in x] for x in grouped_columns]
    p2_total = sum(opcodes[ops[i]](x) for i, x in enumerate(grouped_col_ints))
    print(f"Part two: {p2_total}")


if __name__ == "__main__":
    timer_start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-timer_start}")
