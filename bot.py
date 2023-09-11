from aiogram import executor
from loader import UABarbershop
import middlewares, filters, handlers

if __name__ == '__main__':
    executor.start_polling(UABarbershop, skip_updates=True)