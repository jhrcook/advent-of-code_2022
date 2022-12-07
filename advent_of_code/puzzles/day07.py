"""Advent of Code 2022 – Day 7. No Space Left On Device."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from functools import lru_cache
from textwrap import indent
from typing import Final

from advent_of_code.checks import check_result
from advent_of_code.cli_helpers import print_results
from advent_of_code.data import read_input_to_string
from advent_of_code.logger import logger

DAY: Final[int] = 7
TITLE: Final[str] = "No Space Left On Device"

ex_input = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""


@dataclass
class File:
    """Single file item."""

    name: str
    size: int

    def __str__(self) -> str:
        return f"'{self.name}' ({self.size})"

    def __repr__(self) -> str:
        return str(self)


class Directory:
    """Directory in the filesystem."""

    def __init__(
        self, name: str, contents: list[File | Directory], parent: Directory | None
    ) -> None:
        self.name = name
        self.contents = contents
        self.parent = parent

    def __str__(self) -> str:
        msg = ""
        if len(self.contents) == 0:
            msg += "(empty)" + "\n"
        else:
            for c in self.contents:
                msg += str(c) + "\n"
        msg = msg.strip()
        return f"dir '{self.name}':\n" + indent(msg, "   | ")

    def __repr__(self) -> str:
        return str(self)

    def __getitem__(self, item_name: str) -> File | Directory:
        for c in self.contents:
            if c.name == item_name:
                return c
        raise KeyError(item_name)

    def contains_item_named(self, item_name: str) -> bool:
        """Does the directory contain an item ofa given name."""
        for c in self.contents:
            if c.name == item_name:
                return True
        return False

    @property
    def path_to_root(self) -> str:
        """Get the path from the current directory to the filesystem room."""
        path = self.name
        p: Directory | None = self.parent
        while p is not None:
            path = f"{p.name}/{path}"
            p = p.parent
        return path

    def __hash__(self) -> int:
        return hash(self.path_to_root)

    def add_contents(self, new_contents: Iterable[File | Directory]) -> None:
        """Add contents to a directory."""
        current_contents_names = [x.name for x in self.contents]
        for x in new_contents:
            if x.name not in current_contents_names:
                self.contents.append(x)


def parse_terminal_command_data(cmd_data: str) -> tuple[Directory, list[Directory]]:
    """Parse the terminal commands to a filesystem tree."""
    commands = [x.strip() for x in cmd_data.strip().splitlines()]
    commands.reverse()  # Reverse so can pop next command from top of list.
    cwd: Directory | None = None
    root_dir: Directory | None = None
    directories: list[Directory] = []
    while len(commands) > 0:
        cmd = commands.pop()
        logger.debug(f"command: `{cmd}`")
        cmd_split = cmd.split(" ")
        if cmd_split[0] == "$":
            fxn = cmd_split[1]
            if fxn == "cd":
                next_dir_name = cmd_split[2]
                if next_dir_name == "/" and cwd is None:
                    logger.debug("Making first directory")
                    cwd = Directory("/", contents=[], parent=None)
                    root_dir = cwd
                    directories.append(root_dir)
                elif next_dir_name == "..":
                    assert cwd is not None and cwd.parent is not None
                    logger.debug(f"Changing cwd '{cwd.name}' -> '{cwd.parent.name}'")
                    cwd = cwd.parent
                else:
                    assert cwd is not None
                    next_dir = cwd[next_dir_name]
                    assert isinstance(next_dir, Directory), "Trying to cd into file."
                    logger.debug(f"Changing cwd '{cwd.name}' -> '{next_dir.name}'")
                    cwd = next_dir
            elif fxn == "ls":
                assert cwd is not None, "cwd cannot be None is performing `ls`."
                contents: list[File | Directory] = []
                while True:
                    if len(commands) == 0:
                        cwd.add_contents(contents)
                        break

                    info = commands.pop()
                    if info.startswith("$"):
                        commands.append(info)  # Put it back on the commands list.
                        cwd.add_contents(contents)
                        break
                    else:
                        infos = info.strip().split(" ")
                        if infos[0] == "dir":
                            if not cwd.contains_item_named(infos[1]):
                                logger.debug(f"Making dir '{infos[1]}'")
                                d = Directory(name=infos[1], contents=[], parent=cwd)
                                contents.append(d)
                                directories.append(d)
                        else:
                            if not cwd.contains_item_named(infos[1]):
                                logger.debug(f"Making file '{infos[1]}'")
                                contents.append(File(name=infos[1], size=int(infos[0])))
            else:
                raise BaseException(f"Unexpected function: '{fxn}'")
        else:
            raise BaseException("No command found.")

    assert root_dir is not None
    return root_dir, directories


@lru_cache
def get_directory_size(d: Directory) -> int:
    """Get the size of a directory."""
    total_size = 0
    for c in d.contents:
        if isinstance(c, File):
            total_size += c.size
        elif isinstance(c, Directory):
            total_size += get_directory_size(c)
        else:
            raise BaseException("Content of a dir is not a file or dir.")
    return total_size


def get_all_directory_sizes(dirs: list[Directory]) -> dict[Directory, int]:
    """Get the sizes of all directories."""
    dir_sizes: dict[Directory, int] = {}
    for d in dirs:
        dir_sizes[d] = get_directory_size(d)
    return dir_sizes


def puzzle_1(directories: list[Directory]) -> int:
    """Puzzle 1."""
    dir_sizes = get_all_directory_sizes(dirs=directories)
    total = 0
    for size in dir_sizes.values():
        if size <= 100_000:
            total += size
    return total


def puzzle_2(root_dir: Directory, directories: list[Directory]) -> int:
    """Puzzle 2."""
    dir_sizes = get_all_directory_sizes(dirs=directories)
    space_remaining = 70000000 - dir_sizes[root_dir]
    more_space_needed = 30000000 - space_remaining
    assert more_space_needed > 0
    min_amount = dir_sizes[root_dir]
    for d_size in dir_sizes.values():
        if more_space_needed < d_size < min_amount:
            min_amount = d_size
    return min_amount


def main() -> None:
    """Execute puzzles."""
    # Puzzle 1.
    _, ex_dirs = parse_terminal_command_data(ex_input)
    ex_res = puzzle_1(ex_dirs)
    check_result(95437, ex_res)
    _, dirs = parse_terminal_command_data(read_input_to_string(DAY))
    res1 = puzzle_1(dirs)
    check_result(1334506, res1)

    # Puzzle 2.
    ex_root_dir, ex_dirs = parse_terminal_command_data(ex_input)
    ex_res = puzzle_2(ex_root_dir, ex_dirs)
    check_result(24933642, ex_res)
    root_dir, dirs = parse_terminal_command_data(read_input_to_string(DAY))
    res2 = puzzle_2(root_dir, dirs)
    check_result(7421137, res2)

    print_results(DAY, TITLE, result1=res1, result2=res2)


if __name__ == "__main__":
    # set_console_handler_level("WARNING")
    main()
