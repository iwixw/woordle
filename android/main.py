# -*- coding: utf-8 -*-
"""Woordle (Android/Kivy) — школьная версия Wordle.

Сенсорная версия для телефонов. Логика идентична десктопной:
режимы 5/7/9 букв, режим дальтоника, проверка слов по словарю,
статистика. Собирается в APK через Buildozer (см. buildozer.spec).
"""

import json
import os
import random

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.metrics import dp, sp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, RoundedRectangle


# ── Слова (5 / 7 / 9 букв, школьная тематика) ─────────────────────────────────
A5 = [
    "КЛАСС", "ДОСКА", "ПАРТА", "КНИГА", "РУЧКА", "ПЕНАЛ", "ШКОЛА", "НАУКА",
    "СПОРТ", "ФОРМА", "КАРТА", "АТЛАС", "ТЕКСТ", "СЛОВО", "ЧИСЛО", "ХИМИЯ",
    "ЗАЧЁТ", "БУФЕТ", "ЦИФРА", "БУКВА", "ГЛАВА", "ЭКРАН", "ОСЕНЬ", "ВЕСНА",
    "ОТВЕТ", "УЧЁБА", "МЕЛОК", "КИСТЬ", "УСПЕХ", "НОТКА", "ЦВЕТА", "СХЕМА",
    "ЛИНЗА", "ДОСКИ", "ОЛИМП", "КНИГИ", "БАЛЛА",
]
E5 = [
    "БЕРЕГ", "БИЛЕТ", "БОЧКА", "БЕЛКА", "ВАГОН", "ВЕТЕР", "ВИЛКА", "ВИШНЯ",
    "ВОЛНА", "ВЫХОД", "ГОРКА", "ГРОЗА", "ГУБКА", "ДИВАН", "ДОМИК", "ДОЖДЬ",
    "ЗАБОР", "ЗАВОД", "ЗАКАТ", "ЗАМОК", "ЗАПАХ", "ЗЕМЛЯ", "ЗЕБРА", "ЗВЕРЬ",
    "ИСКРА", "КАПЛЯ", "КОШКА", "КУБИК", "КУКЛА", "ЛАМПА", "ЛЕНТА", "ЛИМОН",
    "ЛОДКА", "ЛОЖКА", "МАЙКА", "МАРКА", "МАСКА", "МАСЛО", "МЕСТО", "МЕТРО",
    "МЕЧТА", "МИСКА", "МИШКА", "МОРОЗ", "МОТОР", "МЫШКА", "НАБОР", "НИТКА",
    "НОМЕР", "НОСОК", "ОГОНЬ", "ОЛЕНЬ", "ОСИНА", "ОХОТА", "ПАКЕТ", "ПАЛКА",
    "ПАПКА", "ПАРУС", "ПАСТА", "ПЕРЕЦ", "ПЕШКА", "ПЛИТА", "ПОЕЗД", "ПОЛКА",
    "ПОРОГ", "ПОХОД", "ПОЧВА", "ПРАВО", "ПТИЦА", "ПЧЕЛА", "РЕЧКА", "РИФМА",
    "РЫНОК", "РЫБКА", "САНКИ", "САПОГ", "СВЕЧА", "СЕМЬЯ", "СКАЛА", "СЛЕЗА",
    "СЛИВА", "СМЕНА", "СОСНА", "СПИНА", "СТЕНА", "СТОЛБ", "СУМКА", "ТАЙНА",
    "ТАНЕЦ", "ТОЧКА", "ТРОПА", "ТУМАН", "ТЫКВА", "УЛИЦА", "ФАКЕЛ", "ФЕРМА",
    "ФОКУС", "ФРУКТ", "ХВОСТ", "ХОМЯК", "ЦАПЛЯ", "ЧАЙКА", "ЧАШКА", "ШАХТА",
    "ШЛЯПА", "ЩЁТКА", "ЯКОРЬ", "ЯГОДА", "АДРЕС", "КЛОУН", "КОРКА", "КОФТА",
    "КРЫША", "ОБМАН", "ОРГАН", "ПИРОГ", "РЕБРО", "СТАДО", "ТАПКА", "ТИГРА",
    "СЛОВА", "ЧИСЛА",
]
A7 = [
    "УЧЕБНИК", "ТЕТРАДЬ", "ДНЕВНИК", "ЛИНЕЙКА", "РЕЗИНКА", "ПРИМЕРЫ", "ЗАДАЧКА",
    "ОТМЕТКА", "ПЯТЁРКА", "РИСУНОК", "ПРОПИСЬ", "ФОРМУЛА", "ПРОЕКТЫ", "ДОКЛАДЫ",
    "РЕФЕРАТ", "ТАБЛИЦА", "АЛГЕБРА", "ДИКТАНТ", "ВОПРОСЫ", "УЧИТЕЛЬ", "ПРЕДМЕТ",
    "ПРИРОДА",
]
E7 = [
    "КОМНАТА", "КАРТИНА", "МАШИНКА", "КОРАБЛЬ", "САМОЛЁТ", "ТЕЛЕФОН", "РЕБЁНОК",
    "ДЕРЕВНЯ", "ГОРОДОК", "БАБОЧКА", "КОШЕЧКА", "СОБАЧКА", "МЕДВЕДЬ", "ВОРОБЕЙ",
    "СОЛОВЕЙ", "МОРКОВЬ", "КАПУСТА", "ПОМИДОР", "КОНФЕТА", "ПЕЧЕНЬЕ", "ПИРОЖОК",
    "БУЛОЧКА", "ВАРЕНЬЕ", "СМЕТАНА", "ШОКОЛАД", "ПОДАРОК", "ДОРОЖКА", "ПОЛЯНКА",
    "БЕРЁЗКА", "РОМАШКА", "ТЮЛЬПАН", "МАГАЗИН", "ДОКТОРА", "СОЛДАТЫ", "КАПИТАН",
    "ПЛАНЕТА", "СПУТНИК", "ОСТРОВА", "ПУСТЫНЯ", "ВОДОПАД", "ДЕВОЧКА", "МАЛЬЧИК",
    "БАБУШКА", "ДЕДУШКА", "ИГРУШКА",
]
A9 = [
    "ПЕРЕМЕНКА", "КАРАНДАШИ", "ГЕОГРАФИЯ", "ШКОЛЬНИКИ", "ШКОЛЬНИЦА", "ОТЛИЧНИЦА",
    "ОТЛИЧНИКИ", "ВЫПУСКНИК", "СОЧИНЕНИЕ", "УРАВНЕНИЕ", "ИЗЛОЖЕНИЕ", "ВЫЧИТАНИЕ",
    "УМНОЖЕНИЕ", "ОКОНЧАНИЕ", "ГЕОМЕТРИЯ", "РИСОВАНИЕ", "ДЕЖУРСТВО", "СПОРТЗАЛЫ",
]
E9 = [
    "КРОКОДИЛЫ", "ДИНОЗАВРЫ", "ЗЕМЛЯНИКА", "ВЕЛОСИПЕД", "МОТОЦИКЛЫ", "ТЕЛЕВИЗОР",
    "КОМПЬЮТЕР", "МИКРОСКОП", "АКВАРИУМЫ", "НАСЕКОМОЕ", "СУББОТНИК", "СНЕГОВИКИ",
    "МОРОЖЕНОЕ", "ШОКОЛАДКА", "БУТЕРБРОД", "АПЕЛЬСИНЫ", "МАНДАРИНЫ", "СМОРОДИНА",
    "БАКЛАЖАНЫ", "ПОДСОЛНУХ", "ОДУВАНЧИК", "НЕЗАБУДКА", "ПРОФЕССИЯ", "НАСЕЛЕНИЕ",
    "ЛАБИРИНТЫ", "КАРНАВАЛЫ", "ФЕЙЕРВЕРК", "ПРЕКРАСНО", "БЛАГОДАРЮ", "ПИРАМИДЫ",
]


