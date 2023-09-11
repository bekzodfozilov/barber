from dm.uz_dm import Uz_September
from dm.ru_dm import Ru_September


async def RuCheckTimeText(state):
    async with state.proxy() as date:
        data = date['Ru_DM']
        index = Ru_September.index(data)
        data = Uz_September[index]
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
        return text
