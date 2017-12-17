import typing as T
import time
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

--- Part Two ---
Now that you're starting to get a feel for the dance moves, you turn your attention to the dance as a whole.

Keeping the positions they ended up in from their previous dance, the programs perform it again and again: including the first dance, a total of one billion (1000000000) times.

In the example above, their second dance would begin with the order baedc, and use the same dance moves:

s1, a spin of size 1: cbaed.
x3/4, swapping the last two programs: cbade.
pe/b, swapping programs e and b: ceadb.
In what order are the programs standing after their billion dances?

"""

ListOp = T.Callable[[T.List[int]], T.List[int]]
Perm = T.List[int]
def spinner(x: int) -> ListOp:
    def spun(a: T.List[int]) -> T.List[int]:
        front, back = a[:-x], a[-x:]
        return back+front
    return spun

def exchanger(i: int, j: int) -> ListOp:
    def exchanged(a: T.List[int]) -> T.List[int]:
        b = a[:]
        b[i], b[j] = b[j], b[i]
        return b
    return exchanged

def swapper(p: str, q: str) -> ListOp:
    def swapped(a: T.List[int]) -> T.List[int]:
        b = a[:]
        i = a.index(ord(p) - ord('a'))
        j = a.index(ord(q) - ord('a'))
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

def permute(a: Perm, b: Perm) -> Perm:
    permuted = a[:]
    for i, n in enumerate(b):
        permuted[i] = a[n]
    return permuted

def find_permutation(a: Perm, ops: T.Iterable[ListOp]) -> Perm:
    original = a[:]
    a = a[:]
    for op in ops:
        a = op(a)
    return [original.index(c) for c in a]


def nth_permutation(a: Perm, table: T.Dict[int, Perm], n: int) -> Perm:
    assert table[2] == permute(permute(a, table[1]), permute(a, table[1]))
    for k, perm in sorted(table.items(), reverse=True):
        while k <= n:
            n -= k
            a = permute(a, perm)
            print(n)
        if n == 0:
            return a
    return a

def find_initial_permutation(path: str) -> Perm:
    ops = list(parse_file(path))
    a = list(range(16))
    perm = find_permutation(a, ops)
    return perm

def build_permutation_table(perm: Perm, n: int) -> T.Dict[int, Perm]:
    perms: T.Dict[int, T.List[int]] = {}
    k = 1
    while k < n:
        perms[k] = perm
        perm = permute(perm, perm)
        k <<= 1
    return perms

def to_str(a: T.List[int]) -> str:
    return ''.join(chr(n+ord('a')) for n in a)


def solve(path: str, n: int) -> str:
    perm = find_initial_permutation(path)
    perms = build_permutation_table(perm, n)
    print(perms)
    return to_str(nth_permutation(list(range(16)), perms, n))


path = 'advent_016_input.txt'
solution = solve(path, n=1_000_000_000)
print(solution)