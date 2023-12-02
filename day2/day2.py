#!/usr/bin/env python3
#
#  Advent of Code 2023 - Day 2
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
        Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
        Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
        Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
        Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
        """,
        8
    ),
]
SAMPLE_CASES2 = [
    (
        """
        Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
        Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
        Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
        Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
        """,
        2286
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
def parse_games(game):
    max_colors = {}
    for hand in game.split(";"):
        for color in hand.split(", "):
            number = int(color.strip().split(" ")[0])
            pebble = None
            if "blue" in color:
                pebble = "blue"
            if "red" in color:
                pebble = "red"
            if "green" in color:
                pebble = "green"
            
            max_pebbles = max_colors.get(pebble)
            if max_pebbles:
                if max_pebbles < number:
                    max_colors[pebble] = number
            else:
                max_colors[pebble] = number
    return max_colors

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    game_to_colors = {}
    power = 0
    for line in lines:
        split_lines = line.split(":")
        game_id = int(split_lines[0].split(" ")[-1])
        colors = parse_games(split_lines[1])
        game_to_colors[game_id] = colors
        power += colors["green"] * colors["red"] * colors["blue"]
    return power

def solve(lines: Lines) -> int:
    """Solve the problem."""
    game_to_colors = {}
    for line in lines:
        split_lines = line.split(":")
        game_id = int(split_lines[0].split(" ")[-1])
        colors = parse_games(split_lines[1])
        game_to_colors[game_id] = colors

    sum_ids = 0
    for game in game_to_colors.keys():
        if game_to_colors[game]["red"] > 12:
            continue
        if game_to_colors[game]["green"] > 13:
            continue
        if game_to_colors[game]["blue"] > 14:
            continue
        sum_ids += game
    return sum_ids


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
    assert result == 2237
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
    assert result == 66681
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
