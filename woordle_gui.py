# -*- coding: utf-8 -*-
"""Woordle GUI — Школьная версия Wordle"""

import tkinter as tk
from tkinter import font as tkfont
import random, json, os, sys

# ── Слова по режимам: 5 / 7 / 9 букв ──────────────────────────────────────────
# Для каждого режима: ANSWERS — что загадывается (школьная тематика),
# EXTRA — дополнительные допустимые слова для ввода.

A5 = [
    "КЛАСС", "ДОСКА", "ПАРТА", "КНИГА", "РУЧКА",
    "ПЕНАЛ", "ШКОЛА", "НАУКА", "СПОРТ", "ФОРМА",
    "КАРТА", "АТЛАС", "ТЕКСТ", "СЛОВО", "ЧИСЛО",
    "ХИМИЯ", "ЗАЧЁТ", "БУФЕТ", "ЦИФРА", "БУКВА",
    "ГЛАВА", "ЭКРАН", "ОСЕНЬ", "ВЕСНА", "ОТВЕТ",
    "УЧЁБА", "МЕЛОК", "КИСТЬ", "ЗАДАЧ", "УСПЕХ",
    "УРОКА", "ПАРТЫ", "КНИГИ", "НОТКА", "БАЛЛА",
    "ЦВЕТА", "СХЕМА", "ЛИНЗА", "ДОСКИ", "ОЛИМП",
]
E5 = [
    "БЕРЕГ", "БЕРЁТ", "БИЛЕТ", "БЛЮДО", "БОЧКА", "БЕГУН", "БЕЛКА",
    "БОБЁР", "БУГОР", "ВАГОН", "ВАННА", "ВЕТЕР", "ВИЛКА", "ВИШНЯ",
    "ВОЛНА", "ВЫХОД", "ГАЗОН", "ГАММА", "ГЛАДЬ", "ГЛИНА", "ГОРКА",
    "ГРОЗА", "ГУБКА", "ДАВКА", "ДЕКАН", "ДИВАН", "ДОМИК", "ДОЧКА",
    "ДОЖДЬ", "ЖИВОТ", "ЖИЗНЬ", "ЗАБОР", "ЗАВОД", "ЗАЙКА", "ЗАКАТ",
    "ЗАМОК", "ЗАПАХ", "ЗЕМЛЯ", "ЗЕБРА", "ЗВЕРЬ", "ЗВЕНО", "ЗЕФИР",
    "ЗУБОК", "ИСКРА", "ИТОГО", "КАДРЫ", "КАПЛЯ", "КАТОК", "КОБРА",
    "КОРНИ", "КОПЫТ", "КОШКА", "КРОХА", "КУБИК", "КУКЛА", "КУПОЛ",
    "ЛАЗЕР", "ЛАРЕЦ", "ЛАПКА", "ЛАСКА", "ЛЕНТА", "ЛЕПКА", "ЛЕСОК",
    "ЛИМОН", "ЛИАНА", "ЛОДКА", "ЛОЖКА", "ЛОМКА", "ЛУНКА", "МАЙКА",
    "МАРКА", "МАСКА", "МАСЛО", "МАЧТА", "МЕСТО", "МЕТКА", "МЕТРО",
    "МЕЧТА", "МИСКА", "МИШКА", "МОНАХ", "МОРОЗ", "МОТОР", "МУСОР",
    "МЫШКА", "НАБОР", "НАПОР", "НИТКА", "НОМЕР", "НОРКА", "НОСОК",
    "ОБЛИК", "ОБЪЁМ", "ОВРАГ", "ОГОНЬ", "ОЛЕНЬ", "ОЛИВА",
    "ОСИНА", "ОТРЯД", "ОХОТА", "ПАКЕТ", "ПАЛКА", "ПАПКА", "ПАРУС",
    "ПАСТА", "ПАУЗА", "ПЕВЕЦ", "ПЕРЕЦ", "ПЕШКА", "ПЛАМЯ", "ПЛАСТ",
    "ПЛИТА", "ПОБЕГ", "ПОВАР", "ПОЕЗД", "ПОЛЁТ", "ПОЛКА", "ПОРОГ",
    "ПОХОД", "ПОЧВА", "ПОЧКА", "ПРАВО", "ПРИНЦ", "ПРУДЫ", "ПТИЦА",
    "ПЧЕЛА", "РАЗУМ", "РЕЧКА", "РИФМА", "РУБЕЖ", "РУБИН", "РУПОР",
    "РЫНОК", "РЫБАК", "РЫБКА", "РЫЧАГ", "РЯБИН", "САБЛЯ", "САНКИ",
    "САПОГ", "СВЕЧА", "СЕМЬЯ", "СИНИЙ", "СКАЛА", "СКЛОН", "СЛЕЗА",
    "СЛИВА", "СЛУГА", "СМЕНА", "СМОЛА", "СОЙКА", "СОКОЛ", "СОСНА",
    "СОТНЯ", "СПИНА", "СТЕНА", "СТОЛБ", "СТРИЖ", "СУДАК", "СУМКА",
    "СУРОК", "ТАЙГА", "ТАЙНА", "ТАНЕЦ", "ТАЧКА", "ТКАНЬ", "ТОСКА",
    "ТОЧКА", "ТРОПА", "ТУМАН", "ТУМБА", "ТУЛУП", "ТЫКВА", "ТЮБИК",
    "УКЛОН", "УКРОП", "УЛИЦА", "УМНИК", "УПРЁК", "ФАКЕЛ", "ФАУНА",
    "ФЕРМА", "ФЛОТА", "ФОКУС", "ФРУКТ", "ХВОСТ", "ХЛЕБА", "ХОМЯК",
    "ХОХОТ", "ХУТОР", "ЦАПЛЯ", "ЧАЙКА", "ЧАШКА", "ЧЕШУЯ", "ЧЕРВЬ",
    "ЧУДАК", "ШАКАЛ", "ШАЛАШ", "ШАХТА", "ШЛЯПА", "ШМЕЛЬ", "ШТРАФ",
    "ЩЁТКА", "ЩИПЦЫ", "ЯКОРЬ", "ЯСЕНЬ", "ЯГОДА",
    "АБЗАЦ", "АДРЕС", "АКТИВ", "АЛЛЕЯ", "ВЕПРЬ", "ВИХРЬ", "ЗИМОЙ",
    "КИРКА", "КЛОУН", "КОЗЁЛ", "КОРКА", "КОТИК", "КОФТА", "КРЫША",
    "ЛЕПТА", "НОВЫЙ", "НЕМОЙ",
    "ОБМАН", "ОПЫТЫ", "ОРГАН", "ПАЧКА", "ПИЛКА", "ПИРОГ", "ПЫШКА",
    "РЕБРО", "СИЛАЧ", "СКРИП", "СОВКА", "СТАДО", "СТУПА", "СУЧОК",
    "СЫЩИК", "ТАПКА", "ТИСКИ", "ТРАТА", "ТРЕНД", "ТИГРА", "ЧИПСЫ",
    "СЛОВА", "ЧИСЛА",
]

