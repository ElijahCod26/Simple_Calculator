# Simple Calculator

A graphical and command-line calculator written in Python 3 using only the
standard library. It supports addition (`+`), subtraction (`-`), multiplication
(`*`), and division (`/`).

## Graphical interface

Start the GUI with:

```sh
python3 gui_calculator.py
```

Click the on-screen buttons or use your keyboard. Press `Enter` to calculate,
`Backspace` to delete, and `Escape` to clear. Operator buttons highlight while
an operation is pending, and long numbers shrink to fit the display.

## Command-line interface

To use the terminal version instead:

```sh
python3 calculator.py
```

Enter the first number, an operator, and the second number when prompted.
Enter `q` at the first-number prompt to quit.

## Run tests

Run the automated tests with Python's built-in `unittest` module:

```sh
python3 -m unittest -v
```
