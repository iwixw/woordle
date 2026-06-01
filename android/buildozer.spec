[app]

# Название и пакет
title = Woordle
package.name = woordle
package.domain = org.woordle

# Исходники
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json
version = 1.0

# Зависимости (Kivy тянет за собой всё нужное)
requirements = python3,kivy==2.3.0

# Версия python-for-android: тег v2024.01.21 собирает Python 3.11.5.
# Без этого buildozer берёт p4a master (Python 3.14), под который Kivy 2.3.0
# не компилируется (_PyInterpreterState_GetConfig и пр.).
p4a.branch = v2024.01.21

# Иконка и заставка (PNG рядом с main.py)
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/icon.png

# Ориентация и вид
orientation = portrait
fullscreen = 0

[android]

# Версии API: 31+ требует Google Play; 21 — минимально поддерживаемая
android.api = 33
android.minapi = 21
android.archs = arm64-v8a

# Разрешения не нужны (игра офлайн, без сети/файлов вне песочницы)
android.permissions =

# Принять лицензии SDK автоматически при сборке
android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1
