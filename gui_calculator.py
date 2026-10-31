"""A graphical calculator built with Python's standard-library Tkinter."""

from collections.abc import Callable
import tkinter as tk

from calculator import calculate


BACKGROUND = "#171923"
PANEL = "#222634"
DISPLAY = "#11141d"
TEXT = "#f4f4f5"
MUTED = "#9ca3af"
ACCENT = "#8b7cff"
ACCENT_HOVER = "#a195ff"
ACCENT_SELECTED = "#6558c7"
OPERATOR = "#34394a"
BUTTON_HOVER = "#41475a"


class CalculatorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Simple Calculator")
        self.root.configure(bg=BACKGROUND)
        self.root.resizable(False, False)

        self.current = "0"
        self.stored_value: float | None = None
        self.pending_operator: str | None = None
        self.replace_current = False
        self.operator_buttons: dict[str, tk.Label] = {}

        self.display_var = tk.StringVar(value=self.current)
        self.status_var = tk.StringVar(value="Ready")

        self._build_ui()
        self._bind_keyboard()
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f"+{x}+{y}")

    def _build_ui(self) -> None:
        frame = tk.Frame(self.root, bg=BACKGROUND, padx=20, pady=20)
        frame.grid()

        tk.Label(
            frame,
            text="CALCULATOR",
            bg=BACKGROUND,
            fg=TEXT,
            font=("Helvetica", 15, "bold"),
            anchor="w",
        ).grid(row=0, column=0, columnspan=3, sticky="ew")
        tk.Label(
            frame,
            text="BASIC · 4 OPERATIONS",
            bg=BACKGROUND,
            fg=MUTED,
            font=("Helvetica", 9, "bold"),
            anchor="e",
        ).grid(row=0, column=3, sticky="ew", pady=(0, 12))

        screen = tk.Frame(frame, bg=DISPLAY, padx=14, pady=12)
        screen.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(0, 14))
        tk.Label(
            screen,
            textvariable=self.status_var,
            bg=DISPLAY,
            fg=MUTED,
            font=("Helvetica", 10),
            anchor="e",
            height=1,
        ).pack(fill="x")
        self.result_label = tk.Label(
            screen,
            textvariable=self.display_var,
            bg=DISPLAY,
            fg=TEXT,
            font=("Helvetica", 32, "bold"),
            anchor="e",
            width=13,
            height=1,
        )
        self.result_label.pack(fill="x", pady=(8, 0))

        buttons = (
            ("C", "⌫", "÷", "×"),
            ("7", "8", "9", "−"),
            ("4", "5", "6", "+"),
            ("1", "2", "3", "="),
            ("±", "0", ".", "="),
        )
        for row_index, row in enumerate(buttons, start=2):
            for column_index, label in enumerate(row):
                if label == "=" and row_index == 6:
                    continue
                if label == "=":
                    button = self._button(frame, label, self._equals, accent=True)
                    button.grid(
                        row=row_index,
                        column=column_index,
                        rowspan=2,
                        sticky="nsew",
                        padx=4,
                        pady=4,
                        ipady=18,
                    )
                    continue
                if label in ("C", "⌫", "÷", "×", "−", "+"):
                    operator_value = {
                        "÷": "/",
                        "×": "*",
                        "−": "-",
                        "+": "+",
                    }.get(label)
                    command = {
                        "C": self._clear,
                        "⌫": self._backspace,
                        "÷": lambda: self._operator("/"),
                        "×": lambda: self._operator("*"),
                        "−": lambda: self._operator("-"),
                        "+": lambda: self._operator("+"),
                    }[label]
                    button = self._button(frame, label, command, secondary=True)
                    if operator_value is not None:
                        self.operator_buttons[operator_value] = button
                        button.bind(
                            "<Leave>",
                            lambda _event, key=operator_value, target=button: target.configure(
                                bg=(
                                    ACCENT_SELECTED
                                    if self.pending_operator == key
                                    else OPERATOR
                                )
                            ),
                        )
                elif label == "±":
                    button = self._button(frame, label, self._toggle_sign, secondary=True)
                else:
                    button = self._button(
                        frame,
                        label,
                        lambda value=label: self._digit(value),
                    )
                button.grid(
                    row=row_index,
                    column=column_index,
                    sticky="nsew",
                    padx=4,
                    pady=4,
                    ipady=10,
                )

        for column in range(4):
            frame.grid_columnconfigure(column, weight=1, uniform="calculator")

    @staticmethod
    def _button(
        parent: tk.Widget,
        text: str,
        command: Callable[[], None],
        *,
        accent: bool = False,
        secondary: bool = False,
    ) -> tk.Label:
        background = ACCENT if accent else OPERATOR if secondary else PANEL
        button = tk.Label(
            parent,
            text=text,
            bg=background,
            fg=TEXT,
            relief="flat",
            borderwidth=0,
            padx=4,
            pady=6,
            font=("Helvetica", 17, "bold"),
            cursor="hand2",
        )
        hover_color = ACCENT_HOVER if accent else BUTTON_HOVER
        button.bind("<Enter>", lambda _event: button.configure(bg=hover_color))
        button.bind(
            "<Leave>",
            lambda _event: button.configure(bg=background),
        )
        button.bind("<Button-1>", lambda _event: command())
        return button

    def _bind_keyboard(self) -> None:
        for key in "0123456789.":
            self.root.bind(key, lambda _event, value=key: self._digit(value))
        for key in "+-*/":
            self.root.bind(key, lambda _event, value=key: self._operator(value))
        self.root.bind("<Return>", lambda _event: self._equals())
        self.root.bind("<KP_Enter>", lambda _event: self._equals())
        self.root.bind("<BackSpace>", lambda _event: self._backspace())
        self.root.bind("<Escape>", lambda _event: self._clear())

    def _update_display(self) -> None:
        self.display_var.set(self.current)
        digits = len(self.current)
        font_size = 32 if digits <= 9 else max(18, 32 - (digits - 9) * 2)
        self.result_label.configure(font=("Helvetica", font_size, "bold"))

    def _digit(self, value: str) -> None:
        if self.replace_current:
            self.current = "0" if value == "." else value
            self.replace_current = False
        elif value == ".":
            if "." not in self.current:
                self.current += value
        elif self.current == "0":
            self.current = value
        else:
            self.current += value
        self._refresh_status()
        self._update_display()

    def _operator(self, operator: str) -> None:
        try:
            if self.pending_operator is not None and not self.replace_current:
                result = calculate(
                    self.stored_value if self.stored_value is not None else 0,
                    self.pending_operator,
                    float(self.current),
                )
                self.current = self._format_number(result)
                self._update_display()

            self.stored_value = float(self.current)
            self.pending_operator = operator
            self._set_active_operator(operator)
            self.replace_current = True
            self._refresh_status()
        except ZeroDivisionError:
            self._show_error("Cannot divide by zero")

    def _equals(self) -> None:
        if self.pending_operator is None or self.stored_value is None:
            return
        try:
            result = calculate(
                self.stored_value,
                self.pending_operator,
                float(self.current),
            )
            self.current = self._format_number(result)
            self.pending_operator = None
            self.stored_value = None
            self._set_active_operator(None)
            self.replace_current = True
            self.status_var.set("Result")
            self._update_display()
        except ZeroDivisionError:
            self._show_error("Cannot divide by zero")

    def _clear(self) -> None:
        self.current = "0"
        self.stored_value = None
        self.pending_operator = None
        self._set_active_operator(None)
        self.replace_current = False
        self.status_var.set("Ready")
        self._update_display()

    def _backspace(self) -> None:
        if self.replace_current:
            return
        self.current = self.current[:-1]
        if self.current in ("", "-"):
            self.current = "0"
        self._refresh_status()
        self._update_display()

    def _toggle_sign(self) -> None:
        if self.current.startswith("-"):
            self.current = self.current[1:]
        elif self.current != "0":
            self.current = f"-{self.current}"
        self.replace_current = False
        self._refresh_status()
        self._update_display()

    def _show_error(self, message: str) -> None:
        self.status_var.set(message)
        self.pending_operator = None
        self.stored_value = None
        self._set_active_operator(None)
        self.current = "0"
        self.replace_current = True
        self._update_display()

    def _refresh_status(self) -> None:
        if self.pending_operator is None or self.stored_value is None:
            self.status_var.set("Ready")
            return
        expression = (
            f"{self._format_number(self.stored_value)} "
            f"{self.pending_operator}"
        )
        if not self.replace_current:
            expression += f" {self.current}"
        self.status_var.set(expression)

    def _set_active_operator(self, operator: str | None) -> None:
        for key, button in self.operator_buttons.items():
            button.configure(bg=ACCENT_SELECTED if key == operator else OPERATOR)

    @staticmethod
    def _format_number(number: float) -> str:
        return f"{number:g}"


def main() -> None:
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
