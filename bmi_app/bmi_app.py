import customtkinter as ctk
from settings import *


class App(ctk.CTk):
    def __init__(self):
        # setup
        super().__init__(fg_color=GREEN)
        self.title("")
        self.geometry("400x400")
        self.resizable(False, False)

        # data
        self.metric_bool = ctk.BooleanVar(value=True)
        self.weight_float = ctk.DoubleVar(value=70)
        self.height_int = ctk.IntVar(value=185)
        self.bmi_string = ctk.StringVar()
        self.bmi_update()

        # trace
        self.height_int.trace("w", self.bmi_update)
        self.weight_float.trace("w", self.bmi_update)
        self.metric_bool.trace("w", self.update_height)
        self.metric_bool.trace("w", self.update_weight)

        ResultText(self, self.bmi_string)
        self.weight_input = WeightInput(self, self.weight_float, self.metric_bool)
        self.height_input = HeightInput(self, self.height_int, self.metric_bool)
        UnitSwitcher(self, self.metric_bool)

        # creating the grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1, uniform="y")
        self.rowconfigure(1, weight=1, uniform="y")
        self.rowconfigure(2, weight=1, uniform="y")
        self.rowconfigure(3, weight=1, uniform="y")

        # run
        self.mainloop()

    def update_height(self, *args):
        self.height_input.update_text(self.height_int.get())

    def update_weight(self, *args):
        self.weight_input.update_weight()

    def bmi_update(self, *args):
        weight_kg = self.weight_float.get()
        height_m = self.height_int.get() / 100
        bmi_formula = round(weight_kg / height_m ** 2, 2)
        self.bmi_string.set(str(bmi_formula))


class ResultText(ctk.CTkLabel):
    def __init__(self, parent, bmi_string):
        font = ctk.CTkFont(family=FONT, size=MAIN_TEXT_SIZE, weight="bold")
        super().__init__(master=parent, text="22.6", font=font, text_color=WHITE, textvariable=bmi_string)

        self.grid(row=0, column=0, rowspan=2, sticky="nsew")


class WeightInput(ctk.CTkFrame):
    def __init__(self, parent, weight_int, metric_bool):
        super().__init__(master=parent, fg_color=WHITE)

        self.grid(column=0, row=2, sticky="nsew", pady=10, padx=10)
        self.weight_int = weight_int
        self.metric_bool = metric_bool

        # grid
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2, uniform="yes")
        self.columnconfigure(1, weight=1, uniform="yes")
        self.columnconfigure(2, weight=3, uniform="yes")
        self.columnconfigure(3, weight=1, uniform="yes")
        self.columnconfigure(4, weight=2, uniform="yes")

        self.output_string = ctk.StringVar()
        self.update_weight()

        # text
        font_weight = ctk.CTkFont(family=FONT, size=INPUT_FONT_SIZE)
        weight_text = ctk.CTkLabel(self, textvariable=self.output_string, text_color=BLACK, font=font_weight)
        weight_text.grid(row=0, column=2)

        # buttons
        minus_button = ctk.CTkButton(self,
                                     text="-",
                                     fg_color=LIGHT_GRAY,
                                     text_color=BLACK,
                                     hover_color=GRAY,
                                     font=font_weight,
                                     command=lambda: self.update_weight(('minus', 'big_button')))
        minus_button.grid(row=0, column=0, sticky="ns", pady=8, padx=8)

        plus_button = ctk.CTkButton(self,
                                    text="+",
                                    fg_color=LIGHT_GRAY,
                                    text_color=BLACK,
                                    hover_color=GRAY,
                                    font=font_weight,
                                    command=lambda: self.update_weight(('plus', 'big_button')))
        plus_button.grid(row=0, column=4, sticky="ns", pady=8, padx=8)

        small_minus_button = ctk.CTkButton(self,
                                           text="-",
                                           fg_color=LIGHT_GRAY,
                                           text_color=BLACK,
                                           hover_color=GRAY,
                                           font=font_weight,
                                           command=lambda: self.update_weight(('minus', 'small_button')))
        small_minus_button.grid(row=0, column=1, pady=4, padx=4)

        small_plus_button = ctk.CTkButton(self,
                                          text="+",
                                          fg_color=LIGHT_GRAY,
                                          text_color=BLACK,
                                          hover_color=GRAY,
                                          font=font_weight,
                                          command=lambda: self.update_weight(('plus', 'small_button')))
        small_plus_button.grid(row=0, column=3, pady=4, padx=4)

    def update_weight(self, info=None):
        if info:
            if self.metric_bool.get():
                if info[1] == "big_button":
                    amount = 1
                else:
                    amount = 0.1
            else:
                if info[1] == "big_button":
                    amount = 0.453592
                else:
                    amount = 0.453592 / 16

            if info[0] == "plus":
                self.weight_int.set(round(self.weight_int.get() + amount, 2))
            else:
                self.weight_int.set(round(self.weight_int.get() - amount, 2))

        if self.metric_bool.get():
            self.output_string.set(f"{self.weight_int.get()}kg")
        else:
            raw_ounces = self.weight_int.get() * 2.20462 * 16
            pounds, ounces = divmod(raw_ounces, 16)
            self.output_string.set(f"{int(pounds)}lb {int(ounces)}oz")


class HeightInput(ctk.CTkFrame):
    def __init__(self, parent, height_int, metric_bool):
        super().__init__(master=parent, fg_color=WHITE)

        self.grid(row=3, column=0, sticky="nsew", pady=10, padx=10)
        self.metric_bool = metric_bool

        # widgets
        slider = ctk.CTkSlider(self,
                               button_color=GREEN,
                               button_hover_color=GRAY,
                               progress_color=GREEN,
                               fg_color=LIGHT_GRAY,
                               variable=height_int,
                               from_=100,
                               to=260,
                               command=self.update_text)
        slider.pack(expand=True, side="left", fill="x", padx=6)

        self.output_sting = ctk.StringVar()
        self.update_text(height_int.get())

        height_text = ctk.CTkLabel(self, textvariable=self.output_sting, font=ctk.CTkFont(family=FONT, size=INPUT_FONT_SIZE), text_color=BLACK)
        height_text.pack(expand=True, padx=6)

    def update_text(self, amount):
        if self.metric_bool.get():
            text = str(int(amount))
            meter = text[0]
            cm = text[1:]
            self.output_sting.set(f"{meter}.{cm}m")
        else:
            feet, inches = divmod(amount / 2.54, 12)
            self.output_sting.set(f'{round(feet)}\'{round(inches)}\"')


class UnitSwitcher(ctk.CTkLabel):
    def __init__(self, parent, metric_bool):
        metric_font = ctk.CTkFont(family=FONT, size=SWITCH_FONT_SIZE, weight='bold')
        super().__init__(parent, text="metric", font=metric_font, text_color=DARK_GREEN)

        self.place(relx=0.98, rely=0.01, anchor="ne")

        self.metric_bool = metric_bool
        self.bind("<Button>", self.update_status)

    def update_status(self, event):
        self.metric_bool.set(not self.metric_bool.get())

        if self.metric_bool.get():
            self.configure(text="metric")
        else:
            self.configure(text="imperial")


if __name__ == "__main__":
    App()