def _norm(w):
    return w.replace("Ё", "Е")


def _pool(answers, extra, n):
    ans = list(dict.fromkeys(_norm(w) for w in answers if len(w) == n))
    valid = set(ans) | {_norm(w) for w in extra if len(w) == n}
    return ans, valid


POOLS = {
    5: _pool(A5, E5, 5),
    7: _pool(A7, E7, 7),
    9: _pool(A9, E9, 9),
}


def evaluate(guess, answer):
    res = ["absent"] * len(guess)
    pool = {}
    for i, (g, a) in enumerate(zip(guess, answer)):
        if g == a:
            res[i] = "correct"
        else:
            pool[a] = pool.get(a, 0) + 1
    for i, (g, a) in enumerate(zip(guess, answer)):
        if res[i] != "correct" and pool.get(g, 0) > 0:
            res[i] = "present"
            pool[g] -= 1
    return res


# ── Цвета (0..1 RGBA) ─────────────────────────────────────────────────────────
def rgba(h):
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)] + [1.0]


BG        = rgba("f4f5fb")
HDR       = rgba("6366f1")
HDR2      = rgba("4f51d8")
TEXT      = rgba("1e2230")
TEXT_DIM  = rgba("8b93a7")
TILE_BG   = rgba("ffffff")
TILE_IDLE = rgba("d7dbe7")
TILE_FILL = rgba("a3aab9")
KEY_BG    = rgba("e5e8f0")
ACCENT    = rgba("fbbf24")
WHITE     = rgba("ffffff")

