from aiogram import Dispatcher
from loader import UABarbershop
from .throttling import ThrottlingMiddleware

if __name__ == "middlewares":
    UABarbershop.middleware.setup(ThrottlingMiddleware())