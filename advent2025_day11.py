import time
from collections import defaultdict
from functools import cache

from utils import read_data


def build_connections(raw_input: str) -> dict[str, set[str]]:
    connections: dict[str, set[str]] = defaultdict(set)
    for line in raw_input.splitlines():
        name, *outputs = (x.replace(":", "") for x in line.split())
        connections[name] = set(outputs)
    return connections


def find_paths(nodes: dict[str, set[str]], path_start: str, path_end: str, must_include: set[str]) -> int:
    @cache
    def _find_paths(start: str, end: str, required_seen: frozenset[str]) -> int:
        if start == end and required_seen == must_include:
            return 1
        if start in must_include:
            required_seen |= {start}
        return sum(_find_paths(x, end, required_seen) for x in nodes[start])
    return _find_paths(path_start, path_end, frozenset())


def main():
    connections = build_connections(read_data())
    print(f"Part one: {find_paths(connections, "you", "out", must_include=set())}")
    print(f"Part two: {find_paths(connections, "svr", "out", must_include={"dac", "fft"})}")


if __name__ == "__main__":
    timer_start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-timer_start}")