THEMES = {
    False: {"correct": rgba("22c55e"), "present": rgba("f59e0b"), "absent": rgba("9aa3b5")},
    True:  {"correct": rgba("2563eb"), "present": rgba("f97316"), "absent": rgba("9aa3b5")},
}

# Раскладка QWERTY → ЙЦУКЕН (для физической клавиатуры на ПК при отладке)
LAT2RU = {
    "q": "Й", "w": "Ц", "e": "У", "r": "К", "t": "Е", "y": "Н", "u": "Г",
    "i": "Ш", "o": "Щ", "p": "З", "a": "Ф", "s": "Ы", "d": "В", "f": "А",
    "g": "П", "h": "Р", "j": "О", "k": "Л", "l": "Д", "z": "Я", "x": "Ч",
    "c": "С", "v": "М", "b": "И", "n": "Т", "m": "Ь",
}

KB_ROWS = ["ЙЦУКЕНГШЩЗХЪ", "ФЫВАПРОЛДЖЭ", "ЯЧСМИТЬБЮ"]


# ── Виджеты ───────────────────────────────────────────────────────────────────
class Tile(Label):
    """Клетка поля: скруглённый прямоугольник + буква."""

    def __init__(self, **kw):
        super().__init__(**kw)
        self.bold = True
        self.color = TEXT
        self.bg = list(TILE_BG)
        self.border = list(TILE_IDLE)
        self.halign = "center"
        self.valign = "middle"
        with self.canvas.before:
            self._col = Color(*self.bg)
            self._rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(6)])
            self._lcol = Color(*self.border)
            self._line = Line(width=dp(1.4))
        self.bind(pos=self._sync, size=self._sync)
        self._sync()

    def _sync(self, *a):
        self._rect.pos = self.pos
        self._rect.size = self.size
        self._line.rounded_rectangle = (self.x, self.y, self.width, self.height, dp(6))
        self.text_size = self.size
        self.font_size = min(self.width, self.height) * 0.46   # шрифт по размеру клетки

    def set_bg(self, color):
        self.bg = list(color)
        self._col.rgba = self.bg

    def set_border(self, color):
        self.border = list(color)
        self._lcol.rgba = self.border


class Key(Button):
    """Плоская кнопка клавиатуры."""

    def __init__(self, **kw):
        super().__init__(background_normal="", background_down="",
                         background_color=KEY_BG, color=TEXT, bold=True, **kw)
        with self.canvas.before:
            self._col = Color(*KEY_BG)
            self._rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(6)])
        self.background_color = (0, 0, 0, 0)
        self.bind(pos=self._sync, size=self._sync)

    def _sync(self, *a):
        self._rect.pos = self.pos
        self._rect.size = self.size

    def set_color(self, color):
        self._col.rgba = color


