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
        return text