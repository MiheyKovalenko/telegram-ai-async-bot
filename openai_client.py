from config import OPENAI_API_KEY, PAID_USERS
from openai import AsyncOpenAI
import g4f
import httpx
import os
from user_provider import load_user_provider

# OpenAI client
http_client = httpx.AsyncClient()
client = AsyncOpenAI(api_key=OPENAI_API_KEY, http_client=http_client)

# Загрузка провайдеров из файла
def load_working_providers():
    path = "working_providers.txt"
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines()]
    providers = []
    for name in lines:
        try:
            providers.append(getattr(g4f.Provider, name))
        except AttributeError:
            continue
    return providers

available_providers = load_working_providers()

async def ask_openai(message_text: str, user_id: int) -> str:
    # Платные — всегда GPT-4o
    if user_id in PAID_USERS:
        try:
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": message_text}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Ошибка OpenAI: {e}"

    # Бесплатные — сначала выбранный пользователем провайдер
    user_choice = load_user_provider(user_id)
    if user_choice:
        try:
            provider = getattr(g4f.Provider, user_choice)
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                provider=provider,
                messages=[{"role": "user", "content": message_text}],
                stream=False
            )
            return response
        except Exception:
            pass  # fallback ниже

    # Перебор из доступных провайдеров
    for provider in available_providers:
        try:
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                provider=provider,
                messages=[{"role": "user", "content": message_text}],
                stream=False
            )
            return response
        except Exception:
            continue

    # Абсолютный fallback на GPT-4o
    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": message_text}]
        )
        return f"🤖 (GPT-4o fallback)\n{response.choices[0].message.content}"
    except Exception as e:
        return f"❌ Ошибка: ни один провайдер не сработал: {e}"
