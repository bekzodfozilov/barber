
import config
import logging
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode
from aiogram.dispatcher import FSMContext, DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.filters.builtin import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import (Unauthorized, InvalidQueryID, TelegramAPIError, CantDemoteChatCreator,
                                      Throttled, MessageNotModified, MessageToDeleteNotFound, MessageTextIsEmpty,
                                      RetryAfter, CantParseEntities, MessageCantBeDeleted)
from states import *
from buttons import *
from data import *
from uz_dm import *
from ru_dm import *

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()

dp = Dispatcher(bot=bot, storage=storage)


@dp.message_handler(commands=["start"], state="*")
async def CMD_Start(message: types.Message):
    # now = datetime.datetime.now()
    # start_time = datetime.time(9, 0)
    # end_time = datetime.time(23, 0)
    # if start_time <= now.time() <= end_time:
    #     await message.reply("Assalomu alaykum! Biz 9:00 dan 0:00 gacha ishlaymiz.", parse_mode=ParseMode.HTML)

    #     day = message.date.weekday()
    #     if day == 4:
    #         await message.answer("🇺🇿Assalomu aleykum hurmatli mijozlarimiz. Juma bizning dam olish kunimiz hisoblanadi\
    #  va biz Juma kuni ishlamaymiz.\n🇷🇺Здравствуйте, дорогие клиенты. Пятница у нас выходной и иы не работаем в Пятницу.")
    #     else:
    await message.answer("🇺🇿O'zingizga qulay bo'lgan muloqot tilini tanlang.\n\
🇷🇺Выберите язык общения, который вам удобен.", reply_markup=Language_Button)

    if not await CheckUsersID(message.from_user.id):
        await WriteUserID(message.from_user.id)
    await GetCount()
    await Condition.Language.set()


@dp.message_handler(commands=["users"], state="*")
async def CMD_Users(message: types.Message):
    await message.answer(
        f"🇺🇿Foydalanuvchilari soni: {await GetCount()} ta.\n🇷🇺Количество пользователей: {await GetCount()}.")


async def WriteUserID(users_id):
    users = open('barbershop.txt', mode='a')
    users.write(f'{users_id}')
    users.close()


async def CheckUsersID(users_id):
    users = open('barbershop.txt', mode='r')
    users_data = users.read().split('\n')
    if str(users_id) in users_data:
        return True
    else:
        return False


async def GetCount():
    users = open('barbershop.txt', mode='r')
    count_users = users.read().split('\n')
    return len(count_users) - 1


