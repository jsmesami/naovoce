from collections import namedtuple

Col = namedtuple('Col', 'R G B')


def from_hex(code):
    return Col(*(int(code[i:i + 2], 16) for i in range(0, 6, 2)))


def hexcode(col):
    return ''.join(format(ch, '02x') for ch in col)


def complementary(col):
    return Col(*(255 - ch for ch in col))


def shade(col, percent):
    r, g, b = col
    t = 0 if percent < 0 else 255
    p = percent * -1 if percent < 0 else percent

    return Col(round((t - r) * p) + r, round((t - g) * p) + g, round((t - b) * p) + b)


Col.from_hex = from_hex
Col.hexcode = hexcode
Col.complementary = complementary
Col.shade = shade
