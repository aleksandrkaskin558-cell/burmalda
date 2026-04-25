# 🚀 Space Shop — Telegram Mini App

Магазин космического мерча — учебный проект Telegram Mini App.

## Стек технологий

- **Backend бота:** Python 3.10+ / Aiogram 3.x
- **Веб-сервер:** FastAPI + Uvicorn
- **Фронтенд:** Семантический HTML5 + Pico.css + Telegram Web App SDK

## Структура проекта

| Файл | Описание |
|------|----------|
| `bot.py` | Telegram-бот: команда `/start` с кнопкой Mini App |
| `main.py` | FastAPI-сервер: отдаёт HTML, принимает заказы, проверяет подпись |
| `index.html` | Фронтенд: интерфейс магазина с нативными функциями Telegram |
| `requirements.txt` | Зависимости Python |

## Быстрый старт

```bash
# 1. Установи зависимости
pip install -r requirements.txt

# 2. Установи переменные окружения
export BOT_TOKEN="твой_токен_от_BotFather"
export WEBAPP_URL="https://твой-домен.com"

# 3. Запусти веб-сервер
python main.py

# 4. В другом терминале запусти бота
python bot.py
```

## Деплой (Uptime 24/7)

### Replit + UptimeRobot

Чтобы приложение на Replit не «засыпало», используй сервис **UptimeRobot**:

1. Задеплой проект на [Replit](https://replit.com).
2. Зарегистрируйся на [UptimeRobot](https://uptimerobot.com).
3. Добавь новый монитор:
   - **Тип:** HTTP(s)
   - **URL:** адрес твоего Replit-приложения (например, `https://your-app.replit.app`)
   - **Интервал:** 5 минут
4. UptimeRobot будет «пинговать» сервер каждые 5 минут, не давая ему уснуть.

> **Совет:** Для продакшена рассмотри [Railway](https://railway.app) или [Fly.io](https://fly.io) — они не требуют костылей с пингами.

## Безопасность

Сервер проверяет подпись `initData` через **HMAC-SHA256** — это гарантирует, что запросы приходят от Telegram, а не от злоумышленника. Никогда не доверяй данным с фронтенда без проверки!
