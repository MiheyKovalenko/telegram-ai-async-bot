import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import router
from database import init_db
from scan_providers import scan_providers

async def periodic_update():
    while True:
        await scan_providers()
        await asyncio.sleep(600)  # каждые 10 минут

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    await init_db()
    asyncio.create_task(periodic_update())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