A7 = [
    "УЧЕБНИК", "ТЕТРАДЬ", "ДНЕВНИК", "ЛИНЕЙКА", "РЕЗИНКА",
    "ПРИМЕРЫ", "ЗАДАЧКА", "ОТМЕТКА", "ПЯТЁРКА", "РИСУНОК",
    "ПРОПИСЬ", "ФОРМУЛА", "ПРОЕКТЫ", "ДОКЛАДЫ", "РЕФЕРАТ",
    "ТАБЛИЦА", "АЛГЕБРА", "ДИКТАНТ", "ВОПРОСЫ", "УЧИТЕЛЬ",
    "ПРЕДМЕТ", "ПРИРОДА",
]
E7 = [
    "КОМНАТА", "КАРТИНА", "МАШИНКА", "КОРАБЛЬ", "САМОЛЁТ", "ТЕЛЕФОН",
    "РЕБЁНОК", "ДЕРЕВНЯ", "ГОРОДОК", "БАБОЧКА", "КОШЕЧКА", "СОБАЧКА",
    "МЕДВЕДЬ", "ВОРОБЕЙ", "ВОРОНКА", "СОЛОВЕЙ", "ЛЕСНИКИ", "МОРКОВЬ",
    "КАПУСТА", "ПОМИДОР", "КОНФЕТА", "ПЕЧЕНЬЕ", "ПИРОЖОК", "БУЛОЧКА",
    "ВАРЕНЬЕ", "СМЕТАНА", "ШОКОЛАД", "ПОДАРОК", "ДОРОЖКА", "ПОЛЯНКА",
    "БЕРЁЗКА", "РОМАШКА", "ТЮЛЬПАН", "КОЛОКОЛ", "МАГАЗИН", "ДОКТОРА",
    "МИЛИЦИЯ", "СОЛДАТЫ", "КАПИТАН", "МАТРОСЫ", "ЛЁТЧИКИ", "ПЛАНЕТА",
    "СПУТНИК", "ВУЛКАНЫ", "ОСТРОВА", "ПУСТЫНЯ", "РЕЧУШКА", "БОЛОТЦЕ",
    "ВОДОПАД", "КАРАМЕЛ", "ТРОПИНК", "КАРТОЧК", "ГОЛОВКА", "ЯБЛОЧКО",
    "ДЕВОЧКА", "МАЛЬЧИК", "БАБУШКА", "ДЕДУШКА", "СЕСТРИЦ", "ИГРУШКА",
]

A9 = [
    "ПЕРЕМЕНКА", "КАРАНДАШИ", "ГЕОГРАФИЯ", "ШКОЛЬНИКИ", "ШКОЛЬНИЦА",
    "ОТЛИЧНИЦА", "ОТЛИЧНИКИ", "ВЫПУСКНИК", "СОЧИНЕНИЕ", "УРАВНЕНИЕ",
    "ИЗЛОЖЕНИЕ", "ВЫЧИТАНИЕ", "УМНОЖЕНИЕ", "ОКОНЧАНИЕ", "СКАЗУЕМОЕ",
    "ГЕОМЕТРИЯ", "РИСОВАНИЕ", "ДЕЖУРСТВО", "СПОРТЗАЛЫ",
]
E9 = [
    "КРОКОДИЛЫ", "ДИНОЗАВРЫ", "ЗЕМЛЯНИКА", "ВЕЛОСИПЕД", "МОТОЦИКЛЫ",
    "ТЕЛЕВИЗОР", "КОМПЬЮТЕР", "МИКРОСКОП", "АКВАРИУМЫ", "НАСЕКОМОЕ",
    "СУББОТНИК", "СНЕГОВИКИ", "МОРОЖЕНОЕ", "ШОКОЛАДКА", "БУТЕРБРОД",
    "АПЕЛЬСИНЫ", "МАНДАРИНЫ", "СМОРОДИНА", "БАКЛАЖАНЫ", "ПОДСОЛНУХ",
    "ОДУВАНЧИК", "НЕЗАБУДКА", "ПРОФЕССИЯ", "НАСЕЛЕНИЕ", "ЛАБИРИНТЫ",
    "КАРНАВАЛЫ", "ФЕЙЕРВЕРК", "ПРЕКРАСНО", "БЛАГОДАРЮ", "КАПИТАНЫ",
    "ПУТЕШЕСТ", "ВЕЛИКОЛЕ", "ЧЕМПИОНЫ", "ПИРАМИДЫ", "КОНТИНЕН",
]


