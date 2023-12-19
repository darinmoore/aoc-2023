#!/usr/bin/env python3
#
#  Advent of Code 2023 - Day 18
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
        R 6 (#70c710)
        D 5 (#0dc571)
        L 2 (#5713f0)
        D 2 (#d2c081)
        R 2 (#59c680)
        D 2 (#411b91)
        L 5 (#8ceee2)
        U 2 (#caa173)
        L 1 (#1b58a2)
        U 2 (#caa171)
        R 2 (#7807d2)
        U 3 (#a77fa3)
        L 2 (#015232)
        U 2 (#7a21e3)
        """,
        62
    ),
]

SAMPLE_CASES2 = [
    (
        """
        R 6 (#70c710)
        D 5 (#0dc571)
        L 2 (#5713f0)
        D 2 (#d2c081)
        R 2 (#59c680)
        D 2 (#411b91)
        L 5 (#8ceee2)
        U 2 (#caa173)
        L 1 (#1b58a2)
        U 2 (#caa171)
        R 2 (#7807d2)
        U 3 (#a77fa3)
        L 2 (#015232)
        U 2 (#7a21e3)
        """,
        952408144115
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
DIR_MAP = {'U' : (-1,0),
           'D' : (1,0),
           'L' : (0, -1),
           'R' : (0, 1),
           0 : (0,1),
           1 : (1,0),
           2 : (0, -1),
           3 : (-1,0)}


def parse_lines(lines):
    lines = [line.split() for line in lines]
    lines = [(direction, int(steps), rgb) for direction,steps,rgb in lines]
    return lines

def parse_lines2(lines):
    lines = [line.split() for line in lines]
    lines = [(int(rgb[7]), int(rgb[2:7], 16), 0) for _,_,rgb in lines]
    return lines

def shoelace(vertices, perimeter):
    # https://en.wikipedia.org/wiki/Shoelace_formula
    # NOTE: Might have been able to do this with the pipe problem
    a1 = 0
    a2 = 0
    for i in (range(len(vertices) - 1)):
        a1 += vertices[i][0] * vertices[i + 1][1]
        a2 += vertices[i][1] * vertices[i + 1][0]
    a = abs(a2 - a1) 
    a += perimeter
    return ((a // 2) + 1)

def get_vertices(instrs):
    points = []
    curr_point = (0,0)
    perimeter = 0
    for _dir, step, _ in instrs:
        points.append(curr_point)
        delta_r = DIR_MAP[_dir][0] * step
        delta_c = DIR_MAP[_dir][1] * step
        curr_point = (curr_point[0] + delta_r, curr_point[1] + delta_c)
        perimeter += abs(delta_r) + abs(delta_c)
    return points, perimeter

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    instrs = parse_lines2(lines)
    points, perimeter = get_vertices(instrs)
    area = shoelace(points, perimeter) 
    return area

def solve(lines: Lines) -> int:
    """Solve the problem."""
    instrs = parse_lines(lines)
    points, perimeter = get_vertices(instrs)
    area = shoelace(points, perimeter) 
    return area


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
