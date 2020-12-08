from pathlib import Path
from copy import deepcopy


def parse_input(input_path: Path) -> list[tuple[str, int]]:
    program = []
    with input_path.open() as f:
        for line in f:
            opcode, argument = line.strip().split()
            program.append((opcode, int(argument)))
    return program


def execute_program(program: list[tuple[str, int]]) -> tuple[int, bool]:
    visited_lines = set()
    line_number = 0
    accumulator = 0

    while line_number not in visited_lines:
        if line_number == len(program):
            return accumulator, True  # proper termination
        visited_lines.add(line_number)
        opcode, argument = program[line_number]
        if opcode == 'acc':
            accumulator += argument
        elif opcode == 'jmp':
            line_number += argument
            continue
        elif opcode == 'nop':
            pass
        line_number += 1

    return accumulator, False  # found an infinite loop


# Part 1
program = parse_input(Path("input") / "08.txt")
accumulator, _ = execute_program(program)
print(accumulator)

# Part 2
for line_number, instruction in enumerate(program):
    opcode, argument = instruction
    if opcode not in ['nop', 'jmp']:
        continue
    modified_program = deepcopy(program)
    modified_program[line_number] = ({'nop': 'jmp', 'jmp': 'nop'}[opcode], argument)
    accumulator, was_terminated = execute_program(modified_program)
    if was_terminated:
        print(accumulator)
