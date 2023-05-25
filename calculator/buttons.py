from customtkinter import CTkButton
from calculator_settings import *


class Button(CTkButton):
    def __init__(self, parent, row, col, text, font, funct):
        super().__init__(master=parent,
                         text=text,
                         command=funct,
                         corner_radius=STYLING["corner-radius"],
                         font=font,
                         fg_color=COLORS["dark_gray"]["fg"],
                         hover_color=COLORS["dark_gray"]["hover"],
                         text_color=COLORS["dark_gray"]["text"])

        self.grid(row=row, column=col, sticky="nsew", padx=STYLING["gap"], pady=STYLING["gap"])


class NumberButton(CTkButton):
    def __init__(self, parent, row, col, span, font, funct, text, operator):
        super().__init__(master=parent,
                         command=lambda: funct(operator),
                         corner_radius=STYLING["corner-radius"],
                         font=font,
                         text=text,
                         fg_color=COLORS["light_gray"]["fg"],
                         hover_color=COLORS["light_gray"]["hover"],
                         text_color=COLORS["light_gray"]["text"])

        self.grid(row=row, column=col, sticky="nsew", padx=STYLING["gap"], pady=STYLING["gap"], columnspan=span)


class MathButton(CTkButton):
    def __init__(self, parent, row, col, text, font, funct, operator):
        super().__init__(master=parent,
                         command=lambda: funct(operator),
                         corner_radius=STYLING["corner-radius"],
                         font=font,
                         text=text,
                         fg_color=COLORS["orange"]["fg"],
                         hover_color=COLORS["orange"]["hover"],
                         text_color=COLORS["orange"]["text"])

        self.grid(row=row, column=col, sticky="nsew", padx=STYLING["gap"], pady=STYLING["gap"])


class ImageButton(CTkButton):
    def __init__(self, parent, row, col, text, image, funct):
        super().__init__(master=parent,
                         text=text,
                         command=funct,
                         corner_radius=STYLING["corner-radius"],
                         image=image,
                         fg_color=COLORS["dark_gray"]["fg"],
                         hover_color=COLORS["dark_gray"]["hover"],
                         text_color=COLORS["dark_gray"]["text"])

        self.grid(row=row, column=col, sticky="nsew", padx=STYLING["gap"], pady=STYLING["gap"])


class ImageMathButton(CTkButton):
    def __init__(self, parent, row, col, text, image, funct, operator):
        super().__init__(master=parent,
                         command=lambda: funct(operator),
                         corner_radius=STYLING["corner-radius"],
                         image=image,
                         text=text,
                         fg_color=COLORS["orange"]["fg"],
                         hover_color=COLORS["orange"]["hover"],
                         text_color=COLORS["orange"]["text"])

        self.grid(row=row, column=col, sticky="nsew", padx=STYLING["gap"], pady=STYLING["gap"])