def _norm(w):
    """Ё ≡ Е — на клавиатуре нет отдельной Ё."""
    return w.replace("Ё", "Е")

def _pool(answers, extra, n):
    ans   = list(dict.fromkeys(_norm(w) for w in answers if len(w) == n))
    valid = set(ans) | {_norm(w) for w in extra if len(w) == n}
    return ans, valid

POOLS = {
    5: _pool(A5, E5, 5),
    7: _pool(A7, E7, 7),
    9: _pool(A9, E9, 9),
}

# Раскладка QWERTY → ЙЦУКЕН: ввод работает при любой активной раскладке
LAT2RU = {
    "q": "Й", "w": "Ц", "e": "У", "r": "К", "t": "Е", "y": "Н",
    "u": "Г", "i": "Ш", "o": "Щ", "p": "З", "[": "Х", "]": "Ъ",
    "a": "Ф", "s": "Ы", "d": "В", "f": "А", "g": "П", "h": "Р",
    "j": "О", "k": "Л", "l": "Д", ";": "Ж", "'": "Э",
    "z": "Я", "x": "Ч", "c": "С", "v": "М", "b": "И", "n": "Т",
    "m": "Ь", ",": "Б", ".": "Ю",
}

# ── Цвета (современная палитра: индиго + прохладные нейтрали) ─────────────────
BG            = "#f4f5fb"   # светлый прохладный фон
HDR_BG        = "#6366f1"   # индиго (фирменный акцент)
HDR_BG2       = "#4f51d8"   # кнопки в шапке
HDR_HOVER     = "#4338ca"   # кнопки шапки при наведении
HDR_FG        = "#ffffff"
HDR_SUB       = "#c7d2fe"   # подзаголовок/подписи на индиго
ACCENT        = "#fbbf24"   # янтарный акцент (активный режим)
TILE_BG       = "#ffffff"
TILE_IDLE_OUT = "#d7dbe7"
TILE_FILL_OUT = "#a3aab9"
TEXT          = "#1e2230"
TEXT_DIM      = "#8b93a7"
KEY_BG        = "#e5e8f0"
KEY_HOVER     = "#d3d8e6"
KEY_TEXT      = "#1e2230"
KEY_ENTER_BG  = "#6366f1"
KEY_ENTER_HV  = "#4f51d8"
SEP_COLOR     = "#e4e7f1"
SURFACE       = "#eceef6"
GREEN_BTN     = "#22c55e"
GREEN_BTN_HV  = "#16a34a"
CHEAT_BG      = "#1e2230"   # секретная плашка
CHEAT_FG      = "#34d399"

# Размер плитки и зазор подбираются под длину слова
TILE_BY_LEN = {5: 72, 7: 64, 9: 56}
TILE_GAP    = 8

THEMES = {
    False: dict(correct="#22c55e", present="#f59e0b", absent="#9aa3b5"),
    True:  dict(correct="#2563eb", present="#f97316", absent="#9aa3b5"),
}

def resource_path(name):
    """Путь к ресурсу: рядом со скриптом или внутри PyInstaller-бандла."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)

def data_dir():
    """Папка для записи (stats.json): рядом с .exe или со скриптом."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

STATS_FILE = os.path.join(data_dir(), "stats.json")
ICON_FILE  = resource_path("woordle.ico")

def load_stats():
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"played": 0, "won": 0, "streak": 0, "max_streak": 0,
            "guesses": {str(i): 0 for i in range(1, 7)}}

def save_stats(s):
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(s, f, ensure_ascii=False, indent=2)

def evaluate(guess, answer):
    res  = ["absent"] * len(guess)
    pool = {}
    for i, (g, a) in enumerate(zip(guess, answer)):
        if g == a: res[i] = "correct"
        else: pool[a] = pool.get(a, 0) + 1
    for i, (g, a) in enumerate(zip(guess, answer)):
        if res[i] != "correct" and pool.get(g, 0) > 0:
            res[i] = "present"; pool[g] -= 1
    return res


