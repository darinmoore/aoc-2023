#!/usr/bin/env python3
#
#  Advent of Code 2023 - Day 7
#
from typing import Sequence, Union, Optional, Any, Dict, List, Tuple
from pathlib import Path
from collections import defaultdict
from collections import Counter
from dataclasses import dataclass
import math
import re

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
        32T3K 765
        T55J5 684
        KK677 28
        KTJJT 220
        QQQJA 483
        """,
        6440
    ),
]

SAMPLE_CASES2 = [
    (
        """
        32T3K 765
        T55J5 684
        KK677 28
        KTJJT 220
        QQQJA 483
        """,
        5905
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

HAND_ORDER = [[1,1,1,1,1], [2,1,1,1], [2,2,1], [3,1,1], [3,2], [4,1], [5]]

# abusing ascii values so we can just use built-in sorting
REPLACEMENTS = {"J" : "U", "Q" : "V", "K" : "W", "A": "X"}
REPLACEMENTS_2 = {"J" : "*", "Q" : "V", "K" : "W", "A": "X"}

# Solution
def make_replacements(hand, repl_dict):
    for text, replace in repl_dict.items():
        hand = hand.replace(text, replace)
    return hand

def flatten(l):
    return [item for sublist in l for item in sublist if item]

def parse_lines(lines, repl_dict):
    hands = []
    bids = []
    for line in lines:
        hands += [line.split()[0]]
        bids  += [line.split()[1]]
    hands = [make_replacements(hand, repl_dict) for hand in hands]
    bids  = [int(bid) for bid in bids]
    return hands, bids

def get_hand_type(hand):
    card_freq = {}
    for card in hand:
        card_freq[card] = card_freq.get(card, 0) + 1
    return HAND_ORDER.index(sorted(list(card_freq.values()), reverse=True))

def get_hand_type_wilds(hand):
    card_freq = {}
    # all jokers, just return that we have 5 of a kind 
    if hand == '*****':
        return 6
    for card in hand:
        if card != '*':
            card_freq[card] = card_freq.get(card, 0) + 1
    most_freq_card = max(card_freq, key=card_freq.get)
    for card in hand:
        if card == '*':
            card_freq[most_freq_card] += 1
    return HAND_ORDER.index(sorted(list(card_freq.values()), reverse=True))

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    hands, bids = parse_lines(lines, REPLACEMENTS_2)
    sorted_hands = [[] for _ in range(len(HAND_ORDER))]
    for hand,bid in zip(hands,bids):
        sorted_hands[get_hand_type_wilds(hand)].append((hand, bid))
    sorted_hands = [sorted(group) for group in sorted_hands]
    sorted_hands = flatten(sorted_hands)
    score = 0
    for i in range(len(sorted_hands)):
        score += sorted_hands[i][1] * (i+1)
    return score

def solve(lines: Lines) -> int:
    """Solve the problem."""
    hands, bids = parse_lines(lines, REPLACEMENTS)
    sorted_hands = [[] for _ in range(len(HAND_ORDER))]
    for hand,bid in zip(hands,bids):
        sorted_hands[get_hand_type(hand)].append((hand, bid))
    sorted_hands = [sorted(group) for group in sorted_hands]
    sorted_hands = flatten(sorted_hands)
    score = 0
    for i in range(len(sorted_hands)):
        score += sorted_hands[i][1] * (i+1)
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
