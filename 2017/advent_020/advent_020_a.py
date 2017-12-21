from typing import *
import numpy as np
import re
from functools import total_ordering
from collections import namedtuple


@total_ordering
class Particle:
    def __init__(self, p, v, a):
        self.p, self.v, self.a = p, v, a
    def __lt__(self, other):
        def d(x):
            return np.sum(np.abs(x)**2)
        if not isinstance(other, Particle):
            return NotImplemented
        return (d(self.a), d(self.v), d(self.p)) < (d(other.a), d(other.v), d(other.p))
    def __eq__(self, other):
        return (self.p, self.v, self.a) == (other.p, other.v, other.a)

    def __repr__(self):
        return f'Particle(p={self.p},v={self.v},a={self.a})'
    

def parse_group(group: str) -> np.ndarray:
    group = group.strip(',')
    x, y, z, *_ = ''.join(c for c in group if c not in '<>pva= ').split(',')
    print(x, y, z)
    out = np.zeros([3], dtype=int)
    out[0], out[1], out[2] = int(x), int(y), int(z)
    return out

def parse_line(line: str) -> Particle:
    p, v, a = (parse_group(group) for group in line.split())
    return Particle(p, v, a)


def parse(path: str) -> Iterable[Particle]:
    with open(path) as fp:
        for line in fp:
            yield parse_line(line)
particles = list(parse("input.txt"))

def step(p: Particle) -> Particle:
    v = p.v+p.a
    p = p.p+v
    return Particle(p, v, p.a)

def solve(particles: List[Particle]):
    i, closest_so_far = 0, particles[0]
    
    for j, y in enumerate(particles, 0):
         if y < closest_so_far:
             print(y.a)
             i, closest_so_far = j, y
    return i, closest_so_far

if __name__ == '__main__':
    particles = list(parse("input.txt"))
    i, closest = solve(particles)
    print(i, closest)