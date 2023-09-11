import datetime
from dm.uz_dm import Uz_September
from dm.uz_dm import Eng_September

async def UzCheckDay(state):
    async with state.proxy() as date:
        data = date['Uz_DM']
    text = data
    index = Uz_September.index(text)
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