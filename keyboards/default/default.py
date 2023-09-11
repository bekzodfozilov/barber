from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

Uz = KeyboardButton("O'zbek🇺🇿")
Ru = KeyboardButton("Русский🇷🇺")
Language_Button = ReplyKeyboardMarkup(resize_keyboard=True).add(Uz, Ru)

Uz_Phone_Number = KeyboardButton("📱", request_contact=True)
Uz_Contact_Button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(Uz_Phone_Number)

Uz_Children_Haircut = KeyboardButton("Bolalar soch turmagi")
Uz_Standart_Haircut = KeyboardButton("Standart")
Uz_Advanced_Haircut = KeyboardButton("Ommabop")
Uz_Wedding_Haircut = KeyboardButton("To'y soch turmagi")
Uz_Haircuts_Button = ReplyKeyboardMarkup(resize_keyboard=True).add(Uz_Children_Haircut, Uz_Standart_Haircut)\
    .add(Uz_Advanced_Haircut, Uz_Wedding_Haircut)

Uz_Yes = KeyboardButton(text="Ha")
Uz_No = KeyboardButton(text="Yo'q")
Uz_Yes_No_Button = ReplyKeyboardMarkup(resize_keyboard=True).add(Uz_Yes, Uz_No)

Ru_Phone_Number = KeyboardButton("📱", request_contact=True)
Ru_Contact_Button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(Ru_Phone_Number)

Ru_Children_Haircut = KeyboardButton("Детская стрижка")
Ru_Standart_Haircut = KeyboardButton("Стандарт")
Ru_Advanced_Haircut = KeyboardButton("Продвинутая стрижка")
Ru_Wedding_Haircut = KeyboardButton("Свадебная стрижка")
Ru_Haircuts_Button = ReplyKeyboardMarkup(resize_keyboard=True).add(Ru_Children_Haircut, Ru_Standart_Haircut)\
    .add(Ru_Advanced_Haircut, Ru_Wedding_Haircut)

Ru_Yes = KeyboardButton(text="Да")
Ru_No = KeyboardButton(text="Нет")
Ru_Yes_No_Button = ReplyKeyboardMarkup(resize_keyboard=True).add(Ru_Yes, Ru_No)

Check_Mark = InlineKeyboardButton(text="✅", callback_data="Check")
Confirmed = InlineKeyboardMarkup().add(Check_Mark)

SendToUsers=KeyboardButton("Foydalanuvchilarga murojaat qilish✍️")
Admin_Button=ReplyKeyboardMarkup(resize_keyboard=True).add(SendToUsers)

Message=KeyboardButton("Xabar📩")
Post=KeyboardButton("Post🗃")
Admin_Menu=ReplyKeyboardMarkup(resize_keyboard=True).add(Message, Post)