@dp.message_handler(commands=["help"], state="*")
async def CMD_Help(message: types.Message):
    await message.answer("🇺🇿Assalomu aleykum!🤝\n🤖Telegram botimizdan foydalanishda muammo yoki savollaringiz bormi?\n\
📄Unda quyidagi ko'rsatma bilan tanishib chiqishingizni tavsiya etamiz.\n\
1️⃣Telegram botdan foydalanish uchun <b>START</b> tugmasini bosing.\n\
2️⃣Til tanlang.\n\
3️⃣Ismingizni kiriting.\n\
4️⃣Telefon raqamingizni yuboring.\n\
5️⃣Qaysi sana va oy kelishingizni kiriting.\n\
6️⃣Soch turmagini tanlang.\n\
7️⃣Agar soch turmagi bo'yicha ma'lumotlaringiz to'g'ri bo'lsa \"Ha\" agar aksincha bo'lsa \"Yo'q\" tugmasini bosing.\n\
8️⃣Soat nechchiga kelishingizni kiriting.\n\
9️⃣Soat intervali yarim soatdan bo'lishi kerak.\n\
⚠️Eslatib o'tamiz qo'llanmada ko'rsatilgandek Telegram botdan foydalanmasangiz, bot foydalanuvchidan kelgan xabarni xato sifatida qabul qiladi va keyingi jarayonga o'tkazmaydi.\n\
🤖Telegram botimizning qo'shimcha komandalari va ularning vazifasi;\n\
/start - Telegram botni ishga tushirish;\n\
/help - Telegram botdan foydalanish uchun qo'llanma;\n\
/users - Bot foydalanuvchilari sonini ko'rish.\n\n\
🇷🇺Здравствуйте!🤝\n🤖У Вас возникли трудности или у Вас есть вопросы по использованию нашего Телеграм бота?\n\
📄Тогда предлагаем ознакомиться с инструкцией по использованию Телеграм бота.\n\
1️⃣Запустите Телеграм бот, для этого нажмите <b>START</b>.\n\
2️⃣Выберите язык.\n\
3️⃣Введите своё имя.\n\
4️⃣Отправьте номер телефона.\n\
5️⃣Введите число и месяц Вашего прибытия.\n\
6️⃣Выберите стрижку.\n\
7️⃣Если ваши данные верны с выбором нажмите кнопку \"Да\", если наоборот то нажмите кнопку \"Нет\".\n\
8️⃣Введите время Вашего прибытия.\n\
9️⃣Часовой интервал должен составлять полчаса.\n\
⚠️Напоминаем, что если вы используете Телеграм бот не так, как показано в инструкции, бот воспримет сообщение от пользователя как ошибку и не перешлёт его к следующему процессу.\n\
🤖Дополнительные команды нашего Телеграм бота и их задачи;\n\
/start - Запустить Телеграм бот заново;\n\
/help - Инструкция по использованию Телеграм бота;\n\
/users - Посмотреть количество пользователей бота.", parse_mode="HTML")


@dp.message_handler(lambda message: message.text not in ["O'zbek🇺🇿", "Русский🇷🇺"], state=Condition.Language)
async def Incorrect_Language(message: types.Message):
    return await message.answer("🇺🇿Til tanlashda xatolik❗️\n🇷🇺Ошибка при выборе языка❗️")


@dp.message_handler(text="O'zbek🇺🇿", state=Condition.Language)
async def Uz_Language_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Language'] = message.text
    await message.answer("<b>Usta Abdulloh</b> - 1999 yilda tashkil etilgan bo'lib,\
 sartaroshxona shahar markazida joylashgan, erkaklar va ayollar uchun mashhur joy.\
 Sartaroshxona turli xil xizmatlarni taklif etadi, jumladan, soch kesish, soch olish, bosh massaji, soqolni kesish va soch turmagi.\
 <b>Usta Abdulloh</b>'ning xodimlari yuqori malakali va tajribali bo'lib, mijozlarga eng yaxshi xizmat ko'rsatishga intiladi.",
                         parse_mode="HTML")
    await message.answer("Ismingizni kiriting. Sizdan bir narsani iltimos qilgan bo'lar edik!\
 Ya'ni botga har xil son va harflar yubormasdan to'liq ismingizni yuborishingizni so'raymiz.",
                         reply_markup=types.ReplyKeyboardRemove())
    await Condition.Uz_Username.set()


@dp.message_handler(state=Condition.Uz_Username)
async def Uz_Username_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Uz_Username'] = message.text
    await message.answer("🤳🏻Sartaroshlarimiz siz bilan bog'lanishlari uchun telefon raqamingizni yuboring.\
 Buning uchun «📱» tugmasini bosing.", reply_markup=Uz_Contact_Button)
    await Condition.Uz_Contact.set()


@dp.message_handler(lambda message: message.text not in ["📱"], state=Condition.Uz_Contact)
async def Incorrect_Uz_Contact(message: types.Message):
    return await message.answer(
        "🚫Noto'g'ri telefon raqam kiritdingiz! Telefon raqamingizni yuborish uchun «📱» tugmasini bosing.")


@dp.message_handler(content_types=["contact"], state=Condition.Uz_Contact)
async def Uz_Contact_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Uz_Contact'] = message.contact.phone_number
    await message.answer("💇🏻‍♂️Qaysi soch turmagini tanlaysiz?", reply_markup=Uz_Haircuts_Button)
    await Condition.Uz_Haircuts.set()


