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
import telebot
import re
from config import BOT_TOKEN
from ollama_gen import generate_test_cases
from file_writer import save_to_xlsx, save_to_pdf

bot = telebot.TeleBot(BOT_TOKEN)

def remove_think_block(text: str) -> str:
    """Удаляет блок <think>...</think> из ответа модели."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! 🧪 Отправь описание функционала, и я сгенерирую тест-кейсы.")

@bot.message_handler(func=lambda m: True)
def handle_description(message):
    description = message.text.strip()
    bot.send_message(message.chat.id, "✍️ Генерирую тест-кейсы по описанию…")

    # Генерация и очистка текста от <think>...</think>
    raw_cases = generate_test_cases(description)
    cases = remove_think_block(raw_cases)

    # Сохраняем в файлы
    xlsx_path = save_to_xlsx(cases)
    pdf_path = save_to_pdf(cases)

    # Отправка пользователю
    bot.send_message(message.chat.id, "✅ Готово! Вот твои тест-кейсы:")
    with open(xlsx_path, 'rb') as xlsx_file:
        bot.send_document(message.chat.id, xlsx_file, caption="📊 .xlsx")
    with open(pdf_path, 'rb') as pdf_file:
        bot.send_document(message.chat.id, pdf_file, caption="📑 .pdf")

if __name__ == '__main__':
    print("✅ Бот запущен, ожидает сообщений от пользователей…")
    bot.polling()
