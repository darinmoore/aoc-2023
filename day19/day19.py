#!/usr/bin/env python3
#
#  Advent of Code 2023 - Day 19
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
        px{a<2006:qkq,m>2090:A,rfg}
        pv{a>1716:R,A}
        lnx{m>1548:A,A}
        rfg{s<537:gd,x>2440:R,A}
        qs{s>3448:A,lnx}
        qkq{x<1416:A,crn}
        crn{x>2662:A,R}
        in{s<1351:px,qqz}
        qqz{s>2770:qs,m<1801:hdj,R}
        gd{a>3333:R,R}
        hdj{m>838:A,pv}

        {x=787,m=2655,a=1222,s=2876}
        {x=1679,m=44,a=2067,s=496}
        {x=2036,m=264,a=79,s=2244}
        {x=2461,m=1339,a=466,s=291}
        {x=2127,m=1623,a=2188,s=1013}
        """,
        19114
    ),
]

SAMPLE_CASES2 = [
    (
        """
        px{a<2006:qkq,m>2090:A,rfg}
        pv{a>1716:R,A}
        lnx{m>1548:A,A}
        rfg{s<537:gd,x>2440:R,A}
        qs{s>3448:A,lnx}
        qkq{x<1416:A,crn}
        crn{x>2662:A,R}
        in{s<1351:px,qqz}
        qqz{s>2770:qs,m<1801:hdj,R}
        gd{a>3333:R,R}
        hdj{m>838:A,pv}

        {x=787,m=2655,a=1222,s=2876}
        {x=1679,m=44,a=2067,s=496}
        {x=2036,m=264,a=79,s=2244}
        {x=2461,m=1339,a=466,s=291}
        {x=2127,m=1623,a=2188,s=1013}
        """,
        167409079868000
    ),
]

Lines = Sequence[str]
Sections = Sequence[Lines]

# Utility functions

def load_input(infile: str, strip=True, blank_lines=False) -> Lines:
    return load_text(Path(infile).read_text())

def load_text(text: str, strip=True, blank_lines=True) -> Lines:
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
def parse_workflows(workflows):
    workflow_dict = {}
    for workflow in workflows:
        label = workflow.split('{')[0]
        rules = workflow.split('{')[1].strip('}')
        rules = rules.split(',')
        rules = [rule.split(':') for rule in rules]
        new_rules = []
        for rule in rules:
            condition = rule[0]
            assign = rule[-1]
            if '<' in condition:
                new_rules.append(((condition.split('<')[0], '<', int(condition.split('<')[1])), assign))
            elif '>' in condition:
                new_rules.append(((condition.split('>')[0], '>', int(condition.split('>')[1])), assign))
            else:
                new_rules.append((None, assign))
        workflow_dict[label] = new_rules
    return workflow_dict

def parse_parts(parts):
    parts = [part.strip('{}').split(',') for part in parts]
    parts = [dict(zip('xmas', 
                      [int(category.strip('xmas=')) for category in part])) for part in parts]
    return parts

def part_inspection(workflows_dict, parts):
    good_part_sum = 0
    for part in parts:
        assign = 'in'
        while not (assign == 'R' or assign == 'A'):
            rules = workflows_dict[assign]
            for condition, possible_assign in rules:
                if condition:
                    label, operation, value = condition
                    if operation == '<' and part[label] < value:
                        assign = possible_assign
                        break
                    if operation == '>' and part[label] > value:
                        assign = possible_assign
                        break
                else:
                    assign = possible_assign
        if assign == 'A':
            good_part_sum += sum(part.values())
            
    return good_part_sum

LABELS = {'x':0, 'm':1, 'a':2, 's':3}

def part_inspection_ranges(workflows_dict, inputs, assign):
    ranges = []
    if assign == 'R':
        return []
    if assign == 'A':
        return [inputs]

    rules = workflows_dict[assign] 
    curr_input = inputs
    for condition, possible_assign in rules:
        if condition:
            label, operation, value = condition
            label_index = LABELS[label]
            label_min, label_max = curr_input[label_index]
            if operation == '<':
                # All to the right, none recur
                if label_min >= value:
                    continue
                # All to the left, all recur
                elif label_max < value:
                    ranges += part_inspection_ranges(workflows_dict, curr_input, possible_assign)
                # Overlapped, need to split
                else:
                    new_input = curr_input[:]
                    new_input[label_index] = (label_min, value - 1)
                    curr_input[label_index] = (value, label_max)
                    ranges += part_inspection_ranges(workflows_dict, new_input, possible_assign)

            if operation == '>':
                if label_min > value:
                    ranges += part_inspection_ranges(workflows_dict, curr_input,  possible_assign)
                if label_max <= value:
                    continue
                else:
                    new_input = curr_input[:]
                    new_input[label_index] = (value+1, label_max)
                    curr_input[label_index] = (label_min, value)
                    ranges += part_inspection_ranges(workflows_dict, new_input, possible_assign)
        else:
            ranges += part_inspection_ranges(workflows_dict, curr_input, possible_assign)

    return ranges

def compute_total(ranges):
    total = 0
    for _range in ranges:
        part_total = 1
        for part_min, part_max in _range:
            part_total *= (part_max - part_min + 1)
        total += part_total
    return total

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    workflows, _ = parse_sections(lines)
    workflows_dict = parse_workflows(workflows)
    start_input = [(1,4000), (1,4000), (1,4000), (1,4000)]
    ranges = part_inspection_ranges(workflows_dict, start_input, 'in')
    total = compute_total(ranges)
    return total

def solve(lines: Lines) -> int:
    """Solve the problem."""
    workflows, parts = parse_sections(lines)
    workflows_dict = parse_workflows(workflows)
    parts = parse_parts(parts)
    good_part_sum = part_inspection(workflows_dict, parts)
    return good_part_sum


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
