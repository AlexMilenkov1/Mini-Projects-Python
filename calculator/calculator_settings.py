APP_SIZE = (400, 700)
MAIN_ROWS = 7
MAIN_COLUMNS = 4

FONT = "Helvetica"
OUTPUT_FONT_SIZE = 70
NORMAL_FONT_SIZE = 32

STYLING = {
    'gap': 0.5,
    'corner-radius': 0
}

NUM_POSITION = {
    '.': {'col': 2,  'row': 6, 'span': 1, "text": "."},
    0: {'col': 0,  'row': 6, 'span': 2, "text": "0"},
    1: {'col': 0,  'row': 5, 'span': 1, "text": "1"},
    2: {'col': 1,  'row': 5, 'span': 1, "text": "2"},
    3: {'col': 2,  'row': 5, 'span': 1, "text": "3"},
    4: {'col': 0,  'row': 4, 'span': 1, "text": "4"},
    5: {'col': 1,  'row': 4, 'span': 1, "text": "5"},
    6: {'col': 2,  'row': 4, 'span': 1, "text": "6"},
    7: {'col': 0,  'row': 3, 'span': 1, "text": "7"},
    8: {'col': 1,  'row': 3, 'span': 1, "text": "8"},
    9: {'col': 2,  'row': 3, 'span': 1, "text": "9"}
}

MATH_POSITION = {
    '/': {'col': 3, 'row': 2, "character": '', 'image_path': 'invert_image.png'},
    '*': {'col': 3, 'row': 3, "character": 'x', 'image_path': None},
    '-': {'col': 3, 'row': 4, "character": '-', 'image_path': None},
    '=': {'col': 3, 'row': 6, "character": '=', 'image_path': None},
    '+': {'col': 3, 'row': 5, "character": '+', 'image_path': None}
}

OPERATORS = {
    'clear': {'col': 0, "row": 2, "text": "AC", "image_path": None},
    'invert': {'col': 1, "row": 2, "text": "", "image_path": "plus_minus_2.png"},
    'percent': {'col': 2, "row": 2, "text": "%", "image_path": None}
}

COLORS = {
    'light_gray': {'fg': '#D4D4D2', 'hover': "#efefed", "text": "black"},
    'dark_gray': {'fg': '#505050', 'hover': "#686868", "text": "white"},
    'orange': {'fg': '#FF9500', 'hover': "#ffb143", "text": "white"},
    'orange_highlight': {'fg': '#white', 'hover': "white", "text": "#FF9500"}
}

BLACK = '#000000'
WHITE = '#EEEEEE'
