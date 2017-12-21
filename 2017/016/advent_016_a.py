import typing as T
"""
--- Day 16: Permutation Promenade ---
You come upon a very unusual sight; a group of programs here appear to be dancing.

There are sixteen programs in total, named a through p. They start by standing in a line: a stands in position 0, b stands in position 1, and so on until p, which stands in position 15.

The programs' dance consists of a sequence of dance moves:

Spin, written sX, makes X programs move from the end to the front, but maintain their order otherwise. (For example, s3 on abcde produces cdeab).
Exchange, written xA/B, makes the programs at positions A and B swap places.
Partner, written pA/B, makes the programs named A and B swap places.
For example, with only five programs standing in a line (abcde), they could do the following dance:

s1, a spin of size 1: eabcd.
x3/4, swapping the last two programs: eabdc.
pe/b, swapping programs e and b: baedc.
After finishing their dance, the programs end up in order baedc.

You watch the dance for a while and record their dance moves (your puzzle input). In what order are the programs standing after their dance?

To begin, get your puzzle input.
"""

ListOp = T.Callable[[T.List[str]], T.List[str]]

def spinner(x: int) -> ListOp:
    def spun(a: T.List[str]) -> T.List[str]:
        front, back = a[:-x], a[-x:]
        return back+front
    return spun

def exchanger(i: int, j: int) -> ListOp:
    def exchanged(a: T.List[str]) -> T.List[str]:
        b = a[:]
        b[i], b[j] = b[j], b[i]
        return b
    return exchanged

def swapper(p: str, q: str) -> ListOp:
    def swapped(a: T.List[str]) -> T.List[str]:
        b = a[:]
        i, j = a.index(p), a.index(q)
        b[i], b[j] = b[j], b[i]
        return b
    return swapped

def parse_token(token: str) -> ListOp:
    prefix, rest = token[0], token[1:]
    if prefix == "s":
        n = int(rest)
        return spinner(n)
    elif prefix == "x":
        x, y = rest.split(r'/')
        i, j = int(x), int(y)
        return exchanger(i, j)
    elif prefix == "p":
        p, q = rest.split(r'/')
        return swapper(p, q)
    else:
        raise ValueError(f"unknown prefix {prefix}")

def parse(raw: str) -> T.Iterable[ListOp]:
    return (parse_token(token) for token in raw.split(","))

def parse_file(path: str) -> T.Iterable[ListOp]:
    with open(path) as fp:
        yield from parse(''.join(fp.readlines()))

def solve(a: T.List[str], path: str) -> str:
    for op in parse_file(path):
        a = op(a)
    return ''.join(a)

starting_positions = [chr(x) for x in range(ord('a'), ord('a')+16)]
path = 'advent_016_input.txt'
solution = solve(starting_positions, path)
print(len(solution))
print(solution)