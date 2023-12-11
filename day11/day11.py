#!/usr/bin/env python3
#
#  Advent of Code 2023 - Day 11
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
        ...#......
        .......#..
        #.........
        ..........
        ......#...
        .#........
        .........#
        ..........
        .......#..
        #...#.....
        """,
        374
    ),
]

SAMPLE_CASES2 = [
    (
        """
        ...#......
        .......#..
        #.........
        ..........
        ......#...
        .#........
        .........#
        ..........
        .......#..
        #...#.....
        """,
        82000210
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
def parse_galaxy(lines):
    galaxy_coords   = []
    compressed_rows = []
    compressed_cols = []

    for row in range(len(lines)):
        for col in range(len(lines[row])):
            if lines[row][col] == '#':
                galaxy_coords.append((row, col))

    for row in range(len(lines)):
        if not any(char == '#' for char in lines[row]):
            compressed_rows.append(row)

    for col in range(len(lines[0])):
        compressed = True
        for row in range(len(lines)):
            if lines[row][col] == '#':
                compressed = False
        if compressed:
            compressed_cols.append(col)

    return galaxy_coords, compressed_rows, compressed_cols

def get_distance(pt1, pt2, compressed_rows, compressed_cols, expansion):

    r1, c1 = pt1
    r2, c2 = pt2

    dist = abs(c2 - c1) + abs(r2 - r1)

    for row in compressed_rows:
        if min(r1, r2) <= row <= max(r1, r2):
            dist += expansion
    for col in compressed_cols:
        if min(c1, c2) <= col <= max(c1, c2):
            dist += expansion
    return dist

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    galaxy_coords, compressed_rows, compressed_cols = parse_galaxy(lines)
    dist = 0
    count = 0
    for i in range(len(galaxy_coords)):
        for j in range(i + 1, len(galaxy_coords)):
            dist += get_distance(galaxy_coords[i],
                                 galaxy_coords[j],
                                 compressed_rows, 
                                 compressed_cols,
                                 1000000 - 1)
            count += 1
    return dist

def solve(lines: Lines) -> int:
    """Solve the problem."""
    galaxy_coords, compressed_rows, compressed_cols = parse_galaxy(lines)
    dist = 0
    count = 0
    for i in range(len(galaxy_coords)):
        for j in range(i + 1, len(galaxy_coords)):
            dist += get_distance(galaxy_coords[i],
                                 galaxy_coords[j],
                                 compressed_rows, 
                                 compressed_cols, 
                                 2-1)
            count += 1
    return dist


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
