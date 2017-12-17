"""
--- Day 3: Spiral Memory ---

You come across an experimental new kind of memory stored on an infinite two-dimensional grid.

Each square on the grid is allocated in a spiral pattern starting at a location marked 1 and then counting up while spiraling outward. For example, the first few squares are allocated like this:

17  16  15  14  13
18   5   4   3  12
19   6   1   2  11
20   7   8   9  10
21  22  23---> ...
While this is very space-efficient (no squares are skipped), requested data must be carried back to square 1 (the location of the only access port for this memory system) by programs that can only move up, down, left, or right. They always take the shortest path: the Manhattan Distance between the location of the data and square 1.

For example:

Data from square 1 is carried 0 steps, since it's at the access port.
Data from square 12 is carried 3 steps, such as: down, left, left.
Data from square 23 is carried only 2 steps: up twice.
Data from square 1024 must be carried 31 steps.
How many steps are required to carry the data from the square identified in your puzzle input all the way to the access port?

Your puzzle input is 265149.
"""

input = 265149

def spiral(n: int) -> int:
    i = 0
    while ((i*2)+1**2) < n:
        i += 1
    return i


def offset(n: int) -> int:

    """which position on the the outer edge of the spiral is it?
    eg, "two" is offset 1, since it's the first element in the second spiral
              n            offset
            5 4 3         4 3 2
            6 1 (2)       5 _ 1
            7 8 9         6 7 8
    """
    if n == 1:
        return 0
    inside = (spiral(n)-1)**2
    return (n-inside)


def squares(spiral: int) -> int:
    return (2*spiral +1)**2
def inside(spiral: int) -> int:
    return squares(spiral-1)

def outside(n: int) -> int:
    return  squares(n)-inside(n)

def sidelen(n: int) -> int:
    return outside(n)//4
def steps(n: int) -> int:
    if n == 1:
        return 0
    return spiral(n) + offset(n)%(sidelen(n)//2)

assert steps(1) == 0
assert steps(2) == steps(4)
