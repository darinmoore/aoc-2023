#!/usr/bin/env python3
#
#  Advent of Code 2023 - Day 12 #
from typing import Sequence, Union, Optional, Any, Dict, List, Tuple
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
from functools import cache

import math
import re

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
        ???.### 1,1,3
        .??..??...?##. 1,1,3
        ?#?#?#?#?#?#?#? 1,3,1,6
        ????.#...#... 4,1,1
        ????.######..#####. 1,6,5
        ?###???????? 3,2,1
        """,
        21
    ),
]

SAMPLE_CASES2 = [
    (
    """
    ???.### 1,1,3
    .??..??...?##. 1,1,3
    ?#?#?#?#?#?#?#? 1,3,1,6
    ????.#...#... 4,1,1
    ????.######..#####. 1,6,5
    ?###???????? 3,2,1
    """,
    525152
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
    springs = []
    for line in lines:
        spring  = line.split()[0]
        pattern = tuple([int(num) for num in line.split()[1].split(',')])
        springs.append((spring, pattern))
    return springs

"""
def recur_valid_patterns(spring, pattern, possible, mem):

    possible_pattern = tuple([len(broken) for broken in possible.split('.') if len(broken)])
    curr_block = len(possible_pattern) - 1
    
    previous_char = possible[-1]
    if not possible_pattern:
        possible_pattern = tuple([0])

    if len(possible_pattern) > len(pattern):
        return 0

    for i in range(len(possible_pattern)):
        if possible_pattern[i] > pattern[i]:
            return 0

    key = (spring, previous_char, curr_block, possible_pattern)
    if key in mem:
        return mem[key]

    if not spring:
        if possible_pattern == pattern:
            mem[key] = 1
            return 1
        else:
            mem[key] = 0
            return 0

    result = 0
    if spring[0] == '?':

        if previous_char == '.':
            result += recur_valid_patterns(spring[1:], pattern, possible + "#", mem)
            result += recur_valid_patterns(spring[1:], pattern, possible + ".", mem)
        else:
            if possible_pattern[curr_block] < pattern[curr_block]:
                result = recur_valid_patterns(spring[1:], pattern, possible + '#', mem)
            else:
                result = recur_valid_patterns(spring[1:], pattern, possible + '.', mem)

    else:
        result = recur_valid_patterns(spring[1:], pattern, possible + spring[0], mem)
    
    mem[key] = result
    return result  
"""

@cache
def count_patterns(spring, pattern):
    curr_pattern = pattern[0]
    total = 0
    spring_start = None
    for i in range(len(spring) - curr_pattern + 1):
        region_end_i = curr_pattern + i
        region = spring[i:region_end_i]

        has_dot = "." in region
        next_region_broken = False 
        
        if region_end_i < len(spring):
            next_region_broken = spring[region_end_i] == "#" 
        
        pound_preceeds = False
        if i > 0:
            pound_preceeds = spring[i - 1] == "#"
        
        if not (has_dot or next_region_broken or pound_preceeds):
            if len(pattern) == 1:
                if "#" not in spring[region_end_i + 1:]:
                    total += 1
            else:
                total += count_patterns(spring[region_end_i + 1:], pattern[1:])

        if spring_start is not None and spring_start < i:
            break
        
        if spring_start is None and "#" in region:
            spring_start = i + region.index("#")
    return total

def unfold(springs):
    new_springs = []
    for spring, pattern in springs:
        new_spring = '?'.join([spring] * 5)
        new_pattern = pattern * 5
        new_springs.append((new_spring, new_pattern))
    return new_springs

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    springs = parse_lines(lines)
    springs = unfold(springs)
    possible_combos = [count_patterns(spring, pattern) for spring,pattern in springs]
    return sum(possible_combos)

def solve(lines: Lines) -> int:
    """Solve the problem."""
    springs = parse_lines(lines)
    possible_combos = [count_patterns(spring, pattern) for spring,pattern in springs]
    return sum(possible_combos)


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
