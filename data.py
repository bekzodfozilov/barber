from uz_dm import Uz_Months

async def UzWriteData(state):
    async with state.proxy() as date:
        data = date['Uz_DM']
        time = date['Uz_Oclock']
        users = open(file='dm.txt', mode='a', encoding='UTF-8')
        users.write(f'{data} {time}\n')
        users.close()

async def RuWriteData(state):
    async with state.proxy() as date:
        time = date['Ru_Oclock']
        index = date['check']
        print(index)
        value = Uz_Months[index]
        users = open(file='dm.txt', mode='a', encoding='UTF-8')
        users.write(f'{value} {time}\n')
        users.close()


async def UzCheckData(state):
    async with state.proxy() as date:
        data = date['Uz_DM']
        time = date['Uz_Oclock']
        users = open(file='dm.txt', mode='r', encoding='UTF-8')
        check_list = users.read().split('\n')
        data_time = data + ' ' + time
        print(data_time)
        print(check_list)
        if data_time in check_list:
            return False
        else:
            return True


async def RuCheckData(state):
    async with state.proxy() as date:
        index = date['check']
        value = Uz_Months[index]
        time = date['Ru_Oclock']
        users = open(file='dm.txt', mode='r', encoding='UTF-8')
        check_list = users.read().split('\n')
        data_time = value + ' ' + time
        if data_time in check_list:
            return False
        else:
            return True
