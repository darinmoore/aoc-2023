#!/usr/bin/env python3
#
#  Advent of Code 2023 - Day 6
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
        Time:      7  15   30
        Distance:  9  40  200
        """,
        288
    ),
]

SAMPLE_CASES2 = [    
    (
        """
        Time:      7  15   30
        Distance:  9  40  200
        """,
        71503
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
    times = []
    distances = []
    times = lines[0].split(':')[1].split()
    times = [int(time) for time in times]
    distances = lines[1].split(':')[1].split()
    distances = [int(distance) for distance in distances]
    return times, distances

def parse_lines2(lines):
    time = lines[0].split(':')[1].replace(" ", "")
    time = int(time)
    distance = lines[1].split(':')[1].replace(" ", "")
    distance = int(distance)
    return time, distance

def possible_combos(time, distance):
    combos = 0
    past_peak = False
    for hold_time in range(1, time):
        new_dist = hold_time * (time - hold_time)
        if new_dist > distance:
            combos += 1
            past_peak = True
        if new_dist < distance and past_peak:
            return combos
    return combos

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    time, distance = parse_lines2(lines)
    combos = possible_combos(time, distance)
    return combos

def solve(lines: Lines) -> int:
    """Solve the problem."""
    times, distances = parse_lines(lines)
    combos = [possible_combos(time, distance) for time, distance in zip(times, distances)]
    return math.prod(combos)


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
