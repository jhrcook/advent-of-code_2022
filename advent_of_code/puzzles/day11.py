"""Advent of Code 2022 – Day 11. Monkey in the Middle."""

from typing import Final

from advent_of_code.checks import check_result
from advent_of_code.cli_helpers import print_results
from advent_of_code.data import read_input_to_string

DAY: Final[int] = 11
TITLE: Final[str] = "Monkey in the Middle"

example_input = """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""


MonkeyID = int


class MonkeyOperation:
    """Monkey operation."""

    def __init__(self, equation: str) -> None:
        self.equation = equation

    def __call__(self, old: int) -> int:
        """Run the monkey's operation.

        Args:
            old (int): Old (i.e. current) value.

        Returns:
            int: New value.
        """
        return eval(self.equation)


class MonkeyTest:
    """Monkey test."""

    def __init__(self, div_value: int, if_true: MonkeyID, if_false: MonkeyID) -> None:
        self.div_value = div_value
        self.if_true = if_true
        self.if_false = if_false

    def __call__(self, value: int) -> MonkeyID:
        """Run the test.

        Args:
            value (int): Value of the item to test.

        Returns:
            MonkeyID: ID of the monkey to receive the item.
        """
        return self.if_true if value % self.div_value == 0 else self.if_false


class Monkey:
    """Monkey playing with items of value."""

    def __init__(
        self,
        id: MonkeyID,
        items: list[int],
        operation: MonkeyOperation,
        test: MonkeyTest,
        div_by_three: bool,
    ) -> None:
        self.id = id
        self.items = items.copy()
        self.operation = operation
        self.test = test
        self.div_by_three = div_by_three

    def __str__(self) -> str:
        return f"Monkey {self.id:02d}: {', '.join([str(x) for x in self.items])}"

    def __repr__(self) -> str:
        return str(self)

    def inspect_item(self, worry_level: int) -> tuple[MonkeyID, int]:
        """Inspect a single item.

        Args:
            worry_level (int): Item's starting worry level.

        Returns:
            tuple[MonkeyID, int]: Monkey that wil receive the item and the updated
            worry level for the item.
        """
        worry_level = self.operation(worry_level)
        if self.div_by_three:
            worry_level = worry_level // 3
        next_monkey = self.test(worry_level)
        return next_monkey, worry_level

    def inspect_items(self) -> list[tuple[MonkeyID, int]]:
        """Inspect all items currently possessed by the monkey."""
        exchanges: list[tuple[MonkeyID, int]] = []
        for worry_level in self.items:
            exchanges.append(self.inspect_item(worry_level))
        self.items = []
        return exchanges

    def receive_item(self, new_item: int) -> None:
        """Receive an item.

        Args:
            new_item (int): Worry level of the new item.
        """
        self.items.append(new_item)


def parse_monkey_instructions(
    input_str: str, div_by_three: bool = True
) -> list[Monkey]:
    """Parse instructions into Monkey objects."""
    monkeys: list[Monkey] = []
    input_split = [x.strip() for x in input_str.strip().split("Monkey")]
    for data in input_split:
        if data == "":
            continue
        lines = [x.strip() for x in data.splitlines()]
        id = int(lines[0].split(":")[0])
        items = [int(x) for x in lines[1].split("Starting items: ")[1].split(", ")]
        operation = MonkeyOperation(lines[2].split("Operation: new = ")[1])
        test_val = int(lines[3].split("Test: divisible by ")[1])
        true_id = int(lines[4].split("If true: throw to monkey ")[1])
        false_id = int(lines[5].split("If false: throw to monkey ")[1])
        monkey = Monkey(
            id=id,
            items=items,
            operation=operation,
            test=MonkeyTest(div_value=test_val, if_true=true_id, if_false=false_id),
            div_by_three=div_by_three,
        )
        monkeys.append(monkey)
    return monkeys


def _print_monkeys(monkeys: list[Monkey]) -> None:
    for m in monkeys:
        print(m)


def _count_number_of_inspections_over_rounds(
    monkeys: list[Monkey], n_round: int
) -> dict[MonkeyID, int]:
    # Check the monkeys are ordered by their ID.
    for i, m in enumerate(monkeys):
        assert i == m.id

    num_inspects: dict[MonkeyID, int] = {m.id: 0 for m in monkeys}
    for _ in range(n_round):
        for monkey in monkeys:
            num_inspects[monkey.id] += len(monkey.items)
            swaps = monkey.inspect_items()
            for idx, item in swaps:
                monkeys[idx].receive_item(item)
    return num_inspects


def _calculate_monkey_business(inspection_counts: dict[MonkeyID, int]) -> int:
    top_counts = sorted(list(inspection_counts.values()))[-2:]
    return top_counts[0] * top_counts[1]


def puzzle_1(monkeys: list[Monkey]) -> int:
    """Puzzle 1."""
    num_inspects = _count_number_of_inspections_over_rounds(monkeys, n_round=20)
    return _calculate_monkey_business(num_inspects)


def puzzle_2(monkeys: list[Monkey]) -> int:
    """Puzzle 2."""
    ...


def main() -> None:
    """Execute puzzles."""
    # Puzzle 1.
    ex_monkeys = parse_monkey_instructions(example_input)
    ex_res = puzzle_1(ex_monkeys)
    check_result(10605, ex_res)
    monkeys = parse_monkey_instructions(read_input_to_string(DAY))
    res1 = puzzle_1(monkeys)
    check_result(113232, res1)

    # Puzzle 2.
    ...

    print_results(DAY, TITLE, result1=res1, result2=None)


if __name__ == "__main__":
    main()
