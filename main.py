"""
main.py — «Мозг» (Backend): Веб-сервер на FastAPI.

Сервер выполняет три задачи:
1. Отдаёт «лицо» (фронтенд) — HTML-страницу Mini App.
2. Принимает заказы через API (эндпоинт /api/order).
3. Проверяет подпись Telegram (HMAC-SHA256) — «замок» приложения.

Метафора: API — это официант, который несёт заказ
от клиента (фронтенд) на кухню (бэкенд) и обратно.
"""

import hashlib
import hmac
import os
from urllib.parse import parse_qs

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Space Shop Mini App")

# --- CORS: разрешаем браузеру обращаться к API ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Токен бота — используется для проверки подписи initData
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")


# --- Pydantic-модель: «контракт» данных ---
# Pydantic защищает «мозг» приложения — если клиент пришлёт
# мусор вместо данных, сервер автоматически вернёт ошибку 422.
class Order(BaseModel):
    item_name: str
    amount: int


# ─────────────────────────────────────────────
# Безопасность — «Никогда не доверяй фронтенду»
# ─────────────────────────────────────────────

def verify_telegram_init_data(init_data: str, bot_token: str) -> bool:
    """
    Проверка цифровой подписи initData (HMAC-SHA256).
    Это «замок» нашего приложения — гарантирует, что запрос
    действительно пришёл от Telegram, а не от злоумышленника.
    """
    if not init_data:
        return False

    parsed = parse_qs(init_data, keep_blank_values=True)

    # Извлекаем хеш, присланный Telegram
    received_hash = parsed.pop("hash", [None])[0]
    if not received_hash:
        return False

    # Формируем строку для проверки: сортируем параметры по алфавиту
    data_check_string = "\n".join(
        f"{key}={values[0]}" for key, values in sorted(parsed.items())
    )

    # Генерируем секретный ключ из токена бота
    secret_key = hmac.new(
        key=b"WebAppData",
        msg=bot_token.encode(),
        digestmod=hashlib.sha256,
    ).digest()

    # Вычисляем хеш и сравниваем с присланным
    computed_hash = hmac.new(
        key=secret_key,
        msg=data_check_string.encode(),
        digestmod=hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(computed_hash, received_hash)


# ─────────────────────────────────────────────
# Эндпоинты
# ─────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def serve_index() -> HTMLResponse:
    """GET / — отдаёт «лицо» приложения (HTML-страницу)."""
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(html_path, encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.post("/api/order")
async def create_order(order: Order, request: Request) -> dict:
    """
    POST /api/order — принимает заказ от «официанта» (фронтенда).
    Проверяет подпись Telegram и валидирует данные через Pydantic.
    """
    # Проверяем подпись initData — «замок» нашего приложения
    init_data = request.headers.get("X-Telegram-Init-Data", "")
    if not verify_telegram_init_data(init_data, BOT_TOKEN):
        raise HTTPException(status_code=403, detail="Подпись не прошла проверку")

    return {
        "status": "success",
        "message": f"Заказ на {order.item_name} принят!",
    }


# ─────────────────────────────────────────────
# Запуск сервера
# ─────────────────────────────────────────────

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
