#!/usr/bin/env python3
#
#  Advent of Code 2023 - Day 13
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
        #.##..##.
        ..#.##.#.
        ##......#
        ##......#
        ..#.##.#.
        ..##..##.
        #.#.##.#.

        #...##..#
        #....#..#
        ..##..###
        #####.##.
        #####.##.
        ..##..###
        #....#..#
        """,
        405
    ),
]

SAMPLE_CASES2 = [
    (
        """
        #.##..##.
        ..#.##.#.
        ##......#
        ##......#
        ..#.##.#.
        ..##..##.
        #.#.##.#.

        #...##..#
        #....#..#
        ..##..###
        #####.##.
        #####.##.
        ..##..###
        #....#..#
        """,
        400
    ),
]

Lines = Sequence[str]
Sections = Sequence[Lines]

# Utility functions

def load_input(infile: str, strip=True, blank_lines=False) -> Lines:
    return load_text(Path(infile).read_text())

def load_text(text: str, strip=True, blank_lines=True) -> Lines:
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

def is_one_off(row1, row2):
    num_diff = 0
    for char1, char2 in zip(row1, row2):
        if char1 != char2:
            num_diff += 1
    return num_diff == 1

def row_mirror_point(section, smudge_exists):
    for i in range(len(section) - 1):
        curr_row = i
        next_row = i + 1
        if not smudge_exists:
            while section[curr_row] == section[next_row]:
                curr_row -= 1
                next_row += 1
                if curr_row < 0 or next_row >= len(section):
                    return i + 1
        else:
            err_seen   = 0  
            is_equal   = section[curr_row] == section[next_row]
            off_by_one = is_one_off(section[curr_row], section[next_row])
            if off_by_one:
                err_seen += 1
            
            while is_equal or (off_by_one and not err_seen > 1):
                curr_row -= 1
                next_row += 1
                if curr_row < 0 or next_row >= len(section):
                    if err_seen != 1:
                        break
                    else:
                        return i + 1
                is_equal   = section[curr_row] == section[next_row]
                off_by_one = is_one_off(section[curr_row], section[next_row])
                if off_by_one:
                    err_seen += 1
            
    return None

# Solution
def get_mirror_point(section, smudge_exists=False):
    res = 0
    row_point = row_mirror_point(section, smudge_exists)
    if row_point:
        return row_point * 100

    # Invert 2d array 
    section = [list(line) for line in section]
    inverted_section = zip(*section)
    inverted_section = [''.join(line) for line in inverted_section]

    col_point = row_mirror_point(inverted_section, smudge_exists)
    if col_point:
        return col_point
    return -1
    

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    sections = parse_sections(lines)
    vals = [get_mirror_point(section, smudge_exists=True) for section in sections]
    return sum(vals)

def solve(lines: Lines) -> int:
    """Solve the problem."""
    sections = parse_sections(lines)
    vals = [get_mirror_point(section) for section in sections]
    return sum(vals)


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
