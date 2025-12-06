import time
from math import prod

from utils import read_data

OPCODES = {"+": sum, "*": prod}


def cephalopod_columns(lines: list[str]) -> list[list[int]]:
    columns, column = [], []
    for raw_column in ("".join(x).strip() for x in zip(*lines)):
        # If we've hit an index that's all blank, that's it for the problem and move onto the next
        if not raw_column:
            columns.append(column)
            column = []
            continue
        column.append(int(raw_column))
    # Make sure we append the last column
    columns.append(column)
    return columns


def main():
    *raw_lines, ops = [x for x in read_data().splitlines()]
    lines = [[int(num) for num in line.split()] for line in raw_lines]
    ops = [op.strip() for op in ops.split()]
    columns = zip(*lines)
    p1_total = sum(OPCODES[ops[i]](x) for i, x in enumerate(columns))
    print(f"Part one: {p1_total}")
    ceph_columns = cephalopod_columns(raw_lines)
    p2_total = sum(OPCODES[ops[i]](x) for i, x in enumerate(ceph_columns))
    print(f"Part two: {p2_total}")


if __name__ == "__main__":
    timer_start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-timer_start}")
