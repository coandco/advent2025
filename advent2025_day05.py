import time

from utils import read_data


def merge_ranges(ranges: list[range]) -> list[range]:
    merged_ranges = [ranges[0]]
    for fresh in ranges[1:]:
        if merged_ranges[-1].stop >= fresh.start:
            merged_ranges[-1] = range(merged_ranges[-1].start, max(fresh.stop, merged_ranges[-1].stop))
        else:
            merged_ranges.append(fresh)
    return merged_ranges


def main():
    raw_ranges, raw_ingredients = read_data().split("\n\n")
    fresh_ranges = [range(int(x.split("-")[0]), int(x.split("-")[1]) + 1) for x in raw_ranges.splitlines()]
    fresh_ranges = sorted(fresh_ranges, key=lambda x: x.start)
    merged_ranges = merge_ranges(fresh_ranges)
    ingredients = [int(x) for x in raw_ingredients.splitlines()]
    fresh_ingredients = [x for x in ingredients if any(x in merged_range for merged_range in merged_ranges)]
    print(f"Part one: {len(fresh_ingredients)}")
    print(f"Part two: {sum(len(x) for x in merged_ranges)}")


if __name__ == "__main__":
    timer_start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-timer_start}")
