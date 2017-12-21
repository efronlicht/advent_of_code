import enum
from typing import *
import string

Direction = Tuple[int, int]
Position = Tuple[int, int]

Move = Tuple[Position, Direction]

NORTH: Direction = (-1, 0)
SOUTH: Direction = (1, 0)
EAST: Direction = (0, 1)
WEST: Direction = (0, -1)


NS = frozenset(Direction.NORTH, Direction.SOUTH)
EW = frozenset(Direction.EAST, Direction.WEST)
ANY = frozenset(Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST)

tokens = {c: ANY for c in chain(string.ascii_uppercase, '+')}
tokens.update({'-': EW, '|': NS})

seen: Set[Move] = set()

def next_move(p: Position, heading: Direction) -> Position:
    t = tokens[p]

    if heading in t and heading not in crossroads[p]:
        seen[t]
        return p + heading
    else:
        if heading in crossroads[p]:
            cross


def parse(raw: str) -> Path
