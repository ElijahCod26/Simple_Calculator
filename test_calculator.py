import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from calculator import calculate, main


class CalculateTests(unittest.TestCase):
    def test_basic_operations(self) -> None:
        cases = (
            (7, "+", 2, 9),
            (7, "-", 2, 5),
            (7, "*", 2, 14),
            (7, "/", 2, 3.5),
        )
        for first, operator, second, expected in cases:
            with self.subTest(operator=operator):
                self.assertEqual(calculate(first, operator, second), expected)

    def test_unsupported_operator_raises_value_error(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unsupported operator"):
            calculate(1, "%", 2)

    def test_division_by_zero_raises_zero_division_error(self) -> None:
        with self.assertRaises(ZeroDivisionError):
            calculate(1, "/", 0)

    def test_cli_reports_division_by_zero_and_quits(self) -> None:
        output = StringIO()
        with patch("builtins.input", side_effect=["1", "/", "0", "q"]):
            with redirect_stdout(output):
                main()

        self.assertIn("Error: Cannot divide by zero.", output.getvalue())
        self.assertIn("Goodbye!", output.getvalue())

    def test_cli_recovers_from_invalid_input_and_calculates(self) -> None:
        output = StringIO()
        inputs = ["not a number", "7", "+", "2", "7", "-", "2", "q"]
        with patch("builtins.input", side_effect=inputs):
            with redirect_stdout(output):
                main()

        self.assertIn("Error:", output.getvalue())
        self.assertIn("7 + 2 = 9", output.getvalue())
        self.assertIn("7 - 2 = 5", output.getvalue())
        self.assertIn("SIMPLE CALCULATOR", output.getvalue())


if __name__ == "__main__":
    unittest.main()