@dp.message_handler(
    lambda message: message.text not in ["Bolalar soch turmagi", "Standart", "Ommabop", "To'y soch turmagi"],
    state=Condition.Uz_Haircuts)
async def Incorrect_Uz_Haircuts(message: types.Message):
    return await message.answer(
        "🚫Soch turmagini tanlashda xatolik!\n🙎🏻‍♂️Tugma orqali sochingizni qanday ko'rinishida oldirmoqchiligingizni tanlang.")


@dp.message_handler(text="Bolalar soch turmagi", state=Condition.Uz_Haircuts)
async def Uz_Children_Haircuts_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Uz_Haircuts'] = message.text
    await message.answer("🙎🏻‍♂️Bolalar soch turmagiga nimalar kiradi?\n\n• Soch turmagi💇🏻‍♂️\n\
• Soch yuvish🚿\n• Soch turmaklash✨\n\n📋Narxi: 100.000 - 150.000 UZS💸\n\nBolalar soch turmagini tanlaysizmi?",
                         reply_markup=Uz_Yes_No_Button)
    await Condition.Uz_Yes_No.set()


@dp.message_handler(text="Standart", state=Condition.Uz_Haircuts)
async def Uz_Standart_Haircut_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Uz_Haircuts'] = message.text
    await message.answer(
        "⭐️Standart soch turmagiga nimalar kiradi?\n\n• Soch turmagi💇🏻‍♂️\n• Soch yuvish🚿\n\
• Bosh massaji💆🏻\n\n📋Narxi: 150.000 UZS💸\n\nStandart soch turmagini tanlaysizmi?",
        reply_markup=Uz_Yes_No_Button)
    await Condition.Uz_Yes_No.set()


@dp.message_handler(text="Ommabop", state=Condition.Uz_Haircuts)
async def Uz_Advanced_Haircut_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Uz_Haircuts'] = message.text
    await message.answer(
        "⚡️Ommabop soch turmagiga nimalar kiradi?\n\n• Soch turmagi💇🏻‍♂️\n• Soch yuvish🚿\n\
• Bosh massaji💆🏻\n• Soch uchun krem🧴\n• Soch turmaklash💫\n\n\
📋Narxi: 200.000 - 250.000 UZS💸\n\nOmmabop soch turmagini tanlaysizmi?", reply_markup=Uz_Yes_No_Button)
    await Condition.Uz_Yes_No.set()


@dp.message_handler(text="To'y soch turmagi", state=Condition.Uz_Haircuts)
async def Uz_Wedding_Haircut_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Uz_Haircuts'] = message.text
    await message.answer("👩‍❤️‍👨To'y soch turmagi:\n\
📋Narxi: 50 - 100 USD💸\n\nTo'y soch turmagini tanlaysizmi?", reply_markup=Uz_Yes_No_Button)
    await Condition.Uz_Yes_No.set()


@dp.message_handler(lambda message: message.text not in ["Ha", "Yo'q"], state=Condition.Uz_Yes_No)
async def Incorrect_Uz_Yes_No(message: types.Message):
    return await message.answer("Agar soch turmagi bo'yicha ma'lumotlaringiz to'g'ri bo'lsa \"Ha\" tugmasini bosing.\
 Boshqa soch turmagini tanlash uchun \"Yo'q\" tugmasini bosing.")


@dp.message_handler(text="Yo'q", state=Condition.Uz_Yes_No)
async def Uz_No_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Uz_Yes_No'] = message.text
    await message.answer("💇🏻‍♂️Qaysi soch turmagini tanlaysiz?", reply_markup=Uz_Haircuts_Button)
    await Condition.Uz_Haircuts.set()


