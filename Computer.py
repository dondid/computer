import tkinter as tk
from tkinter import messagebox
import math
from functools import partial

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator Interactiv")
        self.root.geometry("450x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#2c3e50")

        # Variabile
        self.current_input = ""
        self.first_number = None
        self.operation = None
        self.result_shown = False

        # Configurarea stilului
        self.configure_style()

        # Crearea componentelor
        self.create_widgets()

        icon_image = tk.PhotoImage(file="inf.png") # imaginea
        self.root.iconphoto(True, icon_image) # setarea imaginii

    def configure_style(self):
        # Fonturi
        self.display_font = ("Helvetica", 28, "bold")
        self.button_font = ("Helvetica", 14, "bold")
        self.symbol_font = ("Helvetica", 16, "bold")

        # Culori
        self.bg_color = "#2c3e50"
        self.display_bg = "#ecf0f1"  # Fundal deschis pentru display
        self.display_fg = "#2c3e50"  # Text închis la culoare pentru display

        self.num_button_bg = "#3498db"
        self.num_button_fg = "black"  # Text negru pentru butoanele numerice
        self.num_button_active_bg = "#2980b9"

        self.op_button_bg = "#7f8c8d"  # Gri pentru butoanele de operații
        self.op_button_fg = "black"  # Text negru pentru butoanele de operații
        self.op_button_active_bg = "#95a5a6"  # Gri deschis pentru butoanele de operații

        self.equal_button_bg = "#85c1e9" # Tentă de albastru deschis pentru butonul egal
        self.equal_button_fg = "black"  # Text negru pentru butonul egal
        self.equal_button_active_bg = "#2c3e50"

        self.clear_button_bg = "#7f8c8d"  # Gri pentru butoanele de ștergere
        self.clear_button_fg = "black"  # Text negru pentru butoanele de ștergere
        self.clear_button_active_bg = "#95a5a6"

        self.quit_button_bg = "#7f8c8d"  # Gri pentru butonul de ieșire
        self.quit_button_fg = "black"  # Text negru pentru butonul de ieșire
        self.quit_button_active_bg = "#c0392b"

    def create_widgets(self):
        # Frame pentru afișaj
        display_frame = tk.Frame(self.root, bg=self.bg_color)
        display_frame.pack(padx=10, pady=10, fill="x")

        # Afișaj
        self.display = tk.Entry(display_frame, font=self.display_font, bg=self.display_bg,
                                fg=self.display_fg, justify="right", bd=5)
        self.display.pack(fill="both", ipady=8)
        self.display.insert(0, "0")
        self.display.config(state="readonly")

        # Frame pentru butoane
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Configurarea grilei
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        button_frame.columnconfigure(3, weight=1)

        for i in range(6):
            button_frame.rowconfigure(i, weight=1)

        # Butoane speciale - prima linie
        self.create_button(button_frame, "C", 0, 0, self.clear_button_bg, self.clear_button_fg,
                           self.clear_button_active_bg, self.clear_all)
        self.create_button(button_frame, "CE", 0, 1, self.clear_button_bg, self.clear_button_fg,
                           self.clear_button_active_bg, self.clear_entry)
        self.create_button(button_frame, "√", 0, 2, self.op_button_bg, self.op_button_fg,
                           self.op_button_active_bg, partial(self.special_operation, "sqrt"))
        self.create_button(button_frame, "x²", 0, 3, self.op_button_bg, self.op_button_fg,
                           self.op_button_active_bg, partial(self.special_operation, "square"))

        # Butoane numerice
        button_values = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", ".", "=", "+"
        ]

        row, col = 1, 0
        for value in button_values:
            if value in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]:
                bg_color = self.num_button_bg
                fg_color = self.num_button_fg
                active_bg = self.num_button_active_bg
                command = partial(self.add_digit, value)
            elif value == "=":
                bg_color = self.equal_button_bg
                fg_color = self.equal_button_fg
                active_bg = self.equal_button_active_bg
                command = self.calculate
            else:
                bg_color = self.op_button_bg
                fg_color = self.op_button_fg
                active_bg = self.op_button_active_bg
                command = partial(self.set_operation, value)

            self.create_button(button_frame, value, row, col, bg_color, fg_color, active_bg, command)

            col += 1
            if col > 3:
                col = 0
                row += 1

        # Buton de ieșire cu simbol ⏻ (Power/Exit)
        quit_button = tk.Button(button_frame, text="⏻", font=self.symbol_font,
                                bg=self.quit_button_bg, fg=self.quit_button_fg,

                                activebackground=self.quit_button_active_bg,
                                command=self.root.destroy, relief=tk.RAISED, bd=3)
        quit_button.grid(row=5, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

    def create_button(self, parent, text, row, col, bg, fg, active_bg, command):
        button = tk.Button(parent, text=text, font=self.button_font,
                           bg=bg, fg=fg, activebackground=active_bg,
                           command=command, relief=tk.RAISED, bd=3)
        button.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
        return button

    def update_display(self, text):
        self.display.config(state="normal")
        self.display.delete(0, tk.END)
        self.display.insert(0, text)
        self.display.config(state="readonly")

    def add_digit(self, digit):
        if self.result_shown:
            self.current_input = ""
            self.result_shown = False

        if digit == "." and "." in self.current_input:
            return

        if self.current_input == "0" and digit != ".":
            self.current_input = digit
        else:
            self.current_input += digit

        self.update_display(self.current_input)

    def set_operation(self, op):
        if self.current_input:
            if self.first_number is not None and not self.result_shown:
                self.calculate()

            self.first_number = float(self.current_input)
            self.operation = op
            self.current_input = ""
        elif self.result_shown:
            self.operation = op
            self.result_shown = False
            self.current_input = ""

    def special_operation(self, op_type):
        if not self.current_input:
            return

        num = float(self.current_input)

        if op_type == "sqrt":
            if num < 0:
                messagebox.showerror("Eroare", "Nu se poate calcula radical din număr negativ!")
                return
            result = math.sqrt(num)
        elif op_type == "square":
            result = num ** 2

        self.current_input = str(result)
        if self.current_input.endswith(".0"):
            self.current_input = self.current_input[:-2]

        self.update_display(self.current_input)
        self.result_shown = True

    def calculate(self):
        if not self.operation or not self.current_input:
            return

        second_number = float(self.current_input)

        try:
            if self.operation == "+":
                result = self.first_number + second_number
            elif self.operation == "-":
                result = self.first_number - second_number
            elif self.operation == "*":
                result = self.first_number * second_number
            elif self.operation == "/":
                if second_number == 0:
                    messagebox.showerror("Eroare", "Împărțirea la zero nu este permisă!")
                    return
                result = self.first_number / second_number

            # Formatarea rezultatului
            if result.is_integer():
                result = int(result)

            self.current_input = str(result)
            self.update_display(self.current_input)

            self.first_number = result
            self.result_shown = True

        except Exception as e:
            messagebox.showerror("Eroare", f"A apărut o eroare: {str(e)}")
            self.clear_all()

    def clear_entry(self):
        self.current_input = ""
        self.update_display("0")

    def clear_all(self):
        self.current_input = ""
        self.first_number = None
        self.operation = None
        self.result_shown = False
        self.update_display("0")


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()