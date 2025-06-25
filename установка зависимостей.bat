@echo off
echo Установка виртуального окружения...
python -m venv venv

echo Активация виртуального окружения...
call venv\Scripts\activate

echo Установка зависимостей...
pip install --upgrade pip
pip install -r requirements.txt

echo Запуск бота...
python bot.py

pause
