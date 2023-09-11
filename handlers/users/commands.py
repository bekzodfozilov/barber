from aiogram import types
from keyboards.default.default import Language_Button
from loader import UABarbershop
from database.config import *
from states.states import Condition
from keyboards.default.default import Admin_Button

@UABarbershop.message_handler(commands=["start"], state="*")
async def CMD_Start(message: types.Message):
    # if str(message.from_user.id) in ADMINS:
    #     return await message.answer("Admin menyu:", reply_markup=Admin_Button)
    day = message.date.weekday()
    if day == 4:
        await message.answer("🇺🇿Assalomu aleykum hurmatli mijozlarimiz. Juma bizning dam olish kunimiz hisoblanadi\
va biz Juma kuni ishlamaymiz.\n🇷🇺Здравствуйте, дорогие клиенты. Пятница у нас выходной и иы не работаем в Пятницу.")
    else:
        await message.answer("🇺🇿O'zingizga qulay bo'lgan muloqot tilini tanlang.\n\
🇷🇺Выберите язык общения, который вам удобен.", reply_markup=Language_Button)
    if not await CheckUsersID(message.from_user.id):
        await WriteUserID(message.from_user.id)
    await GetCount()
    await Condition.Language.set()
    
@UABarbershop.message_handler(commands=["users"], state="*")
async def CMD_Users(message: types.Message):
    await message.answer(f"🇺🇿Bot foydalanuvchilari soni: {await GetCount()} ta.\n🇷🇺Количество пользователей бота: {await GetCount()}.")
    
async def WriteUserID(users_id):
    users = open('barbershop.txt', mode='a')
    users.write(f'{users_id}\n')
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

@UABarbershop.message_handler(commands=["help"], state="*")
async def CMD_Help(message: types.Message):
    await message.answer("🇺🇿Assalomu aleykum!🤝\n🤖Telegram-botimizdan foydalanishda muammo yoki savollaringiz bormi?\n\
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
🤖Telegram-botimizning qo'shimcha komandalari va ularning vazifasi;\n\
/start - Telegram-botni ishga tushirish;\n\
/help - Telegram botdan foydalanish uchun qo'llanma;\n\
/change_language - Tilni o'zgartirish.\n\n\
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
/language - Смена языка.", parse_mode="HTML")

@UABarbershop.message_handler(lambda message: message.text not in ["O'zbek🇺🇿", "Русский🇷🇺"], state=Condition.Language)
async def Incorrect_Language(message: types.Message):
    return await message.answer("🇺🇿Til tanlashda xatolik❗️\n🇷🇺Ошибка при выборе языка❗️")
