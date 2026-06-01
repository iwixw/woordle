# Woordle для Android

Версия игры на **Kivy** для сборки в `.apk`. APK собирается **только под Linux**
(Buildozer), поэтому ниже — три способа собрать без покупки Linux-машины.

## Файлы
- `main.py` — приложение (Buildozer требует, чтобы точка входа называлась `main.py`)
- `buildozer.spec` — конфигурация сборки
- `icon.png` — иконка приложения (512×512)

Проверить логику/UI на ПК (нужен установленный Kivy):
```
pip install "kivy[base]==2.3.0"
python main.py
```

---

## Способ 1 — GitHub Actions (рекомендуется, ничего не ставить)

1. Создай репозиторий на GitHub и залей туда **всю папку проекта**
   (вместе с `android/` и `.github/workflows/build-apk.yml`).
2. Открой вкладку **Actions** → workflow «Build Android APK» → **Run workflow**.
   (или просто запушь — он стартует сам).
3. Через ~20–30 минут скачай готовый `.apk` в разделе **Artifacts**
   (имя артефакта `woordle-apk`).

Воркфлоу уже лежит в репозитории: `.github/workflows/build-apk.yml`.

---

## Способ 2 — Google Colab (бесплатно, в браузере)

Создай блокнот на https://colab.research.google.com и выполни ячейки:

```python
# 1) Установка
!sudo apt-get update -qq
!sudo apt-get install -y -qq zip unzip openjdk-17-jdk autoconf libtool pkg-config \
    zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
!pip install --quiet buildozer cython==0.29.36

# 2) Загрузи main.py, buildozer.spec, icon.png (кнопка «Files» слева → Upload)
#    и положи их в одну папку, например /content/android
%cd /content/android

# 3) Сборка (первый раз ~20-40 мин — качает Android SDK/NDK)
!yes | buildozer android debug

# 4) Скачать APK
from google.colab import files
import glob
files.download(glob.glob('bin/*.apk')[0])
```

---

## Способ 3 — локально через WSL (Ubuntu)

В PowerShell (от администратора) один раз поставь Ubuntu:
```powershell
wsl --install -d Ubuntu
```
Затем в Ubuntu:
```bash
sudo apt update
sudo apt install -y python3-pip openjdk-17-jdk zip unzip autoconf libtool \
    pkg-config zlib1g-dev libncurses5-dev libffi-dev libssl-dev cmake
pip3 install --user buildozer cython==0.29.36
cd /mnt/d/woordle/android
yes | buildozer android debug      # первый раз качает SDK/NDK (~2-3 ГБ)
```
Готовый файл появится в `android/bin/woordle-1.0-arm64-v8a_armeabi-v7a-debug.apk`.

---

## Установка на телефон
1. Перекинь `.apk` на Android (через кабель, Telegram, облако).
2. Открой файл → разреши «Установку из неизвестных источников».
3. Готово — иконка Woordle появится в меню.

> Это **debug**-сборка: ставится напрямую, для Google Play нужна release-подпись
> (`buildozer android release` + подпись ключом).
