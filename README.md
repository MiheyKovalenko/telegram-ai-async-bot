
# Telegram AI Async Bot 🤖💬

[![GitHub](https://img.shields.io/badge/GitHub-MiheyKovalenko-181717?logo=github)](https://github.com/MiheyKovalenko)
[![Telegram](https://img.shields.io/badge/Telegram-%40Miheyyka-2CA5E0?logo=telegram)](https://t.me/Miheyyka)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

Асинхронный Telegram-бот с поддержкой **OpenAI GPT-4o**, бесплатных `g4f`-провайдеров, выбором модели и автообновлением.

---

## 🚀 Возможности

- Поддержка платной модели **GPT-4o** для избранных пользователей
- Бесплатные провайдеры через `g4f`, с автообновлением каждые 10 минут
- Пользователь может сам выбрать провайдера через `/provider`
- SQLite-база пользователей и сохранение истории выбора
- Чистая архитектура на `aiogram 3` и `openai>=1.0.0`

---

## 🧠 Используемые технологии

- Python 3.11+
- [aiogram 3](https://docs.aiogram.dev/en/latest/)
- [openai](https://pypi.org/project/openai/)
- [g4f](https://github.com/xtekky/gpt4free)
- SQLite
- systemd или tmux (для автозапуска на сервере)

---

## ⚙️ Установка и запуск

1. Клонируй репозиторий:

```bash
git clone https://github.com/MiheyKovalenko/telegram-ai-async-bot.git
cd telegram-ai-async-bot
```

2. Установи зависимости:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Добавь файл `config.ini` со своими ключами:

```ini
[default]
bot_token = ТВОЙ_ТОКЕН
admin_id = ТВОЙ_ID
openai_api_key = sk-...
```

4. Запусти бота:

```bash
python main.py
```

---

## 📁 Файлы, которые не входят в репозиторий (и будут создаваться автоматически)

- `bot.db` — база данных пользователей
- `config.ini` — ключи и настройки
- `user_providers.txt` — выбор моделей по юзерам
- `working_providers.txt` — автоматически обновляемый список рабочих провайдеров

---

## 📡 Команды

- `/start` — приветствие
- `/provider` — выбор текущей модели
- (опционально: `/update_providers` — ручной запуск сканирования)

---

## ⭐ Поддержать

Если проект тебе полезен — поставь звезду!  
Это поможет развивать его дальше и мотивирует автора :)
