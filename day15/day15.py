#!/usr/bin/env python3
#
#  Advent of Code 2023 - Day 15
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
        rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
        """,
        1320
    ),
]

SAMPLE_CASES2 = [
    (
        """
        rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
        """,
        145
    ),
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
    new_line = []
    for line in lines:
        line = line.split(',')
        new_line.append(line)
    return new_line

def hash_string(string):
    val = 0
    for char in string:
        val += ord(char)
        val *= 17
        val = val % 256
    return val

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    strings = parse_lines(lines)[0]
    hash_map = [[] for _ in range(256)]
    for string in strings:
        if '-' in string:
            key = string.strip('-')
            hashed_key = hash_string(key)
            lenses = hash_map[hashed_key]
            hash_map[hashed_key] = [(lens, focal) for lens,focal in lenses if lens != key]
        
        if "=" in string:
            key = string.split('=')[0]
            new_focal = string.split('=')[1]
            hashed_key = hash_string(key)
            lenses = hash_map[hashed_key]

            lens_found = False
            new_lenses = []
            for lens,focal in lenses:
                if lens == key:
                    new_lenses.append((lens,new_focal))
                    lens_found = True
                else:
                    new_lenses.append((lens,focal))
            
            if not lens_found:
                new_lenses.append((key,new_focal))
            
            hash_map[hashed_key] = new_lenses
    
    total_power = 0
    for i in range(len(hash_map)):
        for j in range(len(hash_map[i])):
            total_power += (i+1) * (j+1) * int(hash_map[i][j][1])

    return total_power

def solve(lines: Lines) -> int:
    """Solve the problem."""
    strings = parse_lines(lines)[0]
    string_vals = [hash_string(string) for string in strings]
    return sum(string_vals)


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
