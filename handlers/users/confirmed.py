from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import UABarbershop

async def Check_Button(text: str) -> InlineKeyboardMarkup:
    Confirm = InlineKeyboardMarkup()
    Check = InlineKeyboardButton(f"{text}", callback_data="Check")
    Confirm.add(Check)
    return Confirm

@UABarbershop.callback_query_handler(text="Check")
async def Update_Process(callback_query: types.CallbackQuery):
    # await bot.answer_callback_query(callback_query.id, text="Tasdiqlandi.")
    await callback_query.message.edit_reply_markup(reply_markup=await Check_Button(text="Tasdiqlandi."))
