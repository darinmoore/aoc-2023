#!/usr/bin/env python3
#
#  Advent of Code 2023 - Day 17
#
from typing import Sequence, Union, Optional, Any, Dict, List, Tuple
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
import heapq
import math
import re
import numpy as np

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
        2413432311323
        3215453535623
        3255245654254
        3446585845452
        4546657867536
        1438598798454
        4457876987766
        3637877979653
        4654967986887
        4564679986453
        1224686865563
        2546548887735
        4322674655533
        """,
        102
    ),
]

SAMPLE_CASES2 = [
    (
        """
        2413432311323
        3215453535623
        3255245654254
        3446585845452
        4546657867536
        1438598798454
        4457876987766
        3637877979653
        4654967986887
        4564679986453
        1224686865563
        2546548887735
        4322674655533
        """,
        94
    ),
    (
    """
        111111111111
        999999999991
        999999999991
        999999999991
        999999999991
        """,
        71
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

RIGHT = (0, 1)
LEFT  = (0, -1)
UP    = (-1, 0)
DOWN  = (1,0)

# Solution
def parse_lines(lines):
    grid = []
    for line in lines:
        line = list(line)
        line = [int(char) for char in line]
        grid.append(line)
    return grid

def in_bounds(pos, grid):
    row_bounds = (0, len(grid))
    col_bounds = (0, len(grid[0]))
    if not (row_bounds[0] <= pos[0] < row_bounds[1]):
        return False
    if not (col_bounds[0] <= pos[1] < col_bounds[1]):
        return False
    return True

def traverse(grid, debug=False):
    heap = []
    start1 = (0, (0,0), RIGHT, 0)
    start2 = (0, (0,0), DOWN, 0)
    heapq.heappush(heap, start1)
    heapq.heappush(heap, start2)

    seen = set()
    distance = {}
    result = None

    while heap:
        score, pos, curr_dir, curr_dir_count = heapq.heappop(heap)
        #print(score, pos, curr_dir, curr_dir_count)
        distance = {}
        if (pos, curr_dir, curr_dir_count) in seen:
            continue
        seen.add((pos, curr_dir, curr_dir_count))

        moves = []
        if curr_dir_count == 3:
            if curr_dir in [LEFT, RIGHT]:
                moves += [UP, DOWN]
            if curr_dir in [UP, DOWN]:
                moves += [LEFT, RIGHT]
        else:
            if curr_dir == LEFT:
                moves = [LEFT, UP, DOWN]
            if curr_dir == RIGHT:
                moves = [RIGHT, UP, DOWN]
            if curr_dir == UP:
                moves = [LEFT, RIGHT, UP]
            if curr_dir == DOWN:
                moves = [LEFT, RIGHT, DOWN]

        for move in moves:
            next_pos = tuple(np.add(pos, move))

            if in_bounds(next_pos, grid):
                new_score = score + grid[next_pos[0]][next_pos[1]]
                prev_distance = distance.get((next_pos, move))
                """
                if prev_distance and prev_distance <= new_score:
                    continue
                distance[(next_pos, move)] = new_score
                """
                if next_pos == (len(grid) - 1, len(grid[0]) - 1):
                    return new_score
                if move == curr_dir:
                    heapq.heappush(heap, (new_score, next_pos, move, curr_dir_count + 1))
                else:
                    heapq.heappush(heap, (new_score, next_pos, move, 1))

    if debug:
        scored_grid = []
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

    return result    

def traverse2(grid, debug=False):
    heap = []
    start1 = (0, (0,0), RIGHT, 0)
    start2 = (0, (0,0), DOWN, 0)
    heapq.heappush(heap, start1)
    heapq.heappush(heap, start2)

    seen = set()
    distance = {}
    result = None

    while heap:
        score, pos, curr_dir, curr_dir_count = heapq.heappop(heap)
        #print(score, pos, curr_dir, curr_dir_count)
        distance = {}
        if (pos, curr_dir, curr_dir_count) in seen:
            continue
        seen.add((pos, curr_dir, curr_dir_count))
        
        if pos == (len(grid) - 1, len(grid[0]) - 1) and curr_dir_count >= 4:
            return score
 
        moves = []
        if curr_dir_count == 10:
            if curr_dir in [LEFT, RIGHT]:
                moves += [UP, DOWN]
            if curr_dir in [UP, DOWN]:
                moves += [LEFT, RIGHT]
        elif curr_dir_count < 4:
            moves += [curr_dir]
        else:
            if curr_dir == LEFT:
                moves = [LEFT, UP, DOWN]
            if curr_dir == RIGHT:
                moves = [RIGHT, UP, DOWN]
            if curr_dir == UP:
                moves = [LEFT, RIGHT, UP]
            if curr_dir == DOWN:
                moves = [LEFT, RIGHT, DOWN]

        for move in moves:
            next_pos = tuple(np.add(pos, move))

            if in_bounds(next_pos, grid):
                new_score = score + grid[next_pos[0]][next_pos[1]]
                prev_distance = distance.get((next_pos, move))
                """
                if prev_distance and prev_distance <= new_score:
                    continue
                distance[(next_pos, move)] = new_score
                """
                if move == curr_dir:
                    heapq.heappush(heap, (new_score, next_pos, move, curr_dir_count + 1))
                else:
                    heapq.heappush(heap, (new_score, next_pos, move, 1))

    if debug:
        scored_grid = []
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

    return result    



def solve2(lines: Lines) -> int:
    """Solve the problem."""
    grid = parse_lines(lines)
    score = traverse2(grid)
    return score

def solve(lines: Lines) -> int:
    """Solve the problem."""
    grid = parse_lines(lines)
    score = traverse(grid)
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
