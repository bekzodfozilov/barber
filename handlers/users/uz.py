import aiogram.utils.markdown as md
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
from handlers.users.data import UzWriteData, UzCheckData
from handlers.users.uzchecktime import UzCheckTimeText
from handlers.users.uzcheckday import UzCheckDay
from keyboards.default.default import Uz_Contact_Button, Uz_Haircuts_Button, Uz_Yes_No_Button, Confirmed
from dm.uz_dm import Uz_September
from states.states import Condition
from loader import UABarbershop, bot

@UABarbershop.message_handler(text="O'zbek🇺🇿", state=Condition.Language)
async def Uz_Language_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Language'] = message.text
    await message.answer("<b>Usta Abdulloh</b> - 1999 yilda tashkil etilgan bo'lib,\
 sartaroshxona shahar markazida joylashgan, erkaklar va ayollar uchun mashhur joy.\
 Sartaroshxona turli xil xizmatlarni taklif etadi, jumladan, soch kesish, soch olish, bosh massaji, soqolni kesish va soch turmagi.\
 <b>Usta Abdulloh</b>'ning xodimlari yuqori malakali va tajribali bo'lib, mijozlarga eng yaxshi xizmat ko'rsatishga intiladi.", parse_mode="HTML")
    await message.answer("Ismingizni kiriting. Sizdan bir narsani iltimos qilgan bo'lar edik!\
 Ya'ni botga har xil son va harflar yubormasdan to'liq ismingizni yuborishingizni so'raymiz.", reply_markup=types.ReplyKeyboardRemove())
    await Condition.Uz_Username.set()

@UABarbershop.message_handler(state=Condition.Uz_Username)
async def Uz_Username_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Uz_Username'] = message.text
    await message.answer("🤳🏻Sartaroshlarimiz siz bilan bog'lanishlari uchun telefon raqamingizni yuboring.\
 Buning uchun «📱» tugmasini bosing.", reply_markup=Uz_Contact_Button)
    await Condition.Uz_Contact.set()

@UABarbershop.message_handler(lambda message: message.text not in ["📱"], state=Condition.Uz_Contact)
async def Incorrect_Uz_Contact(message: types.Message):
    return await message.answer("🚫Noto'g'ri telefon raqam kiritdingiz! Telefon raqamingizni yuborish uchun «📱» tugmasini bosing.")

@UABarbershop.message_handler(content_types=["contact"], state=Condition.Uz_Contact)
async def Uz_Contact_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Uz_Contact'] = message.contact.phone_number
    await message.answer("💇🏻‍♂️Qaysi soch turmagini tanlaysiz?", reply_markup=Uz_Haircuts_Button)
    await Condition.Uz_Haircuts.set()
    
@UABarbershop.message_handler(lambda message: message.text not in ["Bolalar soch turmagi", "Standart", "Ommabop", "To'y soch turmagi"],
    state=Condition.Uz_Haircuts)
async def Incorrect_Uz_Haircuts(message: types.Message):
    return await message.answer("Soch turmagini tanlashda xatolik!\nTugma orqali sochingizni qanday ko'rinishida oldirmoqchiligingizni tanlang.")
    
@UABarbershop.message_handler(text="Bolalar soch turmagi", state=Condition.Uz_Haircuts)
async def Uz_Children_Haircuts_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Uz_Haircuts'] = message.text
    await message.answer("🙎🏻‍♂️Bolalar soch turmagiga nimalar kiradi?\n\n• Soch turmagi💇🏻‍♂️\n\
• Soch yuvish🚿\n• Soch turmaklash✨\n\n📋Narxi: 100.000 - 150.000 UZS💸\n\nBolalar soch turmagini tanlaysizmi?",
        reply_markup=Uz_Yes_No_Button)
    await Condition.Uz_Yes_No.set()

@UABarbershop.message_handler(text="Standart", state=Condition.Uz_Haircuts)
async def Uz_Standart_Haircut_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Uz_Haircuts'] = message.text
    await message.answer(
        "⭐️Standart soch turmagiga nimalar kiradi?\n\n• Soch turmagi💇🏻‍♂️\n• Soch yuvish🚿\n\
• Bosh massaji💆🏻\n\n📋Narxi: 150.000 UZS💸\n\nStandart soch turmagini tanlaysizmi?",
        reply_markup=Uz_Yes_No_Button)
    await Condition.Uz_Yes_No.set()

@UABarbershop.message_handler(text="Ommabop", state=Condition.Uz_Haircuts)
async def Uz_Advanced_Haircut_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Uz_Haircuts'] = message.text
    await message.answer(
        "⚡️Ommabop soch turmagiga nimalar kiradi?\n\n• Soch turmagi💇🏻‍♂️\n• Soch yuvish🚿\n\
• Bosh massaji💆🏻\n• Soch uchun krem🧴\n• Soch turmaklash💫\n\n\
📋Narxi: 200.000 - 250.000 UZS💸\n\nOmmabop soch turmagini tanlaysizmi?", reply_markup=Uz_Yes_No_Button)
    await Condition.Uz_Yes_No.set()

@UABarbershop.message_handler(text="To'y soch turmagi", state=Condition.Uz_Haircuts)
async def Uz_Wedding_Haircut_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Uz_Haircuts'] = message.text
    await message.answer("👩‍❤️‍👨To'y soch turmagi:\n\
📋Narxi: 50 - 100 USD💸\n\nTo'y soch turmagini tanlaysizmi?", reply_markup=Uz_Yes_No_Button)
    await Condition.Uz_Yes_No.set()

