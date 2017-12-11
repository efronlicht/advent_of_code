import typing as T
import operator
import collections
'''--- Day 8: I Heard You Like Registers ---

You receive a signal directly from the CPU. Because of your recent assistance with jump instructions, it would like you to compute the result of a series of unusual register instructions.

Each instruction consists of several parts: the register to modify, whether to increase or decrease that register's value, the amount by which to increase or decrease it, and a condition. If the condition fails, skip the instruction without modifying the register. The registers all start at 0. The instructions look like this:

b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
These instructions would be processed as follows:

Because a starts at 0, it is not greater than 1, and so b is not modified.
a is increased by 1 (to 1) because b is less than 5 (it is 0).
c is decreased by -10 (to 10) because a is now greater than or equal to 1 (it is 1).
c is increased by -20 (to -10) because c is equal to 10.
After this process, the largest value in any register is 1.

You might also encounter <= (less than or equal to) or != (not equal to). However, the CPU doesn't have the bandwidth to tell you what all the registers are named, and leaves that to you to determine.

What is the largest value in any register after completing the instructions in your puzzle input?
'''

BINOP = T.Callable[[int, int], int]
Registers = T.DefaultDict[str, int]
def op(sym: str) -> BINOP:
    lookup = { "<=": operator.le,  
        "<": operator.lt,
        "==": operator.eq, 
        "!=": operator.ne,
        ">": operator.gt,
        ">=": operator.ge,
        "inc": operator.add,
        "dec": operator.sub}
    return lookup[sym]

path = "advent_008_input.txt"


class ThreeOp():
    def __init__(self, register: str, opcode: str, literal: str) -> None:
        self.op = op(opcode)
        self.register = register
        self.right = int(literal)


    def __call__(self, registers: Registers) -> int:
        left = registers[self.register]
        return self.op(left, self.right)
class Instruction():
    def __init__(self, incrementer: ThreeOp, comparer: ThreeOp) -> None:
        self.inc = incrementer
        self.cmp = comparer
    @property
    def reg(self) -> str:
        return self.inc.register
    def __call__(self, registers: Registers) -> bool:
        if self.cmp(registers):
            registers[self.reg] = self.inc(registers)
            return True
        return False

def get_instructions(path: str) ->  T.Iterable[Instruction]:
    with open(path) as fp:
        for line in fp:
            yield parse_instruction(line)


def parse_instruction(raw: str) -> Instruction:
    parts = raw.split()
    if len(parts) != 7:
        raise ValueError("could not parse code")
    return Instruction(ThreeOp(*parts[:3]), ThreeOp(*parts[4:]))
    
def max_register(instructions: T.Iterable[Instruction]) -> int:
    registers: T.DefaultDict[str, int] = collections.defaultdict(int)
    for op in instructions:
        op(registers)
    return max(registers.values())


test_instructions = ['b inc 5 if a > 1',
'a inc 1 if b < 5',
'c dec -10 if a >= 1',
'c inc -20 if c == 10']

if __name__ == '__main__':
    print(max_register(get_instructions(path)))
