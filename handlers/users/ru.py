from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
from handlers.users.data import RuWriteData, RuCheckData
from handlers.users.rucheckday import RuCheckDay
from handlers.users.ruchecktime import RuCheckTimeText
from keyboards.default.default import Ru_Contact_Button, Ru_Haircuts_Button, Ru_Yes_No_Button, Confirmed
from dm.ru_dm import Ru_September
from loader import UABarbershop, bot
from states.states import Condition
import aiogram.utils.markdown as md


@UABarbershop.message_handler(text="Русский🇷🇺", state=Condition.Language)
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


@UABarbershop.message_handler(state=Condition.Ru_Username)
async def Ru_Username_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Ru_Username'] = message.text
    await message.answer(
        "Чтобы наши барберы связались с вами, пожалуйста, отправьте свой номер телефона, нажав на кнопку «📱»",
        reply_markup=Ru_Contact_Button)
    await Condition.Ru_Contact.set()


@UABarbershop.message_handler(lambda message: message.text not in ["📱"], state=Condition.Ru_Contact)
async def Incorrect_Ru_Contact(message: types.Message):
    return await message.answer(
        "🚫Номер телефона не подтверждена!🙅🏻‍♂️\nОтправьте свой номер телефона, нажав на кнопку «📱»", parse_mode="HTML")


@UABarbershop.message_handler(content_types=["contact"], state=Condition.Ru_Contact)
async def Ru_Contact_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Ru_Contact'] = message.contact.phone_number
    await message.answer("💇🏻‍♂️Какую стрижку вы хотите?", reply_markup=Ru_Haircuts_Button)
    await Condition.Ru_Haircuts.set()


@UABarbershop.message_handler(
    lambda message: message.text not in ["Детская стрижка", "Стандарт", "Продвинутая стрижка", "Свадебная стрижка"],
    state=Condition.Ru_Haircuts)
async def Incorrect_Ru_Haircuts(message: types.Message):
    return await message.answer("🚫Ошибка при выборе стрижки!\nВыберите с помощью кнопки какую стрижку вы хотите.")


@UABarbershop.message_handler(text="Детская стрижка", state=Condition.Ru_Haircuts)
async def Ru_Children_Haircuts_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Ru_Haircuts'] = message.text
    await message.answer("👦🏻Что входит в детскую стрижку?\n\n• Стрижка волос💇🏻‍♂️\n• Мытье волос🚿\n\
• Укладка волос✨\n\n📋Цена: 100.000 - 150.000 UZS💸\n\nВыбираете детскую стрижку?", reply_markup=Ru_Yes_No_Button)
    await Condition.Ru_Yes_No.set()


@UABarbershop.message_handler(text="Стандарт", state=Condition.Ru_Haircuts)
async def Ru_Standart_Haircut_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Ru_Haircuts'] = message.text
    await message.answer("⭐️Что входит в стандарт?\n\n• Стрижка волос💇🏻‍♂️\n• Мытье волос🚿\n\
• Массаж головы💆🏻\n\n📋Цена: 150.000 UZS💸\n\nВыбираете стандартную стрижку?", reply_markup=Ru_Yes_No_Button)
    await Condition.Ru_Yes_No.set()


@UABarbershop.message_handler(text="Продвинутая стрижка", state=Condition.Ru_Haircuts)
async def Ru_Advanced_Haircut_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Ru_Haircuts'] = message.text
    await message.answer("⚡️Что входит в продвинутую стрижку?\n\n• Стрижка волос💇🏻‍♂️\n• Мытье волос🚿\n\
• Массаж головы💆🏻\n• Крем для волос🧴\n• Укладка волос💫\n\n\
📋Цена: 200.000 - 250.000 UZS💸\n\nВыбираете продвинутую стрижку?", reply_markup=Ru_Yes_No_Button)
    await Condition.Ru_Yes_No.set()


@UABarbershop.message_handler(text="Свадебная стрижка", state=Condition.Ru_Haircuts)
async def Ru_Wedding_Haircut_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Ru_Haircuts'] = message.text
    await message.answer("👩‍❤️‍👨Свадебная причёска:\n📋Цена: 50 - 100 USD💸\n\nВыбираете свадебную стрижку?",
                         reply_markup=Ru_Yes_No_Button)
    await Condition.Ru_Yes_No.set()


@UABarbershop.message_handler(lambda message: message.text not in ["Да", "Нет"], state=Condition.Ru_Yes_No)
async def Incorrect_Ru_Yes_No(message: types.Message):
    return await message.answer("Если ваши данные верны с выбором нажмите кнопку \"Да\".\
 Чтобы выбрать другую прическу нажмите кнопку \"Нет\".")


@UABarbershop.message_handler(text="Нет", state=Condition.Ru_Yes_No)
async def Ru_No_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Ru_Yes_No'] = message.text
    await message.answer("💇🏻‍♂️Какую стрижку вы выберете?", reply_markup=Ru_Haircuts_Button)
    await Condition.Ru_Haircuts.set()


@UABarbershop.message_handler(text="Да", state=Condition.Ru_Yes_No)
async def Ru_Yes_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Ru_Yes_No'] = message.text
    await message.answer("🚶🏻‍♂️Введите дату Вашего прибытия в сентябре.\nНапример: 31-сентябрь.",
                         reply_markup=types.ReplyKeyboardRemove(), parse_mode="HTML")
    await Condition.Ru_DM.set()


@UABarbershop.message_handler(lambda message: message.text not in Ru_September, state=Condition.Ru_DM)
async def Incorrect_Ru_DM(message: types.Message):
    return await message.answer("🚫Число и месяц не подтвержден!🙅🏻‍♂️\nБот принимает только за месяц сентябрь.")


@UABarbershop.message_handler(state=Condition.Ru_DM)
async def Ru_DM_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Ru_DM'] = message.text
    async with state.proxy() as data:
        data['check'] = Ru_September.index(message.text)
    if await RuCheckDay(state):
        text = await RuCheckTimeText(state)
        await message.answer("🕰Введите время Вашего прибытия с <b>9:00</b> до <b>0:00.</b>\n\
⏳Часовой интервал должен составлять полчаса.\n❕Например: 10:00 или 10:30.\
\n\n🎯Забронированные часы: " + text)
        await Condition.Ru_Oclock.set()
    else:
        await message.answer("🗓Дата и месяц не принимаются!🙅‍♂️\nНапоминаем! Бот принимает только сентябрь\
и не принимает прошлые даты и месяцы.")


@UABarbershop.message_handler(
    lambda message: message.text not in ["9:00", "9:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00",
                                         "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00",
                                         "17:30",
                                         "18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30",
                                         "22:00",
                                         "22:30", "23:00", "23:30", "0:00"],
    state=Condition.Ru_Oclock)
async def Incorrect_Oclock(message: types.Message):
    return await message.answer("🚫Ошибка при выборе времени!\nВведите время Вашего прибытия с <b>9:00</b> до\
 <b>0:00.</b>\n⏳Часовой интервал должен составлять полчаса.\n❕Например: 10:00 или 10:30.", parse_mode="HTML")


@UABarbershop.message_handler(state=Condition.Ru_Oclock)
async def Ru_Oclock_Process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Ru_Oclock'] = message.text
    if await RuCheckData(state):
        await RuWriteData(state)
    else:
        return await message.answer(
            "Это место уже занято. Выберите незабронированное и удобное время, используя список выше👆")
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
    await bot.send_message(chat_id="@UzPythonTelegramBotsGroup", text=md.text("📝Данные клиента;\
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
                           reply_markup=Confirmed)

    await state.finish()
