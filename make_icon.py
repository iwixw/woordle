# -*- coding: utf-8 -*-
"""Конвертирует wordle-512px.png → woordle.ico (белый контур на индиго-фоне)."""

import os
from PIL import Image, ImageDraw

HERE   = os.path.dirname(os.path.abspath(__file__))
SRC    = os.path.join(HERE, "wordle-512px.png")
ICO    = os.path.join(HERE, "woordle.ico")

SIZE   = 512
INDIGO = (99, 102, 241, 255)   # #6366f1 — фирменный цвет приложения

# 1) Исходный PNG → плоское изображение на белом (прозрачность → белый фон)
src   = Image.open(SRC).convert("RGBA")
if src.size != (SIZE, SIZE):
    src = src.resize((SIZE, SIZE), Image.LANCZOS)
flat  = Image.new("RGBA", (SIZE, SIZE), (255, 255, 255, 255))
flat.alpha_composite(src)

# 2) Чёрный контур → маска прозрачности (тёмные пиксели = контур)
art   = flat.convert("L")
alpha = art.point(lambda p: 255 - p)          # инверсия: контур→255, фон→0

# Белый слой с альфой = контур
white = Image.new("RGBA", (SIZE, SIZE), (255, 255, 255, 0))
white.putalpha(alpha)

# 3) Индиго-подложка со скруглёнными углами
bg   = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
mask = Image.new("L", (SIZE, SIZE), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, SIZE - 1, SIZE - 1],
                                       radius=int(SIZE * 0.22), fill=255)
bg.paste(Image.new("RGBA", (SIZE, SIZE), INDIGO), (0, 0), mask)

# 4) Контур уменьшаем (отступы) и центрируем поверх подложки
pad     = int(SIZE * 0.16)
inner   = SIZE - pad * 2
art_sm  = white.resize((inner, inner), Image.LANCZOS)
bg.alpha_composite(art_sm, (pad, pad))

# 5) Многоразмерный ICO
bg.save(ICO, format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])

print("Готово:", ICO)