@dp.message_handler(text="Ha", state=Condition.Uz_Yes_No)
async def Uz_Yes_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Uz_Yes_No'] = message.text
    await message.answer("📅Sana va oyni kiriting.\n✅Misol uchun: 22-mart.",
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

# @dp.message_handler(regexp=r"\d{2}\.\d{2}\.\d{4}")
# async def check_date(message: types.Message):
#     user_date_str = message.text
#     is_valid_date_range = await check_date_range(user_date_str)

#     if is_valid_date_range:
#         await message.answer(f"{message.text}✅")
#     else:
#         await message.answer("Siz kiritgan sana, oy va yil noto'g'ri. "
#                             "Maksimum 3 kunlik davrda bo'lishi kerak.\n"
#                             "Sana formati: 07.08.2023 dan 10.08.2023 gacha.")

@dp.message_handler(lambda message: message.text not in Uz_Months, state=Condition.Uz_DM)
async def Incorrect_Uz_DM(message: types.Message):
    return await message.answer("🗓Sana va oy qabul qilinmadi!🙅‍♂️\n✅Misol uchun: 22-mart.")


@dp.message_handler(state=Condition.Uz_DM)
async def Uz_DM_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Uz_DM'] = message.text
    text = await UzCheckTimeText(state)
    await message.answer(f"🕰{message.text} kuni soat nechiga kelishingizni tungi soat <b>9:00</b> dan\
 kechki soat <b>0:00</b> gacha bo'lgan vaqtni kiriting.\n⏳Soat intervali yarim soatdan bo'lishi kerak.\
\n❕Misol uchun: 10:00 yoki 10:30.\n\n🎯Band qilingan soatlar: " + text, parse_mode="HTML")
    await Condition.Uz_Oclock.set()


@dp.message_handler(
    lambda message: message.text not in ["9:00", "9:30", "10:00", "10:30", "11:00", "11:30", "11:54", "11:55", "12:00",
                                         "12:30", "13:00",
                                         "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00",
                                         "17:30",
                                         "18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30",
                                         "22:00",
                                         "22:30", "23:00", "23:30", "0:00"], state=Condition.Uz_Oclock)
async def Incorrect_Oclock(message: types.Message):
    return await message.answer("🚫Xato vaqtni kiritdingiz!\n🕰Soat nechiga kelishingizni tungi soat <b>9:00</b> dan kechki soat\
 <b>0:00</b> gacha bo'lgan vaqtni kiriting.\n⏳Soat intervali yarim soatdan bo'lishi kerak.\n❕Misol uchun: 10:00 yoki 10:30.",
                                parse_mode="HTML")


@dp.message_handler(state=Condition.Uz_Oclock)
async def Uz_Oclock_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Uz_Oclock'] = message.text
    if await UzCheckData(state):
        await UzWriteData(state)
    else:
        return await message.answer(f"🎯Soat {message.text} band qilingan. Yuqoridagi ro'yxatdan foydalangan holda\
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
    markup = check_markup(data['Language'], message.from_user.id)
    await bot.send_message(chat_id="1329197690", text=md.text("📝Mijoz ma'lumotlari;\
                                                \n👤Ismi:", md.text(data["Uz_Username"],
                                                                   "\n📞Telefon raqam:", md.text(data["Uz_Contact"],
                                                                                                "\n🗓Sana va oy:",
                                                                                                md.text(data["Uz_DM"],
                                                                                                        "\n💇🏻‍♂️Soch turmagi:",
                                                                                                        md.text(data[
                                                                                                                    "Uz_Haircuts"],
                                                                                                                "\n⏰Soat:",
                                                                                                                md.text(
                                                                                                                    data[
                                                                                                                        "Uz_Oclock"])))))),
                           reply_markup=markup)

    await state.finish()


async def UzCheckTimeText(state):
    async with state.proxy() as date:
        data = date['Uz_DM']
        file = open(file='dm.txt', mode='r', encoding='UTF-8')
        list = file.read().split('\n')
        day_time = []

        for i in list:
            day_time.append(i.split(' '))
        text = str()
        for i in day_time:
            if data in i[0]:
                text += i[1]
                text += ', '
        print(text)
        return text


@dp.message_handler(text="Русский🇷🇺", state=Condition.Language)
async def Ru_Language_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Language'] = message.text
    await message.answer("<b>Usta Abdulloh</b> - парикмахерская, основанная в 1999 году.\
Парикмахерская находится в самом центре города и является популярным местом как для мужчин, так и для женщин.\
Барбершоп предлагает различные услуги, включая стрижки, бритье, массаж головы, стрижку бороды и укладку волос.\
Персонал <b>Usta Abdulloh</b> обладает высокой квалификацией и опытом и стремится предоставить своим клиентам наилучший сервис.",
                         parse_mode="HTML")
    await message.answer("Введите своё имя. Мы хотели бы спросить вас кое о чем!\
 То есть мы просим вас отправлять боту свое полное имя без отправки всяких цифр и букв.",
                         reply_markup=types.ReplyKeyboardRemove())
    await Condition.Ru_Username.set()


@dp.message_handler(state=Condition.Ru_Username)
async def Ru_Username_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Ru_Username'] = message.text
    await message.answer(
        "Чтобы наши барберы связались с вами, пожалуйста, отправьте свой номер телефона, нажав на кнопку «📱»",
        reply_markup=Ru_Contact_Button)
    await Condition.Ru_Contact.set()


@dp.message_handler(lambda message: message.text not in ["📱"], state=Condition.Ru_Contact)
async def Incorrect_Ru_Contact(message: types.Message):
    return await message.answer(
        "🚫Номер телефона не подтверждена!🙅🏻‍♂️\nОтправьте свой номер телефона, нажав на кнопку «📱»", parse_mode="HTML")


@dp.message_handler(content_types=["contact"], state=Condition.Ru_Contact)
async def Ru_Contact_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Ru_Contact'] = message.contact.phone_number
    await message.answer("💇🏻‍♂️Какую стрижку вы хотите?", reply_markup=Ru_Haircuts_Button)
    await Condition.Ru_Haircuts.set()


@dp.message_handler(
    lambda message: message.text not in ["Детская стрижка", "Стандарт", "Продвинутая стрижка", "Свадебная стрижка"],
    state=Condition.Ru_Haircuts)
async def Incorrect_Ru_Haircuts(message: types.Message):
    return await message.answer(
        "🚫Ошибка при выборе стрижки!\n💇🏻‍♂️Выберите с помощью кнопки какую стрижку вы хотите.")


@dp.message_handler(text="Детская стрижка", state=Condition.Ru_Haircuts)
async def Ru_Children_Haircuts_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Ru_Haircuts'] = message.text
    await message.answer("👦🏻Что входит в детскую стрижку?\n\n• Стрижка волос💇🏻‍♂️\n• Мытье волос🚿\n\
• Укладка волос✨\n\n📋Цена: 100.000 - 150.000 UZS💸\n\nВыбираете детскую стрижку?", reply_markup=Ru_Yes_No_Button)
    await Condition.Ru_Yes_No.set()


@dp.message_handler(text="Стандарт", state=Condition.Ru_Haircuts)
async def Ru_Standart_Haircut_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Ru_Haircuts'] = message.text
    await message.answer("⭐️Что входит в стандарт?\n\n• Стрижка волос💇🏻‍♂️\n• Мытье волос🚿\n\
• Массаж головы💆🏻\n\n📋Цена: 150.000 UZS💸\n\nВыбираете стандартную стрижку?", reply_markup=Ru_Yes_No_Button)
    await Condition.Ru_Yes_No.set()


@dp.message_handler(text="Продвинутая стрижка", state=Condition.Ru_Haircuts)
async def Ru_Advanced_Haircut_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Ru_Haircuts'] = message.text
    await message.answer("⚡️Что входит в продвинутую стрижку?\n\n• Стрижка волос💇🏻‍♂️\n• Мытье волос🚿\n\
• Массаж головы💆🏻\n• Крем для волос🧴\n• Укладка волос💫\n\n\
📋Цена: 200.000 - 250.000 UZS💸\n\nВыбираете продвинутую стрижку?", reply_markup=Ru_Yes_No_Button)
    await Condition.Ru_Yes_No.set()


@dp.message_handler(text="Свадебная стрижка", state=Condition.Ru_Haircuts)
async def Ru_Wedding_Haircut_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Ru_Haircuts'] = message.text
    await message.answer("👩‍❤️‍👨Свадебная причёска:\n📋Цена: 100 - 150 USD💸\n\
\nВыбираете свадебную стрижку?", reply_markup=Ru_Yes_No_Button)
    await Condition.Ru_Yes_No.set()


@dp.message_handler(lambda message: message.text not in ["Да", "Нет"], state=Condition.Ru_Yes_No)
async def Incorrect_Ru_Yes_No(message: types.Message):
    return await message.answer("Если ваши данные верны с выбором нажмите кнопку \"Да\".\
 Чтобы выбрать другую прическу нажмите кнопку \"Нет\".")


@dp.message_handler(text="Нет", state=Condition.Ru_Yes_No)
async def Ru_No_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Ru_Yes_No'] = message.text
    await message.answer("💇🏻‍♂️Какую стрижку вы выберете?", reply_markup=Ru_Haircuts_Button)
    await Condition.Ru_Haircuts.set()


@dp.message_handler(text="Да", state=Condition.Ru_Yes_No)
async def Ru_Yes_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Ru_Yes_No'] = message.text
    await message.answer("🗓Введите дату и месяц.\n✅Например: 22-марта.",
                         reply_markup=types.ReplyKeyboardRemove(), parse_mode="HTML")
    await Condition.Ru_DM.set()


@dp.message_handler(lambda message: message.text not in Ru_Months, state=Condition.Ru_DM)
async def Incorrect_Ru_DM(message: types.Message):
    return await message.answer("🚫Число и месяц не подтвержден!🙅🏻‍♂️\n✅Например: 22-марта.")


@dp.message_handler(state=Condition.Ru_DM)
async def Ru_DM_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Ru_DM'] = message.text
    async with state.proxy() as data:
        data['check'] = Ru_Months.index(message.text)
    text = await RuCheckTimeText(state)
    await message.answer(f"🕰Введите время Вашего прибытия в {message.text} с <b>9:00</b> до <b>0:00.</b>\n\
⏳Часовой интервал должен составлять полчаса.\n❕Например: 10:00 или 10:30.\
\n\n🎯Забронированные часы: " + text, parse_mode="HTML")
    await Condition.Ru_Oclock.set()


@dp.message_handler(
    lambda message: message.text not in ["9:00", "9:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00",
                                         "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00",
                                         "17:30",
                                         "18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30",
                                         "22:00",
                                         "22:30", "23:00", "23:30", "0:00"], state=Condition.Ru_Oclock)
async def Incorrect_Oclock(message: types.Message):
    return await message.answer("🚫Ошибка при выборе времени!\nВведите время Вашего прибытия с <b>9:00</b> до\
 <b>0:00.</b>\n⏳Часовой интервал должен составлять полчаса.\n❕Например: 10:00 или 10:30.", parse_mode="HTML")


@dp.message_handler(state=Condition.Ru_Oclock)
async def Ru_Oclock_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Ru_Oclock'] = message.text
    if await RuCheckData(state):
        await RuWriteData(state)
    else:
        return await message.answer(f"{message.text} уже занято. Выберите незабронированное и\
 удобное время, используя список выше👆")
    await bot.send_message(
        message.chat.id,
        md.text(
            md.text("📝Ваши данные были приняты."),
            md.text("👤Ваша имя:", md.text(data["Ru_Username"])),
            md.text("📞Номер телефона:", md.text(data["Ru_Contact"])),
            md.text("🗓Число и месяц:", md.text(data["Ru_DM"])),
            md.text("💇🏻‍♂️Прическа:", md.text(data["Ru_Haircuts"])),
            md.text("⏰Время:", md.text(data["Ru_Oclock"])),
            sep="\n",
        ),
        reply_markup=types.ReplyKeyboardRemove(),
        parse_mode=ParseMode.MARKDOWN,
    )
    markup = check_markup(data['Language'], message.from_user.id)
    await bot.send_message(chat_id="1329197690", text=md.text("📝Данные клиента;\
                                                \n👤Имя:", md.text(data["Ru_Username"],
                                                                  "\n📞Номер телефона:", md.text(data["Ru_Contact"],
                                                                                                "\n🗓Число и месяц:",
                                                                                                md.text(data["Ru_DM"],
                                                                                                        "\n💇🏻‍♂️Прическа:",
                                                                                                        md.text(data[
                                                                                                                    "Ru_Haircuts"],
                                                                                                                "\n⏰Время:",
                                                                                                                md.text(
                                                                                                                    data[
                                                                                                                        "Ru_Oclock"])))))),
                           reply_markup=markup)

    await state.finish()


async def RuCheckTimeText(state):
    async with state.proxy() as date:
        data = date['Ru_DM']
        index = Ru_Months.index(data)
        data = Uz_Months[index]
        file = open(file='dm.txt', mode='r', encoding='UTF-8')
        list = file.read().split('\n')
        day_time = []
        print(data)
        for i in list:
            day_time.append(i.split(' '))

        text = str()
        for i in day_time:
            if data in i[0]:
                text += i[1]
                text += ', '
        print(text)
        return text


async def Check_Button(text: str) -> InlineKeyboardMarkup:
    Confirm = InlineKeyboardMarkup()
    Check = InlineKeyboardButton(f"{text}", callback_data="Check")
    Confirm.add(Check)
    return Confirm


@dp.callback_query_handler(check_callback.filter(item_name="Check"))
async def Update_Process(callback_query: types.CallbackQuery, callback_data: dict):
    if callback_data['lan'] == "O'zbek🇺🇿":
        await callback_query.answer()
        await bot.send_message(chat_id=callback_data['chat_id'],
                               text=f"Sizning so'rovingiz tasdiqlandi✅")
    else:
        await bot.send_message(chat_id=callback_data['chat_id'],
                               text="Ваш запрос подтвержден✅")
        await callback_query.answer()
    # await bot.answer_callback_query(callback_query.id, text="Tasdiqlandi.")
    await callback_query.message.edit_reply_markup(reply_markup=await Check_Button(text="Tasdiqlandi."))


@dp.errors_handler()
async def errors_handler(update, exception):
    if isinstance(exception, CantDemoteChatCreator):
        logging.exception("Can't demote chat creator")
        return True

    if isinstance(exception, MessageNotModified):
        logging.exception('Message is not modified')
        return True
    if isinstance(exception, MessageCantBeDeleted):
        logging.exception('Message cant be deleted')
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        logging.exception('Message to delete not found')
        return True

    if isinstance(exception, MessageTextIsEmpty):
        logging.exception('MessageTextIsEmpty')
        return True

    if isinstance(exception, Unauthorized):
        logging.exception(f'Unauthorized: {exception}')
        return True

    if isinstance(exception, InvalidQueryID):
        logging.exception(f'InvalidQueryID: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, TelegramAPIError):
        logging.exception(f'TelegramAPIError: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, RetryAfter):
        logging.exception(f'RetryAfter: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, CantParseEntities):
        logging.exception(f'CantParseEntities: {exception} \nUpdate: {update}')
        return True

    logging.exception(f'Update: {update} \n{exception}')


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            limit = getattr(handler, "throttling_rate_limit", self.rate_limit)
            key = getattr(handler, "throttling_key", f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.message_throttled(message, t)
            raise CancelHandler()

    async def message_throttled(self, message: types.Message, throttled: Throttled):
        if throttled.exceeded_count <= 2:
            await message.answer("Juda ko'p so'rov yubordingiz!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
