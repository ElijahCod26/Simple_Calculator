"""A simple command-line calculator for the four basic operations."""

import sys


_RESET = "\033[0m"
_CYAN = "\033[36m"
_GREEN = "\033[32m"
_RED = "\033[31m"
_DIM = "\033[2m"


def _styled(text: str, color: str) -> str:
    if sys.stdout.isatty():
        return f"{color}{text}{_RESET}"
    return text


def _show_header() -> None:
    border = _styled("  +----------------------------------+", _DIM)
    print(border)
    print(_styled("  |        SIMPLE CALCULATOR        |", _CYAN))
    print(_styled("  |          +  -  *  /             |", _CYAN))
    print(border)
    print("  Enter q at any first-number prompt to quit.")


def calculate(first: float, operator: str, second: float) -> float:
    """Return the result of applying operator to the two numbers."""
    if operator == "+":
        return first + second
    if operator == "-":
        return first - second
    if operator == "*":
        return first * second
    if operator == "/":
        return first / second
    raise ValueError("Unsupported operator. Use +, -, *, or /.")


def main() -> None:
    _show_header()

    while True:
        first_input = input("\n  First number (or q to quit): ").strip()
        if first_input.lower() == "q":
            print("\n  Goodbye!")
            return

        try:
            first = float(first_input)
            operator = input("  Operator (+, -, *, /): ").strip()
            second = float(input("  Second number: ").strip())
            result = calculate(first, operator, second)
        except ValueError as error:
            print(_styled(f"  Error: {error}", _RED))
            continue
        except ZeroDivisionError:
            print(_styled("  Error: Cannot divide by zero.", _RED))
            continue

        print(_styled(f"  {first:g} {operator} {second:g} = {result:g}", _GREEN))


if __name__ == "__main__":
    main()
