#!/usr/bin/env python3
#
#  Advent of Code 2023 - Day 8
#
from typing import Sequence, Union, Optional, Any, Dict, List, Tuple
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
import math
import re

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
        LLR

        AAA = (BBB, BBB)
        BBB = (AAA, ZZZ)
        ZZZ = (ZZZ, ZZZ)
        """,
        6
    ),
    (
        """
        RL

        AAA = (BBB, CCC)
        BBB = (DDD, EEE)
        CCC = (ZZZ, GGG)
        DDD = (DDD, DDD)
        EEE = (EEE, EEE)
        GGG = (GGG, GGG)
        ZZZ = (ZZZ, ZZZ)
        """,
        2
    )
]

SAMPLE_CASES2 = [
    (
        """
        LR

        11A = (11B, XXX)
        11B = (XXX, 11Z)
        11Z = (11B, XXX)
        22A = (22B, XXX)
        22B = (22C, 22C)
        22C = (22Z, 22Z)
        22Z = (22B, 22B)
        XXX = (XXX, XXX)
        """,
        6
    )
]


Lines = Sequence[str]
Sections = Sequence[Lines]

# Utility functions

def load_input(infile: str, strip=True, blank_lines=False) -> Lines:
    return load_text(Path(infile).read_text())

def load_text(text: str, strip=True, blank_lines=False) -> Lines:
    if strip:
        lines = [line.strip() for line in text.strip("\n").split("\n")]
    else:
        lines = [line for line in text.strip("\n").split("\n")]
    if blank_lines:
        return lines
    return [line for line in lines if line.strip()]

def parse_sections(lines: Lines) -> Sections:
    result = []
    sect = []
    for line in lines:
        if not line.strip():
            if sect:
                result.append(sect)
            sect = []
        else:
            sect.append(line)
    if sect:
        result.append(sect)
    return result


# Solution
def parse_lines(lines):
    camel_map = {}
    for line in lines:
        line = line.split(" = ")
        key = line[0]
        
        left_right = line[1].split(", ")
        left = left_right[0].strip('(')
        right = left_right[1].strip(')')
        
        camel_map[key] = (left, right)
    return camel_map

def get_next_pos(camel_map, curr_pos, instruction):
    if instruction == 'L':
        return camel_map[curr_pos][0]
    else:
        return camel_map[curr_pos][1]



def solve2(lines: Lines) -> int:
    """Solve the problem."""
    instructions = lines[0]
    camel_map = parse_lines(lines[1:])
    starting_positions = [position for position in camel_map.keys() if position.endswith('A')]
    steps_to_end = []
    for curr_pos in starting_positions:
        i = 0
        while True:
            curr_instr = instructions[i % len(instructions)]
            curr_pos   = get_next_pos(camel_map, curr_pos, curr_instr)
        
            if curr_pos.endswith('Z'):
                steps_to_end.append(i + 1)
                break

            i += 1

    acc = 1
    [acc := math.lcm(acc, x) for x in steps_to_end]
    """
    lcm = 1
    for i in steps_to_end:
            lcm = lcm*i // math.gcd(lcm, i)
    """
    return acc


def solve(lines: Lines) -> int:
    """Solve the problem."""
    instructions = lines[0]
    camel_map = parse_lines(lines[1:])
    i = 0
    curr_pos = 'AAA'
    while True:
        curr_instr = instructions[i % len(instructions)]
        curr_pos   = get_next_pos(camel_map, curr_pos, curr_instr)
        
        if curr_pos == 'ZZZ':
            return i + 1
        
        i += 1
    
    return 0


# PART 1

def example1() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    for text, expected in SAMPLE_CASES:
        lines = load_text(text)
        result = solve(lines)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    result = solve(lines)
    print(f"result is {result}")
    print("= " * 32)


# PART 2

def example2() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 2:")
    for text, expected in SAMPLE_CASES2:
        lines = load_text(text)
        result = solve2(lines)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part2(lines: Lines) -> None:
    print("PART 2:")
    result = solve2(lines)
    print(f"result is {result}")
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