# ── Приложение ────────────────────────────────────────────────────────────────
class WoordleApp:
    ROWS = 6

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Woordle — Школьная версия")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)
        try:
            if os.path.exists(ICON_FILE):
                self.root.iconbitmap(ICON_FILE)
        except Exception:
            pass

        self.word_len = 5
        self.COLS     = 5
        self.answer  = random.choice(POOLS[self.word_len][0])
        self.guesses : list[str]       = []
        self.results : list[list[str]] = []
        self.current : list[str]       = []
        self.over    = False
        self.cb      = False
        self.anim    = False
        self.stats   = load_stats()
        self.lstates : dict[str, str]  = {}
        self._toast_job  = None
        self._cheat_buf  : list[str]   = []   # буфер для секретной комбинации
        self._cheat_show = False

        F = lambda s, w="normal": tkfont.Font(family="Segoe UI", size=s, weight=w)
        self.fKey   = F(13, "bold")
        self.fTitle = F(20, "bold")
        self.fSub   = F(11)
        self.fMd    = F(12)
        self.fSm    = F(10)
        # Размер плитки/шрифта — зависят от режима
        self.tile_size = TILE_BY_LEN[self.word_len]
        self.fTile     = F(int(self.tile_size * 0.42), "bold")

        self._build()
        self.root.bind("<Key>", self._key)

    # ── Построение UI ─────────────────────────────────────────────────────────

    def _build(self):
        # ── Шапка (полная ширина) ──
        hdr = tk.Frame(self.root, bg=HDR_BG, pady=16)
        hdr.pack(fill="x", side="top")

        left = tk.Frame(hdr, bg=HDR_BG)
        left.pack(side="left", padx=26)
        tk.Label(left, text="📚  WOORDLE", font=self.fTitle,
                 bg=HDR_BG, fg=HDR_FG).pack(anchor="w")
        tk.Label(left, text="Угадай школьное слово за 6 попыток",
                 font=self.fSub, bg=HDR_BG, fg=HDR_SUB).pack(anchor="w")

        # ── Переключатель режимов (5 / 7 / 9 букв) ──
        mid = tk.Frame(hdr, bg=HDR_BG)
        mid.pack(side="left", padx=30)
        tk.Label(mid, text="Длина слова:", font=self.fSub,
                 bg=HDR_BG, fg=HDR_SUB).pack(side="left", padx=(0, 8))
        self.mode_btns: dict[int, tk.Button] = {}
        for n in (5, 7, 9):
            b = tk.Button(mid, text=str(n), command=lambda x=n: self._set_mode(x),
                          font=tkfont.Font(family="Segoe UI", size=12, weight="bold"),
                          relief="flat", padx=14, pady=6, cursor="hand2",
                          bd=0, width=2)
            b.pack(side="left", padx=3)
            self.mode_btns[n] = b
        self._update_mode_buttons()

        right = tk.Frame(hdr, bg=HDR_BG)
        right.pack(side="right", padx=22)
        for label, cmd in [("❓  Правила", self._help),
                            ("📊  Статистика", self._stats)]:
            b = tk.Button(right, text=label, command=cmd,
                          bg=HDR_BG2, fg=HDR_FG, relief="flat",
                          font=self.fSub, padx=14, pady=7, cursor="hand2",
                          activebackground=HDR_HOVER, activeforeground=HDR_FG,
                          bd=0)
            b.pack(side="left", padx=4)
            self._hover(b, HDR_BG2, HDR_HOVER)
        self.cb_btn = tk.Button(right, text="👁  Дальтоник",
                                command=self._toggle_cb,
                                bg=HDR_BG2, fg=HDR_FG, relief="flat",
                                font=self.fSub, padx=14, pady=7, cursor="hand2",
                                activebackground=HDR_HOVER, activeforeground=HDR_FG,
                                bd=0)
        self.cb_btn.pack(side="left", padx=4)

        # ── Золотая акцентная полоса под шапкой ──
        tk.Frame(self.root, bg=ACCENT, height=3).pack(fill="x", side="top")

        # ── Весь остаток экрана — центрирующий контейнер ──
        outer = tk.Frame(self.root, bg=BG)
        outer.pack(expand=True, fill="both", side="top")

        # Toast поверх всего
        self.toast = tk.Label(self.root, text="", bg="#1e2230", fg="#ffffff",
                              font=self.fMd, padx=18, pady=8)
        self._toast_job = None

        # Центральный столбец
        center = tk.Frame(outer, bg=BG)
        center.pack(expand=True)           # pack без fill → центрируется

        # ── Сетка (строится отдельным методом, чтобы пересоздавать) ──
        self.grid_holder = tk.Frame(center, bg=BG, pady=18)
        self.grid_holder.pack()
        self._build_grid()

        # ── Разделитель ──
        tk.Frame(center, bg=SEP_COLOR, height=1).pack(fill="x", padx=10)

        # ── Клавиатура ──
        self.kbtns: dict[str, tk.Button] = {}
        kf = tk.Frame(center, bg=BG, pady=14)
        kf.pack()
        for row_str in ["ЙЦУКЕНГШЩЗХЪ", "ФЫВАПРОЛДЖЭ", "ЯЧСМИТЬБЮ"]:
            rf = tk.Frame(kf, bg=BG)
            rf.pack(pady=3)
            for ch in row_str:
                b = tk.Button(rf, text=ch, bg=KEY_BG, fg=KEY_TEXT,
                              font=self.fKey, relief="flat",
                              padx=8, pady=10, cursor="hand2",
                              activebackground=KEY_HOVER, activeforeground=KEY_TEXT,
                              command=lambda l=ch: self._letter(l))
                b.pack(side="left", padx=3)
                self.kbtns[ch] = b

        af = tk.Frame(kf, bg=BG)
        af.pack(pady=(8, 3))
        del_btn = tk.Button(af, text="⌫  Удалить", bg=KEY_BG, fg=KEY_TEXT,
                  font=self.fSub, relief="flat", padx=20, pady=11,
                  cursor="hand2", activebackground=KEY_HOVER,
                  command=self._backspace)
        del_btn.pack(side="left", padx=4)
        self._hover(del_btn, KEY_BG, KEY_HOVER)
        ent_btn = tk.Button(af, text="ВВОД  ↵", bg=KEY_ENTER_BG, fg="#ffffff",
                  font=tkfont.Font(family="Segoe UI", size=11, weight="bold"),
                  relief="flat", padx=20, pady=11,
                  cursor="hand2", activebackground=KEY_ENTER_HV,
                  command=self._enter)
        ent_btn.pack(side="right", padx=4)
        self._hover(ent_btn, KEY_ENTER_BG, KEY_ENTER_HV)

        # ── Секретный ярлык с ответом (скрыт, комбинация zxc) ──
        self._cheat_lbl = tk.Label(
            self.root,
            text="", font=tkfont.Font(family="Consolas", size=13, weight="bold"),
            bg=CHEAT_BG, fg=CHEAT_FG,
            padx=14, pady=8, relief="flat",
        )

        # ── Кнопка «Новая игра» (скрыта) ──
        self.ng_btn = tk.Button(center, text="🔄  Начать новую игру",
                                command=self._new_game,
                                bg=GREEN_BTN, fg="#ffffff", font=self.fMd,
                                relief="flat", padx=28, pady=12, cursor="hand2",
                                activebackground=GREEN_BTN_HV)
        self._hover(self.ng_btn, GREEN_BTN, GREEN_BTN_HV)

        # ── Подсказка-подвал ──
        tk.Label(center, text="🎹  Печатай слово на клавиатуре  ·  ↵ ВВОД для проверки",
                 font=self.fSm, bg=BG, fg=TEXT_DIM).pack(side="bottom", pady=(0, 14))

    def _build_grid(self):
        """Создаёт (или пересоздаёт) холст с плитками под текущую длину слова."""
        for w in self.grid_holder.winfo_children():
            w.destroy()

        ts, gap = self.tile_size, TILE_GAP
        cw = self.COLS * (ts + gap) - gap
        ch = self.ROWS * (ts + gap) - gap
        self.cv = tk.Canvas(self.grid_holder, width=cw, height=ch,
                            bg=BG, highlightthickness=0)
        self.cv.pack()

        self.tiles: list[list] = []
        for r in range(self.ROWS):
            row = []
            for c in range(self.COLS):
                x0 = c * (ts + gap)
                y0 = r * (ts + gap)
                x1, y1 = x0 + ts, y0 + ts
                mx, my = x0 + ts // 2, y0 + ts // 2
                rid = self.cv.create_rectangle(x0, y0, x1, y1,
                      fill=TILE_BG, outline=TILE_IDLE_OUT, width=2)
                tid = self.cv.create_text(mx, my, text="",
                      font=self.fTile, fill=TEXT)
                row.append([rid, tid, x0, y0, x1, y1, mx, my])
            self.tiles.append(row)

    # ── Переключение режима (длины слова) ──────────────────────────────────────

    def _update_mode_buttons(self):
        for n, b in self.mode_btns.items():
            if n == self.word_len:
                b.config(bg=ACCENT, fg=TEXT,
                         activebackground=ACCENT, activeforeground=TEXT)
            else:
                b.config(bg=HDR_BG2, fg=HDR_FG,
                         activebackground=HDR_HOVER, activeforeground=HDR_FG)

    def _set_mode(self, n):
        if self.anim:
            return
        self.word_len  = n
        self.COLS      = n
        self.tile_size = TILE_BY_LEN[n]
        self.fTile.configure(size=int(self.tile_size * 0.42))
        self._update_mode_buttons()
        self._build_grid()
        self._new_game()

    # ── Ввод ──────────────────────────────────────────────────────────────────

    def _key(self, event):
        if self.anim: return
        k = event.keysym

        # Секретная комбинация z → x → c — ТОЛЬКО на латинской раскладке.
        # На русской раскладке эти клавиши дают keysym вида "Cyrillic_ya",
        # поэтому в буфер попадают только ASCII-латинские буквы.
        if len(k) == 1 and k.lower() in "abcdefghijklmnopqrstuvwxyz":
            self._cheat_buf.append(k.lower())
            if len(self._cheat_buf) > 3:
                self._cheat_buf.pop(0)
            if self._cheat_buf == ["z", "x", "c"]:
                self._cheat_buf.clear()
                self._toggle_cheat()
        else:
            self._cheat_buf.clear()

        if k == "BackSpace":
            self._backspace(); return
        if k in ("Return", "KP_Enter"):
            self._enter(); return

        # Определяем введённую букву независимо от раскладки
        ch = (event.char or "").upper()
        if ch == "Ё":
            ch = "Е"
        if ch not in self.kbtns:                       # не русская раскладка —
            low = (event.char or "").lower()
            if low in ("z", "x", "c"):                 # латинские z/x/c —
                return                                 # только чит, букву не вводим
            ch = LAT2RU.get(low, "")                    # остальное мапим по позиции
        if ch in self.kbtns:
            self._letter(ch)

    def _letter(self, ch):
        if self.anim or self.over or len(self.current) >= self.COLS: return
        col = len(self.current); row = len(self.guesses)
        self.current.append(ch)
        t = self.tiles[row][col]
        self.cv.itemconfig(t[0], outline=TILE_FILL_OUT, fill=TILE_BG)
        self.cv.itemconfig(t[1], text=ch)
        self._pop(row, col)

    def _backspace(self):
        if self.anim or self.over or not self.current: return
        col = len(self.current) - 1; row = len(self.guesses)
        self.current.pop()
        t = self.tiles[row][col]
        self.cv.itemconfig(t[0], outline=TILE_IDLE_OUT, fill=TILE_BG)
        self.cv.itemconfig(t[1], text="")

    def _enter(self):
        if self.anim or self.over: return
        if len(self.current) != self.COLS:
            self._shake(len(self.guesses))
            self._toast_show(f"Нужно ровно {self.COLS} букв!")
            return
        word = "".join(self.current)
        if word not in POOLS[self.word_len][1]:
            self._shake(len(self.guesses))
            self._toast_show("Такого слова нет в словаре!")
            return
        result = evaluate(word, self.answer)
        row    = len(self.guesses)
        self.guesses.append(word)
        self.results.append(result)
        self.current = []
        self.anim    = True
        self._flip_row(row, result, word)

    # ── Анимации ──────────────────────────────────────────────────────────────

    def _pop(self, row, col, step=0):
        seq = [0, -5, -8, -5, 0]
        if step >= len(seq): return
        t  = self.tiles[row][col]
        x0, y0, x1, y1, mx, my = t[2], t[3], t[4], t[5], t[6], t[7]
        dy = seq[step]
        self.cv.coords(t[0], x0, y0+dy, x1, y1+dy)
        self.cv.coords(t[1], mx, my+dy)
        self.root.after(30, lambda: self._pop(row, col, step+1))

    def _shake(self, row, step=0):
        seq = [0, -9, 9, -7, 7, -4, 4, 0]
        if step >= len(seq): return
        dx = seq[step]
        for col in range(self.COLS):
            t = self.tiles[row][col]
            x0, y0, x1, y1, mx, my = t[2], t[3], t[4], t[5], t[6], t[7]
            self.cv.coords(t[0], x0+dx, y0, x1+dx, y1)
            self.cv.coords(t[1], mx+dx, my)
        self.root.after(40, lambda: self._shake(row, step+1))

    def _flip_row(self, row, result, word):
        theme = THEMES[self.cb]
        for col in range(self.COLS):
            clr = theme[result[col]]
            self.root.after(col * 290,
                            lambda c=col, cl=clr: self._flip(row, c, cl))
        def done():
            self.anim = False
            self._update_kb(word, result)
            if all(r == "correct" for r in result): self._win(row + 1)
            elif len(self.guesses) >= self.ROWS:    self._lose()
        self.root.after(self.COLS * 290 + 230, done)

    def _flip(self, row, col, color, step=0):
        N  = 9
        t  = self.tiles[row][col]
        x0, y0, x1, y1, mx = t[2], t[3], t[4], t[5], t[6]
        hw = self.tile_size // 2
        if step <= N:
            f = 1 - step / N
            self.cv.coords(t[0], mx - hw*f, y0, mx + hw*f, y1)
            if step == N:
                self.cv.itemconfig(t[0], fill=color, outline=color)
                self.cv.itemconfig(t[1], fill="#ffffff")
        elif step <= N * 2:
            f = (step - N) / N
            self.cv.coords(t[0], mx - hw*f, y0, mx + hw*f, y1)
        else:
            self.cv.coords(t[0], x0, y0, x1, y1)
            return
        self.root.after(18, lambda: self._flip(row, col, color, step+1))

    def _jump(self, row, col=0):
        if col >= self.COLS: return
        t = self.tiles[row][col]
        x0, y0, x1, y1, mx, my = t[2], t[3], t[4], t[5], t[6], t[7]
        def bounce(step=0):
            dy_seq = [0, -14, -24, -14, 0]
            if step >= len(dy_seq): return
            dy = dy_seq[step]
            self.cv.coords(t[0], x0, y0+dy, x1, y1+dy)
            self.cv.coords(t[1], mx, my+dy)
            self.root.after(65, lambda: bounce(step+1))
        self.root.after(col * 90, bounce)
        self._jump(row, col+1)

    # ── Клавиатура ────────────────────────────────────────────────────────────

    def _update_kb(self, word, result):
        theme = THEMES[self.cb]
        pri   = {"correct": 3, "present": 2, "absent": 1}
        for letter, state in zip(word, result):
            if pri.get(state, 0) > pri.get(self.lstates.get(letter, ""), 0):
                self.lstates[letter] = state
                if letter in self.kbtns:
                    self.kbtns[letter].config(bg=theme[state], fg="#ffffff")

    def _repaint_kb(self):
        theme = THEMES[self.cb]
        for ch, btn in self.kbtns.items():
            s = self.lstates.get(ch)
            btn.config(bg=theme[s] if s else KEY_BG,
                       fg="#ffffff" if s else KEY_TEXT)

    def _repaint_tiles(self):
        theme = THEMES[self.cb]
        for r, (_, result) in enumerate(zip(self.guesses, self.results)):
            for c, state in enumerate(result):
                t = self.tiles[r][c]
                self.cv.itemconfig(t[0], fill=theme[state], outline=theme[state])

    # ── Секретная подсказка (zxc) ─────────────────────────────────────────────

    def _toggle_cheat(self):
        self._cheat_show = not self._cheat_show
        if self._cheat_show:
            self._cheat_lbl.config(text=f"🔑  {self.answer}")
            # Позиционируем в правом нижнем углу
            self._cheat_lbl.place(relx=1.0, rely=1.0,
                                  x=-16, y=-16, anchor="se")
            self._cheat_lbl.lift()
        else:
            self._cheat_lbl.place_forget()

    # ── Toast ──────────────────────────────────────────────────────────────────

    def _toast_show(self, msg, bg="#1e2230", ms=2400):
        if self._toast_job:
            self.root.after_cancel(self._toast_job)
        self.toast.config(text=msg, bg=bg)
        self.toast.place(relx=0.5, rely=0.0, y=90, anchor="n")
        self.toast.lift()
        self._toast_job = self.root.after(ms, self.toast.place_forget)

    # ── Победа / Поражение ────────────────────────────────────────────────────

    def _win(self, n):
        self.over = True
        msgs = {1: "🏆 Невероятно! Пятёрка с плюсом!",
                2: "🥇 Отлично! Заслуженная пятёрка!",
                3: "🎉 Хорошо! Крепкая четвёрка!",
                4: "😊 Тройка с плюсом — неплохо!",
                5: "😅 Уф, успел до звонка!",
                6: "😮 С шестой попытки — тройка!"}
        self._toast_show(msgs.get(n, "Молодец!"), bg=GREEN_BTN, ms=4500)
        self._jump(len(self.guesses) - 1)
        s = self.stats
        s["played"] += 1; s["won"] += 1; s["streak"] += 1
        s["max_streak"] = max(s["max_streak"], s["streak"])
        k = str(min(n, 6))
        s["guesses"][k] = s["guesses"].get(k, 0) + 1
        save_stats(s)
        self.root.after(2400, self._show_ng)

    def _lose(self):
        self.over = True
        self._toast_show(f"😢  Загаданное слово:  {self.answer}",
                         bg="#ef4444", ms=7000)
        s = self.stats; s["played"] += 1; s["streak"] = 0
        save_stats(s)
        self.root.after(2400, self._show_ng)

    def _show_ng(self):
        self.ng_btn.pack(pady=10)

    # ── Новая игра ────────────────────────────────────────────────────────────

    def _new_game(self):
        self.ng_btn.pack_forget()
        self.answer  = random.choice(POOLS[self.word_len][0])
        self.guesses = []; self.results = []; self.current = []
        self.over = self.anim = False; self.lstates = {}
        self._cheat_buf.clear()
        self._cheat_show = False
        self._cheat_lbl.place_forget()
        for row in self.tiles:
            for t in row:
                x0, y0, x1, y1, mx, my = t[2], t[3], t[4], t[5], t[6], t[7]
                self.cv.itemconfig(t[0], fill=TILE_BG, outline=TILE_IDLE_OUT, width=2)
                self.cv.itemconfig(t[1], text="", fill=TEXT)
                self.cv.coords(t[0], x0, y0, x1, y1)
                self.cv.coords(t[1], mx, my)
        for btn in self.kbtns.values():
            btn.config(bg=KEY_BG, fg=KEY_TEXT)

    # ── Режим дальтоника ──────────────────────────────────────────────────────

    def _toggle_cb(self):
        self.cb = not self.cb
        self.cb_btn.config(bg="#2563eb" if self.cb else HDR_BG2)
        self._repaint_tiles()
        self._repaint_kb()

    # ── Hover-эффект ──────────────────────────────────────────────────────────

    @staticmethod
    def _hover(btn, normal, hover):
        btn.bind("<Enter>", lambda e: btn.config(bg=hover))
        btn.bind("<Leave>", lambda e: btn.config(bg=normal))

    # ── Утилиты для диалогов ──────────────────────────────────────────────────

    def _dialog(self, title, w):
        """Создаёт модальное окно фиксированной ширины; высота — по контенту."""
        win = tk.Toplevel(self.root)
        win.title(title); win.configure(bg=BG)
        win.resizable(False, False); win.grab_set()
        win.transient(self.root)
        win._dlg_w = w
        return win

    def _dlg_finalize(self, win):
        """Подгоняет высоту окна под содержимое и центрирует на экране."""
        win.update_idletasks()
        w = win._dlg_w
        h = win.winfo_reqheight()
        sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
        rx, ry = self.root.winfo_x(), self.root.winfo_y()
        rw, rh = self.root.winfo_width(), self.root.winfo_height()
        x = rx + (rw - w) // 2
        y = ry + (rh - h) // 2
        x = max(10, min(x, sw - w - 10))
        y = max(10, min(y, sh - h - 40))
        win.geometry(f"{w}x{h}+{x}+{y}")

    def _dlg_header(self, win, text):
        hf = tk.Frame(win, bg=HDR_BG, pady=16)
        hf.pack(fill="x")
        tk.Label(hf, text=text, font=self.fTitle,
                 bg=HDR_BG, fg=HDR_FG).pack()
        tk.Frame(win, bg=ACCENT, height=3).pack(fill="x")

    def _dlg_close(self, win, text="Закрыть"):
        wrap = tk.Frame(win, bg=BG)
        wrap.pack(fill="x", pady=(8, 16))
        btn = tk.Button(wrap, text=text, command=win.destroy,
                        bg=HDR_BG, fg=HDR_FG, font=self.fMd, relief="flat",
                        padx=28, pady=11, cursor="hand2",
                        activebackground=HDR_HOVER)
        btn.pack()
        self._hover(btn, HDR_BG, HDR_HOVER)

    # ── Статистика ────────────────────────────────────────────────────────────

    def _stats(self):
        win = self._dialog("Статистика", 520)
        s   = self.stats
        pct = round(100 * s["won"] / s["played"]) if s["played"] else 0

        self._dlg_header(win, "📊  Статистика")

        # Числа-карточки
        nf = tk.Frame(win, bg=BG, pady=16)
        nf.pack(fill="x", padx=20)
        for val, lbl in [(s["played"], "Сыграно"), (s["won"], "Победы"),
                         (f"{pct}%", "% побед"), (s["max_streak"], "Рекорд")]:
            cf = tk.Frame(nf, bg=SURFACE, padx=12, pady=12)
            cf.pack(side="left", expand=True, fill="x", padx=5)
            tk.Label(cf, text=str(val),
                     font=tkfont.Font(family="Segoe UI", size=26, weight="bold"),
                     bg=SURFACE, fg=HDR_BG).pack()
            tk.Label(cf, text=lbl, font=self.fSm,
                     bg=SURFACE, fg=TEXT_DIM).pack()

        tk.Frame(win, bg=SEP_COLOR, height=1).pack(fill="x", padx=24, pady=8)
        tk.Label(win, text="РАСПРЕДЕЛЕНИЕ ПОПЫТОК",
                 font=self.fSub, bg=BG, fg=TEXT_DIM).pack(pady=(4, 6))

        max_v   = max(s["guesses"].values(), default=1) or 1
        bar_clr = THEMES[self.cb]["correct"]
        for i in range(1, 7):
            cnt = s["guesses"].get(str(i), 0)
            bf  = tk.Frame(win, bg=BG)
            bf.pack(fill="x", padx=32, pady=3)
            tk.Label(bf, text=str(i), font=self.fMd, bg=BG,
                     fg=TEXT, width=2, anchor="e").pack(side="left")
            bw = max(6, int(280 * cnt / max_v)) if cnt else 6
            bar = tk.Frame(bf, bg=bar_clr if cnt else SEP_COLOR, height=26)
            bar.pack(side="left", padx=8)
            bar.configure(width=bw); bar.pack_propagate(False)
            tk.Label(bf, text=str(cnt), font=self.fMd,
                     bg=BG, fg=TEXT).pack(side="left")

        tk.Frame(win, bg=SEP_COLOR, height=1).pack(fill="x", padx=24, pady=10)
        streak_txt = (f"🔥  Серия побед: {s['streak']}"
                      if s["streak"] else "Серия пока пуста — начни её прямо сейчас!")
        tk.Label(win, text=streak_txt, font=self.fMd, bg=BG, fg=HDR_BG,
                 ).pack(pady=2)
        self._dlg_close(win)
        self._dlg_finalize(win)

    # ── Правила ───────────────────────────────────────────────────────────────

    def _help(self):
        win = self._dialog("Правила", 520)
        self._dlg_header(win, "❓  Как играть")

        body = tk.Frame(win, bg=BG)
        body.pack(fill="both", expand=True, padx=30, pady=14)

        for txt in ["Угадай школьное 5-буквенное слово за 6 попыток.",
                    "После каждой попытки плитки меняют цвет:"]:
            tk.Label(body, text=txt, font=self.fMd, bg=BG, fg=TEXT,
                     anchor="w", wraplength=450, justify="left"
                     ).pack(fill="x", pady=3)

        # Карточки-примеры цветов
        theme = THEMES[self.cb]
        eg = tk.Frame(body, bg=BG, pady=4)
        eg.pack(fill="x", pady=(6, 4))
        for letter, state, desc in [
            ("К", "correct", "буква на правильном месте"),
            ("Н", "present", "буква есть, но стоит не здесь"),
            ("Г", "absent",  "такой буквы нет в слове"),
        ]:
            ef = tk.Frame(eg, bg=BG, pady=4)
            ef.pack(fill="x")
            tk.Label(ef, text=f" {letter} ",
                     font=tkfont.Font(family="Segoe UI", size=18, weight="bold"),
                     bg=theme[state], fg="#ffffff", width=3,
                     padx=4, pady=8).pack(side="left")
            tk.Label(ef, text=f"   {desc}", font=self.fMd,
                     bg=BG, fg=TEXT).pack(side="left")

        tk.Frame(body, bg=SEP_COLOR, height=1).pack(fill="x", pady=12)

        for tip in [
            "🎹   Печатай с клавиатуры или нажимай буквы на экране.",
            "⌫    «Удалить» стирает последнюю введённую букву.",
            "↵    «ВВОД» отправляет слово на проверку.",
            "📖   Вводить можно только слова из словаря.",
            "👁    Дальтоник меняет цвета на синий и оранжевый.",
            "📊   Статистика хранит историю всех партий.",
        ]:
            tk.Label(body, text=tip, font=self.fMd, bg=BG, fg=TEXT,
                     anchor="w", justify="left").pack(fill="x", pady=4)

        self._dlg_close(win, "Всё ясно, играть!  🎓")
        self._dlg_finalize(win)


# ── Запуск ────────────────────────────────────────────────────────────────────

def main():
    root = tk.Tk()

    # Полный экран (развёрнутое окно) на Windows
    if sys.platform == "win32":
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass
        root.state("zoomed")

    WoordleApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
