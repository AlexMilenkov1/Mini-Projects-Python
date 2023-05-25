import customtkinter as ctk
from calculator_settings import *
from buttons import *
from PIL import Image


class Calculator(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=BLACK)

        # setup
        self.geometry(f"{APP_SIZE[0]}x{APP_SIZE[1]}")
        self.resizable(False, False)
        self.title("Calculator")
        self._set_appearance_mode("dark")

        # grid layout
        self.columnconfigure(0, weight=1, uniform="yes")
        self.columnconfigure(1, weight=1, uniform="yes")
        self.columnconfigure(2, weight=1, uniform="yes")
        self.columnconfigure(3, weight=1, uniform="yes")
        self.rowconfigure(0, weight=1, uniform="yes")
        self.rowconfigure(1, weight=1, uniform="yes")
        self.rowconfigure(2, weight=1, uniform="yes")
        self.rowconfigure(3, weight=1, uniform="yes")
        self.rowconfigure(4, weight=1, uniform="yes")
        self.rowconfigure(5, weight=1, uniform="yes")
        self.rowconfigure(6, weight=1, uniform="yes")

        # data
        self.result_string = ctk.StringVar(value="0")
        self.formula_string = ctk.StringVar(value="")
        self.display_nums = []
        self.full_operation = []

        # widgets
        self.widgets()

        self.mainloop()

    def widgets(self):
        # fonts
        main_font = ctk.CTkFont(family=FONT, size=NORMAL_FONT_SIZE)
        output_font = ctk.CTkFont(family=FONT, size=OUTPUT_FONT_SIZE)

        # output labels
        OutputLabel(self, 0, "se", main_font, self.formula_string)  # formula
        OutputLabel(self, 1, "e", output_font, self.result_string)  # result

        # clear button
        Button(parent=self,
               col=OPERATORS["clear"]["col"],
               row=OPERATORS["clear"]["row"],
               text=OPERATORS["clear"]["text"],
               font=main_font,
               funct=self.clear_button)

        # percentage button
        Button(parent=self,
               col=OPERATORS["percent"]["col"],
               row=OPERATORS["percent"]["row"],
               text=OPERATORS["percent"]["text"],
               font=main_font,
               funct=self.percentage_button)

        # image_button
        invert_image = ctk.CTkImage(light_image=Image.open(OPERATORS["invert"]["image_path"]))
        ImageButton(
            parent=self,
            col=OPERATORS["invert"]["col"],
            row=OPERATORS["invert"]["row"],
            text=OPERATORS["invert"]["text"],
            image=invert_image,
            funct=self.invert_button
        )

        # number buttons
        for number, data in NUM_POSITION.items():
            NumberButton(parent=self,
                         col=data["col"],
                         row=data["row"],
                         span=data["span"],
                         font=main_font,
                         funct=self.number_press,
                         text=data["text"],
                         operator=number)

        # math buttons
        for operator, data in MATH_POSITION.items():
            if data["image_path"] is None:
                MathButton(
                    parent=self,
                    row=data["row"],
                    col=data["col"],
                    text=data["character"],
                    font=main_font,
                    funct=self.math_button_pressed,
                    operator=operator
                )
            else:
                divide_image = ctk.CTkImage(dark_image=Image.open(data["image_path"]))
                ImageMathButton(
                    parent=self,
                    row=data["row"],
                    col=data["col"],
                    text=data["character"],
                    image=divide_image,
                    funct=self.math_button_pressed,
                    operator=operator
                )

    def number_press(self, value):
        self.display_nums.append(str(value))
        full_num = "".join(self.display_nums)
        self.result_string.set(full_num)

    def math_button_pressed(self, value):
        current_num = "".join(self.display_nums)

        if current_num:
            self.full_operation.append(current_num)

            if value != "=":
                self.full_operation.append(value)
                self.display_nums.clear()

                self.result_string.set("")
                self.formula_string.set(' '.join(self.full_operation))
            else:
                formula = ''.join(self.full_operation)
                result = eval(formula)

                if isinstance(result, float):
                    if result.is_integer():
                        result = int(result)
                    else:
                        result = round(result, 4)

                self.result_string.set(result)
                self.formula_string.set(formula)

                self.full_operation.clear()
                self.display_nums = [str(result)]

    def clear_button(self):
        self.result_string.set(str(0))
        self.formula_string.set("")

        self.display_nums.clear()
        self.full_operation.clear()

    def percentage_button(self):
        if self.display_nums:
            current_num = float(''.join(self.display_nums))
            percent_num = current_num / 100

        self.display_nums = (list(str(percent_num)))
        self.result_string.set(''.join(self.display_nums))

    def invert_button(self):
        current_num = ''.join(self.display_nums)

        if float(current_num) > 0:
            self.display_nums.insert(0, "-")
        else:
            del self.display_nums[0]

        self.result_string.set(''.join(self.display_nums))


class OutputLabel(ctk.CTkLabel):
    def __init__(self, parent, row, sticky, font, string_var):
        super().__init__(master=parent, textvariable=string_var, font=font)

        self.grid(column=0, columnspan=4, row=row, sticky=sticky, padx=10)


if __name__ == "__main__":
    Calculator()
