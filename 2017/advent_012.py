import typing as T
import collections
import itertools
import bisect
import copy
"""
--- Day 12: Digital Plumber ---

Walking along the memory banks of the stream, you find a small village that is experiencing a little confusion: some programs can't communicate with each other.

Programs in this village communicate using a fixed system of pipes. Messages are passed between programs using these pipes, but most programs aren't connected to each other directly. Instead, programs pass messages between each other until the message reaches the intended recipient.

For some reason, though, some of these messages aren't ever reaching their intended recipient, and the programs suspect that some pipes are missing. They would like you to investigate.

You walk through the village and record the ID of each program and the IDs with which it can communicate directly (your puzzle input). Each program has one or more programs with which it can communicate, and these pipes are bidirectional; if 8 says it can communicate with 11, then 11 will say it can communicate with 8.

You need to figure out how many programs are in the group that contains program ID 0.

For example, suppose you go door-to-door like a travelling salesman and record the following list:

0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5
In this example, the following programs are in the group that contains program ID 0:

Program 0 by definition.
Program 2, directly connected to program 0.
Program 3 via program 2.
Program 4 via program 2.
Program 5 via programs 6, then 4, then 2.
Program 6 via programs 4, then 2.
Therefore, a total of 6 programs are in this group; all but program 1, which has a pipe that connects it to itself.

How many programs are in the group that contains program ID 0?
"""

path = "advent_012_input.txt"

def parse_line(line: str) -> T.Iterator[int]:
    
    lhs, rhs = line.split("<->")
    yield int(lhs.strip())

    yield from (int(x.strip()) for x in rhs.split(","))

def parse_input(path: str) -> T.Iterator[T.Iterator[int]]:
    with open(path) as fp:
        yield from(parse_line(line) for line in fp)

def initial_groups(input: T.Iterator[T.Iterator[int]]) -> T.Dict[int, T.Set[int]]:
    groups: T.Dict[int, T.Set[int]] = {}
    for n, *connections in input:
        groups[n] = {n} | set(connections)
    return groups


def merge(groups: T.Dict[int, T.Set[int]]) -> T.Dict[int, T.Set[int]]:
    groups = copy.deepcopy(groups) 
    # functional programming!
    # we mutate inside this function for performance reasons,
    # but we want to preserve a functional approach.
    
    def _merge(n: int, m: int):
        groups[min(n, m)] = groups[n] | groups[m]
        groups.pop(max(n, m))


    def next_merge() -> bool:
        some_merge = True
        for n, group in groups.items():
            for m in sorted(group):
                if m in groups and m != n:
                    _merge(n, m)
                    return True
        
        return False
    
    while next_merge():
        pass

    return groups

def solve(path: str) -> int:
    groups = initial_groups(parse_input(path))
    merged = merge(groups)
    return len(merged[0])

test_input = """0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""

if __name__ == '__main__':
    # test example:
    want = {0: {0, 2, 3, 4, 5, 6}, 1: {1}}
    got = merge(initial_groups(parse_line(line) for line in test_input.split("\n")))
    assert want == got

    print(solve(path))