#!/usr/bin/env python3
#
#  Advent of Code 2023 - Day 16
#
from typing import Sequence, Union, Optional, Any, Dict, List, Tuple
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
from copy import deepcopy
import numpy as np
import math
import re

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        r"""
        .|...\....
        |.-.\.....
        .....|-...
        ........|.
        ..........
        .........\
        ..../.\\..
        .-.-/..|..
        .|....-|.\
        ..//.|....
        """,
        46
    ),
]

SAMPLE_CASES2 = [
    (
        r"""
        .|...\....
        |.-.\.....
        .....|-...
        ........|.
        ..........
        .........\
        ..../.\\..
        .-.-/..|..
        .|....-|.\
        ..//.|....
        """,
        51
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

RIGHT = (0, 1)
LEFT  = (0, -1)
UP    = (-1, 0)
DOWN  = (1,0)

# Solution
def gen_start_moves(grid):
    starting_moves = []
    for i in range(len(grid[0])):
        starting_moves.append(((0, i), DOWN))
        starting_moves.append(((len(grid) - 1,i), UP))
    for i in range(len(grid)):
        starting_moves.append(((i,0), RIGHT))
        starting_moves.append(((i, len(grid[0]) - 1), LEFT))
    return starting_moves

def in_bounds(pos, grid):
    row_bounds = (0, len(grid))
    col_bounds = (0, len(grid[0]))
    if not (row_bounds[0] <= pos[0] < row_bounds[1]):
        return False
    if not (col_bounds[0] <= pos[1] < col_bounds[1]):
        return False
    return True

def get_moves(pos, char, direction):
    if char == '.':
        return [(tuple(np.add(pos, direction)), direction)]
    
    if char == '|':
        if direction in [LEFT, RIGHT]:
            return [(tuple(np.add(pos, UP)), UP), (tuple(np.add(pos, DOWN)), DOWN)]
        else:
            return [(tuple(np.add(pos, direction)), direction)]

    if char == '-':
        if direction in [UP, DOWN]:
            return [(tuple(np.add(pos, LEFT)), LEFT), (tuple(np.add(pos, RIGHT)), RIGHT)]
        else:
            return [(tuple(np.add(pos, direction)), direction)]

    if char == '/':
        if direction == LEFT:
            return [(tuple(np.add(pos, DOWN)), DOWN)]
        if direction == RIGHT:
            return [(tuple(np.add(pos, UP)), UP)]
        if direction == UP:
            return [(tuple(np.add(pos, RIGHT)), RIGHT)]
        if direction == DOWN:
            return [(tuple(np.add(pos, LEFT)), LEFT)]

    if char == "\\":
        if direction == LEFT:
            return [(tuple(np.add(pos, UP)), UP)]
        if direction == RIGHT:
            return [(tuple(np.add(pos, DOWN)), DOWN)]
        if direction == UP:
            return [(tuple(np.add(pos, LEFT)), LEFT)]
        if direction == DOWN:
            return [(tuple(np.add(pos, RIGHT)), RIGHT)]

def follow_beam(starting_move, grid, debug=False):
    beams = [starting_move]
    seen = set()
    while(beams):
        (curr_pos, curr_dir) = beams[0]
        beams = beams[1:]

        if in_bounds(curr_pos, grid):
            i,j = curr_pos
            char = grid[i][j][0]
            grid[i][j][1] = True
            
            moves = get_moves(curr_pos, char, curr_dir)
            for move in moves:
                if not move in seen:
                    beams.append(move)
                    seen.add(move)

            scored_grid = []
            if debug:
                for i in range(len(grid)):
                    line = ""
                    for j in range(len(grid[0])):
                        if grid[i][j][1]:
                            line += "#"
                        else:
                            line += '.'
                    scored_grid.append(line)
                    print()
                    print('\n'.join(scored_grid))
                    print()
    return grid       

def parse_lines(lines):
    grid = []
    for line in lines:
        line = list(line)
        line = [[char, False] for char in line]
        grid.append(line)
    return grid

def score_grid(grid):
    score = 0
    scored_grid = []
    for i in range(len(grid)):
        line = ""
        for j in range(len(grid[0])):
            if grid[i][j][1]:
                line += "#"
                score += 1
            else:
                line += '.'
        scored_grid.append(line)
                
    return score

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    grid = parse_lines(lines)
    starting_moves = gen_start_moves(grid)
    scores = []
    for starting_move in starting_moves:
        grid_copy = deepcopy(grid)
        grid_copy = follow_beam(starting_move, grid_copy)
        scores.append(score_grid(grid_copy))
    return max(scores)

def solve(lines: Lines) -> int:
    """Solve the problem."""
    grid = parse_lines(lines)
    starting_move = ((0,0), RIGHT)
    grid = follow_beam(starting_move, grid)
    score = score_grid(grid)
    return score


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