# ── Приложение ────────────────────────────────────────────────────────────────
class WoordleApp(App):
    ROWS = 6

    def build(self):
        self.title = "Woordle"
        Window.clearcolor = BG

        self.word_len = 5
        self.cols = 5
        self.answer = random.choice(POOLS[5][0])
        self.guesses = []
        self.results = []
        self.current = []
        self.over = False
        self.cb = False
        self.busy = False
        self.lstates = {}
        self.keys = {}
        self._msg_hide = None

        self.stats_file = os.path.join(self.user_data_dir, "stats.json")
        self.stats = self._load_stats()

        self.root = FloatLayout()
        main = BoxLayout(orientation="vertical")
        self.root.add_widget(main)

        # ── Верхняя панель ──
        bar = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(96),
                        padding=[dp(12), dp(8)], spacing=dp(6))
        with bar.canvas.before:
            Color(*HDR)
            self._bar_rect = RoundedRectangle(pos=bar.pos, size=bar.size, radius=[0])
        bar.bind(pos=lambda *a: setattr(self._bar_rect, "pos", bar.pos),
                 size=lambda *a: setattr(self._bar_rect, "size", bar.size))

        title = Label(text="[b]WOORDLE[/b]", markup=True, font_size=sp(22),
                      color=WHITE, size_hint_y=None, height=dp(34), halign="left")
        title.bind(size=lambda *a: setattr(title, "text_size", title.size))
        bar.add_widget(title)

        ctl = BoxLayout(orientation="horizontal", spacing=dp(6), size_hint_y=None,
                        height=dp(40))
        ctl.add_widget(Label(text="Длина:", color=rgba("c7d2fe"), font_size=sp(13),
                             size_hint_x=None, width=dp(60)))
        self.mode_keys = {}
        for n in (5, 7, 9):
            b = Key(text=str(n), font_size=sp(15), size_hint_x=None, width=dp(44))
            b.bind(on_release=lambda _b, x=n: self.set_mode(x))
            ctl.add_widget(b)
            self.mode_keys[n] = b
        ctl.add_widget(Widget())  # распорка
        self.cb_btn = Key(text="Дальтоник", font_size=sp(13))
        self.cb_btn.bind(on_release=lambda *a: self.toggle_cb())
        ctl.add_widget(self.cb_btn)
        bar.add_widget(ctl)
        main.add_widget(bar)

        # ── Поле ──
        self.grid_area = AnchorLayout(anchor_x="center", anchor_y="center")
        self.grid_area.bind(size=lambda *a: self._resize_grid())
        main.add_widget(self.grid_area)

        # ── Клавиатура ──
        self.kb = BoxLayout(orientation="vertical", size_hint_y=None,
                            height=dp(210), padding=[dp(6), dp(6)], spacing=dp(6))
        main.add_widget(self.kb)
        self._build_keyboard()

        # ── Сообщение (тост) ──
        self.msg = Label(text="", markup=True, font_size=sp(16), color=WHITE,
                         size_hint=(None, None), opacity=0,
                         pos_hint={"center_x": 0.5, "top": 0.86})
        self.root.add_widget(self.msg)

        # ── Кнопка «Новая игра» ──
        self.ng = Button(text="Новая игра", font_size=sp(16), bold=True,
                         background_normal="", background_color=rgba("22c55e"),
                         color=WHITE, size_hint=(None, None), size=(dp(200), dp(52)),
                         pos_hint={"center_x": 0.5, "center_y": 0.5}, opacity=0,
                         disabled=True)
        self.ng.bind(on_release=lambda *a: self.new_game())
        self.root.add_widget(self.ng)

        self._build_grid()
        self._update_mode_keys()

        Window.bind(on_key_down=self._on_key_down)
        return self.root

    # ── Клавиатура ──
    def _build_keyboard(self):
        for row in KB_ROWS:
            rb = BoxLayout(orientation="horizontal", spacing=dp(4))
            for ch in row:
                k = Key(text=ch, font_size=sp(16))
                k.bind(on_release=lambda _b, c=ch: self.tap_letter(c))
                rb.add_widget(k)
                self.keys[ch] = k
            self.kb.add_widget(rb)
        act = BoxLayout(orientation="horizontal", spacing=dp(6), size_hint_y=None,
                        height=dp(52))
        dele = Key(text="Стереть", font_size=sp(15))
        dele.bind(on_release=lambda *a: self.backspace())
        ent = Key(text="ВВОД", font_size=sp(16))
        ent.set_color(HDR)
        ent.color = WHITE
        ent.bind(on_release=lambda *a: self.enter())
        act.add_widget(dele)
        act.add_widget(ent)
        self.kb.add_widget(act)

    # ── Поле ──
    def _tile_size(self):
        """Размер клетки с учётом и ширины, и высоты доступной области."""
        aw = (self.grid_area.width or Window.width) * 0.96
        ah = (self.grid_area.height or (Window.height - dp(310))) * 0.96
        sp_ = dp(6)
        by_w = (aw - sp_ * (self.cols - 1)) / self.cols
        by_h = (ah - sp_ * (self.ROWS - 1)) / self.ROWS
        return max(dp(22), min(by_w, by_h, dp(62)))

    def _build_grid(self):
        self.grid_area.clear_widgets()
        spacing = dp(6)
        tile = self._tile_size()
        gw = tile * self.cols + spacing * (self.cols - 1)
        gh = tile * self.ROWS + spacing * (self.ROWS - 1)
        self.grid = GridLayout(cols=self.cols, rows=self.ROWS, spacing=spacing,
                               size_hint=(None, None), size=(gw, gh))
        self.tiles = []
        for r in range(self.ROWS):
            line = []
            for c in range(self.cols):
                t = Tile()                      # size_hint(1,1) — заполняет ячейку
                self.grid.add_widget(t)
                line.append(t)
            self.tiles.append(line)
        self.grid_area.add_widget(self.grid)

    def _resize_grid(self, *a):
        """Подгоняет размер сетки при изменении окна (плитки тянутся сами)."""
        if not getattr(self, "tiles", None):
            return
        spacing = dp(6)
        tile = self._tile_size()
        self.grid.size = (tile * self.cols + spacing * (self.cols - 1),
                          tile * self.ROWS + spacing * (self.ROWS - 1))

    # ── Ввод ──
    def tap_letter(self, ch):
        if self.busy or self.over or len(self.current) >= self.cols:
            return
        col = len(self.current)
        row = len(self.guesses)
        self.current.append(ch)
        t = self.tiles[row][col]
        t.text = ch
        t.set_border(TILE_FILL)
        Animation(font_size=t.font_size * 1.18, d=0.06).start(t)
        Animation(font_size=t.font_size, d=0.06).start(t)

    def backspace(self):
        if self.busy or self.over or not self.current:
            return
        self.current.pop()
        col = len(self.current)
        row = len(self.guesses)
        t = self.tiles[row][col]
        t.text = ""
        t.set_border(TILE_IDLE)

    def enter(self):
        if self.busy or self.over:
            return
        if len(self.current) != self.cols:
            self.show_msg("Нужно %d букв!" % self.cols)
            return
        word = "".join(self.current)
        if word not in POOLS[self.word_len][1]:
            self.show_msg("Такого слова нет в словаре!")
            return
        result = evaluate(word, self.answer)
        row = len(self.guesses)
        self.guesses.append(word)
        self.results.append(result)
        self.current = []
        self.busy = True
        self._reveal(row, word, result)

    # ── Раскрытие ряда ──
    def _reveal(self, row, word, result, col=0):
        if col >= self.cols:
            self.busy = False
            self._update_kb(word, result)
            if all(s == "correct" for s in result):
                self.win(row + 1)
            elif len(self.guesses) >= self.ROWS:
                self.lose()
            return
        t = self.tiles[row][col]
        color = THEMES[self.cb][result[col]]
        t.set_bg(color)
        t.set_border(color)
        t.color = WHITE
        Animation(font_size=t.font_size * 1.12, d=0.08).start(t)
        Animation(font_size=t.font_size, d=0.08).start(t)
        Clock.schedule_once(lambda *a: self._reveal(row, word, result, col + 1), 0.18)

    # ── Клавиатура: подсветка ──
    def _update_kb(self, word, result):
        pri = {"correct": 3, "present": 2, "absent": 1}
        th = THEMES[self.cb]
        for letter, state in zip(word, result):
            if pri.get(state, 0) > pri.get(self.lstates.get(letter, ""), 0):
                self.lstates[letter] = state
                if letter in self.keys:
                    self.keys[letter].set_color(th[state])
                    self.keys[letter].color = WHITE

    def _repaint_keys(self):
        th = THEMES[self.cb]
        for ch, k in self.keys.items():
            s = self.lstates.get(ch)
            k.set_color(th[s] if s else KEY_BG)
            k.color = WHITE if s else TEXT

    # ── Победа / поражение ──
    def win(self, n):
        self.over = True
        msgs = {1: "Невероятно! Пятёрка с плюсом!", 2: "Отлично! Пятёрка!",
                3: "Хорошо! Четвёрка!", 4: "Тройка с плюсом!",
                5: "Успел до звонка!", 6: "С шестой попытки — тройка!"}
        self.show_msg(msgs.get(n, "Молодец!"), rgba("22c55e"), 4)
        s = self.stats
        s["played"] += 1
        s["won"] += 1
        s["streak"] += 1
        s["max_streak"] = max(s["max_streak"], s["streak"])
        self._save_stats()
        Clock.schedule_once(lambda *a: self._show_ng(), 1.6)

    def lose(self):
        self.over = True
        self.show_msg("Загаданное слово: %s" % self.answer, rgba("ef4444"), 6)
        s = self.stats
        s["played"] += 1
        s["streak"] = 0
        self._save_stats()
        Clock.schedule_once(lambda *a: self._show_ng(), 1.6)

    def _show_ng(self):
        self.ng.disabled = False
        Animation(opacity=1, d=0.25).start(self.ng)

    # ── Новая игра ──
    def new_game(self):
        Animation(opacity=0, d=0.15).start(self.ng)
        self.ng.disabled = True
        self.answer = random.choice(POOLS[self.word_len][0])
        self.guesses = []
        self.results = []
        self.current = []
        self.over = False
        self.busy = False
        self.lstates = {}
        for row in self.tiles:
            for t in row:
                t.text = ""
                t.set_bg(TILE_BG)
                t.set_border(TILE_IDLE)
                t.color = TEXT
        self._repaint_keys()

    # ── Режимы ──
    def set_mode(self, n):
        if self.busy:
            return
        self.word_len = n
        self.cols = n
        self._update_mode_keys()
        self._build_grid()
        self.new_game()

    def _update_mode_keys(self):
        for n, b in self.mode_keys.items():
            if n == self.word_len:
                b.set_color(ACCENT)
                b.color = TEXT
            else:
                b.set_color(HDR2)
                b.color = WHITE

    def toggle_cb(self):
        self.cb = not self.cb
        # перекрасить уже открытые клетки
        for r, res in enumerate(self.results):
            for c, st in enumerate(res):
                col = THEMES[self.cb][st]
                self.tiles[r][c].set_bg(col)
                self.tiles[r][c].set_border(col)
        self._repaint_keys()

    # ── Сообщение ──
    def show_msg(self, text, bg=None, dur=2.2):
        if bg is None:
            bg = rgba("1e2230")
        self.msg.text = text
        self.msg.color = WHITE
        self.msg.texture_update()
        self.msg.size = (self.msg.texture_size[0] + dp(28),
                         self.msg.texture_size[1] + dp(18))
        self.msg.canvas.before.clear()
        with self.msg.canvas.before:
            Color(*bg)
            r = RoundedRectangle(pos=self.msg.pos, size=self.msg.size, radius=[dp(10)])
        self.msg.bind(pos=lambda *a: setattr(r, "pos", self.msg.pos),
                      size=lambda *a: setattr(r, "size", self.msg.size))
        Animation.cancel_all(self.msg)
        if self._msg_hide is not None:
            self._msg_hide.cancel()
        self.msg.opacity = 1
        self._msg_hide = Clock.schedule_once(
            lambda *a: Animation(opacity=0, d=0.4).start(self.msg), dur)

    # ── Физическая клавиатура (отладка на ПК) ──
    def _on_key_down(self, window, key, scancode, codepoint, modifiers):
        if key == 8:
            self.backspace(); return True
        if key in (13, 271):
            self.enter(); return True
        if not codepoint:
            return False
        ch = codepoint.upper()
        if ch == "Ё":
            ch = "Е"
        if ch not in self.keys:
            ch = LAT2RU.get(codepoint.lower(), "")
        if ch in self.keys:
            self.tap_letter(ch)
            return True
        return False

    # ── Статистика ──
    def _load_stats(self):
        try:
            with open(self.stats_file, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"played": 0, "won": 0, "streak": 0, "max_streak": 0}

    def _save_stats(self):
        try:
            with open(self.stats_file, "w", encoding="utf-8") as f:
                json.dump(self.stats, f, ensure_ascii=False)
        except Exception:
            pass


if __name__ == "__main__":
    WoordleApp().run()
