from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from openai_client import ask_openai, load_working_providers
from user_provider import save_user_provider

router = Router()

@router.message(Command("provider"))
async def show_provider_menu(message: types.Message):
    providers = load_working_providers()
    if not providers:
        await message.answer("❌ Нет доступных провайдеров.")
        return

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=prov.__name__, callback_data=f"prov_{prov.__name__}")]
            for prov in providers
        ]
    )
    await message.answer("Выбери модель:", reply_markup=markup)


@router.callback_query()
async def set_provider(callback: types.CallbackQuery):
    if callback.data and callback.data.startswith("prov_"):
        provider_name = callback.data[5:]
        save_user_provider(callback.from_user.id, provider_name)
        await callback.message.edit_text(f"✅ Провайдер установлен: {provider_name}")

@router.message()
async def handle_message(message: types.Message):
    reply = await ask_openai(message.text, message.from_user.id)
    await message.answer(reply)
