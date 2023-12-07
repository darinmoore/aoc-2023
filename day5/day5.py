#!/usr/bin/env python3
#
#  Advent of Code 2023 - Day 5
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
        seeds: 79 14 55 13

        seed-to-soil map:
        50 98 2
        52 50 48

        soil-to-fertilizer map:
        0 15 37
        37 52 2
        39 0 15

        fertilizer-to-water map:
        49 53 8
        0 11 42
        42 0 7
        57 7 4

        water-to-light map:
        88 18 7
        18 25 70

        light-to-temperature map:
        45 77 23
        81 45 19
        68 64 13

        temperature-to-humidity map:
        0 69 1
        1 0 69

        humidity-to-location map:
        60 56 37
        56 93 4
        """,
        35
    ),
]

SAMPLE_CASES2 = [
    (
        """
        seeds: 79 14 55 13

        seed-to-soil map:
        50 98 2
        52 50 48

        soil-to-fertilizer map:
        0 15 37
        37 52 2
        39 0 15

        fertilizer-to-water map:
        49 53 8
        0 11 42
        42 0 7
        57 7 4

        water-to-light map:
        88 18 7
        18 25 70

        light-to-temperature map:
        45 77 23
        81 45 19
        68 64 13

        temperature-to-humidity map:
        0 69 1
        1 0 69

        humidity-to-location map:
        60 56 37
        56 93 4
        """,
        46
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

NUM_MAPS = 7

# Solution
def parse_lines(lines):
    seeds = lines[0].split(': ')[1].split()
    seeds = [int(seed) for seed in seeds]
    maps = [[] for _ in range(NUM_MAPS)]
    i = 1
    map_num = -1
    while i < len(lines):
        line = lines[i]
        if not line[0].isdigit():
            map_num += 1
        else:
            map_range = line.split()
            maps[map_num].append([int(r) for r in map_range])
        i += 1        
    return seeds, maps

def get_location(seed, maps):
    for map_ranges in maps:
        for dest, source, length in map_ranges:
            if source <= seed < source + length:
                seed = dest + seed - source
                break
    return seed

def get_seed(location, maps):
    for map_ranges in maps[::-1]:
        for dest, source, length in map_ranges:
            if dest <= location < dest + length:
                location = location + source - dest
                break
    return location

def get_location2(seed_min, seed_max, maps):
    ranges = [(seed_min, seed_max)]
    processed_ranges = []
    for map_ranges in maps:
        while ranges:
            range_min, range_max = ranges[0]
            ranges = ranges[1:]
            for dest, source, length in map_ranges:
                map_min = source
                map_max = source + length
                offset = dest - source
                if map_max <= range_min or range_min <= map_max:
                    continue
                if range_min < map_min:
                    processed_ranges.append((range_min, map_min))
                    range_min = map_min
                if map_min < range_min:
                    processed_ranges.append((map_max, range_max))
                    range_max = map_max
                processed_ranges.append((range_min + offset, range_max + offset))
                print(processed_ranges)
                break
            else:
                processed_ranges.append((range_min, range_max))
        ranges = processed_ranges
        processed_ranges = []
    return ranges

def solve2(lines: Lines) -> int:
    """Solve the problem."""

    seed_ranges, maps = parse_lines(lines)
    seed_ranges = list(zip(seed_ranges[::2], seed_ranges[1::2]))
    """
    locations = []
    for seed_min, length in seed_ranges:
        locations += get_location2(seed_min, seed_min+length, maps)
    """
    for i in range(2000000000000):
        seed = get_seed(i, maps)
        for seed_range in seed_ranges:
            if seed_range[0] <= seed < seed_range[0] + seed_range[1]:
                return i
    return min(range_min for range_min, _ in locations)

def solve(lines: Lines) -> int:
    """Solve the problem."""
    seeds, maps = parse_lines(lines)
    seeds = [get_location(seed,maps) for seed in seeds]
    return min(seeds)


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
