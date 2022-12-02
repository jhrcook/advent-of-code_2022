# Advent of Code 2022

**My solutions to the [Advent of Code 2022](https://adventofcode.com/2022) using Python.**

[![advent-of-code](https://img.shields.io/badge/Advent_of_Code-2022-F80046.svg?style=flat)](https://adventofcode.com)
[![python](https://img.shields.io/badge/Python-3.10-3776AB.svg?style=flat&logo=python&logoColor=FFD23F)](https://www.python.org)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![pydocstyle](https://img.shields.io/badge/pydocstyle-enabled-AD4CD3)](http://www.pydocstyle.org/en/stable/)

| Day | Code                                                               | Stars |
| ---:| ------------------------------------------------------------------ | ----- |
| 1   | [advent_of_code/puzzles/day01.py](advent_of_code/puzzles/day01.py) | ⭐️⭐️   |
| 2   | [advent_of_code/puzzles/day02.py](advent_of_code/puzzles/day02.py) | ⭐️⭐️   |

## Setup

Create a python virtual environment and activate it before continuing.

```bash
python3 -m venv .env
source .env/bin/activate
```

This code can be installed as an editable package using pip

```bash
pip install -e .
```

or flit (if actively developing)

```bash
flit install -s
```

## Run the code

The puzzles can be run using the command `aoc`.
Providing a day will result in the execution of just that day's puzzles.

```bash
source .env/bin/activate
# To run all puzzles:
aoc
# To run just day 1's puzzles:
aoc --day 1
```
