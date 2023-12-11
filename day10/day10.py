#!/usr/bin/env python3
#
#  Advent of Code 2023 - Day 10
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
        ..F7.
        .FJ|.
        SJ.L7
        |F--J
        LJ...
        """,
        8
    ),
]

SAMPLE_CASES2 = [
    (
        """
        ...........
        .S-------7.
        .|F-----7|.
        .||.....||.
        .||.....||.
        .|L-7.F-J|.
        .|..|.|..|.
        .L--J.L--J.
        ...........
        """,
        4
    ),
    (
        """
        .F----7F7F7F7F-7....
        .|F--7||||||||FJ....
        .||.FJ||||||||L7....
        FJL7L7LJLJ||LJ.L-7..
        L--J.L7...LJS7F-7L7.
        ....F-J..F7FJ|L7L7L7
        ....L7.F7||L7|.L7L7|
        .....|FJLJ|FJ|F7|.LJ
        ....FJL-7.||.||||...
        ....L---J.LJ.LJLJ...
        """,
        8
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

UP = (-1,0)
DOWN = (1,0)
LEFT = (0, -1)
RIGHT = (0,1)

MOVES = [UP, DOWN, LEFT, RIGHT]

# PIPES to up, down, left, right
PIPES_TO_MOVE = { '|' : [UP, DOWN, None, None],
                  '-' : [None, None, LEFT, RIGHT],
                  'L' : [None, RIGHT, UP, None],
                  'J' : [None, LEFT, None, UP],
                  '7' : [LEFT, None, None, DOWN],
                  'F' : [RIGHT, None, DOWN, None]
                }

# Solution
def parse_lines(lines):
    new_lines = []
    padding = '.' * (len(lines[0]) + 2) 
    for line in lines:
        new_lines.append('.' + line + '.')
    return [padding] + new_lines + [padding]

def get_starting_pos(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 'S':
                return i, j
    return -1

def get_first_valid_move(grid, x0, y0):
    for x,y in MOVES:
        next_pos = grid[x0 +x][y0+y]
        if next_pos in PIPES_TO_MOVE.keys():
            first_move = MOVES.index((x,y))
            if PIPES_TO_MOVE[next_pos][first_move]:
                return first_move
    return -1
 

def get_len_path(grid):
    x0, y0 = get_starting_pos(grid)
    curr_dir = get_first_valid_move(grid, x0,y0)
    loop_coords = [(x0,y0)]
    
    x0 = x0 + MOVES[curr_dir][0]
    y0 = y0 + MOVES[curr_dir][1]
    
    loop_coords += [(x0, y0)]
    char = grid[x0][y0]

    loop_exhausted = False
    num_pipes = 1 # cause we're skipping the first part
    
    while not loop_exhausted:

        curr_dir = MOVES.index(PIPES_TO_MOVE[char][curr_dir])
        
        x0 = x0 + MOVES[curr_dir][0]
        y0 = y0 + MOVES[curr_dir][1]

        char = grid[x0][y0]
        loop_coords += [(x0,y0)]
        num_pipes += 1

        if char == 'S':
            loop_exhausted = True
    return num_pipes, set(loop_coords)

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    grid = parse_lines(lines)
    _, loop_coords = get_len_path(grid)
    cells_in = 0

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            thresholds = 0
            
            # TODO Never use x,y vals for 2d matrices in the future
            x = i
            y = j
            
            if (x,y) in loop_coords:
                continue

            while x < len(grid) and y < len(grid[0]):
                if (x,y) in loop_coords and grid[x][y] not in "L7":
                    thresholds += 1
                x += 1
                y += 1

            if thresholds % 2 == 1:
                #print((i,j), grid[i][j], thresholds)
                cells_in += 1
    return cells_in

def solve(lines: Lines) -> int:
    """Solve the problem."""
    grid = parse_lines(lines)
    return get_len_path(grid)[0] // 2

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