@UABarbershop.message_handler(lambda message: message.text not in ["Ha", "Yo'q"], state=Condition.Uz_Yes_No)
async def Incorrect_Uz_Yes_No(message: types.Message):
    return await message.answer("Agar soch turmagi bo'yicha ma'lumotlaringiz to'g'ri bo'lsa \"Ha\" tugmasini bosing.\
 Boshqa soch turmagini tanlash uchun \"Yo'q\" tugmasini bosing.")

@UABarbershop.message_handler(text="Yo'q", state=Condition.Uz_Yes_No)
async def Uz_No_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Uz_Yes_No'] = message.text
    await message.answer("💇🏻‍♂️Qaysi soch turmagini tanlaysiz?", reply_markup=Uz_Haircuts_Button)
    await Condition.Uz_Haircuts.set()

@UABarbershop.message_handler(text="Ha", state=Condition.Uz_Yes_No)
async def Uz_Yes_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Uz_Yes_No'] = message.text
    await message.answer("🚶🏻‍♂️Sentyabr oyining nechinchi sanasiga kelishingizni kiriting.\nMisol uchun: 31-sentyabr",
        reply_markup=types.ReplyKeyboardRemove())
    await Condition.Uz_DM.set()
    
# async def check_date_range(user_date_str):
#     user_date = datetime.strptime(user_date_str, "%d.%m.%Y").date()
#     today = datetime.now().date()
#     max_date = today + timedelta(days=3)

#     if today <= user_date <= max_date:
#         return True
#     else:
#         return False

# @UABarbershop.message_handler(regexp=r"\d{2}\.\d{2}\.\d{4}")
# async def check_date(message: types.Message):
#     user_date_str = message.text
#     is_valid_date_range = await check_date_range(user_date_str)

#     if is_valid_date_range:
#         await message.answer(f"{message.text}✅")
#     else:
#         await message.answer("Siz kiritgan sana, oy va yil noto'g'ri. "
#                             "Maksimum 3 kunlik davrda bo'lishi kerak.\n"
#                             "Sana formati: 07.08.2023 dan 10.08.2023 gacha.")

@UABarbershop.message_handler(lambda message: message.text not in Uz_September, state=Condition.Uz_DM)
async def Incorrect_Uz_DM(message: types.Message):
    return await message.answer("🗓Sana va oy qabul qilinmadi!🙅‍♂️\nBot faqat sentyabr oyi bo'yicha qabul qiladi.")

@UABarbershop.message_handler(state=Condition.Uz_DM)
async def Uz_DM_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Uz_DM'] = message.text
    if await UzCheckDay(state):
        text = await UzCheckTimeText(state)
        await message.answer("🕰Soat nechiga kelishingizni tungi soat <b>9:00</b> dan\
 kechki soat <b>0:00</b> gacha bo'lgan vaqtni kiriting.\n⏳Soat intervali yarim soatdan bo'lishi kerak.\
\n❕Misol uchun: 10:00 yoki 10:30.\n\n🎯Band qilingan soatlar: " + text)
        await Condition.Uz_Oclock.set()
    else:
        await message.answer("🗓Sana va oy qabul qilinmadi!🙅‍♂️\nEslatib o'tamiz! Bot faqat sentyabr oyi bo'yicha qabul qiladi\
 va o'tib ketgan sana va oyni qabul qilmaydi.")

@UABarbershop.message_handler(
    lambda message: message.text not in ["9:00", "9:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00",
                                        "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", 
                                        "18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", "22:00",
                                        "22:30", "23:00", "23:30", "0:00"], state=Condition.Uz_Oclock)
async def Incorrect_Oclock(message: types.Message):
    return await message.answer("🚫Xato vaqtni kiritdingiz!\n🕰Soat nechiga kelishingizni tungi soat <b>9:00</b> dan kechki soat\
 <b>0:00</b> gacha bo'lgan vaqtni kiriting.\n⏳Soat intervali yarim soatdan bo'lishi kerak.\n❕Misol uchun: 10:00 yoki 10:30.", parse_mode="HTML")

@UABarbershop.message_handler(state=Condition.Uz_Oclock)
async def Uz_Oclock_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Uz_Oclock'] = message.text
    if await UzCheckData(state):
        await UzWriteData(state)
    else:
        return await message.answer("Ushbu vaqt band qilingan. Yuqoridagi ro'yxatdan foydalangan holda\
 band qilinmagan va o'zingizniga qulay bo'lgan vaqtni yuboring👆")
    await bot.send_message(
        message.chat.id,
        md.text(
            md.text("📝Sizning ma'lumotlaringiz qabul qilindi."),
            md.text("👤Ismingiz:", md.text(data["Uz_Username"])),
            md.text("📞Telefon raqam:", md.text(data["Uz_Contact"])),
            md.text("🗓Sana va oy:", md.text(data["Uz_DM"])),
            md.text("💇🏻‍♂️Soch turmagi:", md.text(data["Uz_Haircuts"])),
            md.text("⏰Soat:", md.text(data["Uz_Oclock"])),
            sep="\n",
        ),
        reply_markup=types.ReplyKeyboardRemove(),
        parse_mode=ParseMode.MARKDOWN,
    )
    await bot.send_message(chat_id="@UzPythonTelegramBotsGroup", text=md.text("📝Mijoz ma'lumotlari;\
                                                \n👤Ismi:", md.text(data["Uz_Username"],
                                                "\n📞Telefon raqam:", md.text(data["Uz_Contact"],
                                                "\n🗓Sana va oy:", md.text(data["Uz_DM"],
                                                "\n💇🏻‍♂️Soch turmagi:", md.text(data["Uz_Haircuts"],
                                                "\n⏰Soat:", md.text(data["Uz_Oclock"])))))), reply_markup=Confirmed)

    await state.finish()