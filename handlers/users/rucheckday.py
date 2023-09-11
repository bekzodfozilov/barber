import datetime
from dm.ru_dm import Ru_September
from dm.ru_dm import Eng_September


async def RuCheckDay(state):
    async with state.proxy() as date:
        data = date['Ru_DM']
    text = data
    index = Ru_September.index(text)
    print(Eng_September[index])
    day = Eng_September[index].split('-')

    x = datetime.datetime.now()
    now_month = x.strftime("%B")
    now_day = x.strftime("%d")
    zero = str()

    if now_day[0] == '0':
        zero = now_day[1]
    else:
        zero = now_day

    if day[1] == now_month and int(day[0]) >= int(zero):
        return True
    else:
        zero = now_day[1]
