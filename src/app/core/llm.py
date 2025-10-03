import datetime
from typing import Any

import requests

from .config import get_settings
from ..adapters import FinamAPIClient


def call_llm(messages: list[dict[str, str]], temperature: float = 0.2, max_tokens: int | None = None) -> dict[str, Any]:
    """Простой вызов LLM без tools"""
    s = get_settings()
    payload: dict[str, Any] = {
        "model": s.openrouter_model,
        "messages": messages,
        "temperature": temperature,
    }
    if max_tokens:
        payload["max_tokens"] = max_tokens

    r = requests.post(
        f"{s.openrouter_base}/chat/completions",
        headers={
            "Authorization": f"Bearer {s.openrouter_api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    r.raise_for_status()
    return r.json()


def create_system_prompt() -> str:
    """Создать системный промпт для AI ассистента"""
    return (
        "Ты - AI ассистент трейдера, работающий с Finam TradeAPI.\n\n"

        "Когда пользователь задает вопрос о рынке, портфеле или хочет совершить действие:\n"
        "1. Определи нужный API endpoint\n"
        "2. Укажи запрос в формате: API_REQUEST: METHOD /path\n"
        "3. Если видишь {symbol} - оставляй его в виде {symbol:НАЗВАНИЕ} в path, я сам подставлю, кроме строк формата TICKER@MIC.\n"
        "4. После получения данных - проанализируй их и дай понятный ответ\n\n"

        """Доступные endpoints:
        - GET /v1/exchanges - список бирж
        - GET /v1/assets - поиск инструментов
        - GET /v1/assets/{symbol} - информация об инструменте
        - GET /v1/assets/{symbol}/params - параметры инструмента для счета
        - GET /v1/assets/{symbol}/schedule - расписание торгов
        - GET /v1/assets/{symbol}/options - опционы на базовый актив
        - GET /v1/instruments/{symbol}/quotes/latest - последняя котировка
        - GET /v1/instruments/{symbol}/orderbook - биржевой стакан
        - GET /v1/instruments/{symbol}/trades/latest - лента сделок
        - GET /v1/instruments/{symbol}/bars - исторические свечи
          (параметры: timeframe, interval.start_time, interval.end_time)
        - GET /v1/accounts/{account_id} - информация о счете
        - GET /v1/accounts/{account_id}/orders - список ордеров
        - GET /v1/accounts/{account_id}/orders/{order_id} - информация об ордере
        - GET /v1/accounts/{account_id}/trades - история сделок
        - GET /v1/accounts/{account_id}/transactions - транзакции по счету
        - POST /v1/sessions - создание новой сессии
        - POST /v1/sessions/details - детали текущей сессии
        - POST /v1/accounts/{account_id}/orders - создание ордера
        - DELETE /v1/accounts/{account_id}/orders/{order_id} - отмена ордера
        
        Timeframes: TIME_FRAME_M1, TIME_FRAME_M5, TIME_FRAME_M15, TIME_FRAME_M30, TIME_FRAME_H1, TIME_FRAME_H4, TIME_FRAME_D, TIME_FRAME_W, TIME_FRAME_MN"""
        "\n\n"
        
        "symbol - Символ инструмента указывается в формате ticker@mic, если он так не указан - оставь {symbol}.\n\n"
        
        f"Текущее время: {datetime.datetime.now().isoformat()}\n\n"

        """Отвечай на русском, кратко и по делу."""
    )


def extract_api_request(text: str) -> tuple[str | None, str | None]:
    """Извлечь API запрос из ответа LLM"""
    if "API_REQUEST:" not in text:
        return None, None

    lines = text.split("\n")
    for line in lines:
        if line.strip().startswith("API_REQUEST:"):
            request = line.replace("API_REQUEST:", "").strip()
            parts = request.split(maxsplit=1)
            if len(parts) == 2:
                return parts[0], parts[1]
    return None, None
