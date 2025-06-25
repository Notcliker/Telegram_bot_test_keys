"""
🔧 Название: 🤖 Авто-Генератор Тест-Кейсов Telegram-бот 
👤 Автор: Metiso4kas
📅 Июнь 2025
💼 Назначение: Telegram юот для автоматического ии создания тест-кейсов
🛡 Лицензия: MIT

## 📜 Отказ от ответственности

- 🛠️ Данный проект создан исключительно для учебных и ознакомительных целей.
- 👤 Автор проекта не несёт ответственности за любые последствия использования этого инструмента.
- ❌ Коммерческое использование запрещена."

📢 Отказ от связи с Telegram

Данный проект является неофициальным и не аффилирован с Telegram.  
Telegram и логотип Telegram являются зарегистрированными товарными знаками их правообладателей.  
Проект использует открытое Telegram Bot API согласно [официальной документации](https://core.telegram.org/bots/api).
Он не является официальным продуктом Telegram Inc.

"""
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import os
import uuid
import pandas as pd
from textwrap import wrap


# Создание папки keys
os.makedirs("keys", exist_ok=True)

def save_to_xlsx(text):
    cases = text.strip().split('---')
    data = []

    for case in cases:
        lines = case.strip().split('\n')
        entry = {"ID": "", "Название": "", "Предусловия": "", "Шаги": "", "Ожидаемый результат": "", "Приоритет": ""}
        current_field = None
        steps = []

        for line in lines:
            if line.startswith("ID:"):
                entry["ID"] = line[3:].strip()
            elif line.startswith("Название:"):
                entry["Название"] = line[9:].strip()
            elif line.startswith("Предусловия:"):
                entry["Предусловия"] = line[13:].strip()
            elif line.startswith("Шаги:"):
                current_field = "Шаги"
                steps = []
            elif line.startswith("Ожидаемый результат:"):
                entry["Ожидаемый результат"] = line[20:].strip()
                current_field = None
            elif line.startswith("Приоритет:"):
                entry["Приоритет"] = line[11:].strip()
                current_field = None
            elif current_field == "Шаги":
                steps.append(line.strip())

        entry["Шаги"] = '\n'.join(steps)
        if entry["ID"]:
            data.append(entry)

    df = pd.DataFrame(data)
    path = os.path.join("keys", f'testcases_{uuid.uuid4().hex[:6]}.xlsx')
    df.to_excel(path, index=False)
    return path
def wrap_text(text, font_name, font_size, max_width):
    words = text.split()
    lines = []
    line = ""

    for word in words:
        test_line = line + word + " "
        if pdfmetrics.stringWidth(test_line, font_name, font_size) <= max_width:
            line = test_line
        else:
            lines.append(line.rstrip())
            line = word + " "
    if line:
        lines.append(line.rstrip())

    return lines

def save_to_pdf(text):
    path = os.path.join("keys", f'testcases_{uuid.uuid4().hex[:6]}.pdf')
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    margin = 20 * mm
    usable_width = width - 2 * margin
    y = height - margin
    line_height = 14

    # Регистрация шрифта с поддержкой кириллицы
    font_path = os.path.join("fonts", "DejaVuSans.ttf")
    font_name = "DejaVu"
    font_size = 11
    pdfmetrics.registerFont(TTFont(font_name, font_path))
    c.setFont(font_name, font_size)

    for block in text.strip().split('---'):
        block = block.strip()
        if not block:
            continue
        for line in block.split('\n'):
            for wrapped_line in wrap_text(line, font_name, font_size, usable_width):
                if y < margin:
                    c.showPage()
                    c.setFont(font_name, font_size)
                    y = height - margin
                c.drawString(margin, y, wrapped_line)
                y -= line_height
            y -= 5
        y -= line_height

    c.save()
    return path
