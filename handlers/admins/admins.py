from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters.builtin import Text
from aiogram.dispatcher import FSMContext
from handlers.users.commands import GetCount
from keyboards.default.default import Admin_Menu
from states.states import AdminMenuCondition
from loader import UABarbershop, bot

@UABarbershop.message_handler(Text("Foydalanuvchilarga murojaat qilish✍️"))
async def Admin_Menu_Process(message: types.Message):
    await message.answer("Foydalanuvchilarga nima yuborishni istaysiz?", reply_markup=Admin_Menu)
    await AdminMenuCondition.Admin.set()
    
@UABarbershop.message_handler(Text("Xabar📩"), state=AdminMenuCondition.Admin)
async def Message_Process(message: types.Message, state: FSMContext):
    await message.answer("Foydalanuvchilarga yubormoqchi bo'lgan matningizni kiriting:", reply_markup=ReplyKeyboardRemove())
    await AdminMenuCondition.Send_Message.set()
    
@UABarbershop.message_handler(state=AdminMenuCondition.Send_Message)
async def Message_Process(message: types.Message, state: FSMContext):
    users_id = []
    async with state.proxy() as data:
        data['Send_Message'] = message.text
    for i in GetCount():
        for j in i:
            users_id.append(j)
    for id in users_id:
        await bot.send_message(chat_id=id, text=data['Send_Message'])
    await message.answer("Xabar UA Barbershop foydalanuvchilariga yuborildi✅")
    await state.finish()
    
@UABarbershop.message_handler(Text("Post🗃"), state=AdminMenuCondition.Admin)
async def Post_Process(message: types.Message, state: FSMContext):
    await message.answer("Post uchun rasm yuboring:", reply_markup=ReplyKeyboardRemove())
    await AdminMenuCondition.Send_Post.set()
    
@UABarbershop.message_handler(content_types=['photo'], state=AdminMenuCondition.Send_Post)
async def Post_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Send_Post'] = message.photo[0].file_id
    await message.answer("Rasm matnini kiriting:")
    await AdminMenuCondition.Caption.set()
    
@UABarbershop.message_handler(state=AdminMenuCondition.Caption)
async def Caption_Process(message: types.Message, state: FSMContext):
    users_id = []
    async with state.proxy() as data:
        data['Caption'] = message.text
    for i in GetCount():
        for j in i:
            users_id.append(j)
    for i in users_id:
        await bot.send_photo(chat_id=i,
                            photo=data['Send_Post'],
                            caption=data['Caption'])
    await message.answer("Post UA Barbershop foydalanuvchilariga yuborildi✅")
    await state.finish()