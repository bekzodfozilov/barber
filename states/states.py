from aiogram.dispatcher.filters.state import State, StatesGroup

class Condition(StatesGroup):
    Language = State()

    Uz_Username = State()
    Uz_Contact = State()
    Uz_DM = State()
    Uz_Haircuts = State()
    Uz_Oclock = State()
    Uz_Yes_No = State()

    Ru_Username = State()
    Ru_Contact = State()
    Ru_DM = State()
    Ru_Haircuts = State()
    Ru_Oclock = State()
    Ru_Yes_No = State()
    
class AdminMenuCondition(StatesGroup):
   Admin = State()
   Send_Message = State()
   Send_Post = State()
   Caption = State()