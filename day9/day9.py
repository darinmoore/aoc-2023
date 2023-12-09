#!/usr/bin/env python3
#
#  Advent of Code 2023 - Day 9
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
        0 3 6 9 12 15
        1 3 6 10 15 21
        10 13 16 21 30 45
        """,
        114
    ),
]

SAMPLE_CASES2 = [
    (
        """
        0 3 6 9 12 15
        1 3 6 10 15 21
        10 13 16 21 30 45
        """,
        2
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
    nums = []
    for line in lines:
        line = [int(num) for num in line.split()]
        nums.append(line)
    return nums

def get_diffs(nums):
    diffs = []
    for i in range(1, len(nums)):
        diffs.append(nums[i] - nums[i-1])
    return diffs

def get_prediction(nums):
    diffs = get_diffs(nums)
    last_diffs = [diffs[-1]]
    while any([diff != 0 for diff in diffs]):
        diffs = get_diffs(diffs)
        last_diffs.append(diffs[-1])
    return nums[-1] + sum(last_diffs)

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    sets = parse_lines(lines)
    prev_nums = [get_prediction(nums[::-1]) for nums in sets]
    return sum(prev_nums)

def solve(lines: Lines) -> int:
    """Solve the problem."""
    sets = parse_lines(lines)
    predictions = [get_prediction(nums) for nums in sets]
    return sum(predictions)

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
