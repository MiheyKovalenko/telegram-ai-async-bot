
import g4f
import asyncio

async def scan_providers():
    print("🔍 Сканирую доступные провайдеры g4f...")
    all_providers = g4f.Provider.__all__
    working = []

    async def test_provider(provider_name):
        try:
            provider = getattr(g4f.Provider, provider_name)
            response = await asyncio.to_thread(
                g4f.ChatCompletion.create,
                model="gpt-3.5-turbo",
                provider=provider,
                messages=[{"role": "user", "content": "ping"}],
                stream=False
            )
            if response:
                print(f"✅ {provider_name} работает")
                return provider_name
        except Exception:
            pass
        print(f"❌ {provider_name} не работает")
        return None

    tasks = [test_provider(name) for name in all_providers]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    working = [r for r in results if isinstance(r, str)]

    with open("working_providers.txt", "w") as f:
        for name in working:
            f.write(name + "\n")

    print(f"✅ Найдено {len(working)} рабочих провайдеров")
