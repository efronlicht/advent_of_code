from typing import *
import numpy as np
import re
from functools import total_ordering
import collections
"""
--- Part Two ---
To simplify the problem further, the GPU would like to remove any particles that collide. Particles collide if their positions ever exactly match. Because particles are updated simultaneously, more than two particles can collide at the same time and place. Once particles collide, they are removed and cannot collide with anything else after that tick.

For example:

p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>    
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>    (0)   (1)   (2)            (3)
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>

p=<-3,0,0>, v=< 3,0,0>, a=< 0,0,0>    
p=<-2,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
p=<-1,0,0>, v=< 1,0,0>, a=< 0,0,0>             (0)(1)(2)      (3)   
p=< 2,0,0>, v=<-1,0,0>, a=< 0,0,0>

p=< 0,0,0>, v=< 3,0,0>, a=< 0,0,0>    
p=< 0,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
p=< 0,0,0>, v=< 1,0,0>, a=< 0,0,0>                       X (3)      
p=< 1,0,0>, v=<-1,0,0>, a=< 0,0,0>

------destroyed by collision------    
------destroyed by collision------    -6 -5 -4 -3 -2 -1  0  1  2  3
------destroyed by collision------                      (3)         
p=< 0,0,0>, v=<-1,0,0>, a=< 0,0,0>
In this example, particles 0, 1, and 2 are simultaneously destroyed at the time and place marked X. On the next tick, particle 3 passes through unharmed.

How many particles are left after all collisions are resolved?
"""

@total_ordering
class Particle:
    def __init__(self, pos, vel, acc):
        self.pos, self.vel, self.acc = pos, vel, acc
    def __lt__(self, other):
        def d(x):
            return np.sum(np.abs(x)**2)
        if not isinstance(other, Particle):
            return NotImplemented
        return (d(self.acc), d(self.vel), d(self.pos)) < (d(other.acc), d(other.vel), d(other.pos))
    def __eq__(self, other):
        return (self.pos, self.vel, self.acc) == (other.pos, other.vel, other.acc)

    def __repr__(self):
        return f'''Particle(
        pos={self.pos},
        vel={self.vel},
        acc={self.acc})'''

    def step(self):
        v = self.vel + self.acc
        p = self.pos + v
        return Particle(pos=p, vel=v, acc=self.acc)


def parse_group(group: str) -> np.ndarray:
    group = group.strip(',')
    x, y, z = ''.join(c for c in group if c not in '<>pva= ').split(',')
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


def non_collided(particles: Iterable[Particle], i: int) -> Iterable[Particle]:
    def pos(x):
        return x.pos[0], x.pos[1], x.pos[2]
    positions: DefaultDict[np.ndarray, List[Particle]] = collections.defaultdict(list)

    for p in particles:
        positions[pos(p)].append(p)
    for pos, p_at_pos in positions.items():
        if len(p_at_pos) == 1:
            yield from p_at_pos
    


def step(particles: Iterable[Particle], i: int) -> Iterable[Particle]:
    stepped = (p.step() for p in particles)
    return list(non_collided(stepped, i))
def solve(particles: Iterable[Particle]) -> int:
    for i in range(1000):
        particles = step(particles, i=i)
        if i %  100 == 0:
            particles = iter(list(particles)) 
    return len(list(particles))

if __name__ == '__main__':
    particles = parse("input.txt")
    print(solve(particles))



