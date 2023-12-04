#!/usr/bin/env python3
#
#  Advent of Code 2023 - Day 3
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
        467..114..
        ...*......
        ..35..633.
        ......#...
        617*......
        .....+.58.
        ..592.....
        ......755.
        ...$.*....
        .664.598..
        """,
        4361
    ),
]

SAMPLE_CASES2 = [
    (
        """
        467..114..
        ...*......
        ..35..633.
        ......#...
        617*......
        .....+.58.
        ..592.....
        ......755.
        ...$.*....
        .664.598..
        """,
        467835
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
def parse_numbers(lines):
    numbers = []
    for i in range(len(lines)):
        line = lines[i].strip()

        j = 0
        while j < len(line):
            curr_num = None
            start = 0
            length = 0
    
            char = line[j]
            while char.isdigit():
                if not curr_num:
                    curr_num = char
                    start = j
                    length = 1
                else:
                    curr_num += char
                    length += 1
                j += 1
                if j >= len(line):
                    break
                char = line[j]
    
            if curr_num:
                char_length = len(curr_num)
                numbers.append((int(curr_num), i, start, start + length - 1))            
            
            j += 1 
    
    return numbers

def get_neighbor_coords(x, y_0, y_1, row_bound, col_bound):
    coords = []
    if (x - 1) >= 0:
        for i in range(max(0, y_0 - 1), min(col_bound, y_1 + 1 + 1)):
            coords.append((x-1, i))
    if (y_0 - 1) >= 0:
        coords.append((x, y_0 -1))
    if (y_1 + 1) < col_bound:
        coords.append((x, y_1 + 1))
    if (x + 1) < row_bound:
        for i in range(max(0, y_0 - 1), min(col_bound, y_1 + 1 + 1)):
            coords.append((x+1, i))
    return coords 
    
def is_symbol(char):
    return char != '.' and not char.isdigit()

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    numbers = parse_numbers(lines)
    sum_res = 0
    symbol_neighbors = defaultdict(list)
    for number, x, y_start, y_end in numbers:
        coords = get_neighbor_coords(x, y_start, y_end, len(lines), len(lines[0]))
        for coord in coords:
            symbol_neighbors[coord].append(number)
    
    for (x,y), nums in symbol_neighbors.items():
        if len(nums) == 2 and lines[x][y] == '*':
            sum_res += nums[0] * nums[1]
    return sum_res

def solve(lines: Lines) -> int:
    """Solve the problem."""
    numbers = parse_numbers(lines)
    sum_res = 0
    for number, x, y_start, y_end in numbers:
        coords = get_neighbor_coords(x, y_start, y_end, len(lines), len(lines[0]))
        for x,y in coords:
            if is_symbol(lines[x][y]):
                sum_res += number
    return sum_res


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
    assert result == 530849
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
    assert result == 84900879
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
