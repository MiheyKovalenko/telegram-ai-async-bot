
from config import OPENAI_API_KEY, PAID_USERS
from openai import AsyncOpenAI
import g4f
import httpx
import os
from database import get_user_history, save_user_history
from user_provider import load_user_provider

http_client = httpx.AsyncClient()
client = AsyncOpenAI(api_key=OPENAI_API_KEY, http_client=http_client)

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

async def ask_openai(message_text: str, user_id: int) -> str:
    history = get_user_history(user_id)
    history.append({"role": "user", "content": message_text})
    history = history[-20:]

    if user_id in PAID_USERS:
        try:
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=history
            )
            answer = response.choices[0].message.content
            history.append({"role": "assistant", "content": answer})
            save_user_history(user_id, history)
            return answer
        except Exception as e:
            return f"❌ Ошибка OpenAI: {e}"

    user_choice = load_user_provider(user_id)
    if user_choice:
        try:
            provider = getattr(g4f.Provider, user_choice)
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                provider=provider,
                messages=history,
                stream=False
            )
            history.append({"role": "assistant", "content": response})
            save_user_history(user_id, history)
            return response
        except Exception:
            pass

    for provider in load_working_providers():
        try:
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                provider=provider,
                messages=history,
                stream=False
            )
            history.append({"role": "assistant", "content": response})
            save_user_history(user_id, history)
            return response
        except Exception:
            continue

    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=history
        )
        answer = response.choices[0].message.content
        history.append({"role": "assistant", "content": answer})
        save_user_history(user_id, history)
        return f"🤖 (GPT-4o fallback)\n{answer}"
    except Exception as e:
        return f"❌ Ошибка: ни один провайдер не сработал: {e}"
